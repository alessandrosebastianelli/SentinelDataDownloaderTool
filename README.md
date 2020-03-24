# This is an old version of the manual, updating is required
## Action needed:
## 1. Code cleaning (some scripts must be better written and path management for the various operating systems must be fixed.
## 2. Add patch extractor code
## 3. Add gui code

# Dataset creation tool
###### By Alessandro Sebastianelli and Maria Pia Del Rosso
## Introduction

This software has been created to give an easiest way to create datasets of satellites data. 

## Components
The software is composed of 4 main parts:

- **Generator**: it generates points, with longitude and latitude, distributed over the Earth surface
- **Downloader**: it downloads from Google Earth Engine Sentinel-1 and Sentinel-2 images with a specified size and specified bands. It uses the coordinates preaviously generated
- **Converter**: it converts the raw data in png files
- **Cleaner**: it removes corrupted data and cloudy images

###### For more information please contact: alessandro.sebastianelli1995@gmail.com or mariapia.delrosso@gmail.com

# User manual

To use the software run ***main.py***.

### Required packages
The code has been written in Python 3.6. You can easly install the following packages by running:

~~~
pip install <name of package>
~~~

- numpy
- matplotlib
- global-land-mask
- pillow
- earthengine-api
- scipy
- geetools
- pandas
- imageio
- scikit-image
- rasterio

## Main settings
First of all you have to specify the type of operative system you use (Windows and MacOS are supported). If you use **Windows** set:

~~~python
windows = True
~~~

If you use **MacOS** set:

~~~python
windows = False
~~~

You can activate or deactivate the components. For example with these settings:

~~~python
generate = True
download = True
convert = True
clean = True
~~~	

all the components are activated. In this way you can split the workflow. **Keep attention!!! The order of the workflow (generator, downloader, converter and cleaner) must not be changed.**
 
## Generator
You can define the number of points to be generated. The default number is:

~~~python
n_of_points = 5000
~~~

After the generation the points are saved in the ***point.csv*** file located into the code folder. If you deactivate the generator, the points are loaded from that file.

~~~python
points_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/points.csv'
~~~

**Keep attention!!! You should change the existing path using the whole path of your file. Keep attention on the type of operative system you use.** 

The file is organized as follow:

|Point|Longitude|Latitude|
|:-:|:-:|:-:|
|1|71.00281|-178.6984|   
|2|49.01390|132.89771|   
|3|62.33937|37.118731|
|...|...|...| 


## Downloader

First of all you have to create some folders (into the "code" folder):

- Download folder: **download**
- Data folder: **data**
	- Sentinel-1 folder (inside "data"): **sen1**
	- Sentinel-2 folder (inside "data"): **sen2**
- Dataset folder: **dataset**
	- Sentinel-1 folder (inside "data"): **sen1**
	- Sentinel-2 folder (inside "data"): **sen2**

At this point you should have this structure:

- code
	- download
	- data
		- sen1
		- sen2
	- dataset
		- sen1
		- sen2

After that you have to change the path settings in the code:

~~~python
downloads_folder_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/download/*'
download_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/download'
sen2_images_base_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/data/sen2/'
sen1_images_base_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/data/sen1/'
~~~  

**Keep attention!!! You should change the existing paths using the whole paths of the folders previously created. Keep attention on the type of operative system you use.** For example if you use Windows you should set:

~~~python
downloads_folder_path = r'C:\\Users\\alessandrosebastianelli\\Desktop\\downloader_tool\\code\\download\\*'
...
~~~

After that you can specify the start date and the end date vectors. The default settings are:

~~~python
start_date = ['2018-01-01','2018-02-01','2018-03-01','2018-04-01','2018-05-01','2018-06-01','2018-07-01','2018-08-01','2018-09-01','2018-10-01','2018-11-01','2018-12-01']
end_date =   ['2018-01-28','2018-02-28','2018-03-28','2018-04-28','2018-05-28','2018-06-28','2018-07-28','2018-08-28','2018-09-28','2018-10-28','2018-11-28','2018-12-28']
~~~

you should set also the date name. The default setting is:

~~~python
date_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
~~~

and the number of image for each time interval. The default setting is:

~~~python
n_images = 3
~~~

With these settings the software will try to download a 1 year time series, with a monthly interval. For each month 3 Sentinel-1 and 3 Sentinel-2 images will be downloaded. 

After that you should specify the Sentinel-2 and Sentinel-1 bands that have to be downloaded. By default the software will download for each image:

- Sentinel-2: B4, B3, B2 (RGB bands) and the QA60 band that contains the cloud mask
- Sentinel-1: band with VV polarization

~~~python
s2_selectors = ["B2", "B3", "B4", "QA60"]
s1_selectors = ["VV"]
~~~


After that you should set the number of scenes to download and the size of each scene in kilometers. By default these values are:

~~~python
n_of_scene = 3
patch_size = 10 #km
~~~

## Converter

You can set the bands that will be used for the conversion. Using the default selectors:

~~~python
s2_selectors = ["B4", "B3", "B2"]
s1_selectors = ["VV"]
~~~

the software will create an RGB image for the Sentinel-2 data and a gray-scale image for the Sentinel-1 data.

If you are using Sentinel-1 and Sentinel-2 data you should not change these parameters:

~~~python
resolution = 10
patch_size_meter = patch_size*1000
patch_size_in_pixel = int(patch_size_meter/resolution)
~~~

You have to change the path setting into the code:

~~~python
s2_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/data/sen2/*'
s1_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/data/sen1/*'
~~~  

**Keep attention!!! You should change the existing paths using the whole paths of the data folders. Keep attention on the type of operative system you use.**

## Cleaner

You have to change only the paths setting into the code:

~~~python
s2_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/dataset/sen2/*'
s1_path = '/Users/alessandrosebastianelli/Desktop/downloader_tool/code/dataset/sen1/*'
~~~
**Keep attention!!! You should change the existing paths using the whole paths of the dataset folders. Keep attention on the type of operative system you use.**

###### Please report us any issue.








































