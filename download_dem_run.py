from download_dem import *


latlon = [(29.99,-123.65), (31.121, -121.89),(34.567, -118.992),(34.567, -120.0001)]

prefix = write_prefix_names(latlon)
filenames = build_file_paths(prefix, kind='.zip')

retrieve_DEMS_ftp(filenames)