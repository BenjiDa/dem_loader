
import urllib.request  # works with python3
from bs4 import BeautifulSoup
import os
import math
import lxml
import ftplib

# User will input lat long which will be rounded to the top left corner of the DEM.
# A DEM will be downloaded that contains the lat,long inputs specified by
# the user.





def write_prefix_names(latlon):
    '''
    A function to write file names from lat, long positions with 10m resolution. 
    latlon: a list of latitude, longitude tuples
    kind: file format for download only options are '.zip' or '.jpg'
    resolution: 13 stands for 1/3 arcsecond which is ~10 m
    '''

    # Latitude and longitude are rounded up to position of the top
    # left corner of the DEM
    for x in range(0,len(latlon)):
        (lat, lon) = (math.ceil(latlon[x][0]), math.ceil(abs(latlon[x][1])))
        latlon[x] = (lat,lon)

    # For loop that returns a list of file names corresponding to the input
    # latitude, longitude points.
    prefix = []
    for x in range(0,len(latlon)):
        loc = 'n%sw%s' % (str(latlon[x][0]), str(latlon[x][1]))
        prefix.append(loc)

    return prefix


def build_file_paths(prefix, kind='.zip', resolution=13):
    # Create a dictionay of all the possible filename formats.
    filenames = []
    if kind == '.zip':
        for file in prefix:
            f = {'short_name': file + '.zip',
                 'long_name': 'USGS_NED_13_' + file + '_IMG.zip' }
            filenames.append(f)
    else: 
        for file in prefix:
            f = {'short_name': 'img' + str(file) + '_' + str(resolution) + '_thumb.jpg',
                 'short_name_alternate': str(file) + '_' + str(resolution) + '_thumb.jpg',
                 'long_name': 'USGS_NED_13_' + str(file) + '_IMG_thumb.jpg' }
            filenames.append(f)

    return filenames


def retrieve_DEMS(filenames):
    all_file_paths = build_file_paths(filenames)

    for path in all_file_paths:
        for k, v in path.items():
            try:
                ftp_path = URL + v
                wget.download(ftp_path, out=v)

            except urllib.request.URLError:
                print('%s does not exist' % ftp_path)
                continue

def getFile(filepath):
    ftp = ftplib.FTP('rockyftp.cr.usgs.gov')
    ftp.login()
    #print(ftp.getwelcome())
    ftp.cwd('/vdelivery/Datasets/Staged/NED/13/IMG/')
    #ftp.retrlines('LIST')

    ftp.sendcmd("TYPE I")    # Switch to Binary mode
    size_matters = ftp.size(filepath)/1000000
    print('\n Your file ' + str(filepath) + ' is THIS big: ' + str(size_matters) + ' MegaBytes \n')
    ftp.sendcmd("TYPE A")

    what_to_do = input('Do you want to download it? [y/n]: ' )

    if what_to_do == 'y':
        print('Okay, this may take a while...')
        file = open(filepath, 'wb')
        ftp.retrbinary('RETR %s' % filepath, file.write, 1024)
        file.close()
    elif what_to_do == 'n':
        print('Well that\'s boring')
    else: print('I didn\'nt get that try again by typing y for yes and n for no')

    
    ftp.quit()

def retrieve_DEMS_ftp(all_file_paths):
    #all_file_paths = build_file_paths(prefix)
    URL = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/13/IMG/' #% str(resolution) 
    print('Searching all files with these names...\n')

    for path in all_file_paths:
        for k, v in path.items():
            ftp_path = URL + v
            try:
                getFile(v)

            #except urllib.request.URLError:
            except ftplib.all_errors:
                print('%s does not exist' % ftp_path)
                continue
