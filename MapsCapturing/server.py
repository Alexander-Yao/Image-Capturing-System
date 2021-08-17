from os import error
from flask import Flask, jsonify, request
import requests
from bing import TileSystem
import sqlite_util as db
import PIL.Image as Image
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app, supports_credentials=True)
t = TileSystem()

HOST = 'uwtset1.tacoma.uw.edu'
USER = 'mapsuser'
PWD = 'mapsuser'
BASE = 'mapsvisions'
location_photos = db.MSSQL(HOST,USER,PWD,BASE)

def get_uuid():
    idd = str(uuid.uuid1())
    return idd.replace('-','')

def download_tile(xtile, ytile, tileZoom, source):
    qkStr = t.TileXYToQuadKey(xtile, ytile, tileZoom)
    if source == 'bing':
        url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r' + qkStr + '.png?g=604'
    elif source == 'google':
        url = 'http://mt0.google.com/vt/lyrs=m@174000000&src=app&x={}&s=&y={}&z={}'.format(xtile,ytile,tileZoom)
    else:
        url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom,xtile,ytile)
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    print('DOWNLOAD {} SUCCESS'.format(source))
    capture_id = get_uuid()
    pic_name = 'map/{}/{}.png'.format(source, capture_id)
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
    return capture_id, pic_name

def multi_pic_whole(lat, lon, tileZoom, multi, source):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    qkStr = t.TileXYToQuadKey(tx, ty, tileZoom)
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
    IMAGE_SIZE = 256  #   Image size is 256*256
    IMAGE_ROW = 2 ** multi  # The row of image
    IMAGE_COLUMN = 2 ** multi # The column of image
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE)) # Create New Images
    i = 0
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open('map/{}/combine/single/{}.png'.format(source,i))
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
            i += 1
    pic_url = 'map/{}/combine/{}.png'.format(source, get_uuid())
    to_image.save(pic_url) # Save Images
    return pic_url

def multi_pic_part(lat, lon, tileZoom, multi, source, part_list):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    qkStr = t.TileXYToQuadKey(tx, ty, tileZoom)
    new_qkr = qkStr + part_list
    new_tx, new_ty = t.QuadKeyToTileXY(new_qkr)
    if source == 'google':
        url = 'http://mt0.google.com/vt/lyrs=m@174000000&src=app&x={}&s=&y={}&z={}'.format(new_tx,new_ty,tileZoom + multi)
    elif source == 'bing':
        url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r{}.png?g=604'.format(new_qkr)
    elif source == 'osm':
        url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom + multi,new_tx,new_ty)
    else:
        return "error"
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    print('DOWNLOAD {} SUCCESS'.format(part_list))
    pic_name = 'map/{}/combine/single/{}.png'.format(source, part_list)
    # Save Images
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
    part_list = list(map(int,part_list))
    return pic_name
 
@app.route('/pic')
def download_pic():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom =int(request.args["tileZoom"])
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    #bing
    _, bing_pic = download_tile(tx, ty, tileZoom, 'bing')
    location_photos.inser_map(lat, lon, 'B', bing_pic)
    #google
    _, google_pic = download_tile(tx, ty, tileZoom, 'google')
    location_photos.inser_map(lat, lon, 'G', google_pic)
    #osm
    _, osm_pic = download_tile(tx, ty, tileZoom, 'osm')
    location_photos.inser_map(lat, lon, 'O', osm_pic)
    result = {'bing': bing_pic, 'google': google_pic, 'osm': osm_pic}
    return jsonify(result)

@app.route('/multi/whole')
def multi_whole():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom = int(request.args["tileZoom"])
    endZoomLevel = int(request.args["endzoomLevel"])
    bing_urls = multi_pic_whole(lat, lon, tileZoom, endZoomLevel, 'bing')
    google_urls = multi_pic_whole(lat, lon, tileZoom, endZoomLevel, 'google')
    osm_urls = multi_pic_whole(lat, lon, tileZoom, endZoomLevel, 'osm')
    result = {'bing':bing_urls,'google':google_urls,'osm':osm_urls}
    return jsonify(result)

@app.route('/multi/part')
def multi_part():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom = int(request.args["tileZoom"])
    endZoomLevel = int(request.args["endzoomLevel"])
    part_list = request.args['partlist']
    bing_urls = multi_pic_part(lat, lon, tileZoom, endZoomLevel, 'bing', part_list)
    google_urls = multi_pic_part(lat, lon, tileZoom, endZoomLevel, 'google', part_list)
    osm_urls = multi_pic_part(lat, lon, tileZoom, endZoomLevel, 'osm', part_list)
    result = {'bing':bing_urls,'google':google_urls,'osm':osm_urls}
    return jsonify(result)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()





