
import urllib.request  # works with python3
from bs4 import BeautifulSoup
import os
import math
import wget
from wget import bar_thermometer
import lxml

# User will input lat long which will be rounded to the top left corner of the DEM.
# A DEM will be downloaded that contains the lat,long inputs specified by
# the user.





def write_file_names(latlon, kind='.zip', resolution=13):
    '''
    A function to write file names from lat, long positions with 10m resolution. 
    latlon: a list of latitude, longitude tuples
    kind: file format for download only options are '.zip' or '.jpg'
    resolution: 13 stands for 1/3 arcsecond which is ~10 m
    '''
    # Define the URL
    URL = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/%s/IMG/' % str(resolution) 

    # Latitude and longitude are rounded up to position of the top
    # left corner of the DEM
    for x in range(0,len(latlon)):
        (lat, lon) = (math.ceil(latlon[x][0]), abs(math.ceil(latlon[x][1])))
        latlon[x] = (lat,lon)

    # For loop that returns a list of file names corresponding to the input
    # latitude, longitude points.
    filenames = []
    for x in range(0,len(latlon)):
        loc = 'n%sw%s' % (str(latlon[x][0]), str(latlon[x][1]))
        filenames.append(loc)

    return filenames


def build_file_paths(filenames, kind='.zip', resolution=13):
    # Create a dictionay of all the possible filename formats.
    all_filename_possibilities = []
    if kind == '.zip':
        for file in filenames:
            f = {'short_name': file + '.zip',
                 'long_name': 'USGS_NED_13_' + file + '_IMG.zip' }
            all_filename_possibilities.append(f)
    else: 
        for file in filenames:
            f = {'short_name': 'img' + file + '_' + str(resolution) + '_thumb.jpg',
                 'short_name_alternate': file + '_' + str(resolution) + '_thumb.jpg',
                 'long_name': 'USGS_NED_13_' + file + '_IMG_thumb.jpg' }
            all_filename_possibilities.append(f)

    return all_filename_possibilities


def retrieve_DEMS(filenames):
    all_file_paths = build_file_paths(filenames)

    for path in all_file_paths:
        for k, v in path.items():
            try:
                ftp_path = URL + v
                wget.download(ftp_path, bar=bar_thermometer, out=v)

            except urllib.request.URLError:
                print('%s does not exist' % ftp_path)
                continue
