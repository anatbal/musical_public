from psonic import *
from threading import Thread, Event

import wave
import contextlib
from src.config import *
from src.points_norm import dim_x_to_diff_arr, dim_y_to_diff_arr, pick_idxs


class Parameters:
    def __init__(self, song_file):
        self.current_index = 0

        song_duration = Song.get_sample_duration(song_file)
        self.num_chunks = int(song_duration / TIME_FOR_CHUNK) + 1

        self.canvas = None
        self.user_points_dict = {}
        self.user_idx_dict = {}
        self.volume = [1] * self.num_chunks
        self.release = [0] * self.num_chunks
        self.pan = [0] * self.num_chunks

# Global params
gp = None


def update_follow_points(canvas, current_index, follow_oval, user_points_dict):
    global gp
    for param, user_points in user_points_dict.items():
        if not user_points:
            continue
        if not gp.user_idx_dict.get(param):
            gp.user_idx_dict[param] = current_index
        actual_index = current_index - gp.user_idx_dict[param]
        follow_oval_id = follow_oval[param]
        if follow_oval_id is not None:
            canvas.delete(follow_oval_id)
        if actual_index >= len(user_points):
            gp.user_idx_dict[param] = current_index
            actual_index = 0
        x, y, _ = user_points[actual_index]
        x1, y1 = (x - 1), (y - 1)
        x2, y2 = (x + 1), (y + 1)
        follow_oval[param] = canvas.create_oval(x1, y1, x2, y2, outline="red", width=3)


def _clear_ovals(canvas, user_points):
    print("Deleting oval!")
    for _, _, oval_id in user_points:
        canvas.delete(oval_id)
    user_points[:] = []


class Song:
    def __init__(self):
        self.song_file = None
        self.song_thread = None
        self.sender = udp_client.SimpleUDPClient('127.0.0.1', 4559)

    def play_song_loop(self, stop_event, song_file):
        global gp

        num_chunks = gp.num_chunks
        part_diff = 1.0 / num_chunks

        j = 0
        follow_oval = {x: None for x in gp.user_points_dict.keys()}
        while  gp.current_index < num_chunks:
            #this replaces the previous sample
            self.sender.send_message('/reg', ["/Users/anatbalzam/musical/playground/sample1.wav", gp.volume[gp.current_index % len(gp.volume)],j, j + part_diff,
                                            gp.volume[gp.current_index % len(gp.volume)],
                                            gp.pan[gp.current_index % len(gp.pan)], TIME_FOR_CHUNK])

            gp.current_index += 1
            j += part_diff
            sleep(TIME_FOR_CHUNK)
            update_follow_points(gp.canvas, gp.current_index, follow_oval, gp.user_points_dict)

        for param, oval_id in follow_oval.items():
            if oval_id:
                gp.canvas.delete(oval_id)
        self.song_thread = None

    def get_num_chunks_affected(self):
        global gp
        duration = self.get_sample_duration(self.song_file)
        chunks_left_for_song = gp.num_chunks - gp.current_index
        num_chunks_affected = int((CHANGE_SECONDS / duration) * gp.num_chunks)
        return min(chunks_left_for_song, num_chunks_affected)

    def play_song(self, song_file, canvas, user_points_dict):
        """play the song in a different thread"""
        global gp
        self.song_file = song_file
        gp = Parameters(song_file)
        stop_event = Event()
        gp.canvas = canvas
        gp.user_points_dict = user_points_dict

        live_thread_1 = Thread(name='song', target=self.play_song_loop, args=(stop_event, song_file))
        self.song_thread = live_thread_1
        for param, user_points in user_points_dict.items():
            self.try_edit_params(param, user_points)
        live_thread_1.start()

    def try_edit_params(self, param_type, user_points):
        global gp
        if not self.song_thread or not user_points:
            return

        affected_num_chunks = self.get_num_chunks_affected()
        gp.user_points_dict[param_type] = pick_idxs(user_points, min(affected_num_chunks, len(user_points)))
        if param_type in ["volume", "release"]:
            new_vals = dim_y_to_diff_arr(user_points, affected_num_chunks)
        elif param_type in ["pan"]:
            new_vals = dim_x_to_diff_arr(user_points, affected_num_chunks)
        else:
            raise Exception("unfamiliar param type")
        self.edit_params(new_vals, param_type)

    def edit_params(self, diff, col_parm):
        global gp
        picked_index = gp.current_index
        if col_parm == "volume":
            gp.volume = diff
        elif col_parm == "release":
            gp.release = diff
        elif col_parm == "pan":
            gp.pan = diff

    def reset_params(self):
        global gp
        gp.user_points_dict = {}
        gp.user_idx_dict = {}
        gp.volume = [1] * gp.num_chunks
        gp.release = [0] * gp.num_chunks
        gp.pan = [0] * gp.num_chunks

    @staticmethod
    def get_sample_duration(fname):
        """gets the duration of the song given file name in seconds"""
        with contextlib.closing(wave.open(fname, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        return duration


if __name__ == "__main__":
    if True:
        mySamp = "C:/Users/ibokobza/Documents/musical/playground/sample1.wav"
        Song().play_song(mySamp)
