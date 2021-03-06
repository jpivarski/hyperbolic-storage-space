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
execfile("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/transformHalfPlane.py")

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
