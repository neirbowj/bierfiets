<?xml version="1.0" ?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:gpx="http://www.topografix.com/GPX/1/1"
>
<!--

    This XSL file aims to process the subset of GPX 1.1 that
    fietsnet.be implements.

-->
    <xsl:output
        method="text"
        media-type="text/plain"
        omit-xml-declaration="no"
        indent="yes" />

    <xsl:template match="/">
{
    "type": "FeatureCollection",
    "features": [<xsl:apply-templates select="//gpx:metadata" /><xsl:apply-templates select="//gpx:wpt" /><xsl:apply-templates select="//gpx:trk" />
}
    </xsl:template>

    <xsl:template match="gpx:metadata">
        {
            "type": "Feature",
            "geometry": null,
            "id": "metadata",
            "properties": {<xsl:apply-templates select="gpx:author" />}
        },
    </xsl:template>

    <xsl:template match="gpx:author">
                "author": {
                    "link": "<xsl:value-of select="gpx:link/@href" />",
                    "name": "<xsl:value-of select="gpx:name" />"
                }
    </xsl:template>

    <xsl:template match="gpx:wpt">
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    <xsl:value-of select="@lon" />,
                    <xsl:value-of select="@lat" />
                ]
            },
            "id": null,
            "properties": {
                "type": "<xsl:value-of select="./gpx:type" />",
                "sym": "<xsl:value-of select="./gpx:sym" />",
                "name": "<xsl:value-of select="./gpx:name" />"
            }
        },
    </xsl:template>

    <xsl:template match="gpx:trk">
        {
            "type": "Feature",
            "properties": {
                "name": "<xsl:value-of select="./gpx:name" />",
                "type": "<xsl:value-of select="./gpx:type" />"
            }
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [<xsl:apply-templates select="./gpx:trkseg" />]
        }
    </xsl:template>

    <xsl:template match="gpx:trkseg">
                    [
                        <xsl:apply-templates select="./gpx:trkpt" />
                    ]<xsl:if test="not(position()=last())">,</xsl:if>
    </xsl:template>

    <xsl:template match="gpx:trkpt">
                        [
                            <xsl:value-of select="@lon" />,
                            <xsl:value-of select="@lat" />
                        ]<xsl:if test="not(position()=last())">,</xsl:if>
    </xsl:template>

</xsl:stylesheet>
