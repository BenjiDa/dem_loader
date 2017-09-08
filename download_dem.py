
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
    '''function to build file paths to access DEM tiles
    prefix: returned from write_prefix_function, a list of tile names (e.g. 'n39w120')
    kind: file format for download only options are '.zip' or '.jpg'
    resolution: 13 stands for 1/3 arcsecond which is ~10 m. If this is changed will throw 
    error, this is a place we could expand upon to download DEMs with different resolution.
    '''
    # Create a dictionay of all the possible filename formats.
    file_path_names = []
    if kind == '.zip':
        for file in prefix:
            f = {'short_name': file + '.zip',
                 'long_name': 'USGS_NED_13_' + file + '_IMG.zip' }
            file_path_names.append(f)
    else: 
        for file in prefix:
            f = {'short_name': 'img' + str(file) + '_' + str(resolution) + '_thumb.jpg',
                 'short_name_alternate': str(file) + '_' + str(resolution) + '_thumb.jpg',
                 'long_name': 'USGS_NED_13_' + str(file) + '_IMG_thumb.jpg' }
            file_path_names.append(f)

    return file_path_names


def getFile(file_path_names):
    ''' Function used by retrieve_DEMS_ftp that logs into the ftp server
    and downloads the DEM tiles.
    file_path_names: list of extended file path names in dictionary format.
    '''
    ftp = ftplib.FTP('rockyftp.cr.usgs.gov') # Root of USGS ftp NED server
    ftp.login()
    #print(ftp.getwelcome()) # Print welcome statement
    ftp.cwd('/vdelivery/Datasets/Staged/NED/13/IMG/')
    #ftp.retrlines('LIST') # List files

    ftp.sendcmd("TYPE I")    # Switch to Binary mode
    size_matters = ftp.size(file_path_names)/1000000
    print('\n Your file ' + str(file_path_names) + ' is THIS big: ' + str(size_matters) + ' MegaBytes \n')
    ftp.sendcmd("TYPE A") # Switch back to ASCII mode

    what_to_do = input('Do you want to download it? [y/n]: ' )

    if what_to_do == 'y':
        print('Okay, this may take a while...')
        file = open(file_path_names, 'wb')
        ftp.retrbinary('RETR %s' % file_path_names, file.write, 1024)
        file.close()
    elif what_to_do == 'n':
        print('Well that\'s boring')
    else: print('I didn\'nt get that try again by typing y for yes and n for no')

    
    ftp.quit()

def retrieve_DEMS_ftp(file_path_names):
    '''Function that retrieves the DEM tiles from the USGS ftp server.
    file_path_names: dictionay of all possible file path names.
    '''
    print('Searching all files with these names...\n')

    for path in file_path_names:
        for k, v in path.items():
            try:
                getFile(v)

            except ftplib.all_errors:
                print('\n%s does not exist' % v)
                continue
