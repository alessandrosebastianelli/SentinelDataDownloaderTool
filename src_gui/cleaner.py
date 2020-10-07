from glob import glob
from os.path import basename
import numpy as np
import os
from imageio import imread
import rasterio

def find(directory, windows):
    for region in glob(directory):
        r = os.path.join(region, '*')

        for period in glob(r):
            p = os.path.join(period, '*')
            for scene in glob(p):
                if windows:
                    base_name = scene #+ '\\' + basename(scene)
                else:
                    base_name = scene #+ '/' + basename(scene)

                yield base_name

def get_locations(directory, windows):
    locations = []
    for region in glob(directory):
        if windows:
            splitted = region.split('\\')
        else:
            splitted = region.split('/')

        locations.append(splitted[len(splitted)-1])

    return locations

def split_by_locations(files_generator, locations):
    gen = list(files_generator)
    l = len(gen)

    for i in range(len(locations)):
        batch = []

        for j in range(l):
            f = gen[j]
            if locations[i] in f:
                batch.append(f)
        yield batch

def split_by_date(files, date):
    for d in date:
        batch = []
        for f in files:
            if d in f:
                batch.append(f)
        yield batch

def percentage_wrong_values_s1(s1_image, treshold = 170):
    data = s1_image.flatten()
    wrong_values_amount = 0
    for i in range(len(data)):
        if data[i] > treshold:
            wrong_values_amount = wrong_values_amount + 1

    wrong_values_percentage = (wrong_values_amount/len(data))*100
    return wrong_values_percentage

def percentage_wrong_values_s2(s2_image, black_treshold=1, white_treshold=125):
    r = s2_image[:,:,0].flatten()
    g = s2_image[:,:,1].flatten()
    b = s2_image[:,:,2].flatten()

    wrong_values_amount = 0
    white_values_amount = 0

    l = s2_image.shape[0]*s2_image.shape[1]

    for i in range(l):
        if r[i] <= black_treshold and g[i] <= black_treshold and b[i] <= black_treshold:
            wrong_values_amount = wrong_values_amount + 1
        if r[i] >= white_treshold and g[i] >= white_treshold and b[i] >= white_treshold:
            white_values_amount = white_values_amount + 1

    wrong_values_percentage = (wrong_values_amount/l)*100
    white_values_percentage = (white_values_amount/l)*100

    return wrong_values_percentage, white_values_percentage

def read_image(path, satellite):
    if satellite == 'sen1':
        dataset = rasterio.open(path)
        image = dataset.read(1)
        dataset.close()

        image = np.clip(image, -30, 15)
        image = (image-image.mean())/(image.std())
        image = (image-image.min())/(image.max()-image.min())
        image = np.clip(image, 0, 1)
        image = (255.0/image.max() * (image-image.min()))
    elif satellite == 'sen2':
        dataset = rasterio.open(path)
        r = dataset.read(1)
        g = dataset.read(2)
        b = dataset.read(3)
        dataset.close()
        image = np.zeros((r.shape[0], r.shape[1], 3))
        image[:,:,0] = r
        image[:,:,1] = g
        image[:,:,2] = b

        image = (image/10000.)*2.5
        image = np.clip(image, 0, 1)
        image = (255.0/image.max() * (image-image.min()))

    return image

def clean_s1(progressbar, s1_path, date_names, windows):
    file_generator = find(s1_path,  windows)
    locations = get_locations(s1_path, windows)
    locations_genenerator = iter(split_by_locations(file_generator, locations))

    progressbar['maximum'] = len(locations)

    for i in range(0,len(locations)):
        scene = next(locations_genenerator)
        print('     > Scene %d of %d: %s' % (i+1, len(locations), locations[i]))
        date_generator = iter(split_by_date(scene, date_names))
        for j in range(len(list(split_by_date(scene, date_names)))):
            date = next(date_generator)
            print('       - Date: %s' % (date_names[j]))
            wrong_score, prev_wrong_score = 0, 100
            best_image = 'None'
            # Images for each date
            for k in range(len(date)):

                path = date[k]
                image = read_image(path, 'sen1')

                wrong_score = percentage_wrong_values_s1(image)
                print('         * B: ', wrong_score, ' Prev B: ', prev_wrong_score)

                if wrong_score <= prev_wrong_score:
                    best_image = path
                    prev_wrong_score = wrong_score


                print('         * Best image: ' + best_image)

            for k in range(len(date)):
                if not(date[k] == best_image):
                    os.remove(date[k])
                    print('         * Removing Sentinel-1 image %d of %d ' % (k+1, len(date)))
                else:
                    print('         * Best Sentinel-1 image %d of %d ' % (k+1, len(date)))
        progressbar['value'] = i
        progressbar.update()
    
    progressbar.stop()

def clean_s2(progressbar, s2_path, date_names, windows):
    file_generator = find(s2_path,  windows)
    locations = get_locations(s2_path, windows)

    locations_genenerator = iter(split_by_locations(file_generator, locations))

    progressbar['maximum'] = len(locations)

    for i in range(0,len(locations)):
        scene = next(locations_genenerator)
        date_generator = iter(split_by_date(scene, date_names))
        print('     > Scene %d of %d: %s' % (i+1, len(locations), locations[i]))
        for j in range(len(list(split_by_date(scene, date_names)))):
            date = next(date_generator)
            print('       - Date: %s' % (date_names[j]))
            prev_wrong_score, prev_white_score = 100,100
            white_score, wrong_score = 0,0
            best_image = 'None'
            # Images for each date
            # rgb_start = 0
            for k in range(0, len(date)):
                path = date[k]

                if ('RGB' in path):
                    image = read_image(path, 'sen2')
                    wrong_score, white_score = percentage_wrong_values_s2(image)

                    print('         * W: ', white_score, ' Prev W: ', prev_white_score, ' B: ', wrong_score, ' Prev B: ', prev_wrong_score)

                    if white_score <= prev_white_score:
                        best_image = path
                        prev_white_score = white_score


                    print('         * Best image: ' + best_image)

            # Save the best image and remove the other images
            for k in range(0, len(date)):

                if not(date[k] == best_image):
                    if not ('image_CM_' in date[k]):
                        os.remove(date[k])
                        print('         * Removing Sentinel-2 RGB image %d of %d ' % (k+1, len(date)))
                    elif not('RGB' in date[k]):
                        date_split = date[k].split('_')
                        best_image_split = best_image.split('_')

                        if not(date_split[len(date_split)-1] == best_image_split[len(best_image_split)-1]):
                            os.remove(date[k])
                            print('         * Removing Sentinel-2 CL image %d of %d ' % (k+1, len(date)))

                else:
                    print('         * Best Sentinel-2 image %d of %d ' % (k+1, len(date)))
        progressbar['value'] = i
        progressbar.update()
    
    progressbar.stop()

def clean(s2_path, s1_path, date_names, windows):
    print('   # Sentinel-2 data cleaning')
    clean_s2(s2_path, date_names, windows)
    print('   # Sentinel-1 data cleaning')
    clean_s1(s1_path, date_names, windows)
    print('   # Data cleaned')