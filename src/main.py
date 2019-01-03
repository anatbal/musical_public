from tkinter import Tk, Canvas, Label, Frame, StringVar, OptionMenu, Button
from tkinter import YES, BOTH, BOTTOM, N, E, W, S
from tkinter.messagebox import showinfo
import copy

from src.music import Song
from src.config import *

CHANGE_MILISECONDS = 1000 * CHANGE_SECONDS

class UserStatus:
    AWAITING_MOTION = 0
    AWAITING_RELEASE = 1


PARAMETER_TO_COLOR = {
    "volume (blue)": ("volume", "blue"),
    "release(green)": ("release", "green"),
    #    "clap (black)": "black"
}


class MixerPaint(object):
    def __init__(self):
        self.status = UserStatus.AWAITING_MOTION
        self.volume_user_points = []
        self.release_user_points = []
        self.panning_user_points = []

        self.param_to_user_point = {
            "volume": self.volume_user_points,
            "release": self.release_user_points,
            "panning": self.panning_user_points
        }
        self.song = Song()

        self.root = None
        self.canvas_w = None

        self.selected_song = None
        self.parameter = None

        self.init_canvas()
        self.initialize_binds()

    def paint_and_save(self, event):
        param, color = PARAMETER_TO_COLOR[self.parameter.get()]
        user_points = self.param_to_user_point[param]
        if self.status == UserStatus.AWAITING_MOTION:
            if user_points:
                print("Not empty yet")
                return
            self.status = UserStatus.AWAITING_RELEASE
            assert (user_points == [])
        # paint Oval
        if user_points:
            x1, y1 = user_points[-1][0], user_points[-1][1]
            x2, y2 = event.x, event.y
        else:
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
        line_id = self.canvas_w.create_line(x1, y1, x2, y2, fill=color)

        # Add to points
        user_points.append((event.x, event.y, line_id))

    def stop_paint(self, event):
        param_type = PARAMETER_TO_COLOR[self.parameter.get()][0]
        user_points = self.param_to_user_point[param_type]
        if self.status != UserStatus.AWAITING_RELEASE:
            if not user_points:
                print("Single click isn't considered painting")
            return
        self.status = UserStatus.AWAITING_MOTION

        print("Done receiving paint")
        self.song.try_edit_params(param_type, user_points)

    def init_canvas(self):
        self.root = Tk()
        self.root.title("Painting using Ovals")

        # Grid
        mainframe = Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=3)
        mainframe.rowconfigure(0, weight=2)
        mainframe.pack(pady=20, padx=20)

        # Selected song
        song_names = list(SONGS.keys())
        self.selected_song = StringVar(self.root)
        self.selected_song.set(song_names[0])  # set the default option
        Label(mainframe, text="Choose a song").grid(row=1, column=1)
        song_menu = OptionMenu(mainframe, self.selected_song, *song_names)
        song_menu.grid(row=2, column=1)

        # Selected parameter
        parameter_names = list(PARAMETER_TO_COLOR.keys())
        self.parameter = StringVar(self.root)
        self.parameter.set(parameter_names[0])
        Label(mainframe, text="Select Parameter").grid(row=1, column=2)
        color_menu = OptionMenu(mainframe, self.parameter, *parameter_names)
        color_menu.grid(row=2, column=2)

        # Clear button
        clear_btn = Button(self.root, text="Clear", width=10, command=self.reset_canvas)
        clear_btn.pack()

        # Play button
        clear_btn = Button(self.root, text="Play", width=10, command=self.start_song)
        clear_btn.pack()

        # Canvas
        self.canvas_w = Canvas(self.root,
                               width=CANVAS_WIDTH,
                               height=CANVAS_HEIGHT,
                               highlightbackground="black",
                               bg="white")
        self.canvas_w.pack(expand=YES, fill=BOTH)

        # Message
        message = Label(self.root, text="Press and Drag the mouse to draw")
        message.pack(side=BOTTOM)

    def initialize_binds(self):
        self.canvas_w.bind("<B1-Motion>", lambda event: self.paint_and_save(event))
        # TODO: handle the cases of Enter/Leave the widget?
        self.canvas_w.bind("<ButtonRelease-1>", lambda event: self.stop_paint(event))

        # Use it to print debug
        # self.canvas_w.bind("<Leave>", lambda event: print(self.user_points))

    def start(self):
        self.root.mainloop()

    def reset_canvas(self):
        for param, user_points in self.param_to_user_point.items():
            user_points[:] = []
        self.canvas_w.delete("all")
        self.song.reset_params()

    def start_song(self):
        self.song.play_song(SONGS[self.selected_song.get()], self.canvas_w, copy.deepcopy(self.param_to_user_point))


def main():
    painter = MixerPaint()
    painter.start()


if __name__ == "__main__":
    main()
