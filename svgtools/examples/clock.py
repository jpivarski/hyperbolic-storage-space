#!/usr/bin/env python

import math

# from hypertrans import *
execfile("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/hypertrans.py")

print """<!DOCTYPE html>
<html>
<meta charset="utf-8">
<script type="text/javascript" src="HyperbolicViewport.js"></script>
<script type="text/javascript">

var hyperbolicMapService;
var hyperbolicViewport;

function HyperbolicMapClock(clockFace, clockHand) {
    this.clockFace = clockFace;
    this.clockHand = clockHand;
    this.styles = {"default": new HyperbolicStyleClass()};
}

HyperbolicMapClock.prototype.downloadDrawables = function(offsetx, offsety, radius, async, hyperbolicViewport) { }

HyperbolicMapClock.prototype.beginDrawableLoop = function(offsetx, offsety, radius) {
    this.which = 0;
    this.i = 0;
}

HyperbolicMapClock.prototype.nextDrawable = function() {
    if (this.which == 0  &&  this.i >= this.clockFace.length) {
        this.which = 1;
        this.i = 0;
    }
    if (this.which == 0) {
        return this.clockFace[this.i++];
    }
    else {
        return this.clockHand[this.i++];
    }
}

function init() {
    var clockFace = [];
    var clockHand = [];
"""

for i in xrange(12):
    angle = -2.*math.pi/12. * ((i - 2) % 12)
    x1, y1 = 1.0*math.cos(angle), 1.0*math.sin(angle)
    x2, y2 = 1.1*math.cos(angle), 1.1*math.sin(angle)
    x3, y3 = 1.2*math.cos(angle), 1.2*math.sin(angle)
    x4, y4 = 1.5*math.cos(angle), 1.5*math.sin(angle)
    print """    clockFace.push({"type": "polygon", "d": [[%.18e, %.18e, "L"], [%.18e, %.18e]]});""" % (x1, y1, x2, y2)
    print """    clockFace.push({"type": "text", "d": "%d", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#000000"});""" % (i+1, x3, y3, x4, y4)

for i in xrange(60):
    angle = -2.*math.pi/60. * ((i - 14) % 60)
    x1, y1 = 2.2*math.cos(angle), 2.2*math.sin(angle)
    x2, y2 = 2.4*math.cos(angle), 2.4*math.sin(angle)
    x3, y3 = 2.5*math.cos(angle), 2.5*math.sin(angle)
    x4, y4 = 2.8*math.cos(angle), 2.8*math.sin(angle)
    print """    clockFace.push({"type": "polygon", "d": [[%.18e, %.18e, "L"], [%.18e, %.18e]]});""" % (x1, y1, x2, y2)
    print """    clockFace.push({"type": "text", "d": "%d", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#000000"});""" % (i+1, x3, y3, x4, y4)

# for i in xrange(60*10):
#     angle = -2.*math.pi/60./10. * ((i + 1) % (60*10))
#     x1, y1 = 3.0*math.cos(angle), 3.0*math.sin(angle)
#     x2, y2 = 3.8*math.cos(angle), 3.8*math.sin(angle)
#     x3, y3 = 3.9*math.cos(angle), 3.9*math.sin(angle)
#     x4, y4 = 4.2*math.cos(angle), 4.2*math.sin(angle)
#     print """    clockFace.push({"type": "polygon", "d": [[%.18e, %.18e, "L"], [%.18e, %.18e]]});""" % (x1, y1, x2, y2)
#     print """    clockFace.push({"type": "text", "d": "%d", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#000000"});""" % (10 * ((i+1) % 6), x3, y3, x4, y4)

for i in xrange(60*60):
    angle = -2.*math.pi/60./60. * ((i + 1) % (60*60))
    x1, y1 = 5.0*math.cos(angle), 5.0*math.sin(angle)
    x2, y2 = 5.8*math.cos(angle), 5.8*math.sin(angle)
    x3, y3 = 5.9*math.cos(angle), 5.9*math.sin(angle)
    x4, y4 = 6.2*math.cos(angle), 6.2*math.sin(angle)
    print """    clockFace.push({"type": "polygon", "d": [[%.18e, %.18e, "L"], [%.18e, %.18e]]});""" % (x1, y1, x2, y2)
    print """    clockFace.push({"type": "text", "d": "%d", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#000000"});""" % ((i+1) % 60, x3, y3, x4, y4)

print """    clockHand.push({"type": "polygon", "d": [[0.0, 0.01673111, "L"], [0.0, 0.6], [0.0, 0.9, "L"], [0.0, 1.5], [0.0, 2.2, "L"], [0.0, 3.1], [0.0, 4.5, "L"], [0.0, 7.2]], "strokeStyle": "#990000", "lineWidth": 3.0});"""

print """    clockHand.push({"type": "polygon", "d": [[0.05, -0.03314517, "L"], [0.0452134, -0.05452093, "L"], [0.03358215, -0.07018942, "L"], [0.01898142, -0.07941633, "L"], [0.0, -0.08314517, "L"], [-0.02001435, -0.07897846, "L"], [-0.03323666, -0.07049991, "L"], [-0.0444685, -0.05602747, "L"], [-0.05, -0.03314517, "L"], [-0.04499175, -0.01130758, "L"], [-0.03584449, 0.0017142, "L"], [-0.02073447, 0.01236639, "L"], [0.0, 0.01685483, "L"], [0.02542647, 0.0099162, "L"], [0.03827542, -0.000972107, "L"], [0.04723795, -0.01671535, "L"]], "strokeStyle": "#990000", "lineWidth": 3.0});"""

x1, y1 = poincareDisk_to_hyperShadow(*internalToScreen( 0.0, 0.0, 0.0, 0.75, 0.0))
x2, y2 = poincareDisk_to_hyperShadow(*internalToScreen(-0.1, 0.0, 0.0, 0.75, 0.0))
print """    clockHand.push({"type": "text", "d": "hour", "textBaseline": "middle", "textAlign": "center", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#990000"});""" % (x1, y1, x2, y2)

x1, y1 = poincareDisk_to_hyperShadow(*internalToScreen( 0.0, 0.0, 0.0, 1.8, 0.0))
x2, y2 = poincareDisk_to_hyperShadow(*internalToScreen(-0.1, 0.0, 0.0, 1.8, 0.0))
print """    clockHand.push({"type": "text", "d": "minute", "textBaseline": "middle", "textAlign": "center", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#990000"});""" % (x1, y1, x2, y2)

x1, y1 = poincareDisk_to_hyperShadow(*internalToScreen( 0.0, 0.0, 0.0, 3.7, 0.0))
x2, y2 = poincareDisk_to_hyperShadow(*internalToScreen(-0.1, 0.0, 0.0, 3.7, 0.0))
print """    clockHand.push({"type": "text", "d": "second", "textBaseline": "middle", "textAlign": "center", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#990000"});""" % (x1, y1, x2, y2)

x1, y1 = poincareDisk_to_hyperShadow(*internalToScreen(-0.04848732,    -0.12473479, 0.0, 7.2, 0.0))
x2, y2 = poincareDisk_to_hyperShadow(*internalToScreen( 0.00050508,     0.05002161, 0.0, 7.2, 0.0))
x3, y3 = poincareDisk_to_hyperShadow(*internalToScreen( 0.05101271,    -0.12473479, 0.0, 7.2, 0.0))
x4, y4 = poincareDisk_to_hyperShadow(*internalToScreen( 0.00088688396, -0.07548339, 0.0, 7.2, 0.0))
print """    clockHand.push({"type": "polygon", "d": [[%.18e, %.18e, "L"], [%.18e, %.18e, "L"], [%.18e, %.18e, "L"], [%.18e, %.18e, "L"]], "strokeStyle": "none", "fillStyle": "#990000"});""" % (x1, y1, x2, y2, x3, y3, x4, y4)

print """
    hyperbolicMapService = new HyperbolicMapClock(clockFace, clockHand);
    hyperbolicViewport = new HyperbolicViewport(hyperbolicMapService, "hyperbolicViewport", 640, 640, {"allowZoom": false, "initialZoom": 0.95, "minZoom": 0.95, "maxZoom": 0.95, "viewThreshold": 0.98});
}

</script>
<body onload="init();">
<div id="hyperbolicViewport" style="margin: 20px;"></div>
</body>
</html>
"""
