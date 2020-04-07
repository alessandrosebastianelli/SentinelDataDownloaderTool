import tkinter as tk
from GeneratorWidget import *
from DownloaderWidget import *
from ConverterWidget import *
from CleanerWidget import *
from PatchExtractorWidget import *
from AutomaticToolWidget import *
from MenuBarWidget import *
import os

root = tk.Tk()
root.iconphoto(False, tk.PhotoImage(file=os.path.join('gui_code','icon.png')))
root.geometry('650x700')
root.title('Sentinel Data Downloader Tool')
root.resizable(False, False)

menubarWidget = MenuBarWidget(root)
generatorWidget  = GeneratorWidget(root)
downloaderWidget = DownloaderWidget(root, generatorWidget)
converterWidget  = ConverterWidget(root, downloaderWidget)
cleanerWidget = CleanerWidget(root, downloaderWidget)
patchextractorWidget = PatchExtractorWidget(root, downloaderWidget)
automatictoolWidget = AutomaticToolWidget(root)

root.mainloop()