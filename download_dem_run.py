from download_dem import *


latlon = [(38.5, -123.5), (40.63, -124.3), (41.29, -124.35)]

prefix = write_prefix_names(latlon)
file_path_names = build_file_paths(prefix, kind='.zip')

retrieve_DEMS_ftp(file_path_names)