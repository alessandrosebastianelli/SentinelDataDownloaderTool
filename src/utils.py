def print_separator():
         #print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('')

def print_components_menu(generate, download, convert, clean, windows):
    print_separator()
    print_separator()
    print(' * Active components')
    print('     -> Generator:  ', generate)
    print('     -> Downloader: ', download) 
    print('     -> Converter:  ', convert)
    print('     -> Cleaner:    ', clean)
    print(' ')
    print(' * Windows OS: ', windows)

def print_generator_menu(n_of_points):
    print_separator()
    print_separator()
    print(' * Generator settings')
    print('  -> Number of generated points:  ', n_of_points)
    print(' ')
    print(' * Generator execution')

def print_downloader_menu(downloads_folder_path, download_path, sen2_images_base_path, sen1_images_base_path, start_date, end_date, date_names, n_images, s2_selectors, s1_selectors, n_of_scene, patch_size):
    print_separator()
    print_separator()
    print(' * Downloader settings')
    print('  -> Download folder path:       ', downloads_folder_path)
    print('  -> Download path:              ', download_path)
    print('  -> Sentinel-2 folder path:     ', sen2_images_base_path)
    print('  -> Sentinel-1 folder path:     ', sen1_images_base_path)
    print('  -> Start date:                 ', start_date)
    print('  -> End date:                   ', end_date)
    print('  -> Date names:                 ', date_names)
    print('  -> Number of images per date:  ', n_images)
    print('  -> Sentinel-2 bands:           ', s2_selectors)
    print('  -> Sentinel-1 bands:           ', s1_selectors)
    print('  -> Number of scene:            ', n_of_scene)
    print('  -> Patch size (km):            ', patch_size)
    print(' ')
    print(' * Downloader execution')

def print_converter_menu(s2_path, s1_path, s2_selectors, s1_selectors, patch_size_in_pixel):
    print_separator()
    print_separator()

    print(' * Converter settings')
    print('  -> Sentinel-2 folder path:     ', s2_path)
    print('  -> Sentinel-1 folder path:     ', s1_path)
    print('  -> Sentinel-2 bands:           ', s2_selectors)
    print('  -> Sentinel-1 bands:           ', s1_selectors)
    print('  -> Patch size (pixel):         ', patch_size_in_pixel,patch_size_in_pixel)
    print(' ')
    print(' * Converter execution')

def print_cleaner_menu(s2_path, s1_path):
    print_separator()
    print_separator()

    print(' * Cleaner settings')
    print('  -> Sentinel-2 folder path:     ', s2_path)
    print('  -> Sentinel-1 folder path:     ', s1_path)
    print(' ')
    print(' * Cleaner execution')