#!/usr/bin/env python

import sys
import math
import json
import re
try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

# from hypertrans import *
execfile("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/hypertrans.py")

class Path(object):
    def __init__(self, commands, style):
        self.commands = commands
        self.style = style

    def move(self, Br, Bi, angle, rotateInPlace=False):
        Br2 =  Br*cos(angle) + Bi*sin(angle)
        Bi2 = -Br*sin(angle) + Bi*cos(angle)

        for command in self.commands:
            if isinstance(command, list):
                try:
                    x, y = poincareDisk_to_hyperShadow(*internalToScreen(command[0], command[1], Br2, Bi2, angle))
                    command[0] = x
                    command[1] = y
                except ZeroDivisionError:
                    pass

    def svg(self):
        d = []
        for command in self.commands:
            if isinstance(command, list):
                x, y = command[0:2]
                d.append("%s %.18e,%.18e" % tuple([command[2]] + [x, -y])) # list(self.transformBack(*hyperShadow_to_poincareDisk(x, y)))))
            else:
                d.append("Z")
        d = " ".join(d)

        style = []
        for key, val in self.style.items():
            style.append("%s:%s" % (key, val))

        style = ";".join(style)

        return "<path d=\"%s\" style=\"%s\" />" % (d, style)

def loadSVG(documentRoot, coordinateSystem="hyperShadow"):
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

    def transform(x, y):
        return (x - originx)/unitx, (originy - y)/unity

    def transformBack(x, y):
        return x*unitx + originx, -y*unity + originy

    def doit(elem, paths):
        style = dict(x.strip().split(":") for x in elem.attrib["style"].split(";"))
        # skip this path if it is not visible
        if style.get("visibility", "visible") == "visible" and style.get("display", "inline") != "none":
            d = re.split("[\s,]+", elem.attrib["d"].strip())
            commands = []
            i = 0
            while i < len(d):
                if d[i].upper() in ("M", "L"):
                    x, y = float(d[i+1]), float(d[i+2])
                    if coordinateSystem == "halfPlane":
                        commands.append(list(halfPlane_to_hyperShadow(*transform(x, y))) + [d[i].upper()])
                    elif coordinateSystem == "hyperShadow":
                        commands.append(list(transform(x, y)) + [d[i].upper()])
                    elif coordinateSystem == "poincareDisk":
                        commands.append(list(poincareDisk_to_hyperShadow(*transform(x, y))) + [d[i].upper()])
                    i += 2

                elif d[i].upper() == "Z":
                    commands.append("Z")

                i += 1

            p = Path(commands, style)
            p.transformBack = transformBack
            paths.append(p)

    paths = []
    for elem in documentRoot.getchildren():
        if elem.tag == "{http://www.w3.org/2000/svg}path":
            doit(elem, paths)
        elif elem.tag == "{http://www.w3.org/2000/svg}g":
            for e in elem.getchildren():
                if e.tag == "{http://www.w3.org/2000/svg}path":
                    doit(e, paths)

    return paths

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/general_relativity.svg")
backgroundPaths = loadSVG(document.getroot(), coordinateSystem="halfPlane")

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/jumper.svg")
jumper1 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in jumper1:
    p.transformBack = backgroundPaths[0].transformBack
    p.move(0.0, 1.05, 0.0)

jumper2 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in jumper2:
    p.transformBack = backgroundPaths[0].transformBack
    # p.move(0.0, 1.5, 0.0)
    # p.move(0.0, 0.0, 0.1*math.pi)
    p.move(0.0, 0.0, 0.25*math.pi)

# f = open("/tmp/test.pmml", "w")
f = sys.stdout
f.write("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"2800\" height=\"800\">\n")

for p in backgroundPaths:
    f.write(p.svg())
    f.write("\n")

for p in jumper1:
    f.write(p.svg())
    f.write("\n")

# for p in jumper2:
#     f.write(p.svg())
#     f.write("\n")

f.write("</svg>\n")
f.close()
