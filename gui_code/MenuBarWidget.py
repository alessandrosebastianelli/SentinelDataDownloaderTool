import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Separator
import tkinter.font as TkFont
from PreviewWidget import *
from WorldMapWidget import *

class MenuBarWidget:
  def __init__(self, root):
    self.root = root
    self.helv16 = TkFont.Font(self.root, family="Helvetica",size=16)
    self.helv22 = TkFont.Font(self.root, family="Helvetica",size=26)
    self.createGUI(self.root)

  def openPreviewWidget(self):
    self.previewWidget = PreviewWidget(self.root)
  
  def openWorldMap(self):
    self.worldmapWidget = WorldMapWidget(self.root)

  def createGUI(self, root):
    #------------------------- MENU BAR -------------------------
    self.menubar = tk.Menu(tearoff=False)

    self.file_menu = tk.Menu(self.menubar, tearoff=False)
    self.menubar.add_cascade(label='File', menu=self.file_menu)

    self.settings_menu = tk.Menu(self.menubar, tearoff=False)
    self.menubar.add_cascade(label='Settings', menu=self.settings_menu)

    self.authentication_menu = tk.Menu(self.menubar, tearoff=False)
    self.menubar.add_cascade(label='Authentication', menu=self.authentication_menu)

    # Preview Menu
    self.preview_menu = tk.Menu(self.menubar, tearoff=False)
    self.menubar.add_cascade(label='Preview', menu=self.preview_menu)
    self.preview_menu.add_command(label='Open Preview Manager', command=self.openPreviewWidget)

    self.world_map_menu = tk.Menu(self.menubar, tearoff=False)
    self.menubar.add_cascade(label='World Map', menu=self.world_map_menu)
    self.world_map_menu.add_command(label='Open World Map', command=self.openWorldMap)

    self.root.config(menu=self.menubar)