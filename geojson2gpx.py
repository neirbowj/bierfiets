#!/usr/bin/env python3.3

"""
Parse a GeoJSON file and emit its data as a GPX 1.1 XML object
"""

import geojson
from lxml import etree
from lxml.builder import ElementMaker

import sys

def tagsfromprops(props, E):
    """
    Use ElementMaker ``E`` to turn a dict ``props`` into a list of
    elements of the form "<key>value</key>".
    """
    tags = []
    for key, val in props.items():
        tags.append(E(key, val))
    return tags


class GeoJSONTypeNotImplementedError(NotImplementedError):
    def __init__(self, type_name):
        msg = 'GeoJSON type: {}'.format(type_name)
        NotImplementedError.__init__(self, msg)

with open(sys.argv[1], 'r') as f:
    geojson_data = geojson.load(f)

E = ElementMaker(
        nsmap={
            None: 'http://www.topografix.com/GPX/1/1',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsd': 'http://www.w3.org/2001/XMLSchema',
        }
)

if geojson_data.type != 'FeatureCollection':
    raise GeoJSONTypeNotImplementedError(geojson_data.type)

points = [] # Point
routes = [] # LineString or member of MultiLineString
tracks = [] # MultiPoint
for feature in geojson_data.features:
    if feature.type != 'Feature':
        raise GeoJSONTypeNotImplementedError(feature.type)

    props = feature.properties
    geom = feature.geometry

    if geom.type == 'Point':
        lon = geom.coordinates[0]
        lat = geom.coordinates[1]
        tags = tagsfromprops(props, E)
        points.append(
            E.rtept(
                *tags,
                lat=str(lat), lon=str(lon)
            )
        )
        continue

    if geom.type == 'LineString':
        trkpts = []
        for position in geom.coordinates:
            lon = position[0]
            lat = position[1]
            trkpts.append(
                E.trkpt(
                    lat=str(lat), lon=str(lon)
                )
            )
        tags = tagsfromprops(props, E)
        tracks.append(
            E.trk(
                E.trkseg(
                    *trkpts
                ),
                *tags
            )
        )
        continue

    if geom.type == 'MultiLineString':
        # TODO: Handle me
        continue

    if geom.type == 'MultiPoint':
        # TODO: Handle me
        continue

    raise GeoJSONTypeNotImplementedError(geom.type)


if len(points) > 0:
    routes.append(
        E.rte(
            E.name(sys.argv[1]), # XXX: Better way to provide a name?
            *points
        )
    )

gpx_members = tracks + routes

gpx_attrib = {
    'version': '1.1',
    'creator': 'https://github.com/neirbowj/bierfiets'
}

gpx = E.gpx(
    E.metadata(
        E.author(
            E.name('Melissa Muth'),
            E.link(E.text('mrmuth/bierfiets'), href='https://github.com/mrmuth/bierfiets')
        )
    ),
    *gpx_members,
    **gpx_attrib
)

bytesout = etree.tostring(
        gpx,
        pretty_print=True,
        xml_declaration=True,
        standalone=False,
        encoding='UTF-8'
)

print(bytesout.decode('UTF-8'))
