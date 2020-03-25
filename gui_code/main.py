import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import platform

from WorldMap import WorldMap
from PreviewWidget import PreviewWidget

import generator



def quit():
	exit()		

system = platform.system()

if system == 'Windows':
    windows = True
else:
    windows = False

root = tk.Tk()
root.title("Dataset downloader")
root.geometry('600x600')


# ========================================================================================================
# 											GENERATOR
# ========================================================================================================
style = ttk.Style()
style.configure("Bold.TLabel", font=("Helvetica", 18, "bold"))
generator_label = ttk.Label(text="Generator", style="Bold.TLabel")
generator_frame = ttk.Labelframe(root, labelwidget=generator_label)
generator_frame.pack(side=tk.TOP, fill =tk.BOTH)
#--------------------- ROW 1 -------------------------------

n_points_label = tk.Label(generator_frame, text='Number of points: ', font=("Helvetica", 14)) 
n_points_label.grid(row=1, column=1)
num_of_points_entry=tk.Entry(generator_frame)
num_of_points_entry.insert(10, str(0))
num_of_points_entry.grid(row=1, column=2)


generate_btn = tk.Button(generator_frame, text="Generate", font=("Helvetica", 14), command=lambda:generator.get_land_coordinates(0+int(num_of_points_entry.get())))
generate_btn.grid(row=2, column=1)

load_btn = tk.Button(generator_frame, text="Load", font=("Helvetica", 14), command=generator.load_points)
load_btn.grid(row=2, column=2)

getnew_btn = tk.Button(generator_frame, text="Get new", font=("Helvetica", 14), command=lambda:generator.get_new_points(0+int(num_of_points_entry.get())))
getnew_btn.grid(row=2, column=3)


# ========================================================================================================
# 											EXTRA
# ========================================================================================================

extra_label = ttk.Label(text="Extra", style="Bold.TLabel")
extra_frame = ttk.Labelframe(root, labelwidget=extra_label)
extra_frame.pack(side=tk.BOTTOM, fill =tk.BOTH)
# World map 
wm = WorldMap(extra_frame,label="World Map")
map_btn = tk.Button(extra_frame, text="Show map", font=("Helvetica", 14), command=wm.show_map)
map_btn.grid(row=1, column=1)

# World map 
pw = PreviewWidget(extra_frame,label="Preview")
preview_btn = tk.Button(extra_frame, text="Dataset Preview", font=("Helvetica", 14), command=pw.show_map)
preview_btn.grid(row=1, column=2)




root.protocol("WM_DELETE_WINDOW", quit)
root.mainloop()




