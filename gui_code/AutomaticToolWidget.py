import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Separator
import tkinter.font as TkFont

class AutomaticToolWidget:
  def __init__(self, root):
    self.root = root
    self.helv16 = TkFont.Font(self.root, family="Helvetica",size=16)
    self.helv22 = TkFont.Font(self.root, family="Helvetica",size=26)
    self.createGUI(self.root)

  def createGUI(self, root):
    #----------------------- CLEANER FRAME ---------------------
    main_frame = tk.Frame(root)
    main_frame.grid(row=6, column=1, sticky=tk.E, pady=15)

    generator_label = tk.Label(main_frame, text='AUTOMATIC', font=self.helv22)
    generator_label.grid(row=1, column=1, sticky=tk.E)

    generator_label = tk.Label(main_frame, text='Generator', font=self.helv16)
    generator_label.grid(row=2, column=1, sticky=tk.E)
    self.generator_progress = Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='determinate') 
    self.generator_progress.grid(row=2, column=2, sticky=tk.E)

    downloader_label = tk.Label(main_frame, text='Downloader', font=self.helv16)
    downloader_label.grid(row=3, column=1, sticky=tk.E)
    self.downloader_progress = Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='determinate') 
    self.downloader_progress.grid(row=3, column=2, sticky=tk.E)

    converter_label = tk.Label(main_frame, text='Converter', font=self.helv16)
    converter_label.grid(row=4, column=1, sticky=tk.E)
    self.converter_progress = Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='determinate') 
    self.converter_progress.grid(row=4, column=2, sticky=tk.E)

    cleaner_label = tk.Label(main_frame, text='Cleaner', font=self.helv16)
    cleaner_label.grid(row=5, column=1, sticky=tk.E)
    self.cleaner_progress = Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='determinate') 
    self.cleaner_progress.grid(row=5, column=2, sticky=tk.E)

    extractor_label = tk.Label(main_frame, text='Extractor', font=self.helv16)
    extractor_label.grid(row=6, column=1, sticky=tk.E)
    self.extractor_progress = Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='determinate') 
    self.extractor_progress.grid(row=6, column=2, sticky=tk.E)

    self.start_button = tk.Button(main_frame, text='START', height=1, width=15, font=self.helv16, command = None)
    self.start_button.grid(row=4, column=3, sticky=tk.E)



