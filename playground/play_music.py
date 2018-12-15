from glob import glob
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import *


song = AudioSegment.from_mp3("sample.mp3")
ten_seconds = 10 * 1000

first_10_seconds = song[:10000]

last_5_seconds = song[-5000:]
# boost volume by 8dB
beginning = first_10_seconds + 8

# reduce volume by 8dB
end = last_5_seconds - 8

without_the_middle = beginning + end
backwards = song.reverse()
with_style = beginning.append(end, crossfade=1500)
play(without_the_middle)