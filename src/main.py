from tkinter import Tk, Canvas, Label, Frame, StringVar, OptionMenu, Button
from tkinter import YES, BOTH, BOTTOM, N, E, W, S
from tkinter.messagebox import showinfo

from src.mixer import SONGS, complex_algorithm, translate_change
from src.music import play_song, edit_params
from src.music import NUM_CHUNKS, get_sample_duration

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 150
PYTHON_GREEN = "#476042"

CHANGE_SECONDS = 8
CHANGE_MILISECONDS = 1000 * CHANGE_SECONDS


class UserStatus:
    AWAITING_PLAY = 0
    AWAITING_MOTION = 1
    AWAITING_RELEASE = 2
    AWAITING_CLEAR = 3


PARAMETER_TO_COLOR = {
    "volume (blue)": ("volume", "blue"),
    "release(green)": ("release", "green"),
#    "clap (black)": "black"
}

class MixerPaint(object):
    def __init__(self):
        self.status = UserStatus.AWAITING_PLAY
        self.volume_user_points = []
        self.release_user_points = []

        self.param_to_user_point = {
            "volume": self.volume_user_points,
            "release": self.release_user_points
        }

        self.root = None
        self.canvas_w = None

        self.selected_song = None
        self.parameter = None

        self.init_canvas()
        self.initialize_binds()

    def paint_and_save(self, event):
        if self.status not in [UserStatus.AWAITING_MOTION, UserStatus.AWAITING_RELEASE]:
            print("You have to clear the canvas before drawing")
            return
        param, color = PARAMETER_TO_COLOR[self.parameter.get()]
        user_points = self.param_to_user_point[param]
        if self.status == UserStatus.AWAITING_MOTION:
            if user_points:
                print("Not empty yet")
                return
            self.status = UserStatus.AWAITING_RELEASE
            assert (user_points == [])
        # paint Oval
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        oval_id = self.canvas_w.create_oval(x1, y1, x2, y2, fill=color, outline=color)

        # Add to points
        user_points.append((event.x, event.y, oval_id))

    def stop_paint(self, event):
        user_points = self.param_to_user_point[PARAMETER_TO_COLOR[self.parameter.get()][0]]
        print(PARAMETER_TO_COLOR[self.parameter.get()][0])
        if self.status != UserStatus.AWAITING_RELEASE:
            if not user_points:
                print("Single click isn't considered painting")
            return
        self.status = UserStatus.AWAITING_MOTION

        print("Done receiving paint")
        self.start_follow()
        #showinfo("Success", "Painting received!")

        duration = get_sample_duration(SONGS[self.selected_song.get()])
        affected_num_chunks = int((CHANGE_SECONDS / duration) * NUM_CHUNKS)

        diff = translate_change(user_points, affected_num_chunks)
        diff = [1 + 10*x for x in diff]
        edit_params(diff,PARAMETER_TO_COLOR[self.parameter.get()][0])

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
        clear_btn = Button(self.root, text="Clear", width=10, command=self._reset_canvas)
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
        #self.canvas_w.bind("<Leave>", lambda event: print(self.user_points))

    def start(self):
        self.root.mainloop()

    def _reset_canvas(self):
        user_points = self.param_to_user_point[PARAMETER_TO_COLOR[self.parameter.get()][0]]
        self.canvas_w.delete("all")
        self.status = UserStatus.AWAITING_MOTION
        user_points[:] = []

    def start_song(self):
        play_song(SONGS[self.selected_song.get()])
        self.status = UserStatus.AWAITING_MOTION

    def start_follow(self):
        user_points = self.param_to_user_point[PARAMETER_TO_COLOR[self.parameter.get()][0]]
        num_points = len(user_points)
        if not num_points:
            print("Can't follow without any lead")
            return
        interval = int(CHANGE_MILISECONDS / num_points)
        self.do_follow(0, None, interval, user_points)

    def do_follow(self, current_index, follow_oval, interval, user_points):
        if follow_oval is not None:
            self.canvas_w.delete(follow_oval)
        if current_index < len(user_points):
            x, y, _ = user_points[current_index]
            x1, y1 = (x - 1), (y - 1)
            x2, y2 = (x + 1), (y + 1)
            follow_oval = self.canvas_w.create_oval(x1, y1, x2, y2, outline="red", width=3)
            self.canvas_w.after(interval, self.do_follow, current_index + 1, follow_oval, interval, user_points)
        else:
            self._clear_ovals(user_points)

    def _clear_ovals(self, user_points):
        print ("Deleting oval!")
        for _, _, oval_id in user_points:
            self.canvas_w.delete(oval_id)
        user_points[:] = []



def main():
    painter = MixerPaint()
    painter.start()


if __name__ == "__main__":
    main()
