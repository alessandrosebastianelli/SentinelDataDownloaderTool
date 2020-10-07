import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Separator
import tkinter.font as TkFont
import converter
import os
import platform

class ConverterWidget:
  def __init__(self, root, downloaderWidget):
    self.root = root
    self.downloaderWidget = downloaderWidget
    self.helv16 = TkFont.Font(self.root, family="Helvetica",size=16)
    self.helv22 = TkFont.Font(self.root, family="Helvetica",size=26)
    self.normalization_types = ["Min-Max", "Max", "Standarditazion"]
    self.normalization_var = tk.StringVar(root)
    self.output_types = ["tif", "png"]
    self.output_var = tk.StringVar(root)
    self.createGUI(self.root)

  def convertCommand(self):
    system = platform.system()
    if system == 'Windows':
      windows = True
    else:
      windows = False

    s2_selectors, s1_selectors = self.getSelectors()
    s2_conversion_mode = self.getNormalizationType()
    
    converter.convert_s2(self.converter_progress, 
      os.path.join(os.getcwd(), 'gui_code', 'data', 'sen2', "*"),
      os.path.join(os.getcwd(), 'gui_code', 'data', 'sen1', "*"),
      self.downloaderWidget.getSceneSizeInPixel(), 
      s2_selectors,
      s1_selectors,
      s2_conversion_mode,
      windows)

    converter.convert_s1(self.converter_progress, 
      os.path.join(os.getcwd(), 'gui_code', 'data', 'sen2',"*"),
      os.path.join(os.getcwd(), 'gui_code', 'data', 'sen1',"*"),
      self.downloaderWidget.getSceneSizeInPixel(), 
      s2_selectors,
      s1_selectors,
      s2_conversion_mode,
      windows)

  def getNormalizationType(self):
    norm_type_raw = self.normalization_var.get()

    return 's&n'

  def getSelectors(self):
    band_options = self.downloaderWidget.getSelectors()
    if band_options == 'RGB+QA60 & VV':
      s2_selectors = ["B4", "B3", "B2", "QA60"]
      s1_selectors = ["VV"]
    elif band_options == 'RGB & VV':
      s2_selectors = ["B4", "B3", "B3"]
      s1_selectors = ["VV"]
    elif band_options == 'RGB+QA60 & VH':
      s2_selectors = ["B4", "B3", "B2", "QA60"]
      s1_selectors = ["VH"]
    elif band_options == 'RGB & VH':
      s2_selectors = ["B4", "B3", "B2"]
      s1_selectors = ["VH"]

    return s2_selectors, s1_selectors

  def createGUI(self, root):
    #----------------------- CONVERTER FRAME ---------------------
    converter_frame = tk.Frame(root)
    converter_frame.grid(row=3, column=1, sticky=tk.E, pady=3)
    #-------------------- CONVERTER SUB FRAME 1 ------------------
    converter_sub_frame_1 = tk.Frame(converter_frame)
    converter_sub_frame_1.grid(row=1, column=1, sticky=tk.E)

    converter_label = tk.Label(converter_sub_frame_1, text='CONVERTER', font=self.helv22)
    converter_label.grid(row=1, column=1, sticky=tk.E)

    self.converter_progress = Progressbar(converter_sub_frame_1, orient=tk.HORIZONTAL, length=400, mode='determinate') 
    self.converter_progress.grid(row=1, column=2, sticky=tk.E)

    #------------------- CONVERTER SUB FRAME 2 ------------------
    converter_sub_frame_2 = tk.Frame(converter_frame)
    converter_sub_frame_2.grid(row=2, column=1, sticky=tk.E)

    normalization_type_label = tk.Label(converter_sub_frame_2, text='Normalization type', font=self.helv16)
    normalization_type_label.grid(row=2, column=2, sticky=tk.E)
    
    self.normalization_var.set(self.normalization_types[0])
    normalization_menu = tk.OptionMenu(converter_sub_frame_2, self.normalization_var, *self.normalization_types)
    normalization_menu.config(width=15, font=self.helv16)
    normalization_menu.grid(row=2, column=3)

    output_type_label = tk.Label(converter_sub_frame_2, text='Output type', font=self.helv16)
    output_type_label.grid(row=3, column=2, sticky=tk.E)
    
    self.output_var.set(self.output_types[0])
    output_menu = tk.OptionMenu(converter_sub_frame_2, self.output_var, *self.output_types)
    output_menu.config(width=15, font=self.helv16)
    output_menu.grid(row=3, column=3, sticky=tk.E)

    self.convert_button = tk.Button(converter_sub_frame_2, text='CONVERT', height=2, width=15, font=self.helv16, command = self.convertCommand)
    self.convert_button.grid(row=4, column=3, sticky=tk.E)

