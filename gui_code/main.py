import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Separator
import tkinter.font as TkFont
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from GeneratorWidget import *
from DownloaderWidget import *
from ConverterWidget import *
from CleanerWidget import *
from PatchExtractorWidget import *

root = tk.Tk()
root.geometry('650x600')
root.title('Sentinel Data Downloader Tool')
root.resizable(False, False)
helv16 = TkFont.Font(root, family="Helvetica",size=16)#,weight="bold")
helv22 = TkFont.Font(root, family="Helvetica",size=26)#,weight="bold")

#------------------------- MENU BAR -------------------------
menubar = tk.Menu(tearoff=False)

file_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='File', menu=file_menu)
settings_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='Settings', menu=settings_menu)
authentication_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='Authentication', menu=authentication_menu)
preview_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='Preview', menu=preview_menu)
world_map_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='World Map', menu=world_map_menu)
# display the menu
root.config(menu=menubar)

generatorWidget  = GeneratorWidget(root)
downloaderWidget = DownloaderWidget(root)
converterWidget  = ConverterWidget(root)
cleanerWidget = CleanerWidget(root)
patchextractorWidget = PatchExtractorWidget(root)


#sep = Separator(root, orient="horizontal")
#sep.pack(side = tk.TOP, anchor="nw", fill=tk.X)

root.mainloop()