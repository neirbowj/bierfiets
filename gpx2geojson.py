#!/usr/bin/env python3.3

"""
Parse the subset of GPX 1.1 that www.fietsnet.be emits and convert it to
conformant GeoJSON.

Usage:

    gpx2geojson.py gpxfile.gpx > gsojsonfile.json

"""

import xml.etree.ElementTree as ET
import geojson
import sys

ns = '{http://www.topografix.com/GPX/1/1}'


def handle_metadata(node):
    """
    Create a Feature with null geometry to contain the metadata properties
    """
    author = node.find(ns + 'author')
    name = author.find(ns + 'name')
    link = author.find(ns + 'link')
    props = { 'author':
        {
            'name': name.text,
            'link': link.get('href'),
        }
    }

    return geojson.Feature(properties=props, id='metadata')


def handle_wpt(node):
    """
    Convert a waypoint to a Feature
    """
    lat, lon = float(node.get('lat')), float(node.get('lon'))
    pt = geojson.Point(coordinates=(lon, lat))

    name = node.find(ns + 'name')
    sym = node.find(ns + 'sym')
    typ = node.find(ns + 'type')
    props = {
        'name': name.text,
        'sym':  sym.text,
        'type': typ.text,
    }
    wpt = geojson.Feature(geometry=pt, properties=props)
    return wpt


def handle_trk(node):
    """
    Model a Track as a MultiLineString, where each Track Segment is
    one LineString.
    """
    name = node.find(ns + 'name')
    typ = node.find(ns + 'type')
    props = {
        'name': name.text,
        'type': typ.text,
    }

    segs = []
    for seg in node.findall(ns + 'trkseg'):
        segs.append(handle_trkseg(seg))
    mls = geojson.MultiLineString(coordinates=segs)

    trk = geojson.Feature(geometry=mls, properties=props)
    return trk


def handle_trkseg(node):
    """
    Convert Track Points to positions
    """
    pts = []
    for trkpt in node.findall(ns + 'trkpt'):
        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        pts.append((lon, lat))
    return pts


dispatch = {
    ns + 'metadata': handle_metadata,
    ns + 'wpt':      handle_wpt,
    ns + 'trk':      handle_trk,
    ns + 'trkseg':   handle_trkseg,
}

def main(args):
    tree = ET.parse(args[1])
    gpx = tree.getroot()
    if gpx.tag != ns + 'gpx':
        print("ERROR: Need a GPX object not '{}'".format(gpx.tag))
        sys.exit(1)

    feature_list = []

    for child in gpx:
        try:
            handler = dispatch[child.tag]
        except IndexError:
            print("ERROR: Don't have a handler for a {}".format(child.tag))
            sys.exit(1)

        feature_list.append(handler(child))

    gpxjson = geojson.FeatureCollection(feature_list)
    print(geojson.dumps(gpxjson, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    import sys
    main(sys.argv)
