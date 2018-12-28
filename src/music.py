from psonic import *
from threading import Thread, Condition, Event

import wave
import contextlib


# Amp loop
#duration = 12
NUM_CHUNKS = 100
ring = [1] * NUM_CHUNKS
current_index = 0

def live_loop(condition, stop_event, song_file):
    global ring, current_index
    duration = get_sample_duration(song_file)
    current_index = 0
    j = 0
    while not stop_event.is_set():
        num_chunks = NUM_CHUNKS
        time_diff = 1.0/num_chunks

        sample(song_file, start=j, finish=j + time_diff, amp=ring[current_index])
        globals()["current_index"] += 1
        j += time_diff
        sleep(duration / num_chunks)
        if current_index >= num_chunks:
            stop_event.set()


def get_sample_duration(fname):
    with contextlib.closing(wave.open(fname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration


def play_song(song_file):
    condition = Condition()
    stop_event = Event()

    live_thread_1 = Thread(name='song', target=live_loop, args=(condition, stop_event, song_file))
    live_thread_1.start()


def edit_params(amp_diff):
    global ring, current_index
    picked_index = current_index
    ring[picked_index:picked_index + len(amp_diff)] = amp_diff
    ring[picked_index + len(amp_diff):] = [amp_diff[-1]] * (len(ring) - len(amp_diff) - picked_index)


if __name__ == "__main__":
    if True:
        mySamp = "C:/Users/ibokobza/Documents/git/musical/playground/sample1.wav"
        play_song(mySamp)