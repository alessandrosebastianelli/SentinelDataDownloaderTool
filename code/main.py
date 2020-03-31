import utils
# If you are using windows set to True
# If you are using macos set to False

windows =    False

generate =   False
download =   False
# ~~~~~~ Converter ~~~~~~
convert_s2 = True
convert_s1 = True
# ~~~~~~ Cleaner ~~~~~~
clean_s2 =   False
clean_s1 =   False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

utils.print_components_menu(generate, download, convert_s2 or convert_s1, clean_s1 or clean_s2, windows)
# ------------------------------------------------- GENERATOR -------------------------------------------------
# ----------------------------------------------- USER SETTINGS -----------------------------------------------
n_of_points = 5000
utils.print_generator_menu(n_of_points)

if windows:
    points_path = 'C:\\Users\\Phicollaborator\\Desktop\\SentinelDataDownloaderTool\\code\\points.csv'
else:
    points_path = '/Users/alessandrosebastianelli/Desktop/SentinelDataDownloaderTool/code/points.csv'

# --------------------------------------------- GENERATOR EXECUTION -------------------------------------------
if generate:
    import generator
    points = generator.get_land_coordinates(n_of_points)
    generator.save_points(points, points_path)
else:
    import generator
    points = generator.load_points(points_path)
                                                                                                                                                                        
# ------------------------------------------------- DOWNLOADER ------------------------------------------------
# ----------------------------------------------- USER SETTINGS -----------------------------------------------
if windows:
    download_path = 'C:\\Users\\Phicollaborator\\Desktop\\SentinelDataDownloaderTool\\code\\download'
    downloads_folder_path = download_path+'\\*'
    sen2_images_base_path = 'C:\\Users\\Phicollaborator\\Desktop\\SentinelDataDownloaderTool\\code\\data\\sen2\\'
    sen1_images_base_path = 'C:\\Users\\Phicollaborator\\Desktop\\SentinelDataDownloaderTool\\code\\data\\sen1\\'
else:
    download_path = '/Users/alessandrosebastianelli/Desktop/SentinelDataDownloaderTool/code/download'
    downloads_folder_path = download_path+'/*'
    sen2_images_base_path = '/Users/alessandrosebastianelli/Desktop/SentinelDataDownloaderTool/data/sen2/'
    sen1_images_base_path = '/Users/alessandrosebastianelli/Desktop/SentinelDataDownloaderTool/data/sen1/'

start_date = ['2018-01-01','2018-02-01','2018-03-01','2018-04-01','2018-05-01','2018-06-01','2018-07-01','2018-08-01','2018-09-01','2018-10-01','2018-11-01','2018-12-01']
end_date =   ['2018-01-28','2018-02-28','2018-03-28','2018-04-28','2018-05-28','2018-06-28','2018-07-28','2018-08-28','2018-09-28','2018-10-28','2018-11-28','2018-12-28']
date_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
n_images = 3
s2_selectors = ["B2", "B3", "B4", "QA60"]
s1_selectors = ["VV"]
n_of_scene = 1
patch_size = 10 #km

utils.print_downloader_menu(downloads_folder_path, download_path, sen2_images_base_path, sen1_images_base_path, start_date, end_date, date_names, n_images, s2_selectors, s1_selectors, n_of_scene, patch_size)
# -------------------------------------------- DOWNLOADER EXECUTION -------------------------------------------
if download:
    import downloader
    downloader.download(points, patch_size, start_date, end_date, date_names,s2_selectors,s1_selectors,n_of_scene,n_images,downloads_folder_path,download_path, sen2_images_base_path, sen1_images_base_path, windows)

# ------------------------------------------------- CONVERTER -------------------------------------------------
# ----------------------------------------------- USER SETTINGS -----------------------------------------------
s2_selectors = ["B4", "B3", "B2", "QA60"]
s1_selectors = ["VV"]
resolution = 10
patch_size_meter = patch_size*1000
patch_size_in_pixel = int(patch_size_meter/resolution)

image_size = (patch_size_in_pixel, patch_size_in_pixel) 
if windows:
    s2_path = sen2_images_base_path+'*'
    s1_path = sen1_images_base_path+'*'
else:
    s2_path = sen2_images_base_path+'*'
    s1_path = sen1_images_base_path+'*'

utils.print_converter_menu(s2_path, s1_path, s2_selectors, s1_selectors, patch_size_in_pixel)
# -------------------------------------------- CONVERTER EXECUTION --------------------------------------------

import converter
import converter_v_2
#converter_v_2.convert(s2_path, s1_path, 's&n', image_size, s2_selectors, s1_selectors, windows)
if convert_s2:
    converter_v_2.convert_s2(s2_path, s1_path, image_size, s2_selectors, s1_selectors, 's&n', windows)
if convert_s1:
    converter_v_2.convert_s1(s2_path, s1_path, image_size, s2_selectors, s1_selectors, 's&n', windows)

# -------------------------------------------------- CLEANER --------------------------------------------------
# ----------------------------------------------- USER SETTINGS -----------------------------------------------
if windows:
    s2_path = 'C:\\Users\\Phicollaborator\\Desktop\\SentinelDataDownloaderTool\\code\\dataset\\sen2\\*'
    s1_path = 'C:\\Users\\Phicollaborator\\Desktop\\SentinelDataDownloaderTool\\code\\dataset\\sen1\\*'
else:
    s2_path = '/Users/alessandrosebastianelli/Desktop/SentinelDataDownloaderTool/code/dataset/sen2/*'
    s1_path = '/Users/alessandrosebastianelli/Desktop/SentinelDataDownloaderTool/code/dataset/sen1/*'

utils.print_cleaner_menu(s2_path, s1_path)
# --------------------------------------------- CLEANER EXECUTION ---------------------------------------------

import cleaner
import cleaner_v_2
#cleaner_v_2.clean(s2_path, s1_path, date_names, windows)
if clean_s2:
    cleaner_v_2.clean_s2(s2_path, date_names, windows)
if clean_s1:
    cleaner_v_2.clean_s1(s1_path, date_names, windows)

