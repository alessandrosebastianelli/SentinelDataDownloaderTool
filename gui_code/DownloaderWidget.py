import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Separator
import tkinter.font as TkFont

class DownloaderWidget:
  def __init__(self, root):
    self.root = root
    self.helv16 = TkFont.Font(self.root, family="Helvetica",size=16)
    self.helv22 = TkFont.Font(self.root, family="Helvetica",size=26)
    self.date_var = tk.StringVar(self.root)
    self.band_var = tk.StringVar(self.root)
    self.number_of_images = tk.StringVar(root, value='3')
    self.band_options = ["RGB+QA60"]
    self.date_options = ["Jan-Dec"]

    self.createGUI(self.root)

  def createGUI(self, root):
    #---------------------- DOWNLOADER FRAME ---------------------
    downloader_frame = tk.Frame(root)
    downloader_frame.grid(row=2, column=1, sticky=tk.E, pady=15)
    #------------------- DOWNLOADER SUB FRAME 1 ------------------
    downloader_sub_frame_1 = tk.Frame(downloader_frame)
    downloader_sub_frame_1.grid(row=1, column=1, sticky=tk.E)

    downloader_label = tk.Label(downloader_sub_frame_1, text='DOWNLOADER', font=self.helv22)
    downloader_label.grid(row=1, column=1, sticky=tk.E)

    self.downloader_progress = Progressbar(downloader_sub_frame_1, orient=tk.HORIZONTAL, length=400, mode='determinate') 
    self.downloader_progress.grid(row=1, column=2, sticky=tk.E)

    #------------------- DOWNLOADER SUB FRAME 2 ------------------
    downloader_sub_frame_2 = tk.Frame(downloader_frame)
    downloader_sub_frame_2.grid(row=2, column=1, sticky=tk.E)

    n_of_images_label = tk.Label(downloader_sub_frame_2, text='Number of images', font=self.helv16)
    n_of_images_label.grid(row=2, column=1)
    self.n_of_images_area = tk.Entry(downloader_sub_frame_2, textvariable=self.number_of_images, width=10, font=self.helv16, borderwidth=1, relief="solid")
    self.n_of_images_area.grid(row=2, column=2)

    date_def_label = tk.Label(downloader_sub_frame_2, text='Date definition', font=self.helv16)
    date_def_label.grid(row=2, column=3)
    
    self.date_var.set(self.date_options[0])
    date_menu = tk.OptionMenu(downloader_sub_frame_2, self.date_var, *self.date_options)
    date_menu.config(width=15, font=self.helv16)
    date_menu.grid(row=2, column=4)

    self.download_button = tk.Button(downloader_sub_frame_2, text='DOWNLOAD', height=1, width=15, font=self.helv16, command = None)
    self.download_button.grid(row=3, column=1, sticky=tk.E)

    band_def_label = tk.Label(downloader_sub_frame_2, text='Band definition', font=self.helv16)
    band_def_label.grid(row=3, column=3)
    
    self.band_var.set(self.band_options[0])
    band_menu = tk.OptionMenu(downloader_sub_frame_2, self.band_var, *self.band_options)
    band_menu.config(width=15, font=self.helv16)
    band_menu.grid(row=3, column=4)


