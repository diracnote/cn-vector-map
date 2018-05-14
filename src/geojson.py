#!/usr/bin/python
# -*- coding: utf-8 -*-

'''\
dump geoson version for administrative divisions of china from tianditu.com
'''

import json
import os
import requests

import polyline

def dump(path, gbcode = '000000'):
    json.encoder.FLOAT_REPR = lambda o: format(o, '.5f')

    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(os.path.join(path, 'geojson')):
        os.mkdir(os.path.join(path, 'geojson'))

    gbcodes = {'gbcode' : '000000', 'name' : '中国', 'children' : {}}
    for gbcode, geojson in _dump(gbcode, gbcodes, set()):
        if geojson:
            with open(os.path.join(path, 'geojson', gbcode + '.json'), 'w', encoding='utf-8') as fd:
                json.dump(geojson, fd, ensure_ascii=False, indent = '\t')

    with open(os.path.join(path, 'gbcodes.json'), 'w', encoding='utf-8') as fd:
        json.dump(gbcodes, fd, ensure_ascii=False, indent = '\t')

def _dump(gbcode, gbcodes, visited):
    geojson = _geojson(gbcode)
    visited.add(gbcode)
    yield gbcode, geojson

    if 'features' in geojson:
        for feature in geojson['features']:
            if 'properties' in feature and 'GB' in feature['properties']:
                gbcode = feature['properties']['GB']
                name = feature['properties']['CNAME']
                if gbcode not in visited:
                    gbcodes['children'][gbcode] = {'gbcode' : gbcode, 'name' : name, 'children' : {}}
                    yield from _dump(gbcode, gbcodes['children'][gbcode], visited)

def _geocode(gbcode):
    gbcode = int(gbcode.split('.', 1)[0])
    if gbcode < 156000000:
        gbcode += 156000000
    return str(gbcode)

def _gbcode(geocode):
    geocode = int(geocode.split('.', 1)[0])
    if geocode > 156000000:
        geocode -= 156000000
    return str(geocode)

def _geojson(gbcode):
    response = requests.get('http://zhfw.tianditu.com/zhfw/border', {'type':'s', 'gbcode':_geocode(gbcode)})

    geojson = {}
    try:
        geojson = json.loads(response.json()['geodata'])
    except:
        pass

    if 'features' in geojson:
        for feature in geojson['features']:
            if 'geometry' in feature and 'coordinates' in feature['geometry']:
                coordinates = feature['geometry']['coordinates']
                for ipolyline in range(0, len(coordinates)):
                    try:
                        for ilinear in range(0, len(coordinates[ipolyline])):
                            coordinates[ipolyline][ilinear] = polyline.decode(coordinates[ipolyline][ilinear])
                            coordinates[ipolyline][ilinear].reverse()
                    except:
                        coordinates[ipolyline] = polyline.decode(coordinates[ipolyline])
                        coordinates[ipolyline].reverse()

    return geojson

if __name__ == '__main__':
    dump('geojson')