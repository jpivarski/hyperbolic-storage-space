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

    def transformation(self, Br, Bi, angle, flip=1, opacity=1):
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

        return Path(commands, style)

    def svg(self):
        d = []
        for command in self.commands:
            if isinstance(command, list):
                x, y = command[0:2]
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
for elem in document.getroot().getchildren():
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

# pathsN = []
# style = dict(paths[0].style)
# style["stroke"] = "black"
# style["fill"] = "none"
# commands = []
# for n in range(10):
#     x, y = hyperShadow_to_poincareDisk(0.54*cos(n*2.0*pi/9.0), 0.54*sin(n*2.0*pi/9.0))
#     commands.append([x, y, "L"])
# commands[0][2] = "M"
# pathsN.append(Path(commands, style))

pathsA0 = []
Br, Bi, angle = 1.07*cos(15.0*pi/9.0), 1.07*sin(15.0*pi/9.0), 15.0*pi/9.0 + 3.0*pi/9.0
for p in paths:
    pathsA0.append(p.transformation(Br, Bi, angle, flip=-1))

pathsA1 = []
Br, Bi, angle = 1.07*cos(17.0*pi/9.0), 1.07*sin(17.0*pi/9.0), 17.0*pi/9.0
for p in paths:
    pathsA1.append(p.transformation(Br, Bi, angle))

pathsA2 = []
Br, Bi, angle = 1.07*cos(1.0*pi/9.0), 1.07*sin(1.0*pi/9.0), 1.0*pi/9.0 + 3.0*pi/9.0
for p in paths:
    pathsA2.append(p.transformation(Br, Bi, angle, flip=-1))

pathsA3 = []
Br, Bi, angle = 1.07*cos(3.0*pi/9.0), 1.07*sin(3.0*pi/9.0), 3.0*pi/9.0 + 3.0*pi/9.0
for p in paths:
    pathsA3.append(p.transformation(Br, Bi, angle, flip=-1))

pathsA4 = []
Br, Bi, angle = 1.07*cos(5.0*pi/9.0), 1.07*sin(5.0*pi/9.0), 5.0*pi/9.0
for p in paths:
    pathsA4.append(p.transformation(Br, Bi, angle))

pathsA5 = []
Br, Bi, angle = 1.07*cos(7.0*pi/9.0), 1.07*sin(7.0*pi/9.0), 7.0*pi/9.0 + 3.0*pi/9.0
for p in paths:
    pathsA5.append(p.transformation(Br, Bi, angle, flip=-1))

pathsA6 = []
Br, Bi, angle = 1.07*cos(9.0*pi/9.0), 1.07*sin(9.0*pi/9.0), 9.0*pi/9.0 + 3.0*pi/9.0
for p in paths:
    pathsA6.append(p.transformation(Br, Bi, angle, flip=-1))

pathsA7 = []
Br, Bi, angle = 1.07*cos(11.0*pi/9.0), 1.07*sin(11.0*pi/9.0), 11.0*pi/9.0
for p in paths:
    pathsA7.append(p.transformation(Br, Bi, angle))

pathsA8 = []
Br, Bi, angle = 1.07*cos(13.0*pi/9.0), 1.07*sin(13.0*pi/9.0), 13.0*pi/9.0 + 3.0*pi/9.0
for p in paths:
    pathsA8.append(p.transformation(Br, Bi, angle, flip=-1))

pathsB0 = []
Br, Bi, angle = 1.07*cos(1.0*pi/9.0), 1.07*sin(1.0*pi/9.0), 1.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB0.append(p.transformation(Br, Bi, angle))

pathsB1 = []
Br, Bi, angle = 1.07*cos(3.0*pi/9.0), 1.07*sin(3.0*pi/9.0), 3.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB1.append(p.transformation(Br, Bi, angle))

pathsB2 = []
Br, Bi, angle = 1.07*cos(5.0*pi/9.0), 1.07*sin(5.0*pi/9.0), 5.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB2.append(p.transformation(Br, Bi, angle))

pathsB3 = []
Br, Bi, angle = 1.07*cos(7.0*pi/9.0), 1.07*sin(7.0*pi/9.0), 7.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB3.append(p.transformation(Br, Bi, angle))

pathsB4 = []
Br, Bi, angle = 1.07*cos(9.0*pi/9.0), 1.07*sin(9.0*pi/9.0), 9.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB4.append(p.transformation(Br, Bi, angle))

pathsB5 = []
Br, Bi, angle = 1.07*cos(11.0*pi/9.0), 1.07*sin(11.0*pi/9.0), 11.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB5.append(p.transformation(Br, Bi, angle))

pathsB6 = []
Br, Bi, angle = 1.07*cos(13.0*pi/9.0), 1.07*sin(13.0*pi/9.0), 13.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB6.append(p.transformation(Br, Bi, angle))

pathsB7 = []
Br, Bi, angle = 1.07*cos(15.0*pi/9.0), 1.07*sin(15.0*pi/9.0), 15.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB7.append(p.transformation(Br, Bi, angle))

pathsB8 = []
Br, Bi, angle = 1.07*cos(17.0*pi/9.0), 1.07*sin(17.0*pi/9.0), 17.0*pi/9.0
for p in pathsA0 + pathsA1 + pathsA2 + pathsA3 + pathsA4:
    pathsB8.append(p.transformation(Br, Bi, angle))

pathsC0 = []
Br, Bi, angle = 1.07*cos(1.0*pi/9.0), 1.07*sin(1.0*pi/9.0), 1.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC0.append(p.transformation(Br, Bi, angle))

pathsC1 = []
Br, Bi, angle = 1.07*cos(3.0*pi/9.0), 1.07*sin(3.0*pi/9.0), 3.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC1.append(p.transformation(Br, Bi, angle))

pathsC2 = []
Br, Bi, angle = 1.07*cos(5.0*pi/9.0), 1.07*sin(5.0*pi/9.0), 5.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC2.append(p.transformation(Br, Bi, angle))

pathsC3 = []
Br, Bi, angle = 1.07*cos(7.0*pi/9.0), 1.07*sin(7.0*pi/9.0), 7.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC3.append(p.transformation(Br, Bi, angle))

pathsC4 = []
Br, Bi, angle = 1.07*cos(9.0*pi/9.0), 1.07*sin(9.0*pi/9.0), 9.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC4.append(p.transformation(Br, Bi, angle))

pathsC5 = []
Br, Bi, angle = 1.07*cos(11.0*pi/9.0), 1.07*sin(11.0*pi/9.0), 11.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC5.append(p.transformation(Br, Bi, angle))

pathsC6 = []
Br, Bi, angle = 1.07*cos(13.0*pi/9.0), 1.07*sin(13.0*pi/9.0), 13.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC6.append(p.transformation(Br, Bi, angle))

pathsC7 = []
Br, Bi, angle = 1.07*cos(15.0*pi/9.0), 1.07*sin(15.0*pi/9.0), 15.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC7.append(p.transformation(Br, Bi, angle))

pathsC8 = []
Br, Bi, angle = 1.07*cos(17.0*pi/9.0), 1.07*sin(17.0*pi/9.0), 17.0*pi/9.0
for p in pathsB6 + pathsB7 + pathsB8 + pathsB0 + pathsB1:
    pathsC8.append(p.transformation(Br, Bi, angle))

f = open("/tmp/test.svg", "w")
f.write("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"600\" height=\"602\">\n")
f.write("\n".join([p.svg() for p in paths]) + "\n")
f.write("\n".join([p.svg() for p in pathsA0]) + "\n")
f.write("\n".join([p.svg() for p in pathsA1]) + "\n")
f.write("\n".join([p.svg() for p in pathsA2]) + "\n")
f.write("\n".join([p.svg() for p in pathsA3]) + "\n")
f.write("\n".join([p.svg() for p in pathsA4]) + "\n")
f.write("\n".join([p.svg() for p in pathsA5]) + "\n")
f.write("\n".join([p.svg() for p in pathsA6]) + "\n")
f.write("\n".join([p.svg() for p in pathsA7]) + "\n")
f.write("\n".join([p.svg() for p in pathsA8]) + "\n")
# f.write("\n".join([p.svg() for p in pathsB0]) + "\n")
# f.write("\n".join([p.svg() for p in pathsB1]) + "\n")
# f.write("\n".join([p.svg() for p in pathsB2]) + "\n")
# f.write("\n".join([p.svg() for p in pathsB3]) + "\n")
# f.write("\n".join([p.svg() for p in pathsB4]) + "\n")
# f.write("\n".join([p.svg() for p in pathsB5]) + "\n")
# f.write("\n".join([p.svg() for p in pathsB6]) + "\n")
# f.write("\n".join([p.svg() for p in pathsB7]) + "\n")
# f.write("\n".join([p.svg() for p in pathsB8]) + "\n")
# f.write("\n".join([p.svg() for p in pathsC0]) + "\n")
# f.write("\n".join([p.svg() for p in pathsC1]) + "\n")
# f.write("\n".join([p.svg() for p in pathsC2]) + "\n")
# f.write("\n".join([p.svg() for p in pathsC3]) + "\n")
# f.write("\n".join([p.svg() for p in pathsC4]) + "\n")
# f.write("\n".join([p.svg() for p in pathsC5]) + "\n")
# f.write("\n".join([p.svg() for p in pathsC6]) + "\n")
# f.write("\n".join([p.svg() for p in pathsC7]) + "\n")
# f.write("\n".join([p.svg() for p in pathsC8]) + "\n")
f.write(ElementTree.tostring(circle))
f.write("</svg>\n")
f.close()
