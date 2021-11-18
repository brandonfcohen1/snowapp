from datetime import datetime
import requests
import os
import shutil
import xml.etree.ElementTree as ET
import json

reload = False

# Download latest overlay KMZ
datestring = datetime.now().strftime("%Y%m%d")

if reload:
    overlay_url = "https://www.nohrsc.noaa.gov/snow_model/GE/" + \
        datestring + "/nohrsc_nsm_" + datestring + "05.kmz"
    overlay_file = requests.get(overlay_url)
    with open('latest_overlay.kmz', 'wb') as f:
        f.write(overlay_file.content)

    # Extract KML from KMZ
    os.rename('latest_overlay.kmz', 'latest_overlay.zip')
    shutil.unpack_archive('latest_overlay.zip', 'latest_overlay')

# Parse KML
filename = 'nohrsc_nsm_' + datestring + '.kml'


tree = ET.parse('latest_overlay/' + filename)
xml_data = tree.getroot()
layers = []
for child in xml_data[0]:
    if child.tag.split("}")[1] == "Folder":
        layername = ""
        tiles = []
        for grandchild in child:

            if grandchild.tag.split("}")[1] == "name":
                layername = grandchild.text
            elif grandchild.tag.split("}")[1] == "GroundOverlay":
                north = float(grandchild[4][0].text)
                south = float(grandchild[4][1].text)
                east = float(grandchild[4][2].text)
                west = float(grandchild[4][3].text)
                lat_lon_box = [[north, east], [south, west]]
                imagery_url = grandchild[5][0].text
                tiles.append({'imagery_url': imagery_url,
                             'lat_lon_box': lat_lon_box})
        layers.append({'name': layername, 'tiles': tiles})
