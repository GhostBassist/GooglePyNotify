# GooglePyNotify
Using Python and Google home to Build a Simple Notification System with TTS

# Installation

This was built and tested on Windows 10, However should be compatible with any internet enabled device that can run python
Please ensure to install the pychromecast Librarys in order for this to work

<code> python -m pip install pychromecast </code>

once installed run the .py script on your device and remember that you will need to port forward in order to intergrate with IFTTT Webhooks Service

Usage: http://IP-OR-WEB-ADDRESS/Notify?Notification+Message+Goes+Here

This will create your text to Speech MP3 on the device and stream this via Casting to your Google Home Appliance, Or Google Chromecast Audio etc.
