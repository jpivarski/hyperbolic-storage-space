#!/usr/bin/env python

# To prepare an SVG image for transformation:

# Set Inkscape preferences -> SVG output:
#     Allow relative coordinates: false
#     Force repeat commands: true
#     Numeric precision: 14
#     Minimum exponent: -32
# and save as "Plain SVG".

# Make sure to include a <rect/> with id="UnitRectangle" (name it in Inkscape's XML Editor).
# This will be mapped to a rectangle from (0, 0) to (1, 1) in the hyperbolicShadow or
#                                         (0, log2(0)) to (1, log2(1)) in the halfPlane, with log-base-2 y axis.
# The UnitRectangle will not be drawn.

# Make sure that none of the elements have a transform attribute.  (Maybe we can loosen that restriction in the future.)
# Make sure that none of the elements are in any groups (ungrouping is a good way to remove transform attributes).

import sys
import math
import json
try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

from hypertrans import *


