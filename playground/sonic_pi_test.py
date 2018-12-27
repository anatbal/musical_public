from psonic import *
from threading import Thread, Condition, Event
#SILSULIM = sample("~/musical/playground/sample.wav")

def loop_foo():
    sample(GUIT_HARMONICS, amp=0.5,rate= 5)
    sleep (0.5)



def live_loop_1(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.notifyAll() #Message to threads
        loop_foo()



condition = Condition()
stop_event = Event()
live_thread_1 = Thread(name='producer', target=live_loop_1, args=(condition,stop_event))


live_thread_1.start()

yes = input("Press Enter to continue...")
if yes == 'y':
    def loop_foo():
        sample(GUIT_HARMONICS, amp=2.5, rate = -1)
        sleep(0.5)
    sleep(10)
    stop_event.set()
