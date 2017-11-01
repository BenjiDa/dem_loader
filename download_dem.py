
#Import statements for remote file retrival
import os
import math
import lxml
import ftplib

#Import statements fpr shape based queries
import ogr #For opening shapefiles
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


################
# Functions for shape based queries
################

def get_latlonPts_within_shape(shpPath):
    '''
    Given a shape file, finds all the lat long coordinates of the upper left corners of the 1/3 arc second DEMs contained
    within the extent of those shapes

    :param shpPath: a file path to a shapefile
    :return: latlons, a list of lat,lon tuple pairs to feed to 'write_prefix_names'.
    '''


    src = ogr.Open(shpPath) #Load in the OGR shapefile object

    try:

        lyr = src.GetLayer(0) #Get the top layer from the shapefile

    except:

        print('Whoopsy, a problem with retrieving the layer from the shapefile - you sure you got the filepath right?')
        return None

    try:

        extent = lyr.GetExtent() #Get the bounding coordinates of the shapefile (min lon, max lon, min lat, max lat_

    except:

        print('Whoopsy, a problem with retrieving the extent of the layer - you sure this is a valid shapefile?')
        return None

    #Get the bounds
    longBounds = extent[0:2]
    latBounds = extent[2:]

    #Quick and dirty check to make sure that this shape was in geographic coordinates
    if any([(abs(lb)>180) for lb in longBounds]) or any([(abs(lb)>90) for lb in latBounds]):
        print('Whoopsy, that file is either out of bounds or in the wrong coordinate system. Please use a geographic projection.')
        return None

    else:
        return _getGridsInBounds(latBounds,longBounds)

def _getGridsInBounds(latBounds,longBounds,dTheta = 1):
    '''
    Splits the lat long boundaries given into a list of all points within that range at the specified spacing dTheta

    :param latBounds: (min latitude, max latitude)
    :param longBounds: (min longitude, max longitude)
    :return:
    '''

    #Get X-Y points at the specified spacing
    lats = [math.floor(latBounds[0]) + i*dTheta for i in range(int(1 + (math.floor(latBounds[1]) - math.floor(latBounds[0]))/dTheta))]
    longs = [math.floor(longBounds[0]) + i*dTheta for i in range(int(1 + (math.floor(longBounds[1]) - math.floor(longBounds[0]))/dTheta))]

    #Iterate through points, creating a list of tuples as we go
    latLongs = []
    for lat in lats:
        for long in longs:
            latLongs.append((lat,long))

    return latLongs

