import cleaner
from imageio import imread
import matplotlib.pyplot as plt
import numpy as np

windows = False
s2_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/dataset/sen2/*'
s1_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/dataset/sen1/*'
preview_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/preview/'

#s1_path='/Users/alessandrosebastianelli/Desktop/dataset_v_2/dataset/sen1/*'
#s2_path='/Users/alessandrosebastianelli/Desktop/dataset_v_2/dataset/sen2/*'
#preview_path = '/Users/alessandrosebastianelli/Desktop/dataset_v_2/dataset/preview/'

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

for i in range(0,l):
    scene = next(s2_locations_genenerator)
    print('> Scene: %s' % (s2_locations[i]))
    date_generator = iter(cleaner.split_by_date(scene, date_names))
    for j in range(len(list(cleaner.split_by_date(scene, date_names)))):
        date = next(date_generator)
        try:
            image = imread(date[0])
        except Exception:
            pass
        axes[0,j].imshow(image)
        axes[0,j].set_title(date_names[j])
        image = np.ones((1000,1000))
        
    scene = next(s1_locations_genenerator)
    date_generator = iter(cleaner.split_by_date(scene, date_names))
    for j in range(len(list(cleaner.split_by_date(scene, date_names)))):
        date = next(date_generator)
        try:
            image = imread(date[0])
        except Exception:
            pass
        axes[1,j].imshow(image, cmap = 'gray')
        axes[1,j].set_title(date_names[j])
        image = np.ones((1000,1000))
        

    fig.tight_layout()
    fig.savefig(preview_path+s2_locations[i]+'.png')



    