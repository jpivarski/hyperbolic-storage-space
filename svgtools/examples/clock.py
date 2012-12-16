#!/usr/bin/env python

import math

# from hypertrans import *
execfile("/home/pivarski/fun/projects/hyperbolic-storage-space/svgtools/hypertrans.py")

html = open("/tmp/clock.html", "w")
dbtmp = open("/tmp/clock_dbtmp.txt", "w")

html.write("""<!DOCTYPE html>
<html>
<meta charset="utf-8">
<script type="text/javascript" src="HyperbolicViewport.js"></script>
<script type="text/javascript">

var hyperbolicMapService;
var hyperbolicViewport;

function HyperbolicMapClock(url, clockHand) {
    if (url == null) {
        this.url = "get";
    } else {
        this.url = url;
    }
    this.drawables = null;

    this.clockHandOriginal = clockHand;
    this.styles = {"default": new HyperbolicStyleClass()};
}

HyperbolicMapClock.prototype.downloadDrawables = HyperbolicMapServlet.prototype.downloadDrawables;

HyperbolicMapClock.prototype.beginDrawableLoop = function(offsetx, offsety, radius) {
    if (this.drawables == null) {
        this.downloadDrawables(offsetx, offsety, radius, false, null);
    }

    var date = new Date();
    var now = date.getHours();
    if (now > 12) { now -= 12; }
    now = now/12.0 + date.getMinutes()/12.0/60.0 + date.getSeconds()/12.0/60.0/60.0;

    var angle = -2.0*Math.PI * now;
    this.clockHand = [];
    for (var i in this.clockHandOriginal) {
        var drawable = this.clockHandOriginal[i];
        var drawable2 = {};

        if (drawable["type"] == "polygon") {
            var d2 = [];
            for (var di in drawable["d"]) {
                var di2 = drawable["d"][di].slice(0);
                var x = drawable["d"][di][0];
                var y = drawable["d"][di][1];
                di2[0] = Math.cos(angle)*x - Math.sin(angle)*y;
                di2[1] = Math.sin(angle)*x + Math.cos(angle)*y;
                d2.push(di2);
            }
            drawable2["type"] = "polygon";
            drawable2["d"] = d2;
            drawable2["strokeStyle"] = drawable["strokeStyle"];
            drawable2["fillStyle"] = drawable["fillStyle"];
            drawable2["lineWidth"] = drawable["lineWidth"];

            this.clockHand.push(drawable2);
        }
        else if (drawable["type"] == "text") {
            var ax = drawable["ax"];
            var ay = drawable["ay"];
            var upx = drawable["upx"];
            var upy = drawable["upy"];

            drawable2["ax"] = Math.cos(angle)*ax - Math.sin(angle)*ay;
            drawable2["ay"] = Math.sin(angle)*ax + Math.cos(angle)*ay;
            drawable2["upx"] = Math.cos(angle)*upx - Math.sin(angle)*upy;
            drawable2["upy"] = Math.sin(angle)*upx + Math.cos(angle)*upy;

            drawable2["type"] = "text";
            drawable2["d"] = drawable["d"];
            drawable2["textBaseline"] = drawable["textBaseline"];
            drawable2["textAlign"] = drawable["textAlign"];
            drawable2["fillStyle"] = drawable["fillStyle"];

            this.clockHand.push(drawable2);
        }
    }

    this.which = 0;
    this.i = 0;
}

HyperbolicMapClock.prototype.nextDrawable = function() {
    if (this.which == 0  &&  this.i >= this.drawables.length) {
        this.which = 1;
        this.i = 0;
    }
    if (this.which == 0) {
        return this.drawables[this.i++];
    }
    else {
        return this.clockHand[this.i++];
    }
}

function init() {
    var clockHand = [];
\n""")

for i in xrange(12):
    angle = -2.*math.pi/12. * ((i - 2) % 12)
    x1, y1 = 1.0*math.cos(angle), 1.0*math.sin(angle)
    x2, y2 = 1.1*math.cos(angle), 1.1*math.sin(angle)
    x3, y3 = 1.2*math.cos(angle), 1.2*math.sin(angle)
    x4, y4 = 1.5*math.cos(angle), 1.5*math.sin(angle)
    dbtmp.write("""{"type": "polygon", "d": [[%.18e, %.18e, "L"], [%.18e, %.18e]]}\n""" % (x1, y1, x2, y2))
    dbtmp.write("""{"type": "text", "d": "%d", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#000000"}\n""" % (i+1, x3, y3, x4, y4))

for i in xrange(12*60):
    angle = -2.*math.pi/12.0/60.0 * ((i - 2*60) % (12*60))
    x1, y1 = 3.2*math.cos(angle), 3.2*math.sin(angle)
    x2, y2 = 3.3*math.cos(angle), 3.3*math.sin(angle)
    x3, y3 = 3.4*math.cos(angle), 3.4*math.sin(angle)
    x4, y4 = 3.7*math.cos(angle), 3.7*math.sin(angle)
    dbtmp.write("""{"type": "polygon", "d": [[%.18e, %.18e, "L"], [%.18e, %.18e]]}\n""" % (x1, y1, x2, y2))
    dbtmp.write("""{"type": "text", "d": "%d", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#000000"}\n""" % (i % 60, x3, y3, x4, y4))

for i in xrange(12*60*60):
    angle = -2.*math.pi/12.0/60.0/60.0 * ((i - 3*60*60) % (12*60*60))
    x1, y1 = 25.0*math.cos(angle), 25.0*math.sin(angle)
    x2, y2 = 27.0*math.cos(angle), 27.0*math.sin(angle)
    x3, y3 = 28.0*math.cos(angle), 28.0*math.sin(angle)
    x4, y4 = 31.0*math.cos(angle), 31.0*math.sin(angle)
    dbtmp.write("""{"type": "polygon", "d": [[%.18e, %.18e, "L"], [%.18e, %.18e]]}\n""" % (x1, y1, x2, y2))
    dbtmp.write("""{"type": "text", "d": "%d", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#000000"}\n""" % (i % 60, x3, y3, x4, y4))

html.write("""    clockHand.push({"type": "polygon", "d": [[0.0, 0.01673111, "L"], [0.0, 0.6], [0.0, 0.9, "L"], [0.0, 1.75], [0.0, 2.55, "L"], [0.0, 15.0], [0.0, 22.0, "L"], [0.0, 36.0]], "strokeStyle": "#990000", "lineWidth": 3.0});\n""")

html.write("""    clockHand.push({"type": "polygon", "d": [[0.05, -0.03314517, "L"], [0.0452134, -0.05452093, "L"], [0.03358215, -0.07018942, "L"], [0.01898142, -0.07941633, "L"], [0.0, -0.08314517, "L"], [-0.02001435, -0.07897846, "L"], [-0.03323666, -0.07049991, "L"], [-0.0444685, -0.05602747, "L"], [-0.05, -0.03314517, "L"], [-0.04499175, -0.01130758, "L"], [-0.03584449, 0.0017142, "L"], [-0.02073447, 0.01236639, "L"], [0.0, 0.01685483, "L"], [0.02542647, 0.0099162, "L"], [0.03827542, -0.000972107, "L"], [0.04723795, -0.01671535, "L"]], "strokeStyle": "#990000", "lineWidth": 3.0});\n""")

x1, y1 = poincareDisk_to_hyperShadow(*internalToScreen( 0.0, 0.0, 0.0, 0.75, 0.0))
x2, y2 = poincareDisk_to_hyperShadow(*internalToScreen(-0.1, 0.0, 0.0, 0.75, 0.0))
html.write("""    clockHand.push({"type": "text", "d": "hour", "textBaseline": "middle", "textAlign": "center", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#990000"});""" % (x1, y1, x2, y2))

x1, y1 = poincareDisk_to_hyperShadow(*internalToScreen( 0.0, 0.0, 0.0, 2.1, 0.0))
x2, y2 = poincareDisk_to_hyperShadow(*internalToScreen(-0.1, 0.0, 0.0, 2.1, 0.0))
html.write("""    clockHand.push({"type": "text", "d": "minute", "textBaseline": "middle", "textAlign": "center", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#990000"});""" % (x1, y1, x2, y2))

x1, y1 = poincareDisk_to_hyperShadow(*internalToScreen( 0.0, 0.0, 0.0, 18.0, 0.0))
x2, y2 = poincareDisk_to_hyperShadow(*internalToScreen(-0.1, 0.0, 0.0, 18.0, 0.0))
html.write("""    clockHand.push({"type": "text", "d": "second", "textBaseline": "middle", "textAlign": "center", "ax": %.18e, "ay": %.18e, "upx": %.18e, "upy": %.18e, "fillStyle": "#990000"});""" % (x1, y1, x2, y2))

x1, y1 = poincareDisk_to_hyperShadow(*internalToScreen(-0.04848732,    -0.12473479, 0.0, 36.0, 0.0))
x2, y2 = poincareDisk_to_hyperShadow(*internalToScreen( 0.00050508,     0.05002161, 0.0, 36.0, 0.0))
x3, y3 = poincareDisk_to_hyperShadow(*internalToScreen( 0.05101271,    -0.12473479, 0.0, 36.0, 0.0))
x4, y4 = poincareDisk_to_hyperShadow(*internalToScreen( 0.00088688396, -0.07548339, 0.0, 36.0, 0.0))
html.write("""    clockHand.push({"type": "polygon", "d": [[%.18e, %.18e, "L"], [%.18e, %.18e, "L"], [%.18e, %.18e, "L"], [%.18e, %.18e, "L"]], "strokeStyle": "none", "fillStyle": "#990000"});""" % (x1, y1, x2, y2, x3, y3, x4, y4))

html.write("""

    hyperbolicMapService = new HyperbolicMapClock("get_clock", clockHand);
    hyperbolicViewport = new HyperbolicViewport(hyperbolicMapService, "hyperbolicViewport", 640, 640, {"allowZoom": false, "initialZoom": 0.95, "minZoom": 0.95, "maxZoom": 0.95, "viewThreshold": 0.98});

    hyperbolicViewport.updateTime = function() {
        this.draw();
        var _this = this;
        this.timer = setInterval(function() { _this.updateTime(); }, 1000);
    }
    hyperbolicViewport.updateTime();
}

</script>
<body onload="init();">
<div id="hyperbolicViewport" style="margin: 20px;"></div>
</body>
</html>
\n""")
