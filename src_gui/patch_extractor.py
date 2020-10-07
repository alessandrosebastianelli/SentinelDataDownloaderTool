#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This script extracts smaller images from the dataset images
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import cleaner
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import os
import rasterio

def extract(progressbar, s2_path, s1_path, preview_path, date_names, image_size, patch_size, windows):
    s2_file_generator = cleaner.find(s2_path,  windows)
    s2_locations = cleaner.get_locations(s2_path, windows)
    s2_locations_genenerator = iter(cleaner.split_by_locations(s2_file_generator, s2_locations))    

    s1_file_generator = cleaner.find(s1_path,  windows)
    s1_locations = cleaner.get_locations(s1_path, windows)
    s1_locations_genenerator = iter(cleaner.split_by_locations(s1_file_generator, s1_locations))    

    image = np.ones((image_size, image_size))
    patch = np.ones((patch_size, patch_size))

    patch_x = 0
    patch_y = 0
    patch_num = 0
    counter = 0

    rgb_path = ' '
    cm_path = ' '

    save_flag = False

    progressbar['maximum'] = len(s2_locations)
    # Iterate on scene
    for i in range(len(s2_locations)):
        fig, axes = plt.subplots(nrows = 24, ncols=(image_size//patch_size)+1, figsize = (100,100))
        # Get S1 and S2 scene
        s2_scene = next(s2_locations_genenerator)
        s1_scene = next(s1_locations_genenerator)
        print('> S2 - Scene: %s' % (s2_locations[i]))
        print('> S1 - Scene: %s' % (s1_locations[i]))
        print('> Scene %d of %d' % (i, len(s2_locations)))
        
        if s2_locations[i] == s1_locations[i]:
            print('> Same')
            date_generator = iter(cleaner.split_by_date(s2_scene, date_names))

            for j in range(len(list(cleaner.split_by_date(s2_scene, date_names)))):
                date = next(date_generator)
                image = np.zeros((patch_size, patch_size, 3))

                try:
                    if 'RGB' in date[0]:
                        rgb_path = date[0]
                    else:
                        cm_path = date[0]

                    if 'RGB' in date[1]:  
                        rgb_path = date[1]
                    else:
                        cm_path = date[1]
                    
                    dataset = rasterio.open(rgb_path)
                    r = dataset.read(1)
                    g = dataset.read(2)
                    b = dataset.read(3)
                    dataset.close()

                    dataset = rasterio.open(cm_path)
                    cm = dataset.read(1)
                    dataset.close()

                    save_flag = True

                except Exception:
                    image = np.zeros((patch_size, patch_size, 3))
                    print(' No S2 data', str(j+1))
                    save_flag = False
                    pass

                counter = 0
                    
                for w in range(0, r.shape[0]//patch_size):
                    for h in range(0, r.shape[1]//patch_size):

                        patch_r = r[patch_y:patch_y+patch_size, patch_x:patch_x+patch_size]
                        patch_g = g[patch_y:patch_y+patch_size, patch_x:patch_x+patch_size]
                        patch_b = b[patch_y:patch_y+patch_size, patch_x:patch_x+patch_size]
                        patch_cm = cm[patch_y:patch_y+patch_size, patch_x:patch_x+patch_size]

                        if(save_flag == True):
                            path = rgb_path.replace('dataset','dataset_patch')
                            path = path.replace(s2_locations[i],'zone_'+ str(patch_num))
                            if windows:
                                path = path.replace(date_names[j]+'\\','')
                            else:
                                path = path.replace(date_names[j]+'/','')
                            name = '_'+date_names[j]+'_patch_' + str(counter)
                            path = path.replace('.tif',name)

                            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
                            os.rmdir(path)
                            
                            new_dataset = rasterio.open(path+'.tif','w',driver='GTiff',height=patch_r.shape[0],width=patch_r.shape[1],count=3,dtype=r.dtype)
                            new_dataset.write(patch_r, 1)
                            new_dataset.write(patch_g, 2)
                            new_dataset.write(patch_b, 3)
                            new_dataset.close()

                            path = cm_path.replace('dataset','dataset_patch')
                            path = path.replace(s2_locations[i],'zone_'+ str(patch_num))
                            if windows:
                                path = path.replace(date_names[j]+'\\','')
                            else:
                                path = path.replace(date_names[j]+'/','')
                            name = '_'+date_names[j]+'_patch_' + str(counter)
                            path = path.replace('.tif',name)
                

                            new_dataset = rasterio.open(path+'.tif','w',driver='GTiff',height=patch_cm.shape[0],width=patch_cm.shape[1],count=1,dtype=cm.dtype)
                            new_dataset.write(patch_cm, 1)
                            new_dataset.close()
                        

                            image = np.zeros((patch_r.shape[0], patch_r.shape[1], 3))

                            image[:,:,0] = (patch_r/10000.0)*2.5
                            image[:,:,0] = (image[:,:,0]-image[:,:,0].min())/(image[:,:,0].max()-image[:,:,0].min())

                            image[:,:,1] = (patch_g/10000.0)*2.5
                            image[:,:,1] = (image[:,:,1]-image[:,:,1].min())/(image[:,:,1].max()-image[:,:,1].min())

                            image[:,:,2] = (patch_b/10000.0)*2.5
                            image[:,:,2] = (image[:,:,2]-image[:,:,2].min())/(image[:,:,2].max()-image[:,:,2].min())
                            
                            image = np.clip(image, 0, 1)
                        print(2*j, counter)
                        axes[(2*j),counter].imshow(image)
                        axes[(2*j),counter].set_ylabel(date_names[j], fontsize=18)
                        axes[(2*j),counter].set_title('patch_' + str(counter),  fontsize=18)

                        counter = counter+1
                        patch_x = w*patch_size
                        patch_y = h*patch_size
                
            patch_x = 0
            patch_y = 0
            counter = 0

            rgb_path = ' '
            cm_path = ' '

            date_generator = iter(cleaner.split_by_date(s1_scene, date_names))
            image = np.zeros((patch_size, patch_size))
            vv = np.zeros((patch_size, patch_size))

            save_flag = False
            
            for j in range(len(list(cleaner.split_by_date(s1_scene, date_names)))):
                date = next(date_generator)
                try:
                    dataset = rasterio.open(date[0])
                    
                    vv = dataset.read(1)
                    dataset.close()

                    save_flag = True
                    
                except Exception:
                    image = np.zeros((patch_size, patch_size))
                    vv = np.zeros((patch_size, patch_size))
                    print(' No data S1', str(j+1))
                    save_flag = False
                    pass
            
                counter = 0

                for w in range(0, vv.shape[0]//patch_size):
                    for h in range(0, vv.shape[1]//patch_size):
                                        
                        if save_flag == True:
                            patch_vv = vv[patch_y:patch_y+patch_size, patch_x:patch_x+patch_size]

                            path = date[0].replace('dataset','dataset_patch')
                            path = path.replace(s2_locations[i],'zone_'+ str(patch_num))
                            if windows:
                                path = path.replace(date_names[j]+'\\','')
                            else:
                                path = path.replace(date_names[j]+'/','')
                            
                            name = '_'+date_names[j]+'_patch_' + str(counter)
                            path = path.replace('.tif',name)

                            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
                            
                            new_dataset = rasterio.open(path+'.tif','w',driver='GTiff',height=patch_vv.shape[0],width=patch_vv.shape[1],count=1,dtype=vv.dtype)
                            new_dataset.write(patch_vv, 1)
                            new_dataset.close()

                            os.rmdir(path)

                            image = np.zeros((patch_vv.shape[0], patch_vv.shape[1]))
                            image = np.clip(patch_vv, -30, 15)
                            #image = (image-image.mean())/(image.std())
                            image = (image-image.min())/(image.max()-image.min())
                            image = np.clip(image, 0, 1)

                        axes[(2*j)+1,counter].imshow(image, cmap = 'gray')
                        axes[(2*j)+1,counter].set_ylabel(date_names[j], fontsize=18)
                        axes[(2*j)+1,counter].set_title('patch_' + str(counter),  fontsize=18)
        
                        counter = counter+1
                        patch_x = w*patch_size
                        patch_y = h*patch_size

                        image = np.zeros((patch_size, patch_size))
                
                save_flag = False
        else:
            print('> Not Same')
                    
        fig.tight_layout()
        fig.savefig(preview_path+'zone_'+str(patch_num)+'.png')
        plt.close(fig)

        patch_num = patch_num + 1
        progressbar['value'] = i
        progressbar.update()
    progressbar.stop()