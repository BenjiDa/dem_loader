
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

def dem_loader(latitude, longitude, resolution=13, kind='IMG'):
    '''
    A function that downloads DEM data from the National Elevation Dataset. Currently it only works for 1/3 arcsecond data (~10m),
    but this can be expanded upon.

    User inputs:
    latitude = latitude position of area of interest
    longitude = longitude position of area of interest
    resoultion = the data resolution (default 1/3 arcsecond resolution (~10 meter))
    kind = the format (default is .IMG), this can be expanded upon in the future
    '''

    #Latitude and longitude are rounded up to position of the top
    #left corner of the DEM
    longitude = abs(longitude)  # Get absolute value of longitude
    longitude = math.ceil(longitude) # Round up
    latitude = math.ceil(latitude) # Round up
    

    location = 'n%sw%s' % (str(latitude), str(longitude)) # Set the string that points to the DEM
    short_name = location + '.zip'
    long_name = 'USGS_NED_%s_%s_%s.zip' % (str(resolution), location, kind) # Set to full string
    new_folder_name = 'dem_%s' % location # Set name of new folder to put data into

    URL = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/%s/%s/' % (str(resolution), kind) # Full URL to DEM
    filenames = ['n39w122', 'USGS_NED_13_n39w122_IMG'] 


    source_directory = os.getcwd() # Get current directory
    data_directory = os.path.join(source_directory, new_folder_name) # Set path name to new directory

    # Check and see if the local directory currently exists or not, if not create that directory
    if os.path.exists(data_directory):
        os.chdir(data_directory)
    else:
        os.makedirs(new_folder_name)
        os.chdir(data_directory)

    # Download data (This will take time)

def write_file_names(latitude, longitude, kind='.zip', resolution=13):

    #Latitude and longitude are rounded up to position of the top
    #left corner of the DEM
    latitude_all = []
    longitude_all = []
    for lat in latitude:
        latitude = math.ceil(lat) # Round up
        latitude_all.append(latitude)
    for lon in longitude:
        #longitude = abs(lon)  # Get absolute value of longitude
        longitude = math.ceil(abs(lon)) # Round up
        longitude_all.append(longitude)

    location = []
    location = 'n%sw%s' % (str(latitude), str(longitude)) # Set the string that points to the DEM
    return latitude_all, longitude_all

    

def build_file_paths(filenames):
    all_filename_possibilities = []
    for file in filenames: 
        #you can add as many odd filename builders here as you want
        f = {'short_name': file + '.zip', 'long_name':'USGS_NED_13_' + file + '.zip'}
        all_filename_possibilities.append(f)

    return all_filename_possibilities 


def retrieve_DEMS(filenames): 
    all_file_paths = build_file_paths(filenames) 

    for path in all_file_paths: 
        for k,v in path.items(): 
            try:
                ftp_path = URL + v 
                wget.download(ftp_path, bar=bar_thermometer, out=v)#

            except urllib.request.URLError:
                print('%s does not exist' % ftp_path)
                continue


