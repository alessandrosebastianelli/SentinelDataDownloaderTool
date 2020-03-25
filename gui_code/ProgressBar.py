import tkinter as tk
from tkinter import ttk

class ProgressBar:

    def __init__(self, title, max_value = 100):
        self.master = tk.Tk()
        self.master.title(title)
        self.master.resizable(False, False)

        self.maxValue=max_value
        self.progressbar=ttk.Progressbar(self.master,orient="horizontal",length=300,mode="determinate")
        self.progressbar.pack(side=tk.TOP)
        
        self.percentage = 0
        self.percentage_label = tk.Label(self.master, text=str(self.percentage) + "%")
        self.percentage_label.pack(side="bottom")

        self.currentValue=0
        self.progressbar["value"]=self.currentValue
        self.progressbar["maximum"]= self.maxValue

    def progress(self, currentValue):
         self.progressbar["value"]=currentValue

    def update(self):
        self.currentValue= self.currentValue+1
        self.progress(self.currentValue)
        self.progressbar.update() # Force an update of the GUI
        self.percentage = int((self.currentValue / self.maxValue)*100)
        self.percentage_label.config(text=str(self.percentage) + "%")

    def close(self):
        self.master.destroy()
