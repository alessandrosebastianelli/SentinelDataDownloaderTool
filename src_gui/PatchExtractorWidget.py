import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Separator
import tkinter.font as TkFont
import patch_extractor
import os
import platform

class PatchExtractorWidget:
  def __init__(self, root, downloaderWidget):
    self.root = root
    self.downloaderWidget = downloaderWidget
    self.helv16 = TkFont.Font(self.root, family="Helvetica",size=16)
    self.helv22 = TkFont.Font(self.root, family="Helvetica",size=26)
    self.extractor_size = tk.StringVar(root, value='256')
    self.createGUI(self.root)

  def extractCommand(self):
    system = platform.system()
    if system == 'Windows':
      windows = True
    else:
      windows = False
    _, _, date_names = self.downloaderWidget.getDate()
    image_size = self.downloaderWidget.getSceneSizeInPixel()

    patch_extractor.extract(self.extractor_progress, 
                      os.path.join(os.getcwd(), 'gui_code', 'dataset', 'sen2', '*'), 
                      os.path.join(os.getcwd(), 'gui_code', 'dataset', 'sen1', '*'), 
                      os.path.join(os.getcwd(), 'gui_code', 'dataset_patch', 'preview', ""), 
                      date_names, 
                      image_size, 
                      int(self.extractor_size.get()), 
                      windows)

  def createGUI(self, root):
    #--------------- PATCH EXTRACTOR FRAME ---------------------
    extractor_frame = tk.Frame(root)
    extractor_frame.grid(row=5, column=1, sticky=tk.E, pady=3)
    #------------ PATCH EXTRACTOR SUB FRAME 1 -------------------
    extractor_sub_frame_1 = tk.Frame(extractor_frame)
    extractor_sub_frame_1.grid(row=1, column=1, sticky=tk.E)

    extractor_label = tk.Label(extractor_sub_frame_1, text='EXTRACTOR', font=self.helv22)
    extractor_label.grid(row=1, column=1, sticky=tk.E)

    self.extractor_progress = Progressbar(extractor_sub_frame_1, orient=tk.HORIZONTAL, length=400, mode='determinate') 
    self.extractor_progress.grid(row=1, column=2, sticky=tk.E)

    #------------ PATCH EXTRACTOR SUB FRAME 2 -------------------
    extractor_sub_frame_2 = tk.Frame(extractor_frame)
    extractor_sub_frame_2.grid(row=2, column=1, sticky=tk.E)

    extractor_x_label = tk.Label(extractor_sub_frame_2, text='Patch Size', font=self.helv16)
    extractor_x_label.grid(row=2, column=1, sticky=tk.E)
    self.extractor_x_area = tk.Entry(extractor_sub_frame_2, textvariable=self.extractor_size, width=10, font=self.helv16, borderwidth=1, relief="solid")
    self.extractor_x_area.grid(row=2, column=2, sticky=tk.E)

    self.extractor_button = tk.Button(extractor_sub_frame_2, text='EXTRACT', height=2, width=15, font=self.helv16, command = self.extractCommand)
    self.extractor_button.grid(row=2, column=3, sticky=tk.E)


