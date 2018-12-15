import os

from pydub import AudioSegment
from pydub.playback import play

SONGS = {
    "Static & Ben-el - Silsulim": "silsulim.mp3",
    "Static & Ben-el - Blabla": "blabla.mp3"
}

def complex_algorithm(input_points, selected_song):
    """

    :param input_points: Points drawn by the user
    :param selected_song: The name of the song to play
    :return: Play the edited song
    """
    mp3_filename = SONGS[selected_song]
    song = AudioSegment.from_mp3(os.path.join("..\samples", mp3_filename))
    cutted_song = song[:10000]

    # boost volume by 8dB
    edited_song = cutted_song + 8
    play(edited_song)
