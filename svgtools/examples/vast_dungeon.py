#!/usr/bin/env python

import sys
import math
import json
import re
import random
try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

# from hypertrans import *
execfile("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/hypertrans.py")
execfile("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/transformHalfPlane.py")

# maxLongitude = {
#     1: 15675,
#     2: 11084,
#     3: 7838,
#     4: 5542,
#     5: 3919,
#     6: 2771,
#     7: 1960,
#     8: 1386,
#     9: 980,
#     10: 693,
#     11: 490,
#     12: 347,
#     13: 245,
#     14: 174,
#     15: 123,
#     16: 87,
#     17: 62,
#     18: 44,
#     19: 31,
#     20: 22,
#     21: 16,
#     22: 11,
#     23: 8,
#     24: 6,
#     25: 4,
#     26: 3,
#     }

maxLongitude = {
    0: 500,
    1: 500,
    2: 500,
    3: 500,
    4: 500,
    5: 500,
    6: 500,
    7: 500,
    8: 500,
    9: 500,
    10: 500,
    11: 490,
    12: 347,
    13: 245,
    14: 174,
    15: 123,
    16: 87,
    17: 62,
    18: 44,
    19: 31,
    20: 22,
    21: 16,
    22: 11,
    23: 8,
    24: 6,
    25: 4,
    26: 3,
    }

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/vast_dungeon.svg")
backgroundPaths = loadSVG(document.getroot(), coordinateSystem=None)

backgroundPaths2 = []
for p in backgroundPaths:
    backgroundPaths2.append(p)

for longitude in xrange(-500, 500+1):
    if longitude != 0:
        for p in backgroundPaths:
            backgroundPaths2.append(p.naivemove(0.5*longitude, 0.0))

# down a level
nextrow = []
for p in backgroundPaths:
    nextrow.append(p.naivemove(0.0, 0.0, 0.5, 0.5))

for latitude in xrange(1, 27):
    sys.stderr.write("down latitude: %d\n" % latitude)

    for longitude in xrange(-maxLongitude[latitude], maxLongitude[latitude]+1):
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

for latitude in xrange(1, 27):
    sys.stderr.write("up latitude: %d\n" % latitude)

    for longitude in xrange(-maxLongitude[latitude], maxLongitude[latitude]+1):
        for p in nextrow:
            backgroundPaths2.append(p.naivemove(longitude*2.0**(latitude-1), 0.0))

    # longitude = 0
    # done = False
    # while not done:
    #     longitude += 1
    #     x, y = nextrow[0].commands[0][0:2]
    #     x += longitude*2.0**(latitude-1)
    #     x, y = halfPlane_to_hyperShadow(x, y)
    #     distance = math.sqrt(x**2 + y**2)
    #     if abs(distance) > 6000 and not done:
    #         sys.stderr.write("%d: %d\n" % (latitude, longitude))
    #         done = True

    nextnextrow = []
    for p in nextrow:
        nextnextrow.append(p.naivemove(0.0, 0.0, 2.0, 2.0))
    nextrow = nextnextrow

for p in backgroundPaths2:
    p.transform(halfPlane_to_hyperShadow)

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/dungeonman.svg")
dungeonman = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in dungeonman:
    p.transformBack = backgroundPaths2[0].transformBack

# document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter1.svg")
# critter1 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
# for p in critter1:
#     p.transformBack = backgroundPaths2[0].transformBack

# document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter2.svg")
# critter2 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
# for p in critter2:
#     p.transformBack = backgroundPaths2[0].transformBack

# document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter3.svg")
# critter3 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
# for p in critter3:
#     p.transformBack = backgroundPaths2[0].transformBack

# document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter4.svg")
# critter4 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
# for p in critter4:
#     p.transformBack = backgroundPaths2[0].transformBack

# document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter5.svg")
# critter5 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
# for p in critter5:
#     p.transformBack = backgroundPaths2[0].transformBack

# document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter6.svg")
# critter6 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
# for p in critter6:
#     p.transformBack = backgroundPaths2[0].transformBack

# document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter7.svg")
# critter7 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
# for p in critter7:
#     p.transformBack = backgroundPaths2[0].transformBack

# document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter8.svg")
# critter8 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
# for p in critter8:
#     p.transformBack = backgroundPaths2[0].transformBack

critterPositions = {}
# for latitude in xrange(-26, 27):
#     maxL = maxLongitude[abs(latitude)]
#     for longitude in xrange(-maxL, maxL):
#         x = 2**(latitude-1)*longitude
#         y = 2**latitude
#         x, y = halfPlane_to_hyperShadow(x, y)
#         if math.sqrt(x**2 + y**2) > 20.0 and random.uniform(0.0, 500.0) < math.exp(-(x**2 + y**2)/2./100.**2):
#             critterPositions[latitude, longitude] = (critter8, math.pi)
#             sys.stderr.write("critter8 at %g\n" % math.sqrt(x**2 + y**2))
#         if random.uniform(0.0, 10.0) < math.exp(-(x**2 + y**2)/2./20.**2):
#             critter = random.sample([critter2, critter3, critter4, critter5, critter6, critter7], 1)[0]
#             critterPositions[latitude, longitude] = (critter, math.pi)
#             sys.stderr.write("critter at %g\n" % math.sqrt(x**2 + y**2))
#         if random.uniform(0.0, 5.0) < math.exp(-(x**2 + y**2)/2./10.**2):
#             angle = math.pi/2. * random.randint(0, 3)
#             critterPositions[latitude, longitude] = (critter1, angle)
#             sys.stderr.write("critter1 at %g\n" % math.sqrt(x**2 + y**2))

critterPositions[0, 0] = (dungeonman, 0.0)

critters = []
for (latitude, longitude), (critter, angle) in critterPositions.items():
    for p in critter:
        p2 = p.naivemove(0., 0., 1., 1., angle)
        p2.transform(hyperShadow_to_halfPlane)
        p3 = p2.naivemove(0.25, -0.25, 1., 1.)
        p3 = p3.naivemove(0.0, 0.0, 2**latitude, 2**latitude)
        p4 = p3.naivemove(2**(latitude-1)*longitude, 0.0, 1., 1.)
        p4.transform(halfPlane_to_hyperShadow)
        critters.append(p4)

# f = open("/tmp/test.pmml", "w")
f = sys.stdout
f.write("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"2800\" height=\"800\">\n")

for p in backgroundPaths2:
    f.write(p.svg())
    f.write("\n")

for p in critters:
    f.write(p.svg())
    f.write("\n")

f.write("</svg>\n")
f.close()
