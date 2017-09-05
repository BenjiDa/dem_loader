
import urllib.request  # works with python3
from bs4 import BeautifulSoup
import os
import math
import wget
import lxml


# User will input lat long which will be rounded to the top left corner of the DEM.
# A DEM will be downloaded that contains the lat,long inputs specified by
# the user.

def dem_loader(latitude, logitude, resolution=13, kind='IMG'):
	'''
	A function that downloads DEM data from the National Elevation Dataset. Currently it only works for 1/3 arcsecond data (~10m),
	but this can be expanded upon.

	User inputs:
	latitude = latitude position of area of interest
	longitude = longitude position of area of interest
	resoultion = the data resolution (default 1/3 arcsecond resolution (~10 meter))
	kind = the format (default is .IMG), this can be expanded upon in the future
	'''

    # Latitude and longitude are rounded up to position of the top
    # left corner of the DEM
    longitude = abs(longitude)  # Get absolute value of longitude
    longitude = math.ceil(longitude) # Round up
    latitude = math.ceil(latitude) # Round up


    location = 'n%sw%s' % (str(latitude), str(longitude)) # Set the string that points to the DEM
    name = 'USGS_NED_%s_%s_%s.zip' % (str(resolution), location, kind) # Set to full string
    short_name = 'dem_%s' % location # Set name of new folder to put data into

    URL = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/%s/%s/' % (str(resolution), kind) # Full URL to DEM

    source_directory = os.getcwd() # Get current directory
    data_directory = os.path.join(source_directory, short_name) # Set path name to new directory

    # Check and see if the local directory currently exists or not, if not create that directory
    if os.path.exists(data_directory):
        os.chdir(data_directory)
    else:
        os.makedirs(short_name)
        os.chdir(data_directory)

    # Download data (This will take time)
    url_name = URL+name
    wget.download(url_name)

