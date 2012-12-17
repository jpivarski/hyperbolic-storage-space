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

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/vast_dungeon.svg")
backgroundPaths = loadSVG(document.getroot(), coordinateSystem=None)

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/dungeonman.svg")
dungeonman = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in dungeonman:
    p.transformBack = backgroundPaths[0].transformBack

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter1.svg")
critter1 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in critter1:
    p.transformBack = backgroundPaths[0].transformBack

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter2.svg")
critter2 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in critter2:
    p.transformBack = backgroundPaths[0].transformBack

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter3.svg")
critter3 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in critter3:
    p.transformBack = backgroundPaths[0].transformBack

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter4.svg")
critter4 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in critter4:
    p.transformBack = backgroundPaths[0].transformBack

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter5.svg")
critter5 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in critter5:
    p.transformBack = backgroundPaths[0].transformBack

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter6.svg")
critter6 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in critter6:
    p.transformBack = backgroundPaths[0].transformBack

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter7.svg")
critter7 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in critter7:
    p.transformBack = backgroundPaths[0].transformBack

document = ElementTree.parse("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/examples/critter8.svg")
critter8 = loadSVG(document.getroot(), coordinateSystem="hyperShadow")
for p in critter8:
    p.transformBack = backgroundPaths[0].transformBack

critterPositions = {}

for latitude in range(-20, -4) + range(5, 21):
    for i in xrange(3):
        longitude = int(round(random.gauss(0., 20.)))
        x = 2**(latitude-1)*longitude
        y = 2**latitude
        x, y = halfPlane_to_hyperShadow(x, y)
        distance = math.sqrt(x**2 + y**2)
        if distance > 10.0:
            critterPositions[latitude, longitude] = (critter8, math.pi)
            sys.stderr.write("critter8 at %d %d (%g)\n" % (latitude, longitude, distance))

for latitude in xrange(-20, 11):
    for i in xrange(10):
        longitude = int(round(random.gauss(0., 20.)))
        x = 2**(latitude-1)*longitude
        y = 2**latitude
        x, y = halfPlane_to_hyperShadow(x, y)
        distance = math.sqrt(x**2 + y**2)
        if distance > 5.0:
            critterIndex = random.randint(2, 7)
            critterPositions[latitude, longitude] = ({2: critter2, 3: critter3, 4: critter4, 5: critter5, 6: critter6, 7: critter7}[critterIndex], math.pi)
            sys.stderr.write("critter%d at %d %d (%g)\n" % (critterIndex, latitude, longitude, distance))

for latitude in xrange(-10, 10):  # xrange(-26, 27):
    for i in xrange(10):
        longitude = int(round(random.gauss(0., 10.)))
        x = 2**(latitude-1)*longitude
        y = 2**latitude
        x, y = halfPlane_to_hyperShadow(x, y)
        distance = math.sqrt(x**2 + y**2)
        if distance > 3.0:
            angle = math.pi/2. * random.randint(0, 3)
            critterPositions[latitude, longitude] = (critter1, angle)
            sys.stderr.write("critter1 at %d %d (%g)\n" % (latitude, longitude, distance))

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

# for p in backgroundPaths:
#     f.write(p.svg())
#     f.write("\n")

for p in critters:
    f.write(p.svg())
    f.write("\n")

f.write("</svg>\n")
f.close()
