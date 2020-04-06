import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Separator
import tkinter.font as TkFont
import downloader
import os
import platform


class DownloaderWidget:
  def __init__(self, root, generatorWidget):
    self.root = root
    self.generatorWidget = generatorWidget

    self.helv16 = TkFont.Font(self.root, family="Helvetica",size=16)
    self.helv22 = TkFont.Font(self.root, family="Helvetica",size=26)
    self.date_var = tk.StringVar(self.root)
    self.band_var = tk.StringVar(self.root)
    self.number_of_scenes = tk.StringVar(root, value='20')
    self.number_of_images = tk.StringVar(root, value='3')
    self.scene_size = tk.StringVar(root, value = '10')
    self.band_options = ["RGB+QA60 & VV", "RGB & VV", "RGB+QA60 & VH", "RGB & VH"]
    self.date_options = ["Jan-Dec 2019", "Jan-Dec 2018", "Jan-Dec 2017", "Jan-Dec 2016"]

    self.createGUI(self.root)

  def downloadCommand(self):

    points = self.generatorWidget.getPoints()

    if points is None:
      tk.messagebox.showinfo("Error", "Before starting the downloading process, please generate, load or get new points!!!")
    else:
      s2_selectors, s1_selectors = self.getBandFromOptions()
      start_date, end_date, date_names = self.getDate()
      n_of_regions = int(self.number_of_scenes.get())
      n_of_images = int(self.number_of_images.get())
      scene_size = int(self.scene_size.get())
      
      system = platform.system()
      if system == 'Windows':
        windows = True
      else:
        windows = False

      downloader.download(self.downloader_progress, 
        points, 
        scene_size, 
        start_date, 
        end_date, 
        date_names, 
        s2_selectors, 
        s1_selectors, 
        n_of_regions, 
        n_of_images, 
        os.path.join(os.getcwd(), 'gui_code', 'download', '*'),
        os.path.join(os.getcwd(), 'gui_code', 'download'),
        os.path.join(os.getcwd(), 'gui_code', 'data', 'sen2',""),
        os.path.join(os.getcwd(), 'gui_code', 'data', 'sen1',""),
        windows)
    
  def getDate(self):
    date_names = []
    start_date = []
    end_date = []
    date_options = self.date_var.get()

    if date_options == 'Jan-Dec 2019':
      start_date = ['2019-01-01','2019-02-01','2019-03-01','2019-04-01','2019-05-01','2019-06-01','2019-07-01','2019-08-01','2019-09-01','2019-10-01','2019-11-01','2019-12-01']
      end_date =   ['2019-01-28','2019-02-28','2019-03-28','2019-04-28','2019-05-28','2019-06-28','2019-07-28','2019-08-28','2019-09-28','2019-10-28','2019-11-28','2019-12-28']
      date_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    elif date_options == 'Jan-Dec 2018':
      start_date = ['2018-01-01','2018-02-01','2018-03-01','2018-04-01','2018-05-01','2018-06-01','2018-07-01','2018-08-01','2018-09-01','2018-10-01','2018-11-01','2018-12-01']
      end_date =   ['2018-01-28','2018-02-28','2018-03-28','2018-04-28','2018-05-28','2018-06-28','2018-07-28','2018-08-28','2018-09-28','2018-10-28','2018-11-28','2018-12-28']
      date_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    elif date_options == 'Jan-Dec 2017':
      start_date = ['2017-01-01','2017-02-01','2017-03-01','2017-04-01','2017-05-01','2017-06-01','2017-07-01','2017-08-01','2017-09-01','2017-10-01','2017-11-01','2017-12-01']
      end_date =   ['2017-01-28','2017-02-28','2017-03-28','2017-04-28','2017-05-28','2017-06-28','2017-07-28','2017-08-28','2017-09-28','2017-10-28','2017-11-28','2017-12-28']
      date_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    elif date_options == 'Jan-Dec 2016':
      start_date = ['2016-01-01','2016-02-01','2016-03-01','2016-04-01','2016-05-01','2016-06-01','2016-07-01','2016-08-01','2016-09-01','2016-10-01','2016-11-01','2016-12-01']
      end_date =   ['2016-01-28','2016-02-28','2016-03-28','2016-04-28','2016-05-28','2016-06-28','2016-07-28','2016-08-28','2016-09-28','2016-10-28','2016-11-28','2016-12-28']
      date_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    return start_date, end_date, date_names

  def getBandFromOptions(self):
    band_options = self.band_var.get()
    s2_selectors = []
    s1_selectors = []
    if band_options == 'RGB+QA60 & VV':
      s2_selectors = ["B2", "B3", "B4", "QA60"]
      s1_selectors = ["VV"]
    elif band_options == 'RGB & VV':
      s2_selectors = ["B2", "B3", "B4"]
      s1_selectors = ["VV"]
    elif band_options == 'RGB+QA60 & VH':
      s2_selectors = ["B2", "B3", "B4", "QA60"]
      s1_selectors = ["VH"]
    elif band_options == 'RGB & VH':
      s2_selectors = ["B2", "B3", "B4"]
      s1_selectors = ["VH"]
    
    return s2_selectors, s1_selectors

  def createGUI(self, root):
    #---------------------- DOWNLOADER FRAME ---------------------
    downloader_frame = tk.Frame(root)
    downloader_frame.grid(row=2, column=1, sticky=tk.E, pady=3)
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

    n_of_scenes_label = tk.Label(downloader_sub_frame_2, text='Number of scenes', font=self.helv16)
    n_of_scenes_label.grid(row=2, column=1, sticky=tk.E)
    self.n_of_scenes_area = tk.Entry(downloader_sub_frame_2, textvariable=self.number_of_scenes, width=10, font=self.helv16, borderwidth=1, relief="solid")
    self.n_of_scenes_area.grid(row=2, column=2, sticky=tk.E)

    n_of_images_label = tk.Label(downloader_sub_frame_2, text='Number of images per date', font=self.helv16)
    n_of_images_label.grid(row=3, column=1, sticky=tk.E)
    self.n_of_images_area = tk.Entry(downloader_sub_frame_2, textvariable=self.number_of_images, width=10, font=self.helv16, borderwidth=1, relief="solid")
    self.n_of_images_area.grid(row=3, column=2, sticky=tk.E)

    date_def_label = tk.Label(downloader_sub_frame_2, text='Date definition', font=self.helv16)
    date_def_label.grid(row=2, column=3, sticky=tk.E)
    
    self.date_var.set(self.date_options[0])
    date_menu = tk.OptionMenu(downloader_sub_frame_2, self.date_var, *self.date_options)
    date_menu.config(width=15, font=self.helv16)
    date_menu.grid(row=2, column=4, sticky=tk.E)

    scene_size_label = tk.Label(downloader_sub_frame_2, text='Scene size', font=self.helv16)
    scene_size_label.grid(row=4, column=1, sticky=tk.E)
    self.scene_size_area = tk.Entry(downloader_sub_frame_2, textvariable=self.scene_size, width=10, font=self.helv16, borderwidth=1, relief="solid")
    self.scene_size_area.grid(row=4, column=2, sticky=tk.E)


    band_def_label = tk.Label(downloader_sub_frame_2, text='Band definition', font=self.helv16)
    band_def_label.grid(row=3, column=3, sticky=tk.E)
    
    self.band_var.set(self.band_options[0])
    band_menu = tk.OptionMenu(downloader_sub_frame_2, self.band_var, *self.band_options)
    band_menu.config(width=15, font=self.helv16)
    band_menu.grid(row=3, column=4, sticky=tk.E)

    self.download_button = tk.Button(downloader_sub_frame_2, text='DOWNLOAD', height=2, width=15, font=self.helv16, command = self.downloadCommand)
    self.download_button.grid(row=4, column=4, sticky=tk.E)
