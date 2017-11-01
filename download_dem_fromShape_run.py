from download_dem import *

shapefilePath = '/Users/sjohnstone/Documents/Research/Projects/Stillwater/MiscShapes/StillwaterExtent.kml' #Your shape path here
latlon = get_latlonPts_within_shape(shapefilePath)

prefix = write_prefix_names(latlon)
file_path_names = build_file_paths(prefix, kind='.zip')

retrieve_DEMS_ftp(file_path_names)