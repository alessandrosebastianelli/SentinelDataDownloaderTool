import cleaner_v_2
from imageio import imread
import matplotlib.pyplot as plt
import numpy as np
import rasterio

windows = True

if windows:
    s2_path = 'C:\\Users\\Phicollaborator\\Desktop\\downloader_tool\\code\\dataset\\sen2\\*'
    s1_path = 'C:\\Users\\Phicollaborator\\Desktop\\downloader_tool\\code\\dataset\\sen1\\*'
    preview_path = 'C:\\Users\\Phicollaborator\\Desktop\\downloader_tool\\code\\preview\\'
else:
    s2_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/dataset/sen2/*'
    s1_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/dataset/sen1/*'
    preview_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/preview/'

date_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

s2_file_generator = cleaner_v_2.find(s2_path,  windows)
s2_locations = cleaner_v_2.get_locations(s2_path, windows)
s2_locations_genenerator = iter(cleaner_v_2.split_by_locations(s2_file_generator, s2_locations))    

s1_file_generator = cleaner_v_2.find(s1_path,  windows)
s1_locations = cleaner_v_2.get_locations(s1_path, windows)
s1_locations_genenerator = iter(cleaner_v_2.split_by_locations(s1_file_generator, s1_locations))   

fig, axes = plt.subplots(nrows = 2, ncols = 12, figsize = (40, 10))

# Iterate on scene
for i in range(len(s2_locations)):
    # Get S1 and S2 scene
    s2_scene = next(s2_locations_genenerator)
    s1_scene = next(s1_locations_genenerator)
    print('> S2 - Scene: %s' % (s2_locations[i]))
    print('> S1 - Scene: %s' % (s1_locations[i]))
    print('> Scene %d of %d' % (i, len(s2_locations)))

    
    if s2_locations[i] == s1_locations[i]:
        print('> Same')
        date_generator = iter(cleaner_v_2.split_by_date(s2_scene, date_names))
        
        for j in range(len(list(cleaner_v_2.split_by_date(s2_scene, date_names)))):
            date = next(date_generator)
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

                image = np.zeros((r.shape[0], r.shape[1], 3))

                image[:,:,0] = (r/10000.0)*2.5
                image[:,:,0] = (image[:,:,0]-image[:,:,0].min())/(image[:,:,0].max()-image[:,:,0].min())

                image[:,:,1] = (g/10000.0)*2.5
                image[:,:,1] = (image[:,:,1]-image[:,:,1].min())/(image[:,:,1].max()-image[:,:,1].min())

                image[:,:,2] = (b/10000.0)*2.5
                image[:,:,2] = (image[:,:,2]-image[:,:,2].min())/(image[:,:,2].max()-image[:,:,2].min())
                
                image = np.clip(image, 0, 1)
            except Exception: 
                pass
            axes[0,j].imshow(image)
            axes[0,j].set_title(date_names[j])
            image = np.ones((1000,1000))
            
            
        date_generator_2 = iter(cleaner_v_2.split_by_date(s1_scene, date_names))
       
        for j in range(len(list(cleaner_v_2.split_by_date(s1_scene, date_names)))):
            date = next(date_generator_2)
        
            try:    
                dataset = rasterio.open(date[0])
                vv = dataset.read(1)
                
                dataset.close()

                image = np.zeros((r.shape[0], r.shape[1]))
                image = vv
                image = np.clip(image, -30, 15)
                #image = (image-image.mean())/(image.std())
                image = (image-image.min())/(image.max()-image.min())
                image = np.clip(image, 0, 1)
            except Exception:
                pass
            axes[1,j].imshow(image, cmap = 'gray')
            axes[1,j].set_title(date_names[j])
            image = np.ones((1000,1000))
    
        

    fig.tight_layout()
    fig.savefig(preview_path+s2_locations[i]+'.png')



    