# -*- coding: utf-8 -*-
"""Images Caputring

"""

import requests
from bing import TileSystem
import sqlite_util as db
import PIL.Image as Image


# Local Database address
DB_PATH = 'db/map.db'
# Set the initial zoom level
tileZoom = input("please enter a tilezoom level: ")
tileZoom = int(tileZoom)
multi = input("Please enter the magnification: ")
multi = int(multi)
# tileZoom = 17
lat = input("please enter a latitude: ")
lat = float(lat)
# lat = 47.6205099
lon = input("please enter a longtitude: ")
lon = float(lon)
# lon = -122.3514661

t = TileSystem()

def get_quadKey(lat, lon, tileZoom):
    # Calculate QuadKey
    px, py = t.LatLongToPixelXY(lat, lon, tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    print('The converted tx ty is {} {}'.format(tx,ty))
    quadKey = t.TileXYToQuadKey(tx, ty, tileZoom)
    print("The converted QuadKey is {}".format(quadKey))
    tx, ty = t.QuadKeyToTileXY(quadKey)
    return str(quadKey)


def download_bing_tile(qkStr):
    url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r' + qkStr + '.png?g=604'
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    print('DOWNLOAD BING SUCCESS')
    pic_name = 'map/bing/'+ qkStr + '.png'
    # Save Images for Bing Maps
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
    return response.content

def download_google_tile(xtile, ytile, tileZoom, qkStr):
    url = 'http://mt0.google.com/vt/lyrs=m@174000000&src=app&x={}&s=&y={}&z={}'.format(xtile,ytile,tileZoom)
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    print('DOWNLOAD GOOGLE SUCCESS')
    pic_name = 'map/google/'+ qkStr + '.png'
    # Save Images for Google Maps
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)

def download_osm_tile(xtile, ytile, tileZoom, qkStr):
    url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom,xtile,ytile)
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    print('DOWNLOAD OSM SUCCESS')
    pic_name = 'map/osm/'+ qkStr + '.png'
    # Save Images for Openstreet Maps
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)

def multi_pic(qkStr, multi, source):
    start = qkStr + '0' * multi
    end = qkStr + '3' * multi
    start_tx, start_ty = t.QuadKeyToTileXY(start)
    end_tx, end_ty = t.QuadKeyToTileXY(end)
    loc = 0
    for ty in range(start_ty, end_ty + 1):
        for tx in range(start_tx, end_tx + 1):
            if source == 'google':
                url = 'http://mt0.google.com/vt/lyrs=m@174000000&src=app&x={}&s=&y={}&z={}'.format(tx,ty,tileZoom + multi)
            elif source == 'bing':
                new_qkStr = t.TileXYToQuadKey(tx, ty, tileZoom + multi)
                url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r{}.png?g=604'.format(new_qkStr)
            elif source == 'osm':
                url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom + multi,tx,ty)
            else:
                return "error"
            response = requests.get(url, stream=True)
            assert response.status_code == 200, "connect error"
            print('DOWNLOAD {} SUCCESS'.format(loc))
            pic_name = 'map/{}/combine/single/{}.png'.format(source, loc)
            # Save Images
            with open(pic_name, 'wb') as out_file:
                out_file.write(response.content)
            loc += 1
    # Merge
    IMAGE_SIZE = 256  #  Image size is 256*256
    IMAGE_ROW = 2 ** multi  # The row of image
    IMAGE_COLUMN = 2 ** multi # The column of image
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE)) # Create a merged image
    i = 0
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open('map/{}/combine/single/{}.png'.format(source,i))
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
            i += 1
    to_image.save('map/{}/combine/{}_{}_{} {}.png'.format(source, lat, lon, tileZoom, multi)) # Save image
    print('Merged successfully')

qkStr = get_quadKey(lat, lon, tileZoom)

# Download Bing's Data
# Check if the Quadkeys are in the database
is_exists = db.is_exists(DB_PATH,qkStr)
if not is_exists: # If not exists
    # Download data
    print("Data does not exist, downloading")
    data = download_bing_tile(qkStr)
    # Insert data
    db.insert(DB_PATH, qkStr, data)
else:
    print("Data Exists in DB")
    # Extract data from databse
    db.save_images(DB_PATH, qkStr)

# Download Google's data
px, py = t.LatLongToPixelXY(lat, lon, tileZoom)
tx, ty = t.PixelXYToTileXY(px, py)
download_google_tile(tx, ty, tileZoom, qkStr)
# Download OSM's data
download_osm_tile(tx,ty,tileZoom, qkStr)


#Zoom In

multi_pic(qkStr, multi, 'Bing')
multi_pic(qkStr, multi, 'Google')
multi_pic(qkStr, multi, 'OSM')
