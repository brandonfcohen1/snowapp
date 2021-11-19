from datetime import datetime
import requests
import os
import shutil
import xml.etree.ElementTree as ET
import json
import time

SLEEP = 0
DOWNLOAD_KMZ = False
DOWNLOAD_PNG = False

# Download latest overlay KMZ
datestring = datetime.now().strftime("%Y%m%d")

if DOWNLOAD_KMZ:
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
id = 0
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

                # Download imagery URL
                if DOWNLOAD_PNG:
                    imagename = str(id) + '-' + imagery_url.split("_")[-2] + '.png'
                    print(imagename)
                    png = requests.get(imagery_url)
                    with open('latest_overlay/png/' + imagename, 'wb') as f:
                        f.write(png.content)

                tiles.append({'imagery_url': imagery_url,
                            'lat_lon_box': lat_lon_box})

                time.sleep(SLEEP)

            elif grandchild.tag.split("}")[1] == "ScreenOverlay":
                if grandchild[0].text == "legend":
                    legend_url = grandchild[2][0].text
                    if DOWNLOAD_PNG:
                        png = requests.get(legend_url)
                        with open('latest_overlay/png/legends/' + str(id) + '_legend.png', 'wb') as f:
                            f.write(png.content)


        layers.append({'id': id, 'name': layername, 'tiles': tiles, 'legend_url': legend_url})

        id += 1

with open('latest_overlay/nsm_latest.json', 'w') as outfile:
    json.dump(layers, outfile)
