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
        if elem.tag == "{http://www.w3.org/2000/svg}text":
            style = dict(x.strip().split(":") for x in elem.attrib["style"].split(";"))
            x1 = float(elem.attrib["x"])
            y1 = float(elem.attrib["y"])
            position1 = list(transform(x1, y1))

            if "hackX2" in style and "hackY2" in style:
                x2, y2 = float(style["hackX2"]), float(style["hackY2"])

            else:
                fontSize = float(style["font-size"].replace("px", ""))
                a, b, c, d, e, f = map(float, elem.attrib.get("transform", "matrix(1,0,0,1,0,0)").replace("matrix(", "").replace(")", "").split(","))
                x2 = x1
                y2 = y1 - fontSize
                x2, y2 = (a*x2 + c*y2 + e), (b*x2 + d*y2 + f)

            position2 = list(transform(x2, y2))

            content = [elem.text.strip() if elem.text is not None else "",
                       elem.tail.strip() if elem.tail is not None else ""]
            for e in elem.getchildren():
                if e.tag == "{http://www.w3.org/2000/svg}tspan":
                    content.append(e.text.strip() if e.text is not None else "")
                    content.append(e.tail.strip() if e.tail is not None else "")

            drawable = {"type": "text", "textBaseline": "alphabetic", "d": "".join(content), "ax": position1[0], "ay": position1[1], "upx": position2[0], "upy": position2[1], "fillStyle": style["fill"], "textAlign": style["text-align"]}

            drawables.append(drawable)
            
        elif elem.tag == "{http://www.w3.org/2000/svg}path":
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
    makeTestPage = True

    if makeTestPage:
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
        if makeTestPage:
            print "    drawables.push(",

        if doubleJSON:
            print json.dumps(json.dumps(drawable)),
        else:
            print json.dumps(drawable),

        if makeTestPage:
            print ");"
        else:
            print

    if makeTestPage:
        print """hyperbolicMapService = new HyperbolicMapStatic({"drawables": drawables});
    hyperbolicViewport = new HyperbolicViewport(hyperbolicMapService, "hyperbolicViewport", 640, 640, {"allowZoom": true, "initialZoom": 5.0, "minZoom": 0.95, "maxZoom": 10.0, "initialOffsetX": 0.001, "initialOffsetY": 0.0001, "initialRotation": 3.141592653589793});
}

</script>
<body onload="init();">
<div id="hyperbolicViewport" style="margin: 20px;"></div>
</body>
</html>
"""
