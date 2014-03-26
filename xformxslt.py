#!/usr/bin/env python

"""
Perform an XSL transformation with an arbitrary combination of
XML and XSL.

Usage:
    ./xformxslt.py xmlfile xslfile > output_file
"""

from lxml import etree


def main(args):
    xml = etree.parse(args[1])
    xsl = etree.parse(args[2])
    transform = etree.XSLT(xsl)
    result = transform(xml)
    print(str(result))


if __name__ == '__main__':
    import sys
    main(sys.argv)
