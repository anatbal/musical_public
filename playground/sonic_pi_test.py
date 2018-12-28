from psonic import *
from threading import Thread, Condition, Event

#Amp loop
duration = 12
mySamp = "/Users/anatbalzam/musical/playground/sample1.wav"
ring = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
pitch = [0.8,1.2,1,1,1,1]
def live_loop(condition, stop_event):
    i = 0
    j=0
    while not stop_event.is_set():
            num_chunks = 10
            sample(mySamp, start=j,finish=j+0.1,amp=ring[i])
            i += 1
            j+= 0.1
            sleep(duration/num_chunks)
            if ( i > num_chunks):
                stop_event.set()

#Pitch loop
def live_loop_2(condition, stop_event):
    i = 0
    j=0
    while not stop_event.is_set():
            num_chunks = 1
            sample(mySamp, start=j,finish=j+0.5,rate=pitch[i])
            i += 1
            j+= 0.5
            sleep(7)
            if ( i > num_chunks):
                stop_event.set()

condition = Condition()
stop_event = Event()
live_thread_1 = Thread(name='silsulim', target=live_loop_2, args=(condition, stop_event))

live_thread_1.start()