import os
import shutil
from kml2geojson import main

#os.rename('nohrsc_nsm_2021111505.kmz', 'nohrsc_nsm_2021111505.zip')
#shutil.unpack_archive('nohrsc_nsm_2021111505.zip')

geojson = main.convert('nohrsc_nsm_20211115.kml')

print(geojson)