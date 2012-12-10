#!/usr/bin/env python

# To prepare an SVG image for transformation:

# Set Inkscape preferences -> SVG output:
#     Allow relative coordinates: false
#     Force repeat commands: true
#     Numeric precision: 14
#     Minimum exponent: -32
# and save as "Plain SVG".

# Make sure to include a <rect/> with id="UnitRectangle" (name it in Inkscape's XML Editor).
# This will be mapped to a rectangle from (0, 0) to (1, 1).
# The UnitRectangle will not be drawn.

# Make sure that none of the elements have a transform attribute.  (Maybe we can loosen that restriction in the future.)
# Make sure that none of the elements are in any groups (ungrouping is a good way to remove transform attributes).
# Make sure that all desired graphics (except text) have been turned into paths

import sys
import math
import json
import re
try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

from hypertrans import *

def drawablesFromSVG(documentRoot, coordinateSystem="hyperShadow"):
    originx = 0.0
    originy = 0.0
    unitx = 1.0
    unity = 1.0
    for elem in documentRoot.getchildren():
        if elem.tag == "{http://www.w3.org/2000/svg}rect" and elem.attrib["id"] == "UnitRectangle":
            originx = float(elem.attrib["x"])
            originy = float(elem.attrib["y"]) + float(elem.attrib["height"])
            unitx = float(elem.attrib["width"])
            unity = float(elem.attrib["height"])

    if coordinateSystem == "hyperShadow":
        def transform(x, y):
            return (x - originx)/unitx, (originy - y)/unity

    # note: no recursive searching for paths: they must not be in groups (<g/> elements)
    drawables = []
    for elem in documentRoot.getchildren():
        if elem.tag == "{http://www.w3.org/2000/svg}path":
            style = dict(x.strip().split(":") for x in elem.attrib["style"].split(";"))
            # skip this path if it is not visible
            if style.get("visibility", "visible") == "visible" and style.get("display", "inline") != "none":
                fillStyle = style.get("fill", "black")
                strokeStyle = style.get("stroke", "none")
                lineWidth = float(style.get("stroke-width", 1.0))
                lineCap = style.get("stroke-linecap", "butt")
                lineJoin = style.get("stroke-linejoin", "miter")
                miterLimit = float(style.get("stroke-miterlimit", 4.0))

                commands = []
                lines = []
                close = False

                d = re.split("[\s,]+", elem.attrib["d"].strip())
                i = 0
                while i < len(d):
                    if d[i].upper() == "M":
                        x, y = float(d[i+1]), float(d[i+2])
                        commands.append(list(transform(x, y)))
                        lines.append(False)
                        i += 2

                    elif d[i].upper() == "L":
                        x, y = float(d[i+1]), float(d[i+2])
                        commands.append(list(transform(x, y)))
                        lines.append(True)
                        i += 2

                    elif d[i].upper() == "Z":
                        close = True

                    i += 1

                # An "L" in a drawable's point indicates that the *next* segment should be drawn with a line,
                # so an "L" in the last point means that the polygon should be closed ("Z" in SVG).
                # In SVG, the first point can only be an "M", so the first "False" tells us nothing.
                lines = lines[1:] + [close]
                for c, l in zip(commands, lines):
                    if l: c.append("L")

                drawable = {"type": "polygon", "fillStyle": fillStyle, "strokeStyle": strokeStyle, "lineWidth": lineWidth, "lineCap": lineCap, "lineJoin": lineJoin, "miterLimit": miterLimit, "d": commands}
                # drop attributes if they are drawable defaults
                if drawable["fillStyle"] == "none":
                    del drawable["fillStyle"]
                if drawable["strokeStyle"] in ("#000000", "black"):
                    del drawable["strokeStyle"]
                if abs(drawable["lineWidth"] - 1.0) < 1e-5:
                    del drawable["lineWidth"]
                if drawable["lineCap"] == "butt":
                    del drawable["lineCap"]
                if drawable["lineJoin"] == "miter":
                    del drawable["lineJoin"]
                if abs(drawable["miterLimit"] - 4.0) < 1e-5:
                    del drawable["miterLimit"]

                drawables.append(drawable)

    return drawables

if __name__ == "__main__":
    if len(sys.argv) == 2:
        documentRoot = ElementTree.parse(sys.argv[1]).getroot()
    else:
        documentRoot = ElementTree.fromstring(sys.stdin.read())
    
    doubleJSON = False

    print """
<!DOCTYPE html>
<html>
<meta charset="utf-8">
<script type="text/javascript" src="HyperbolicViewport.js"></script>
<script type="text/javascript">

var hyperbolicMapService;
var hyperbolicViewport;

function init() {
    var drawables = [];"""

    for drawable in drawablesFromSVG(documentRoot, coordinateSystem="hyperShadow"):
        print "    drawables.push(",

        if doubleJSON:
            print json.dumps(json.dumps(drawable)),
        else:
            print json.dumps(drawable),

        print ");"

    print """hyperbolicMapService = new HyperbolicMapStatic({"drawables": drawables});
    hyperbolicViewport = new HyperbolicViewport(hyperbolicMapService, "hyperbolicViewport", 640, 640, {"allowZoom": false, "initialZoom": 0.95, "minZoom": 0.95, "maxZoom": 0.95, "rotationMode": "compass"});
}

</script>
<body onload="init();">
<div id="hyperbolicViewport" style="margin: 20px;"></div>
</body>
</html>
"""
