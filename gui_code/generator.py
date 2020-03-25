from random import uniform
import numpy as np
from global_land_mask import globe
from pandas import DataFrame
import pandas as pd

from ProgressBar import ProgressBar
import tkinter as tk

# If you are using Sentinel-1 and Sentinel-2 data please use the default values
def new_point(latitude_from=-56, latitude_to=84, longitude_from=-180, longitude_to=180):
    '''
        It generates randomly a geo point
    '''

    latitude = uniform(latitude_from, latitude_to)
    longitude = uniform(longitude_from, longitude_to)

    return latitude, longitude


def get_land_coordinates(number = 500):
    '''
        It generates a list of points distributed on the Earth land
    '''
    pb = ProgressBar('Generating points...', number)
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
            pb.update()
    
    print('   # Points generated')
    pb.close()

    save_points(points)

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

    pb = ProgressBar('Loading points...', l)

    for i in range(0, l):
        points[0,i] = data[i][0]
        points[1,i] = data[i][1]
        pb.update()

    print('   # Points loaded')
    pb.close()

    return points

def get_new_points(n_of_scene, points_path = './points.csv'):
    
    df = pd.read_csv(points_path)
    df = df.drop(columns=['Unnamed: 0'])
    data = df.to_numpy()
    data = np.transpose(data)

    points = np.zeros((2, n_of_scene))
    j = 0
    counter = 0

    pb = ProgressBar('Loading new points...', n_of_scene)

    while j<n_of_scene:
        if counter < len(data[2][:]):
            if data[2][counter] == 1 or data[2][counter] == 2 or data[2][counter] == 3:
                counter = counter + 1
            elif data[2][counter] == 0:
                data[2][counter] = 1
                points[0,j] = data[0,counter]
                points[1,j] = data[1,counter]
                j = j + 1
                pb.update()
        else:
            pb.close()
            tk.messagebox.showinfo("Error", "There are no points that can be loaded! Please generate new ones")
            return 
            
    save_points(data, points_path)
    pb.close()

    return points