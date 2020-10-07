#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This script extracts smaller images from the 1000x1000 dataset images
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import cleaner
from imageio import imread
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pathlib
import os

def save_image(path, image, satellite):
    if satellite == 'sen2':
        #rescaled = (255.0/image.max() * (image-image.min())).astype(np.uint8)
        img = Image.fromarray(image,'RGB')
        img.save(path+'.png')
    elif satellite == 'sen1':
        #rescaled = (255.0/image.max() * (image-image.min())).astype(np.uint8)
        img = Image.fromarray(image)
        img.save(path+'.png')
       

windows = False
s2_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/dataset/sen2/*'
s1_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/dataset/sen1/*'
preview_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/dataset_patch/preview/'

date_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, axes = plt.subplots(nrows = 2, ncols = 12, figsize = (40, 10))

s2_file_generator = cleaner.find(s2_path,  windows)
s2_locations = cleaner.get_loactions(s2_path, windows)
s2_locations_genenerator = iter(cleaner.split_by_locations(s2_file_generator, s2_locations))    

s1_file_generator = cleaner.find(s1_path,  windows)
s1_locations = cleaner.get_loactions(s1_path, windows)
s1_locations_genenerator = iter(cleaner.split_by_locations(s1_file_generator, s1_locations))    

l = 0

if len(s2_locations) < len(s1_locations):
    l = len(s2_locations)
else:
    l = len(s1_locations)

image = np.ones((1000,1000))

patch_x = 0
patch_y = 0
patch_size = 256
patch_num = 333
counter = 0

patch = np.ones((patch_size, patch_size))

# Iterate on scene
for i in range(0,l):
    # Get S1 and S2 scene
    s2_scene = next(s2_locations_genenerator)
    s1_scene = next(s1_locations_genenerator)
    print('> S2 - Scene: %s' % (s2_locations[i]))
    print('> S1 - Scene: %s' % (s1_locations[i]))
    print('> Scene %d of %d' % (i, l))
    
    
    if s2_locations[i] == s1_locations[i]:
        counter = 0
        print('> Same')
        for h in range(0, (1000//patch_size)):
            for w in range(0, (1000//patch_size)):
                
                print('     * Patch %d of %d' % (patch_num, 9*l))

                date_generator = iter(cleaner.split_by_date(s2_scene, date_names))
                for j in range(len(list(cleaner.split_by_date(s2_scene, date_names)))):
                    date = next(date_generator)
                    try:
                        image = imread(date[0])
                        patch = image[patch_y:patch_y+patch_size, patch_x:patch_x+patch_size, :]
                        path = date[0].replace('dataset','dataset_patch')
                        path = path.replace(s2_locations[i],'patch_'+ str(patch_num))
                        name = '_patch' + str(counter)
                        path = path.replace('.png',name)

                        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
                        save_image(path, patch, 'sen2')
                        os.rmdir(path)

                        #print(path)
                    except Exception:
                        print("Something may have gone wrong")
                        pass
                    axes[0,j].imshow(patch)
                    axes[0,j].set_title(date_names[j], fontsize=20)
                    image = np.ones((1000,1000))
                    patch = np.ones((patch_size, patch_size))
                
                date_generator = iter(cleaner.split_by_date(s1_scene, date_names))
                for j in range(len(list(cleaner.split_by_date(s1_scene, date_names)))):
                    date = next(date_generator)
                    try:
                        image = imread(date[0])
                        patch = image[patch_y:patch_y+patch_size, patch_x:patch_x+patch_size]
                        path = date[0].replace('dataset','dataset_patch')
                        path = path.replace(s1_locations[i],'patch_'+ str(patch_num))
                        name = '_patch' + str(counter)
                        path = path.replace('.png',name)

                        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
                        save_image(path, patch, 'sen1')
                        os.rmdir(path)

                        #print(path)
                    except Exception:
                        print("Something may have gone wrong")
                        pass
                    axes[1,j].imshow(patch, cmap = 'gray')
                    axes[1,j].set_title(date_names[j], fontsize=20)
                    image = np.ones((1000,1000))
                    patch = np.ones((patch_size, patch_size))

                counter = counter+1

                fig.tight_layout()
                fig.savefig(preview_path+"patch_"+str(patch_num)+'.png')

                patch_x = w*patch_size
                patch_y = h*patch_size
                patch_num = patch_num + 1
    else:
        print('> Not Same')
                
            



    