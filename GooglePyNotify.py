from __future__ import print_function
import time
import socket
import os.path
import pychromecast
from http.server import HTTPServer, SimpleHTTPRequestHandler
from gtts import gTTS

HOST_NAME = "0.0.0.0"
HOST_PORT = 80

MP3_CACHE_DIR = "mp3_cache"
CHROMECASTS = 0

class HttpServer(SimpleHTTPRequestHandler):
            
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # Check For URL Stream "http://IPADDRESS/Notify?"
            
        if "/Notify?" in self.path:
            self._set_headers()
            preurl, notification = self.path.split("?")

            # Add some error handling for chrome looping
            redir = "<html><head><meta http-equiv='refresh' content='0;url=.\' /></head><body><h1>Notification Sent! <br>"+notification+"</h1></body></html>"
            print(redir)

            self.wfile.write(redir.encode())
            self.notify(str(notification))
            return
        
        elif "/HelloWorld" in self.path:
            self._set_headers()
            print("Hello World Test")
            self.notify("Hello+World")
            return
            
        else:
            SimpleHTTPRequestHandler.do_GET(self)
   
    # POST is for submitting data
    def do_POST(self):

        print( "incomming http: ", self.path )

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self.send_response(200)

    def notify(self, notification):
        if notification == "":
                notification = "No+Notification+Data+Recieved"
        
        mp3 = MP3_CACHE_DIR + "/" + notification.replace("+","_") + ".mp3"
        text = notification.replace("+"," ")

        if not os.path.isfile(mp3) :
            print("Generating MP3...")
            tts = gTTS(text=text, lang='en-uk') # See Google TTS API for more Languages (Note: This may do translation Also - Needs Testing)
            tts.save(mp3)
        else:
            print("Reusing MP3...")

        print("Sending notification...")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Pull IP Address for Local HTTP File Serving (Note: This requires an internet connection)
        s.connect(("8.8.8.8", 80))
        ip_add = s.getsockname()[0]
        print (ip_add)
        s.close()
        self.Cast(ip_add, mp3)

        print("Notification Sent.")

        return
    
    def Cast(self, ip_add, mp3):
        castdevice = next(cc for cc in CHROMECASTS if cc.device.model_name == "Google Home")
        castdevice.wait()
        mediacontroller = castdevice.media_controller # ChromeCast Specific
        url = "http://" + ip_add + "/" + mp3
        print (url)
        mediacontroller.play_media(url, 'audio/mp3')
        return

if not os.path.exists(MP3_CACHE_DIR):
    os.makedirs(MP3_CACHE_DIR)

print("Getting chromecasts...")
CHROMECASTS = pychromecast.get_chromecasts()

print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, HOST_PORT))
httpServer = HTTPServer((HOST_NAME, HOST_PORT), HttpServer) #HTTP Server Stuff (Python Librarys)

try:
    httpServer.serve_forever()
except KeyboardInterrupt:
    pass

httpServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, HOST_PORT))
