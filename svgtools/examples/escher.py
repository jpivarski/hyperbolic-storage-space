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

hideStrokes = ("--hideStrokes" in sys.argv)
onlyStrokes = ("--onlyStrokes" in sys.argv)
hideCircle = ("--hideCircle" in sys.argv)
hyperShadow = ("--hyperShadow" in sys.argv)

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/escher_circle_limit_3_step2.svg")

originx = 0.0
originy = 0.0
originr = 1.0
for elem in document.getroot().getchildren():
    if elem.tag == "{http://www.w3.org/2000/svg}path" and elem.attrib["id"] == "PoincareDisk":
        originx = float(elem.attrib["{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cx"])
        originy = float(elem.attrib["{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cy"])
        originr = float(elem.attrib["{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}rx"])
        circle = elem

def transform(x, y):
    return (x - originx)/originr, (originy - y)/originr
        
def transformBack(x, y):
    return x*originr + originx, -y*originr + originy

class Path(object):
    def __init__(self, commands, style):
        self.commands = commands
        self.style = style

    def transformation(self, Br, Bi, angle, flip=1, opacity=0.5, color={}):
        Br2 =  Br*cos(angle) + Bi*sin(angle)
        Bi2 = -Br*sin(angle) + Bi*cos(angle)

        commands = []
        for command in self.commands:
            if isinstance(command, list):
                try:
                    x, y = poincareDisk_to_hyperShadow(*command[0:2])
                    x, y = internalToScreen(flip*x, y, Br2, Bi2, angle)
                    commands.append([x, y, command[2]])
                except ZeroDivisionError:
                    pass

        style = dict(self.style)
        style["stroke-opacity"] = opacity
        style["fill-opacity"] = opacity
        style["fill"] = color.get(style["fill"], style["fill"])

        return Path(commands, style)

    def svg(self):
        d = []
        for command in self.commands:
            if isinstance(command, list):
                x, y = command[0:2]
                if hyperShadow:
                    d.append("%s %.18e,%.18e" % tuple([command[2]] + list(transformBack(*poincareDisk_to_hyperShadow(x, y)))))
                else:
                    d.append("%s %.18e,%.18e" % tuple([command[2]] + list(transformBack(x, y))))
            else:
                d.append("Z")
        d = " ".join(d)

        style = []
        for key, val in self.style.items():
            style.append("%s:%s" % (key, val))

        style = ";".join(style)

        return "<path d=\"%s\" style=\"%s\" />" % (d, style)

paths = []
for g in document.getroot().getchildren():
    if g.tag == "{http://www.w3.org/2000/svg}g":
        for elem in g.getchildren():
            if elem.tag == "{http://www.w3.org/2000/svg}path":
                style = dict(x.strip().split(":") for x in elem.attrib["style"].split(";"))
                # skip this path if it is not visible
                if style.get("visibility", "visible") == "visible" and style.get("display", "inline") != "none":
                    d = re.split("[\s,]+", elem.attrib["d"].strip())
                    commands = []
                    i = 0
                    while i < len(d):
                        if d[i].upper() in ("M", "L"):
                            x, y = float(d[i+1]), float(d[i+2])
                            commands.append(list(transform(x, y)) + [d[i].upper()])
                            i += 2

                        elif d[i].upper() == "Z":
                            commands.append("Z")

                        i += 1

                    paths.append(Path(commands, style))

# I changed my mind about some colors
for p in paths:
    if p.style["fill"] == "#517179":
        p.style["fill"] = "#218ba6"
    if p.style["fill"] == "#9f7054":
        p.style["fill"] = "#ed6b51"
    if p.style["fill"] == "#9aa87c":
        p.style["fill"] = "#79bd68"
    if p.style["stroke"] == "#676767":
        p.style["stroke"] = "#6e5638"
    p.style["stroke-width"] = "1.0"

# needed for brevity in color-mappings
Y = "#e1ba62"
B = "#218ba6"
R = "#ed6b51"
G = "#79bd68"

# The following transformations are approximate; some fish don't line up in orientation or color.
# It turns out that this Escher painting is more mathematically complicated than I had thought!
# (But I'm not going to spend a lot of time figuring it out...)

pathsA0 = []
Br, Bi, angle = 1.07*cos(15.0*pi/9.0), 1.07*sin(15.0*pi/9.0), 15.0*pi/9.0 - 2.0*pi/9.0
for p in paths:
    # pathsA0.append(p.transformation(Br, Bi, angle, flip=-1, opacity=1, color={B: G, G: R, R: B}))
    pathsA0.append(p.transformation(Br, Bi, angle, flip=1, opacity=1, color={R:G, B:R, G:B}))

pathsA1 = []
Br, Bi, angle = 1.07*cos(17.0*pi/9.0), 1.07*sin(17.0*pi/9.0), 17.0*pi/9.0
for p in paths:
    # pathsA1.append(p.transformation(Br, Bi, angle, opacity=1, color={Y: R, R: B, B: Y}))
    pathsA1.append(p.transformation(Br, Bi, angle, opacity=1, color={Y:R, R:Y, B:G, G:B}))

pathsA2 = []
Br, Bi, angle = 1.07*cos(1.0*pi/9.0), 1.07*sin(1.0*pi/9.0), 1.0*pi/9.0 - 1.0*pi/9.0
for p in paths:
    # pathsA2.append(p.transformation(Br, Bi, angle, flip=-1, opacity=1, color={B: G, G: Y, Y: B}))
    pathsA2.append(p.transformation(Br, Bi, angle, flip=-1, opacity=1, color={}))

pathsA3 = []
Br, Bi, angle = 1.07*cos(3.0*pi/9.0), 1.07*sin(3.0*pi/9.0), 3.0*pi/9.0 - 2.0*pi/9.0
for p in paths:
    # pathsA3.append(p.transformation(Br, Bi, angle, flip=-1, opacity=1, color={G: R, R: Y, Y: G}))
    pathsA3.append(p.transformation(Br, Bi, angle, flip=1, opacity=1, color={R:B, B:R, G:Y, Y:G}))

pathsA4 = []
Br, Bi, angle = 1.07*cos(5.0*pi/9.0), 1.07*sin(5.0*pi/9.0), 5.0*pi/9.0
for p in paths:
    # pathsA4.append(p.transformation(Br, Bi, angle, opacity=1, color={R: Y, Y: R}))
    pathsA4.append(p.transformation(Br, Bi, angle, opacity=1, color={Y:R, R:G, G:Y}))

pathsA5 = []
Br, Bi, angle = 1.07*cos(7.0*pi/9.0), 1.07*sin(7.0*pi/9.0), 7.0*pi/9.0 + 3.0*pi/9.0
for p in paths:
    pathsA5.append(p.transformation(Br, Bi, angle, flip=-1, opacity=1, color={}))

pathsA6 = []
Br, Bi, angle = 1.07*cos(9.0*pi/9.0), 1.07*sin(9.0*pi/9.0), 9.0*pi/9.0 + 3.0*pi/9.0
for p in paths:
    pathsA6.append(p.transformation(Br, Bi, angle, flip=-1, opacity=1, color={B:Y, R:G, Y:B, G:R}))

pathsA7 = []
Br, Bi, angle = 1.07*cos(11.0*pi/9.0), 1.07*sin(11.0*pi/9.0), 11.0*pi/9.0
for p in paths:
    # pathsA7.append(p.transformation(Br, Bi, angle, opacity=1, color={B: G, Y: R, G: B, R: Y}))
    pathsA7.append(p.transformation(Br, Bi, angle, opacity=1, color={Y:R, B:Y, R:G, G:B}))

pathsA8 = []
Br, Bi, angle = 1.07*cos(13.0*pi/9.0), 1.07*sin(13.0*pi/9.0), 13.0*pi/9.0 + 1.0*pi/9.0
for p in paths:
    # pathsA8.append(p.transformation(Br, Bi, angle, flip=-1, opacity=1, color={B: Y, Y: B}))
    pathsA8.append(p.transformation(Br, Bi, angle, flip=-1, opacity=1, color={G:Y, Y:R, R:B, B:G}))

pathsB0 = []
Br, Bi, angle = 1.07*cos(1.0*pi/9.0), 1.07*sin(1.0*pi/9.0), 1.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    # pathsB0.append(p.transformation(Br, Bi, angle, opacity=1, color={R: G, B: Y, G: B, Y: R}))
    pathsB0.append(p.transformation(Br, Bi, angle, opacity=1, color={B:Y, R:B, Y:R}))

pathsB1 = []
Br, Bi, angle = 1.07*cos(3.0*pi/9.0), 1.07*sin(3.0*pi/9.0), 3.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    # pathsB1.append(p.transformation(Br, Bi, angle, opacity=1, color={R: B, B: R}))
    pathsB1.append(p.transformation(Br, Bi, angle, opacity=1, color={G:B, B:R, R:Y, Y:G}))

pathsB2 = []
Br, Bi, angle = 1.07*cos(5.0*pi/9.0), 1.07*sin(5.0*pi/9.0), 5.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB2.append(p.transformation(Br, Bi, angle, opacity=1, color={Y:B, B:R, R:Y}))

pathsB3 = []
Br, Bi, angle = 1.07*cos(7.0*pi/9.0), 1.07*sin(7.0*pi/9.0), 7.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB3.append(p.transformation(Br, Bi, angle, opacity=1, color={R:B, B:G, G:R}))

pathsB4 = []
Br, Bi, angle = 1.07*cos(9.0*pi/9.0), 1.07*sin(9.0*pi/9.0), 9.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB4.append(p.transformation(Br, Bi, angle, opacity=1, color={B:R, R:Y, Y:G, G:B}))

pathsB5 = []
Br, Bi, angle = 1.07*cos(11.0*pi/9.0), 1.07*sin(11.0*pi/9.0), 11.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB5.append(p.transformation(Br, Bi, angle, opacity=1, color={R:G, B:Y, G:R, Y:B}))

pathsB6 = []
Br, Bi, angle = 1.07*cos(13.0*pi/9.0), 1.07*sin(13.0*pi/9.0), 13.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB6.append(p.transformation(Br, Bi, angle, opacity=1, color={Y:R, R:Y}))

pathsB7 = []
Br, Bi, angle = 1.07*cos(15.0*pi/9.0), 1.07*sin(15.0*pi/9.0), 15.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB7.append(p.transformation(Br, Bi, angle, opacity=1, color={}))

pathsB8 = []
Br, Bi, angle = 1.07*cos(17.0*pi/9.0), 1.07*sin(17.0*pi/9.0), 17.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB8.append(p.transformation(Br, Bi, angle, opacity=1, color={B:Y, Y:B}))

pathsC0 = []
Br, Bi, angle = 1.07*cos(1.0*pi/9.0), 1.07*sin(1.0*pi/9.0), 1.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC0.append(p.transformation(Br, Bi, angle, opacity=1))

pathsC1 = []
Br, Bi, angle = 1.07*cos(3.0*pi/9.0), 1.07*sin(3.0*pi/9.0), 3.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC1.append(p.transformation(Br, Bi, angle, opacity=1))

pathsC2 = []
Br, Bi, angle = 1.07*cos(5.0*pi/9.0), 1.07*sin(5.0*pi/9.0), 5.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC2.append(p.transformation(Br, Bi, angle, opacity=1))

pathsC3 = []
Br, Bi, angle = 1.07*cos(7.0*pi/9.0), 1.07*sin(7.0*pi/9.0), 7.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC3.append(p.transformation(Br, Bi, angle, opacity=1))

pathsC4 = []
Br, Bi, angle = 1.07*cos(9.0*pi/9.0), 1.07*sin(9.0*pi/9.0), 9.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC4.append(p.transformation(Br, Bi, angle, opacity=1))

pathsC5 = []
Br, Bi, angle = 1.07*cos(11.0*pi/9.0), 1.07*sin(11.0*pi/9.0), 11.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC5.append(p.transformation(Br, Bi, angle, opacity=1))

pathsC6 = []
Br, Bi, angle = 1.07*cos(13.0*pi/9.0), 1.07*sin(13.0*pi/9.0), 13.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC6.append(p.transformation(Br, Bi, angle, opacity=1))

pathsC7 = []
Br, Bi, angle = 1.07*cos(15.0*pi/9.0), 1.07*sin(15.0*pi/9.0), 15.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC7.append(p.transformation(Br, Bi, angle, opacity=1))

pathsC8 = []
Br, Bi, angle = 1.07*cos(17.0*pi/9.0), 1.07*sin(17.0*pi/9.0), 17.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC8.append(p.transformation(Br, Bi, angle, opacity=1))

sys.stdout.write("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"600\" height=\"602\">\n")

def draw(somePaths):
    for p in somePaths:
        if hideStrokes and p.style["stroke"] != "none": continue
        if onlyStrokes and p.style["stroke"] == "none": continue
        sys.stdout.write(p.svg())
        sys.stdout.write("\n")

draw(paths)
draw(pathsA0)
draw(pathsA1)
draw(pathsA2)
draw(pathsA3)
draw(pathsA4)
draw(pathsA5)
draw(pathsA6)
draw(pathsA7)
draw(pathsA8)
draw(pathsB0)
draw(pathsB1)
draw(pathsB2)
draw(pathsB3)
draw(pathsB4)
draw(pathsB5)
draw(pathsB6)
draw(pathsB7)
draw(pathsB8)
draw(pathsC0)
draw(pathsC1)
draw(pathsC2)
draw(pathsC3)
draw(pathsC4)
draw(pathsC5)
draw(pathsC6)
draw(pathsC7)
draw(pathsC8)

if not hideCircle:
    sys.stdout.write(ElementTree.tostring(circle))

if hyperShadow:
    x1, y1 = transformBack(0, 0)
    x2, y2 = transformBack(1, 1)
    sys.stdout.write("<rect x=\"%g\" y=\"%g\" width=\"%g\" height=\"%g\" id=\"UnitRectangle\" stroke=\"black\" fill=\"none\"/>\n" % (x1, y1 - abs(y2 - y1), abs(x2 - x1), abs(y2 - y1)))

sys.stdout.write("</svg>\n")
