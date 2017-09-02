
#User will input lat long and will have to round it to the correct DEM, so whatever position is inside the dem it will download that dem
latitude = 40
longitude = 124

resoultion = 13 #for 1/3 arc second data
kind = IMG #for .img files
location = n40w124

path = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/%s/%s/' % (resolution, kind)