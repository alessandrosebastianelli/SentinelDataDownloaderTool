from glob import glob
from os.path import basename
import numpy as np
from PIL import Image
import os
import pathlib
import rasterio

def find(directory, satellite, s2_selectors, s1_selectors, windows):

    for region in glob(directory):
        if windows:
            r = region+"\\*"

        else:
            r = region+'/*'

        for period in glob(r):
            if windows:
                p =period+'\\*'

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



def get_save_path(path, windows):
    # Create the new folders tree
    save_path = path.replace('data', 'dataset')
    if windows:
        split = save_path.split('\\')
    else:
        split = save_path.split('/')

    split.pop(len(split)-1)
    split.pop(len(split)-1)
    new_save_path = ''
    for i in range(1,len(split)):
        if windows:
            new_save_path = new_save_path + '\\' + split[i]
        else:
            new_save_path = new_save_path + '/' + split[i]

    if windows:
        new_save_path = 'C:'+new_save_path + '\\'
    else:
        new_save_path = new_save_path + '/'

    return new_save_path


def convert_s2(s2_path, s1_path, image_size, s2_selectors, s1_selectors, s2_conversion_mode, windows):
    gen = iter(find(s2_path, 'sen2', s2_selectors, s1_selectors, windows))
    s2_len = len(list(find(s2_path, 'sen2', s2_selectors, s1_selectors, windows)))//4
    master_counter = 0

    print('Len: ', s2_len)
    for i in range(s2_len):
        try:

            path = next(gen)
            print(path)
            dataset = rasterio.open(path)
            img_r = dataset.read(1)
            dataset.close()

            path = next(gen)
            dataset = rasterio.open(path)
            img_g = dataset.read(1)
            dataset.close()

            path = next(gen)
            dataset = rasterio.open(path)
            img_b = dataset.read(1)
            dataset.close()

            path = next(gen)
            dataset = rasterio.open(path)
            cloud_mask = dataset.read(1)
            dataset.close()
        except Exception:
            pass

        new_save_path = get_save_path(path, windows)
        pathlib.Path(new_save_path).mkdir(parents=True, exist_ok=True)

        new_dataset = rasterio.open(new_save_path+'image_RGB_'+str(master_counter)+'.tif','w',driver='GTiff',height=img_b.shape[0],width=img_b.shape[1],count=3,dtype=img_r.dtype)
        new_dataset.write(img_r, 1)
        new_dataset.write(img_g, 2)
        new_dataset.write(img_b, 3)
        new_dataset.close()

        new_dataset = rasterio.open(new_save_path+'image_CM_'+str(master_counter)+'.tif','w',driver='GTiff',height=cloud_mask.shape[0],width=cloud_mask.shape[1],count=3,dtype=cloud_mask.dtype)
        new_dataset.write(cloud_mask, 1)
        new_dataset.close()


        master_counter = master_counter + 1
        print('     > Sentinel-2 image %d of %d conversion completed' % (i+1, s2_len))



def convert_s1(s2_path, s1_path, image_size, s2_selectors, s1_selectors, s2_conversion_mode, windows):
    gen_2 = iter(find(s1_path, 'sen1', s2_selectors, s1_selectors, windows))
    s1_len = len(list(find(s1_path, 'sen1', s2_selectors, s1_selectors, windows)))
    counter = 0

    for i in range(s1_len):
        try:
            path = next(gen_2)

            print(path)
            dataset = rasterio.open(path)
            img_r = dataset.read(1)
            dataset.close()

            new_save_path = get_save_path(path, windows)
            pathlib.Path(new_save_path).mkdir(parents=True, exist_ok=True)

            new_dataset = rasterio.open(new_save_path+'image_VV_'+str(counter)+'.tif','w',driver='GTiff',height=img_r.shape[0],width=img_r.shape[1],count=1,dtype=img_r.dtype)
            new_dataset.write(img_r, 1)
            new_dataset.close()

            counter = counter + 1
            print('     > Sentinel-1 image %d of %d conversion completed' % (i+1, s1_len))
        except Exception:
            print('     ! Missing data')

def convert(s2_path, s1_path, s2_conversion_mode, image_size, s2_selectors, s1_selectors, windows):
    print('   # Sentinel-2 data conversion')
    convert_s2(s2_path, s1_path, image_size, s2_selectors, s1_selectors, s2_conversion_mode, windows)
    print('   # Sentinel-1 data conversion')
    convert_s1(s2_path, s1_path, image_size, s2_selectors, s1_selectors, s2_conversion_mode, windows)

    print('   # Conversion completed')
