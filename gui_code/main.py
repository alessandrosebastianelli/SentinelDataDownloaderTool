import tkinter as tk
from tkinter.ttk import Separator
import tkinter.font as TkFont


from GeneratorWidget import *
from DownloaderWidget import *
from ConverterWidget import *
from CleanerWidget import *
from PatchExtractorWidget import *
from AutomaticToolWidget import *
from MenuBarWidget import *

root = tk.Tk()
root.geometry('650x700')
root.title('Sentinel Data Downloader Tool')
root.resizable(False, False)
helv16 = TkFont.Font(root, family="Helvetica",size=16)#,weight="bold")
helv22 = TkFont.Font(root, family="Helvetica",size=26)#,weight="bold")


menubarWidget = MenuBarWidget(root)
generatorWidget  = GeneratorWidget(root)
downloaderWidget = DownloaderWidget(root)
converterWidget  = ConverterWidget(root)
cleanerWidget = CleanerWidget(root)
patchextractorWidget = PatchExtractorWidget(root)
automatictoolWidget = AutomaticToolWidget(root)

root.mainloop()