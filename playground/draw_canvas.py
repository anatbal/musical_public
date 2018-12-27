from tkinter import *
from tkinter import ttk

# create global variables
canvas_width = 1200
canvas_height = 700
brush_size = 3
color = "black"


# create all function
def paint(event):
	global brush_size
	global color
	x1 = event.x - brush_size
	x2 = event.x + brush_size
	y1 = event.y - brush_size
	y2 = event.y + brush_size
	w.create_oval(x1, y1, x2, y2,
			   fill=color, outline=color)


def brush_size_change(new_size):
	global brush_size
	brush_size = new_size


def color_change(new_color):
	global color
	color = new_color


# draw a window
root = Tk()
root.title("Paint")


# create logic "DRAWING AREA"
w = Canvas(root,
		   width=canvas_width,
		   height=canvas_height,
		   bg="white")
w.bind("<B1-Motion>", paint)

red_btn = ttk.Button(text="Red", width=10,
				 command=lambda: color_change("red"))

blue_btn = ttk.Button(text="Blue", width=10,
				  command=lambda: color_change("blue"))

black_btn = ttk.Button(text="Black", width=10,
				  command=lambda: color_change("black"))

white_btn = ttk.Button(text="White", width=10,
				  command=lambda: color_change("white"))

clear_btn = ttk.Button(text="Delete All", width=10,
				   command=lambda: w.delete("all"))

one_btn = ttk.Button(text="1", width=10,
				 command=lambda: brush_size_change(1))

five_btn = ttk.Button(text="5", width=10,
				  command=lambda: brush_size_change(5))

ten_btn = ttk.Button(text="10", width=10,
				 command=lambda: brush_size_change(10))

fifteen_btn = ttk.Button(text="15", width=10,
					 command=lambda: brush_size_change(15))

twenty_btn = ttk.Button(text="20", width=10,
					command=lambda: brush_size_change(20))

w.grid(row=2, column=0,
	   columnspan=7, padx=5,
	   pady=5, sticky=E+W+S+N)

# call all functions
w.columnconfigure(6, weight=1)
w.rowconfigure(2, weight=1)

red_btn.grid(row=0, column=2)
blue_btn.grid(row=0, column=3)
black_btn.grid(row=0, column=4)
white_btn.grid(row=0, column=5)
clear_btn.grid(row=0, column=6, sticky=W)

one_btn.grid(row=1, column=2)
five_btn.grid(row=1, column=3)
ten_btn.grid(row=1, column=4)
fifteen_btn.grid(row=1, column=5)
twenty_btn.grid(row=1, column=6, sticky=W)

root.mainloop()