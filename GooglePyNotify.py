from __future__ import print_function
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import time
from gtts import gTTS
import time
import pychromecast
import socket

hostName = "0.0.0.0"
hostPort = 80

class MyServer(SimpleHTTPRequestHandler):

	
    def do_GET(self):
        #Check For URL Stream "http://IPADDRESS/Notify?"
        
        if "/Notify?" in self.path:
            pre,notification = self.path.split("?")
            if notification == "":
                notification = "No+Notification+Data+Recieved"
                
            notification = notification.replace("+"," ") #Replace "+" Char in String for Spaces
            print("Notification Sent")
            print(notification)
            #print("The Path Matched")
            text = gTTS(text=notification, lang='en-uk') #See Google TTS API for more Languages (Note: This may do translation Also - Needs Testing)
            text.save("Notification.mp3")
            chromecasts = pychromecast.get_chromecasts()
            castdevice = next(cc for cc in chromecasts if cc.device.model_name == "Google Home")
            castdevice.wait()

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Pull IP Address for Local HTTP File Serving (Note: This requires an internet connection)
            s.connect(("8.8.8.8", 80))
            IpAdd = s.getsockname()[0]
            print (IpAdd)
            s.close()
            
            mediacontroller = castdevice.media_controller #ChromeCast Specifics
            URL = "http://"+IpAdd+"/"+"Notification.mp3"
            print (URL)
            mediacontroller.play_media(URL, 'audio/mp3')
            #mediacontroller.block_until_active()
            #print(mediacontroller.status)
            
        else:
            SimpleHTTPRequestHandler.do_GET(self)
            
		

	#	POST is for submitting data. -- This is Unused as of yet
    def do_POST(self):

        print( "incomming http: ", self.path )

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self.send_response(200)

        client.close()

		#import pdb; pdb.set_trace()


myServer = HTTPServer((hostName, hostPort), MyServer) #HTTP Server Stuff (Python Librarys)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
