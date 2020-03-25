from numpy.random import randint
import random
import os
import rasterio
import matplotlib.pyplot as plt
import numpy as np
from ProgressBar import ProgressBar

def get_images_path(path, satellite):
    '''
        It returns a list of path. 
        Satellite must be 'sen1' or 'sen2'.
        Path must be the master folder with 'sen1' and 'sen2' folder inside
    '''


    path = os.path.join(path, satellite)
    
    images_path = []
    
    zones = os.listdir(path)

    pb = ProgressBar('Loading data....', len(zones))
    for zone in zones:
        zone_path = os.path.join(path, zone)
        
        images = os.listdir(zone_path)
        
        for image in images:
            image_path = os.path.join(zone_path, image)
            images_path.append(image_path)

        pb.update()
            
    images_path.sort()
    pb.close()
    return images_path, zones


def get_s2_image(image_path):
	'''
	    It returns an RGB image using a path.
	    Image path must be the full path of an RGB image (tif format)
	'''
    
    # rasterio function to read bands of a tif file
	dataset = rasterio.open(image_path)
	r = dataset.read(1)
	g = dataset.read(2)
	b = dataset.read(3)
	dataset.close()
	# RGB composite
	rgb = np.zeros((r.shape[0],r.shape[1], 3))
	rgb[...,0] = r
	rgb[...,1] = g
	rgb[...,2] = b

	rgb = (rgb - rgb.min())/(rgb.max() - rgb.min())
    
	return rgb.astype(float)


def split_S2_images(s2_paths):
    '''
        It splits a list of Sentinel-2 path and returs two new lists: rgb images and cloud masks.
        The path must contains 'RGB' or 'CM'.
    '''
    
    cloud_mask = []
    rgb = []
    
    for p in s2_paths:
        if "RGB" in p:
            rgb.append(p)
        elif "CM" in p:
            cloud_mask.append(p)
    
    return rgb, cloud_mask

def get_s1_image(image_path):
    '''
        It returns an grayscale image (VV Sentinel-1) using a path.
        Image path must be the full path of an grayscale (VV) image (tif format)
    '''
    
    # rasterio function to read bands of a tif file
    dataset = rasterio.open(image_path)
    vv = dataset.read(1)
    dataset.close()
    
    # Normalization
    vv = (vv - vv.min())/(vv.max() - vv.min())
    
    return vv.astype(float)

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

def patch_sort(e):
    
    ''' 
        This function is used to sort the paths by the patch order. 
    '''
    
    s = 0
    if 'patch_0.tif' in e:
        s = 0
    elif 'patch_1.tif' in e:
        s = 1
    elif 'patch_2.tif' in e:
        s = 2
    elif 'patch_3.tif' in e:
        s = 3
    elif 'patch_4.tif' in e:
        s = 4
    elif 'patch_5.tif' in e:
        s = 5
    elif 'patch_6.tif' in e:
        s = 6
    elif 'patch_7.tif' in e:
        s = 7
    elif 'patch_8.tif' in e:
        s = 8
    elif 'patch_9.tif' in e:
        s = 9
    elif 'patch_10.tif' in e:
        s = 10
    elif 'patch_11.tif' in e:
        s = 11
    elif 'patch_12.tif' in e:
        s = 12
    elif 'patch_13.tif' in e:
        s = 13
    elif 'patch_14.tif' in e:
        s = 14
    elif 'patch_15.tif' in e:
        s = 15
    
    return s

def get_time_series(images):
    images.sort(key=patch_sort)
    series = []
    counter = 0

    pb = ProgressBar('Creating time series....', int(len(images)/4))

    for i in range(int(len(images)/4)):

        se = []

        for j in range(4):
            se.append(images[counter])
            se.sort(key=date_sort)
            counter = counter + 1

        for j in range(4):
            series.append(se[j])

        pb.update()
            
    pb.close()
    return series

def image_generator(s2_paths, s1_paths, shape = (256,256), batch_size = 16, info = False):
    
    '''
        Image generator keras like. It provides also data augmentation.
    '''
    
    batch_s2  = np.zeros((batch_size*4,shape[0], shape[1], 3))
    batch_s1 = np.zeros((batch_size*4,shape[0], shape[1], 1))
    path_s2 = []
    path_s1 = []
    
    while True:   
        
        counter = 0      
        for i in range(0, batch_size): 
            
            batch_index = randint(0, high=int(len(s2_paths)/4))*4

            
            for j in range(4):
                
                if info:
                    path_s2.append(s2_paths[batch_index+j])
                    path_s1.append(s1_paths[batch_index+j])
                
                s2 = get_s2_image(s2_paths[batch_index+j])
                s1 = get_s1_image(s1_paths[batch_index+j])[..., np.newaxis]

                # Some images may be smaller than 256x256 pixels, 
                # so the following code forces copying

                batch_s2[counter,:s2.shape[0],:s1.shape[1],...] = s2
                batch_s1[counter,:s1.shape[0],:s1.shape[1],...] = s1
                
                counter += 1
        if info:
            yield batch_s2, batch_s1, path_s2, path_s1
        else:
            yield batch_s2, batch_s1