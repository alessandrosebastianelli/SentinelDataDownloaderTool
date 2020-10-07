from glob import glob
from os.path import basename
from imageio import imread
from skimage.transform import resize
import numpy as np
from PIL import Image
import os
import pathlib

def find(directory, satellite, s2_selectors, s1_selectors, windows):
    for region in glob(directory):
        if windows:
            r = region+'\\*'
        else:
            r = region+'/*'

        for period in glob(r):
            if windows:
                p = period+'\\*'
            else:
                p = period+'/*'

            for scene in glob(p):
                if windows: 
                    base_name = scene + '\\' + basename(scene)
                else:
                    base_name = scene + '/' + basename(scene)
                
                    if satellite == 'sen2':
                        bands = s2_selectors
                    elif satellite == 'sen1':
                        bands = s1_selectors
                    
                    for channel in bands:
                        yield base_name+'.'+channel+'.tif'




def load_data(files, satellite, image_size = (1000, 1000)):
    if satellite == 'sen2':
        # B4, B3, B2
        bands = np.zeros((image_size[0], image_size[1], 3))

        for i in range(0,3):
            band = imread(files[i])/10000.
            #band = imread(files[i])/3000.
            resized_band = resize(band, (image_size[0], image_size[1]), anti_aliasing=True, preserve_range=True)
            bands[:,:,i] = np.clip(resized_band[:,:], 0, 1)
        
        return bands
    elif satellite == 'sen1':
        bands = np.zeros((image_size[0], image_size[1], 1))
        band = imread(files)
        band = np.clip(band, -30, 15)
        band = (band-band.mean())/(band.std())
        band = (band-band.min())/(band.max()-band.min())
        band = np.clip(band, 0, 1)
        resized_band = resize(band, (image_size[0], image_size[1]), anti_aliasing=True, preserve_range=True)
        bands[:,:,0] = np.clip(resized_band[:,:], 0, 1)
        return bands

def merge_bands(bands, satellite, image_size = (1000, 1000), mode='norm'):
    if satellite == 'sen2':
        rgb_image = np.zeros((image_size[0], image_size[1], 3))
        if mode == 'norm':
            rgb_image[:,:,0] = (bands[:,:,0] * 2.5)
            rgb_image[:,:,1] = (bands[:,:,1] * 2.5)
            rgb_image[:,:,2] = (bands[:,:,2] * 2.5)
        elif mode == 's&n':
            r = bands[:,:,0] * 2.5
            #r = (r-r.mean())/(r.std())
            r = (r-r.min())/(r.max()-r.min())
            rgb_image[:,:,0] = r

            g = bands[:,:,1] * 2.5
            #g = (g-g.mean())/(g.std())
            g = (g-g.min())/(g.max()-g.min())
            rgb_image[:,:,1] = g

            b = bands[:,:,2] * 2.5
            #b = (b-b.mean())/(b.std())
            b = (b-b.min())/(b.max()-b.min())
            rgb_image[:,:,2] = b
        
        return np.clip(rgb_image, 0, 1)
    elif satellite == 'sen1':
        return bands

def save_image(path, image, satellite):
    if satellite == 'sen2':
        rescaled = (255.0/image.max() * (image-image.min())).astype(np.uint8)
        img = Image.fromarray(rescaled,'RGB')
        img.save(path+'.png')
    elif satellite == 'sen1':
        rescaled = (255.0/image.max() * (image-image.min())).astype(np.uint8)
        img = Image.fromarray(rescaled[:,:,0])
        img.save(path+'.png')
    
def create_image_names(files, windows, s1_selectors, s2_selectors):

    new_name = files.replace('data','dataset')
    new_name = new_name.replace('.tif','')
    
    for i in range(len(s2_selectors)):
        prefix = '.'+s2_selectors[i]
        if prefix in new_name:
            new_name = new_name.replace(prefix,'')
    for i in range(len(s1_selectors)):
        prefix = '.'+s1_selectors[i]
        if prefix in new_name:
            new_name = new_name.replace(prefix,'')

    #splitted = new_name.split('.')
    # It removes .band and .tif
    #splitted.pop(len(splitted)-1)
    #splitted.pop(len(splitted)-1)
    
    #new_name = ''

    #for i in range(len(splitted)):
        #new_name = new_name + splitted[i]

    # It removes the image name to create the path
    if windows:
        splitted_2 = new_name.split('\\')
        splitted_2.pop([len(splitted_2)-1])
        path = ''
        for i in range(len(splitted_2)-1):
            if i!=0:
                path = path+'\\'+ splitted_2[i]
        path = path + '\\'
    else:
        splitted_2 = new_name.split('/')
        splitted_2.pop(len(splitted_2)-1)
        path = ''
        for i in range(len(splitted_2)-1):
            if i!=0:
                path = path+'/'+ splitted_2[i]
        path = path + '/'
  
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    return path+splitted_2[len(splitted_2)-1]


def convert_s2(s2_path, s1_path, image_size, s2_selectors, s1_selectors, s2_conversion_mode, windows):
    file_generator = iter(find(s2_path, 'sen2', s2_selectors, s1_selectors, windows))

    files = []
    s2_len = len(list(find(s2_path, 'sen2', s2_selectors, s1_selectors, windows)))//3

    

    for i in range(s2_len):
        for j in range(3):
            try:
                f = next(file_generator)
                files.append(f)
            except Exception:
                pass
        try:
            bands = load_data(files, 'sen2', image_size=image_size)
            rgb_image = merge_bands(bands, 'sen2', image_size=image_size, mode=s2_conversion_mode)
            path = create_image_names(files[0], windows, s1_selectors, s2_selectors)
            save_image(path, rgb_image, 'sen2')

            print('     > Sentinel-2 image %d of %d conversion completed' % (i+1, s2_len))
        except Exception:
            print(' ')
            print('     ! Error during conversion of file %d of %d' % (i+1, s2_len))
            print(' ')
            pass

        files.clear()
        files = []

def convert_s1(s2_path, s1_path, image_size, s2_selectors, s1_selectors, s2_conversion_mode, windows):
    file_generator = iter(find(s1_path, 'sen1', s2_selectors, s1_selectors, windows))
    files = []
    s1_len = len(list(find(s1_path, 'sen1', s2_selectors, s1_selectors, windows)))

    
    for i in range(s1_len):
        try:
            files = next(file_generator)
            bands = load_data(files, 'sen1', image_size=image_size)
            sar_image = merge_bands(bands, 'sen1', image_size=image_size, mode=s2_conversion_mode)
            path = create_image_names(files, windows, s1_selectors, s2_selectors)
            save_image(path, sar_image, 'sen1')
            
            print('     > Sentinel-1 image %d of %d conversion completed' % (i+1, s1_len))
        except Exception:
            print(' ')
            print('     ! Error during conversion of file %d of %d' % (i+1, s1_len))
            print(' ')
            pass

        files = [] 

def convert(s2_path, s1_path, s2_conversion_mode, image_size, s2_selectors, s1_selectors, windows):
    print('   # Sentinel-2 data conversion')
    convert_s2(s2_path, s1_path, image_size, s2_selectors, s1_selectors, s2_conversion_mode, windows)
    print('   # Sentinel-1 data conversion')
    convert_s1(s2_path, s1_path, image_size, s2_selectors, s1_selectors, s2_conversion_mode, windows)

    print('   # Conversion completed')
