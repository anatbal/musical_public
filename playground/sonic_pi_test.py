import os
from psonic import *
from threading import Thread, Condition, Event
from pythonosc import osc_message_builder
from pythonosc import udp_client
#Amp loop
duration = 10
mySamp = "/Users/anatbalzam/musical/playground/sample1.wav"
#We need to figure in windows but as for right now works in windows.
os.system("cat SonicPiEffects.rb | sonic_pi")
sender = udp_client.SimpleUDPClient('127.0.0.1', 4559)
sender.send_message('/whammy', ["/Users/anatbalzam/musical/playground/sample1.wav",0,0.0,0.3,1,1,1])
os.system("echo stop |sonic_pi ")

