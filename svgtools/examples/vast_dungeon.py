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

for longitude in xrange(-10, 10+1):
    if longitude != 0:
        for p in backgroundPaths:
            backgroundPaths2.append(p.naivemove(0.5*longitude, 0.0))

# down a level
nextrow = []
for p in backgroundPaths:
    nextrow.append(p.naivemove(0.0, 0.0, 0.5, 0.5))

for latitude in xrange(1, 3): # xrange(1, 27):
    for longitude in xrange(-3, 3+1):
        for p in nextrow:
            backgroundPaths2.append(p.naivemove(longitude*0.5**(latitude+1), 0.0))
    nextnextrow = []
    for p in nextrow:
        nextnextrow.append(p.naivemove(0.0, 0.0, 0.5, 0.5))
    nextrow = nextnextrow

# up a level
nextrow = []
for p in backgroundPaths:
    nextrow.append(p.naivemove(0.0, 0.0, 2.0, 2.0))

for latitude in xrange(1, 3): # xrange(1, 27):
    for longitude in xrange(-3, 3+1):
        for p in nextrow:
            backgroundPaths2.append(p.naivemove(longitude*2.0**(latitude-1), 0.0))
    nextnextrow = []
    for p in nextrow:
        nextnextrow.append(p.naivemove(0.0, 0.0, 2.0, 2.0))
    nextrow = nextnextrow

for p in backgroundPaths2:
    p.transform(halfPlane_to_hyperShadow)
    # p.move(0.117, 0.17, 0.27)

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/dungeonman.svg")
dungeonman = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in dungeonman:
    p.transformBack = backgroundPaths2[0].transformBack
    # p.move(0.0, 1.05, 0.0)

dungeonman2 = []
for p in dungeonman:
    p2 = p.naivemove(0., 0., 1., 1.)
    p2.transform(hyperShadow_to_halfPlane)
    p3 = p2.naivemove(0.25, -0.25, 1., 1.)
    p3.transform(halfPlane_to_hyperShadow)
    dungeonman2.append(p3)

# dungeonman2 = []
# for p in dungeonman:
#     p2 = p.naivemove(0., 0., 1., 1.)
#     p2.transform(hyperShadow_to_halfPlane)
#     for latitude in xrange(-3, 3):
#         p3 = p2.naivemove(0.25, -0.25, 1., 1.)
#         p3 = p3.naivemove(0.0, 0.0, 2**latitude, 2**latitude)
#         for longitude in xrange(-3, 3):
#             p4 = p3.naivemove(2**(latitude-1)*longitude, 0.0, 1., 1.)
#             p4.transform(halfPlane_to_hyperShadow)
#             dungeonman2.append(p4)

# f = open("/tmp/test.pmml", "w")
f = sys.stdout
f.write("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"2800\" height=\"800\">\n")

for p in backgroundPaths2:
    f.write(p.svg())
    f.write("\n")

for p in dungeonman2:
    f.write(p.svg())
    f.write("\n")

f.write("</svg>\n")
f.close()
