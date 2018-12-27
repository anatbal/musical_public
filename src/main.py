from tkinter import Tk, Canvas, Label, Frame, StringVar, OptionMenu
from tkinter import YES, BOTH, BOTTOM, N, E, W, S
from tkinter.messagebox import showinfo

from src.mixer import SONGS, complex_algorithm

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 150
PYTHON_GREEN = "#476042"


class UserStatus:
    AWAITING_MOTION = 0
    AWAITING_RELEASE = 1
    AWAITING_CLEAR = 2


class MixerPaint(object):
    def __init__(self):
        self.status = UserStatus.AWAITING_MOTION
        self.user_points = []

        self.canvas_w = None
        self.tkinter_master = None
        self.selected_song = None

        self.init_canvas()
        self.initialize_binds()

    def paint_and_save(self, event):
        if self.status not in [UserStatus.AWAITING_MOTION, UserStatus.AWAITING_RELEASE]:
            print("You have to clear the canvas before drawing")
            return
        if self.status == UserStatus.AWAITING_MOTION:
            self.status = UserStatus.AWAITING_RELEASE
            assert (self.user_points == [])
        # paint Oval
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas_w.create_oval(x1, y1, x2, y2, fill=PYTHON_GREEN)

        # Add to points
        self.user_points.append((event.x, event.y))

    def stop_paint(self, event):
        if self.status != UserStatus.AWAITING_RELEASE:
            print("Single click isn't considered painting")
            if self.status == UserStatus.AWAITING_MOTION:
                assert (self.user_points == [])
            return
        self.status = UserStatus.AWAITING_CLEAR

        print("Done receiving paint")
        showinfo("Success", "Painting received!")

        complex_algorithm(self.user_points, self.selected_song.get())

    def init_canvas(self):
        self.tkinter_master = Tk()
        self.tkinter_master.title("Painting using Ovals")

        # Add a grid
        mainframe = Frame(self.tkinter_master)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.pack(pady=20, padx=20)

        # Create a Tkinter variable
        self.selected_song = StringVar(self.tkinter_master)

        # Dictionary with options
        choices = list(SONGS.keys())
        self.selected_song.set(choices[0])  # set the default option

        popup_menu = OptionMenu(mainframe, self.selected_song, *choices)
        Label(mainframe, text="Choose a song").grid(row=1, column=1)
        popup_menu.grid(row=2, column=1)

        self.canvas_w = Canvas(self.tkinter_master,
                               width=CANVAS_WIDTH,
                               height=CANVAS_HEIGHT,
                               highlightbackground="black")
        self.canvas_w.pack(expand=YES, fill=BOTH)

        message = Label(self.tkinter_master, text="Press and Drag the mouse to draw")
        message.pack(side=BOTTOM)

    def initialize_binds(self):
        self.canvas_w.bind("<B1-Motion>", lambda event: self.paint_and_save(event))
        # TODO: handle the cases of Enter/Leave the widget?
        self.canvas_w.bind("<ButtonRelease-1>", lambda event: self.stop_paint(event))

        # Use it to print debug
        #self.canvas_w.bind("<Leave>", lambda event: print(self.user_points))

    def start(self):
        self.tkinter_master.mainloop()


def main():
    painter = MixerPaint()
    painter.start()


if __name__ == "__main__":
    main()
