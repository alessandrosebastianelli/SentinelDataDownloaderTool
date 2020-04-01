import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Separator
import tkinter.font as TkFont
import generator

class GeneratorWidget:
  def __init__(self, root):
    self.root = root
    self.helv16 = TkFont.Font(self.root, family="Helvetica",size=16)
    self.helv22 = TkFont.Font(self.root, family="Helvetica",size=26)
    self.number_of_points = tk.StringVar(root, value='1000')

    self.points = None
    self.createGUI(self.root)


  def generateCommand(self):
    n = int(self.number_of_points.get())
    self.points = generator.get_land_coordinates(self.generator_progress, number = n)
  
  def loadCommand(self):
    self.points = generator.load_points(self.generator_progress)

  def getNewCommand(self):
    n = int(self.number_of_points.get())
    self.points = generator.get_new_points(self.generator_progress, n)

  def createGUI(self, root):
    #---------------------- GENERATOR FRAME ----------------------
    generator_frame = tk.Frame(root)
    generator_frame.grid(row=1, column=1, sticky=tk.E)
    #------------------- GENERATOR SUB FRAME 1 -------------------
    generator_sub_frame_1 = tk.Frame(generator_frame)
    generator_sub_frame_1.grid(row=1, column=1, sticky=tk.E)

    generator_label = tk.Label(generator_sub_frame_1, text='GENERATOR', font=self.helv22)
    generator_label.grid(row=1, column=1, sticky=tk.E)

    self.generator_progress = Progressbar(generator_sub_frame_1, orient=tk.HORIZONTAL, length=400, mode='determinate') 
    self.generator_progress.grid(row=1, column=2, sticky=tk.E)

    #------------------- GENERATOR SUB FRAME 2 -------------------
    generator_sub_frame_2 = tk.Frame(generator_frame)
    generator_sub_frame_2.grid(row=2, column=1, sticky=tk.E)

    self.n_of_points_label = tk.Label(generator_sub_frame_2, text='Number of points', font=self.helv16)
    self.n_of_points_label.grid(row=2, column=1, sticky=tk.E)

    self.n_of_points_area = tk.Entry(generator_sub_frame_2, textvariable=self.number_of_points, width=10, font=self.helv16, borderwidth=1, relief="solid")
    self.n_of_points_area.grid(row=2, column=2, sticky=tk.E)

    self.generate_button = tk.Button(generator_sub_frame_2, text='GENERATE', height=2, width=15, font=self.helv16, command = self.generateCommand)
    self.generate_button.grid(row=2, column=3, sticky=tk.E)

    self.load_button = tk.Button(generator_sub_frame_2, text='LOAD', height=2, width=15, font=self.helv16, command = self.loadCommand)
    self.load_button.grid(row=2, column=4, sticky=tk.E)

    self.get_new_button = tk.Button(generator_sub_frame_2, text='GET NEW', height=2, width=15, font=self.helv16, command = self.getNewCommand)
    self.get_new_button.grid(row=2, column=5, sticky=tk.E)
