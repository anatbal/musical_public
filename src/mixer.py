import os
import math
from pydub import AudioSegment
from pydub.playback import play
import itertools

SAMPLES_PATH = "..\samples"
SONGS = {
    "Static & Ben-el - Silsulim": "silsulim.mp3"
}

RAISE_FACTOR = 20
MAX_SAMPLES = 10  # TODO: change to 100


def splitNum(num, parts):
    diff = num % parts
    base = int(num/parts)
    if diff == 0:
        return [base] * parts
    else:
        return [base+1] * diff + [base] * (parts-diff)

def translate_change(input_points):
    y_axis_list = [point[1] for point in input_points]
    z_p = y_axis_list[0]
    max_p, min_p = max(y_axis_list), min(y_axis_list)
    if max_p == min_p:
        scale = 1
    else:
        scale = max_p - min_p
    diff_list = [-(y-z_p)/scale for y in y_axis_list]

    # Alter to get MAX_SAMPLES
    num_samples = min(MAX_SAMPLES, len(diff_list))
    nums_split = splitNum(len(diff_list), num_samples)
    idxs = list(itertools.accumulate(nums_split))
    truncated_diff_list = [RAISE_FACTOR * diff_list[i-1] for i in idxs]
    return truncated_diff_list


def complex_algorithm(input_points, selected_song):
    """

    :param input_points: Points drawn by the user
    :param selected_song: The name of the song to play
    :return: Play the edited song
    """
    mp3_filename = SONGS[selected_song]
    song = AudioSegment.from_mp3(os.path.join(SAMPLES_PATH, mp3_filename))
    cutted_song = song
    cutted_song = song[:10000]  # for debug purposes

    dbDiff = translate_change(input_points)
    nums_split = splitNum(len(cutted_song), len(dbDiff))
    idxs = [0] + list(itertools.accumulate(nums_split))
    part_songs = [cutted_song[idxs[i]:idxs[i+1]] + dbDiff[i] for i in range(len(idxs)-1)]
    whole_song = sum(part_songs)
    play(whole_song)
