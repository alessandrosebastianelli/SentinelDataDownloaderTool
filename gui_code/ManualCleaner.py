import tkinter as tk
import tkinter.font as TkFont
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from imageManager import *
import os

# Global variable
dataset_path = None
sentinel = None
image_generator = None
img1 = None
img2 = None
img3 = None
cm1 = None
cm2 = None
cm3 = None
RGB = None
CM = None
GRAY = None

# Global setting
figsize = (3,3)

def set_path():
  global dataset_path 
  dataset_path = filedialog.askdirectory(initialdir="/", title="Select the dataset path")
  path_area.config(state=tk.NORMAL)
  path_area.delete(1.0,tk.END)
  path_area.insert(tk.END, dataset_path)
  path_area.config(state=tk.DISABLED)

  global sentinel
  global image_generator
  
  # Version 1.0, only Sentinel-1 and Sentinel-2 supported
  if 'sen1' in dataset_path:
    sentinel = 'sen1'
  elif 'sen2' in dataset_path:
    sentinel = 'sen2'

  image_generator = iter(generator(dataset_path, sentinel))
  get_new_data()

def get_new_data():
  global img1
  global img2
  global img3
  global cm1
  global cm2
  global cm3
  global RGB
  global CM
  global GRAY

  if sentinel == 'sen2':
    RGB, CM = next(image_generator)
    try:
      img1 = load_image(RGB[0])
      cm1 = load_image(CM[0])
      ax = fig1.axes[0]
      ax.imshow(img1)
      info1_area.config(state=tk.NORMAL)
      info1_area.delete(1.0,tk.END)
      info1_area.insert(tk.END, RGB[0]+'\n'+CM[0])
      info1_area.config(state=tk.DISABLED)
    except:
      img1 = np.ones((1000, 1000, 3))
      cm1 = np.ones((1000, 1000, 3))
      ax = fig1.axes[0]
      ax.imshow(img1)
      info1_area.delete(1.0,tk.END)
      pass

    try:
      img2 = load_image(RGB[1])
      cm2 = load_image(CM[1])
      ax = fig2.axes[0]
      ax.imshow(img2)
      info2_area.config(state=tk.NORMAL)
      info2_area.delete(1.0,tk.END)
      info2_area.insert(tk.END, RGB[1]+'\n'+CM[1])
      info2_area.config(state=tk.DISABLED)
    except:
      img2 = np.ones((1000, 1000, 3))
      cm2 = np.ones((1000, 1000, 3))
      ax = fig2.axes[0]
      ax.imshow(img2)
      info2_area.delete(1.0,tk.END)
      pass

    try:
      img3 = load_image(RGB[2])
      cm3 = load_image(CM[2])
      ax = fig3.axes[0]
      ax.imshow(img3)
      info3_area.config(state=tk.NORMAL)
      info3_area.delete(1.0,tk.END)
      info3_area.insert(tk.END, RGB[2]+'\n'+CM[2])
      info3_area.config(state=tk.DISABLED)
    except:
      img3 = np.ones((1000, 1000, 3))
      cm3 = np.ones((1000, 1000, 3))
      ax = fig3.axes[0]
      ax.imshow(img3)
      info3_area.delete(1.0,tk.END)
      pass

  else:
    GRAY = next(image_generator)
    print(GRAY)
    try:
      img1 = load_image(GRAY[0])
      ax = fig1.axes[0]
      ax.imshow(img1[...,0])
      info1_area.config(state=tk.NORMAL)
      info1_area.delete(1.0,tk.END)
      info1_area.insert(tk.END, GRAY[0])
      info1_area.config(state=tk.DISABLED)
    except:
      img1 = np.ones((1000, 1000,3))
      ax = fig1.axes[0]
      ax.imshow(img1[...,0])
      info1_area.delete(1.0,tk.END)
      pass
    
    try:
      img2 = load_image(GRAY[1])
      ax = fig2.axes[0]
      ax.imshow(img2[...,0])
      info2_area.config(state=tk.NORMAL)
      info2_area.delete(1.0,tk.END)
      info2_area.insert(tk.END, GRAY[1])
      info2_area.config(state=tk.DISABLED)
    except:
      img2 = np.ones((1000, 1000,3))
      ax = fig2.axes[0]
      ax.imshow(img2[...,0])
      info2_area.delete(1.0,tk.END)
      pass

    try:
      img3 = load_image(GRAY[2])
      ax = fig3.axes[0]
      ax.imshow(img3[...,0])
      info3_area.config(state=tk.NORMAL)
      info3_area.delete(1.0,tk.END)
      info3_area.insert(tk.END, GRAY[2])
      info3_area.config(state=tk.DISABLED)
    except:
      img3 = np.ones((1000, 1000,3))
      ax = fig3.axes[0]
      ax.imshow(img3[...,0])
      info3_area.delete(1.0,tk.END)
      pass
    
  canvas1.draw()
  canvas2.draw()
  canvas3.draw()
  info1_area.update()
  info2_area.update()
  info3_area.update()
  
def nextBatch():
  answer = tk.messagebox.askyesno(title='Cleaning dataset', message='Do you want to remove the images?')
  if answer:
    keep = image_number.get()
    if sentinel == 'sen1':
      for i in range(len(GRAY)):
        if i != keep:
          os.remove(GRAY[i])
    else:
      for i in range(len(RGB)):
        if i != keep:
          os.remove(RGB[i])
          os.remove(CM[i])
    get_new_data()


def drawCloudMask1():
  try:
    ax = fig1.axes[0]
    ax.imshow(cm1)
  except:
    pass
  canvas1.draw()

def drawCloudMask2():
  try:
    ax = fig2.axes[0]
    ax.imshow(cm2)
  except:
    pass
  
  canvas2.draw()

def drawCloudMask3():
  try:
    ax = fig3.axes[0]
    ax.imshow(cm3)
  except:
    pass

  canvas3.draw()

root = tk.Tk()
root.geometry('900x570')
root.title('Manual Cleaner')
root.resizable(False, False)
helv36 = TkFont.Font(root, family="Helvetica",size=16)#,weight="bold")

#-------------------- PATH FRAME ------------------
path_frame = tk.Frame(root)
path_frame.pack(side=tk.TOP)

path_area = tk.Text(path_frame, height=2, width=80, font=helv36, borderwidth=1, relief="solid")
path_area.config(state=tk.DISABLED)
path_area.grid(row=1, column=1, sticky=tk.W)

path_button = tk.Button(path_frame, text='SET PATH', height=2, width=15, font=helv36, command=set_path)
path_button.grid(row=1, column=2)

#-------------------- IMAGES FRAME ------------------
images_frame = tk.Frame(root)
images_frame.pack(side=tk.TOP)

fig1= Figure(figsize=figsize, dpi=100)
fig1.add_subplot(111)
fig1.subplots_adjust(left=0.03, bottom=0.07, right=0.98, top=0.97, wspace=0, hspace=0)
ax = fig1.axes[0]
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
canvas1 = FigureCanvasTkAgg(fig1, master=images_frame)  # A tk.DrawingArea.
canvas1.get_tk_widget().grid(row=2, column=1, sticky=tk.W)
fig2= Figure(figsize=figsize, dpi=100)
fig2.add_subplot(111)
fig2.subplots_adjust(left=0.03, bottom=0.07, right=0.98, top=0.97, wspace=0, hspace=0)
ax = fig2.axes[0]
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
canvas2 = FigureCanvasTkAgg(fig2, master=images_frame)  # A tk.DrawingArea.
canvas2.get_tk_widget().grid(row=2, column=2, sticky=tk.W)
fig3= Figure(figsize=figsize, dpi=100)
fig3.add_subplot(111)
fig3.subplots_adjust(left=0.03, bottom=0.07, right=0.98, top=0.97, wspace=0, hspace=0)
ax = fig3.axes[0]
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
canvas3 = FigureCanvasTkAgg(fig3, master=images_frame)  # A tk.DrawingArea.
canvas3.get_tk_widget().grid(row=2, column=3, sticky=tk.W)

cloud1_button = tk.Button(images_frame, text='CLOUD MASK', height=2, width=15, font=helv36, command = drawCloudMask1)
cloud1_button.grid(row=1, column=1)
cloud2_button = tk.Button(images_frame, text='CLOUD MASK', height=2, width=15, font=helv36, command = drawCloudMask2)
cloud2_button.grid(row=1, column=2)
cloud3_button = tk.Button(images_frame, text='CLOUD MASK', height=2, width=15, font=helv36, command = drawCloudMask3)
cloud3_button.grid(row=1, column=3)

image_number = tk.IntVar()
image1 = tk.Radiobutton(images_frame, text="KEEP", variable=image_number, value=0, font=helv36)
image1.grid(row=3, column=1)
image2 = tk.Radiobutton(images_frame, text="KEEP", variable=image_number, value=1, font=helv36)
image2.grid(row=3, column=2)
image3 = tk.Radiobutton(images_frame, text="KEEP", variable=image_number, value=2, font=helv36)
image3.grid(row=3, column=3)

#-------------------- INFO and NEXT FRAME ------------------

info_frame = tk.Frame(root)
info_frame.pack(side=tk.TOP)

info1_area = tk.Text(info_frame, height=2, width=80, font=helv36, borderwidth=1, relief="solid")
info1_area.config(state=tk.DISABLED)
info1_area.grid(row=1, column=1, sticky=tk.W)
info2_area = tk.Text(info_frame, height=2, width=80, font=helv36, borderwidth=1, relief="solid")
info2_area.config(state=tk.DISABLED)
info2_area.grid(row=2, column=1, sticky=tk.W)
info3_area = tk.Text(info_frame, height=2, width=80, font=helv36, borderwidth=1, relief="solid")
info3_area.config(state=tk.DISABLED)
info3_area.grid(row=3, column=1, sticky=tk.W)

next_button = tk.Button(info_frame, text = 'NEXT', height=2, width=15, font=helv36, command = nextBatch)
next_button.grid(row=2, column=2)

root.mainloop()