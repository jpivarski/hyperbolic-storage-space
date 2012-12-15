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

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/vast_dungeon.svg")
backgroundPaths = loadSVG(document.getroot(), coordinateSystem=None)

backgroundPaths2 = []
for p in backgroundPaths:
    backgroundPaths2.append(p)

for index in xrange(-5, 5):
    if index != 0:
        for p in backgroundPaths:
            backgroundPaths2.append(p.naivemove(0.5*index, 0.0))

# down a level
nextrow = []
for p in backgroundPaths:
    nextrow.append(p.naivemove(0.25, -0.25, 2., 2.))
for index in xrange(-3, 3):
    for p in nextrow:
        backgroundPaths2.append(p.naivemove(index, 0.0))

# up a level
nextrow = []
for p in backgroundPaths:
    nextrow.append(p.naivemove(0.125, 0.125, 0.5, 0.5))
for index in xrange(-10, 10):
    for p in nextrow:
        backgroundPaths2.append(p.naivemove(0.25*index, 0.0))

for p in backgroundPaths2:
    p.transform(halfPlane_to_hyperShadow)

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/dungeonman.svg")
dungeonman = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in dungeonman:
    p.transformBack = backgroundPaths2[0].transformBack
    # p.move(0.0, 1.05, 0.0)

# f = open("/tmp/test.pmml", "w")
f = sys.stdout
f.write("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"2800\" height=\"800\">\n")

for p in backgroundPaths2:
    f.write(p.svg())
    f.write("\n")

for p in dungeonman:
    f.write(p.svg())
    f.write("\n")

f.write("</svg>\n")
f.close()
