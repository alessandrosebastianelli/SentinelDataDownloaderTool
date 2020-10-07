from random import uniform
import numpy as np
from global_land_mask import globe
from pandas import DataFrame
import pandas as pd

# If you are using Sentinel-1 and Sentinel-2 data please use the default values
def new_point(latitude_from=-56, latitude_to=84, longitude_from=-180, longitude_to=180):
    '''
        It generates randomly a geo point
    '''

    latitude = uniform(latitude_from, latitude_to)
    longitude = uniform(longitude_from, longitude_to)

    return latitude, longitude


def get_land_coordinates(number = 500, gui=False):
    '''
        It generates a list of points distributed on the Earth land
    '''
    
    i = 0
    points = np.zeros((3,number))

    while i<number:
        lat, lon = new_point()
        # If the generated point is on land, it will be added to the list 
        # otherwise a new point will be generated
        if globe.is_land(lat, lon):
            points[0, i] = lat
            points[1, i] = lon
            i = i + 1
    
    print('   # Points generated')

    return points

def save_points(points, path = './points.csv'):
    '''
        It saves the generated points into a csv file
    '''
    lat = points[0,:]
    lon = points[1,:]
    state = points[2,:]
    points_to_save = {'Latitude':lat, 'Longitude':lon, 'State':state}
    globe_points = DataFrame(data = points_to_save)
    globe_points.to_csv(path)

    print('   # Points saved')

def load_points(path = './points.csv'):
    '''
        It loads the preaviously generated points from a csv file
    '''
    data_frame = pd.read_csv(path, index_col=0)
    data = data_frame.to_numpy()

    l = len(data)
    points = np.zeros((2,l)) 

    for i in range(0, l):
        points[0,i] = data[i][0]
        points[1,i] = data[i][1]

    print('   # Points loaded')
    
    return points

def get_new_points(n_of_scene, points_path):
    
    df = pd.read_csv(points_path)
    df = df.drop(columns=['Unnamed: 0'])
    data = df.to_numpy()
    data = np.transpose(data)

    points = np.zeros((2, n_of_scene))
    j = 0
    counter = 0
    while j<n_of_scene:
        if data[2][counter] == 1 or data[2][counter] == 2 or data[2][counter] == 3:
            counter = counter + 1
        elif data[2][counter] == 0:
            data[2][counter] = 1
            points[0,j] = data[0,counter]
            points[1,j] = data[1,counter]
            j = j + 1
            
    save_points(data, points_path)
    
    return points