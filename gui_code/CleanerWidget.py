import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Separator
import tkinter.font as TkFont

class CleanerWidget:
  def __init__(self, root):
    self.root = root
    self.helv16 = TkFont.Font(self.root, family="Helvetica",size=16)
    self.helv22 = TkFont.Font(self.root, family="Helvetica",size=26)
    self.createGUI(self.root)

  def createGUI(self, root):
    #----------------------- CLEANER FRAME ---------------------
    cleaner_frame = tk.Frame(root)
    cleaner_frame.grid(row=4, column=1, sticky=tk.E, pady=15)
    #-------------------- CLEANER SUB FRAME 1 ------------------
    cleaner_sub_frame_1 = tk.Frame(cleaner_frame)
    cleaner_sub_frame_1.grid(row=1, column=1, sticky=tk.E)

    cleaner_label = tk.Label(cleaner_sub_frame_1, text='CLEANER', font=self.helv22)
    cleaner_label.grid(row=1, column=1, sticky=tk.E)

    self.cleaner_progress = Progressbar(cleaner_sub_frame_1, orient=tk.HORIZONTAL, length=400, mode='determinate') 
    self.cleaner_progress.grid(row=1, column=2, sticky=tk.E)

    #------------------- CLEANER SUB FRAME 2 ------------------
    cleaner_sub_frame_2 = tk.Frame(cleaner_frame)
    cleaner_sub_frame_2.grid(row=2, column=1, sticky=tk.E)

    self.cleaner_button = tk.Button(cleaner_sub_frame_2, text='CLEAN', height=1, width=15, font=self.helv16, command = None)
    self.cleaner_button.grid(row=2, column=1, sticky=tk.E)
    self.manual_cleaner_button = tk.Button(cleaner_sub_frame_2, text='MANUAL CLEAN', height=1, width=15, font=self.helv16, command = None)
    self.manual_cleaner_button.grid(row=2, column=2, sticky=tk.E)


