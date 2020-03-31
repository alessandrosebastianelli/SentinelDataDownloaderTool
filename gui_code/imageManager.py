import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt



def date_sort(e):
    
    ''' 
        This function is used to sort the paths by the months order. 
    '''
    
    s = 0
    if 'Jan' in e:
        s = 0
    elif 'Feb' in e:
        s = 1
    elif 'Mar' in e:
        s = 2
    elif 'Apr' in e:
        s = 3
    elif 'May' in e:
        s = 4
    elif 'Jun' in e:
        s = 5
    elif 'Jul' in e:
        s = 6
    elif 'Aug' in e:
        s = 7
    elif 'Sep' in e:
        s = 8
    elif 'Oct' in e:
        s = 9
    elif 'Nov' in e:
        s = 10
    elif 'Dec' in e:
        s = 11
    
    return s

def load_s1_paths(path, months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
  locations = os.listdir(path)
  sentinel_images = []

  for raw_location in locations:
    location = os.path.join(path, raw_location)
    dates = os.listdir(location)
    

    for raw_date in dates:
      date = os.path.join(location, raw_date)
      
      images = os.listdir(date)

      for raw_image in images:
        if not('.tfw') in raw_image:
          image = os.path.join(date, raw_image)
          sentinel_images.append(image)

  sentinel_images.sort(key=date_sort)
  splitted = []

  for month in months:  
    partial = []
    for img in sentinel_images:
      if month in img:
        partial.append(img)
    splitted.append(partial)

  return splitted

def load_s2_paths(path, months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
  locations = os.listdir(path)
  sentinel_images = []

  for raw_location in locations:
    location = os.path.join(path, raw_location)
    dates = os.listdir(location)
    

    for raw_date in dates:
      date = os.path.join(location, raw_date)
      
      images = os.listdir(date)

      for raw_image in images:
        image = os.path.join(date, raw_image)
        sentinel_images.append(image)

  sentinel_images.sort(key=date_sort)
  splitted_RGB = []
  splitted_CM = []

  for month in months:  
    partial_RGB = []
    partial_CM = []
    for img in sentinel_images:
      if month in img:
        if 'RGB' in img:
          partial_RGB.append(img)
        else:
          partial_CM.append(img)

    splitted_RGB.append(partial_RGB)
    splitted_CM.append(partial_CM)

  return splitted_RGB, splitted_CM

def load_image(path, normalization='minmax'):
    
  if '.tif' in path:
      
    dataset = rasterio.open(path)
    img = dataset.read()

    if 'sen2' in path:
      image = np.zeros((1000,1000,3))
    else:
      image = np.zeros((1000,1000, 1))

    
    for i in range(image.shape[2]):
      raw = dataset.read(i+1)
      image[..., i] = raw[:1000, :1000, ...]
        
    dataset.close()
  else:
    image = plt.imread(path)
      
  if normalization == 'minmax':
    image = (image - image.min())/(image.max() - image.min())
    image = np.clip(image, 0.0, 1.0)
  elif normalization == 'max':
    image = image/image.max()
    image = np.clip(image, 0.0, 1.0)
  elif normalization == 'std':
    image = (image - image.mean())/(image.std())
    image = np.clip(image, 0.0, 1.0)
      
  return image 

def generator(path, sentinel):
  if sentinel == 'sen2':
    splitted_RGB, splitted_CM = load_s2_paths(path)
    counter = 0;
    while True:

      RGB = []
      CM = []
      for i in range(3):
        try:
          RGB.append(splitted_RGB[counter][i])
          CM.append(splitted_CM[counter][i])
        except:
          pass

      counter = counter + 1
      
      yield RGB, CM
  else:
    splitted_GRAY = load_s1_paths(path)
    counter = 0;
    while True:

      GRAY = []
      for i in range(3):
        try:
          GRAY.append(splitted_GRAY[counter][i])
        except:
          pass

      counter = counter + 1
      
      yield GRAY    