import tkinter as tk
from tkinter import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from shapely.geometry import Point,Polygon
import pandas as pd
import geopandas as gpd
import descartes
import numpy as np
from matplotlib.figure import Figure
import os
import image_loader

class PreviewWidget(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        self.root = root
        self.preview_window = None

        s2_paths, s2_zones = image_loader.get_images_path('/Users/alessandrosebastianelli/Desktop/SentinelDataDownloaderTool/dataset_sample/', 'sen2')
        s1_images, s1_zones = image_loader.get_images_path('/Users/alessandrosebastianelli/Desktop/SentinelDataDownloaderTool/dataset_sample/', 'sen1')
        s2_images, cloud_masks = image_loader.split_S2_images(s2_paths)
        s2_series = image_loader.get_time_series(s2_images)
        s1_series = image_loader.get_time_series(s1_images)

        self.generator = iter(image_loader.image_generator(s2_series, s1_series, batch_size = 1, info = True))
        self.rgb, self.vv, self.rgb_path, self.vv_path = None, None, None, None

        self.preview_map = None
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.S2_text = None
        self.S1_text = None

        self.show_map()

    def create_plot(self):
        for i in range(8):
            self.fig.add_subplot(2,4,i+1)

        axes = self.fig.axes

        for i in range(4):
            axes[i].imshow(self.rgb[i,...])
            axes[i].set_title('Sentinel_2 - img '+str(i))
        for i in range(4):
            axes[4+i].imshow(self.vv[i,...,0], cmap='gray')
            axes[4+i].set_title('Sentinel_1 - img '+str(i))

    def format_paths(self):
        self.S2_text.delete(1.0,tk.END)
        self.S1_text.delete(1.0,tk.END)

        rgb_formatted = ""
        vv_formatted = ""
        for path in self.rgb_path:
            rgb_formatted = rgb_formatted + path + '\n'

        for path in self.vv_path:
            vv_formatted = vv_formatted + path + '\n' 

        self.S2_text.insert(tk.END, rgb_formatted)
        self.S1_text.insert(tk.END, vv_formatted)

        self.S2_text.update()
        self.S1_text.update()


    def draw_map(self):
        self.fig.axes.clear()
        self.rgb, self.vv, self.rgb_path, self.vv_path = next(self.generator)
        self.create_plot()
        self.format_paths()

        self.preview_map.draw()
        
        
        
    def show_map(self):
        #----Create a new indipendent window from the root
        self.preview_window = tk.Toplevel(self.root)
        #----Set the "attention" on it
        self.preview_window .grab_set()
        m = self.root.maxsize()
        self.preview_window.geometry('{}x{}+0+0'.format(*m))
        self.preview_window.title("Dataset Preview")

        self.preview_map  = FigureCanvasTkAgg(self.fig, master=self.preview_window)
        self.preview_map.draw()
        self.preview_map.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.preview_map , self.preview_window)
        toolbar.update()
        self.preview_map.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  

        path_frame = tk.Frame(self.preview_window)
        path_frame.pack(side=tk.TOP)

        next_button = tk.Button(path_frame, text="Next", font=("Helvetica", 14), command= self.draw_map)
        

        s2_path_label = tk.Label(path_frame, text='Sentinel-2 images paths: ', font=("Helvetica", 14)) 
        s1_path_label = tk.Label(path_frame, text='Sentinel-1 images paths: ', font=("Helvetica", 14)) 
        

        self.S2_text = tk.Text(path_frame, height=4, width=50)
        self.S1_text = tk.Text(path_frame, height=4, width=50)

        S2_scroll = tk.Scrollbar(path_frame)
        S2_scroll.config(command=self.S2_text.yview)
        self.S2_text.config(yscrollcommand=S2_scroll.set)

        S1_scroll = tk.Scrollbar(path_frame)
        S1_scroll.config(command=self.S1_text.yview)

        next_button.grid(row=1, column=1)

        s2_path_label.grid(row=1, column=2)
        self.S2_text.grid(row=1, column=3)
        S2_scroll.grid(row=1, column=4)

        s1_path_label.grid(row=1, column=5)
        self.S1_text.grid(row=1, column=6)
        S1_scroll.grid(row=1, column=7)
        
        #self.S1_text.insert(tk.END, self.vv_path)

        
        self.draw_map()

        #----When press the x button then destroy the child window
        #self.preview_window.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        self.preview_window.destroy()
