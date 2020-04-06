# Google Earth Engine & Python API

import math
import ee
ee.Initialize()
from geetools import batch

# Distances are measured in kilometers
# Longitudes and latitudes are measured in degrees
# Earth is assumed to be perfectly spherical
EARTH_RADIUS  = 6271.0
DEGREES_TO_RADIANS = math.pi/180.0
RADIANS_TO_DEGREE = 180.0/math.pi


def change_in_latitude(kms):
    '''
        Given a distance north, it returns the change in latitude
    '''

    return (kms/EARTH_RADIUS)*RADIANS_TO_DEGREE

def change_in_longitude(latitude, kms):
    '''
        Given a latitude and a distance west, it returns the change in longitude
    '''

    r = EARTH_RADIUS*math.cos(latitude*DEGREES_TO_RADIANS)
    return (kms/r)*RADIANS_TO_DEGREE

def get_coordinates_square(latitude, longitude, size = 10):
    '''
        Given a latitude and a longitude it returns a square of size=size of coordinates
    '''

    half_size = size/2

    slat = latitude+change_in_latitude(-half_size)
    nlat = latitude+change_in_latitude(half_size)
    wlon = longitude+change_in_longitude(latitude, -half_size)
    elon = longitude+change_in_longitude(latitude, half_size)

    return ['[[{:.4f},{:.4f}],[{:.4f},{:.4f}],[{:.4f},{:.4f}],[{:.4f},{:.4f}]]'.format(wlon,nlat,elon,nlat,wlon,slat,elon,slat), [wlon,slat,elon,nlat]]

def get_region_and_rectangle(longitude_list, latitude_list, size=10):
    '''
        Given a latitude and a longitude list it returns a square of coordinates list
    '''
    regions = []
    rectangles = []

    for i in range(len(longitude_list)):
        coordinates_square = get_coordinates_square(longitude_list[i], latitude_list[i], size=size)
        regions.append(coordinates_square[0])
        rectangles.append(coordinates_square[1])

    return regions, rectangles

def get_s2_data_from_gge(rectangle, start_date, end_date, selectors = ["B2", "B3", "B4", "QA60"]):
    patch = ee.Geometry.Rectangle(rectangle)
    dataset = ee.ImageCollection("COPERNICUS/S2").filterBounds(patch).filterDate(start_date,end_date).sort('system:time_start', True)
    # The final product will contains 4 bands, the RGB bands and the QA60 band
    dataset = dataset.select(selectors)
    data = dataset.toList(dataset.size())

    return data

def download_s2_data(data, region, zone_name, date, download_path, n_imgs=3, selectors = ["B2", "B3", "B4", "QA60"]):
    downloaded_image = 0

    for i in range(1, n_imgs+1):
        try:
            image = ee.Image(data.get(i))
            image.select(selectors)
            name = image.id().getInfo()
            batch.image.toLocal(image, name=name, path=download_path, scale=10, region=region, toFolder=True)
            print('          * Zone %s, period: %s, img: %d of %d' % (zone_name, date, i, n_imgs))
            downloaded_image = downloaded_image + 1
        except Exception:
            print('          ! Missing data for zone %s, period: %s, img: %d of %d' % (zone_name, date, i, n_imgs))
            pass
    print('          => Downloaded %d of %d' % (downloaded_image, n_imgs))

def get_s1_data_from_gge(rectangle, start_date, end_date, selectors = ["VV"]):
    patch = ee.Geometry.Rectangle(rectangle)
    dataset = ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(patch).filterDate(start_date,end_date).sort('system:time_start', True)
    # The final product will contains 4 bands, the RGB bands and the QA60 band
    dataset = dataset.select(selectors)
    #dataset = dataset.filter(ee.Filter.eq('orbitProperties_pass','ASCENDING'))
    data = dataset.toList(dataset.size())

    return data

def download_s1_data(data, region, zone_name, date, download_path, n_imgs=3, selectors = ["VV"]):
    downloaded_image = 0

    for i in range(1, n_imgs+1):
        try:
            image = ee.Image(data.get(i))
            image.select(selectors)
            name = image.id().getInfo()
            batch.image.toLocal(image, name=name, path=download_path, scale=10, region=region, toFolder=True)
            print('          * Zone %s, period: %s, img: %d of %d' % (zone_name, date, i, n_imgs))
            downloaded_image = downloaded_image + 1
        except Exception:
            print('          ! Missing data for zone %s, period: %s, img: %d of %d' % (zone_name, date, i, n_imgs))
            pass
    print('          => Downloaded %d of %d' % (downloaded_image, n_imgs))

