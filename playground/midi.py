import mido
import time

mid = mido.MidiFile('song.mid')
outport = mido.open_output()
for msg in mid.play():
    outport.send(msg)

"""
import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

note_on = [0x99, 60, 112] # channel 10, middle C, velocity 112
note_off = [0x89, 60, 0]
midiout.send_message(note_on)
time.sleep(2.5)
midiout.send_message(note_off)

del midiout
"""