//////////////////////////////////////////// style classes

function HyperbolicStyleClass(fillStyle, strokeStyle, lineWidth, pointRadius, pointFill, textAlign, textBaseline, font, lineCap, lineJoin, miterLimit) {
    if (fillStyle == null) {
        this.fillStyle = "none";
    } else {
        this.fillStyle = fillStyle;
    }

    if (strokeStyle == null) {
        this.strokeStyle = "#000000";
    } else {
        this.strokeStyle = strokeStyle;
    }

    if (lineWidth == null) {
        this.lineWidth = 1.0;
    } else {
        this.lineWidth = lineWidth;
    }

    if (pointRadius == null) {
        this.pointRadius = 3.5;
    } else {
        this.pointRadius = pointRadius;
    }

    if (pointFill == null) {
        this.pointFill = "#000000";
    } else {
        this.pointFill = pointFill;
    }

    if (textAlign == null) {
        this.textAlign = "center";
    } else {
        this.textAlign = textAlign;
    }

    if (textBaseline == null) {
        this.textBaseline = "alphabetic";
    } else {
        this.textBaseline = textBaseline;
    }

    if (font == null) {
        this.font = "10px sans-serif";
    } else {
        this.font = font;
    }

    if (lineCap == null) {
        this.lineCap = "butt";
    } else {
        this.lineCap = lineCap;
    }

    if (lineJoin == null) {
        this.lineJoin = "miter";
    } else {
        this.lineJoin = lineJoin;
    }

    if (miterLimit == null) {
        this.miterLimit = 10.0;
    } else {
        this.miterLimit = miterLimit;
    }
}

//////////////////////////////////////////// HyperbolicMapService -> HyperbolicMapServlet

function HyperbolicMapServlet(url) {
    if (url == null) {
        this.url = "get";
    } else {
        this.url = url;
    }

    this.styles = {"default": new HyperbolicStyleClass(),
                   "grid": new HyperbolicStyleClass("none", "#c7d4ed"),
                   "gridText": new HyperbolicStyleClass("#c7d4ed", "#c7d4ed")};

    this.drawables = null;
}

HyperbolicMapServlet.prototype.downloadDrawables = function(offsetx, offsety, radius, async, hyperbolicViewport) {
    var xmlhttp = new XMLHttpRequest();

    if (async) {
        xmlhttp.onreadystatechange = function(h) { return function() {
            if (xmlhttp.readyState == 4  &&  xmlhttp.status == 200) {
                h.drawables = JSON.parse(xmlhttp.responseText);
                if (hyperbolicViewport != null) { hyperbolicViewport.draw(); }
            }
        } }(this);
    }

    xmlhttp.open("GET", this.url + "?Bx=" + offsetx + "&By=" + offsety + "&a=" + radius, async);
    xmlhttp.send();

    if (!async) {
        this.drawables = JSON.parse(xmlhttp.responseText);
        if (hyperbolicViewport != null) { hyperbolicViewport.draw(); }
    }
}

HyperbolicMapServlet.prototype.beginDrawableLoop = function(offsetx, offsety, radius) {
    if (this.drawables == null) {
        this.downloadDrawables(offsetx, offsety, radius, false, null);
    }

    this.i = 0;
}

HyperbolicMapServlet.prototype.nextDrawable = function() {
    return this.drawables[this.i++];
}

//////////////////////////////////////////// HyperbolicMapService -> HyperbolicMapFromJSON

function HyperbolicMapFromJSON(data) {
    data = JSON.parse(data);

    this.drawables = data["drawables"];
    if (this.drawables == undefined) { this.drawables = []; }

    this.styles = {"default": new HyperbolicStyleClass(),
                   "grid": new HyperbolicStyleClass("none", "#c7d4ed"),
                   "gridText": new HyperbolicStyleClass("#c7d4ed", "#c7d4ed")};
}

HyperbolicMapFromJSON.prototype.downloadDrawables = function(offsetx, offsety, radius, async, hyperbolicViewport) { }

HyperbolicMapFromJSON.prototype.beginDrawableLoop = function(offsetx, offsety, radius) {
    this.i = 0;
}

HyperbolicMapFromJSON.prototype.nextDrawable = function() {
    return this.drawables[this.i++];
}

//////////////////////////////////////////// HyperbolicViewport

function HyperbolicViewport(service, elem, width, height, options) {
    this.MAX_STRAIGHT_LINE_LENGTH = 0.1;
    this.VIEW_THRESHOLD = 0.9;
    this.DOWNLOAD_THRESHOLD = 0.95;
    this.NUMERICAL_STABILITY_THRESHOLD = 100.0;
    this.FONT_SCALE = 20.0;
    this.MIN_TEXT_SIZE = 1.0;

    if (options == null) {
        this.options = {};
        for (prop in this.defaultOptions) {
            this.options[prop] = this.defaultOptions[prop];
        }
    } else {
        this.options = options;
    }

    this.offsetReal = 0.0;
    this.offsetImag = 0.0;
    this.zoom = 0.95;
    this.rotation = 0.0;

    this.offsetRealNow = this.offsetReal;
    this.offsetImagNow = this.offsetImag;
    this.zoomNow = 0.95;
    this.rotationNow = this.rotation;

    this.service = service;
    
    if (typeof elem == "string") {
        elem = document.getElementById(elem);
    }

    this.canvas = document.createElement("canvas");
    this.canvas.width = width;
    this.canvas.height = height;
    this.context = this.canvas.getContext("2d");
    this.context.strokeStyle = "#000000";
    this.context.fillStyle = "#000000";
    this.context.lineWidth = 1.5;

    elem.appendChild(this.canvas);
    this.draw();

    this.isMouseDown = false;
    this.finger1Real = null;
    this.finger1Imag = null;
    this.finger2Real = null;
    this.finger2Imag = null;

    document.addEventListener("mousedown", function(hyperbolicViewport) { return function(event) {
        event.preventDefault();
        var x, y;
        [x, y] = hyperbolicViewport.mousePosition(event);

        hyperbolicViewport.finger1Real = x/Math.sqrt(1.0 - x*x - y*y);
        hyperbolicViewport.finger1Imag = y/Math.sqrt(1.0 - x*x - y*y);

        if (x*x + y*y < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
            hyperbolicViewport.isMouseDown = true;
        }

    }; }(this));

    document.addEventListener("mousemove", function(hyperbolicViewport) { return function(event) {
        if (hyperbolicViewport.isMouseDown) {
            var x, y;
            [x, y] = hyperbolicViewport.mousePosition(event);
            if (x*x + y*y < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
                hyperbolicViewport.updateOffset(x, y);
            }
        }
    }; }(this));

    document.addEventListener("mouseup", function(hyperbolicViewport) { return function(event) {
        hyperbolicViewport.offsetReal = hyperbolicViewport.offsetRealNow;
        hyperbolicViewport.offsetImag = hyperbolicViewport.offsetImagNow;
        hyperbolicViewport.zoom = hyperbolicViewport.zoomNow;
        hyperbolicViewport.rotation = hyperbolicViewport.rotationNow;
        hyperbolicViewport.isMouseDown = false;

        hyperbolicViewport.service.downloadDrawables(hyperbolicViewport.offsetReal, hyperbolicViewport.offsetImag, hyperbolicViewport.DOWNLOAD_THRESHOLD, true, hyperbolicViewport);

    }; }(this));
}

HyperbolicViewport.prototype.defaultOptions = {"lineColor": "#000000", "rimColor": "#f5d6ab"};

HyperbolicViewport.prototype.mousePosition = function(event) {
    var shift = this.canvas.width/2.0;
    var scale = this.zoom*this.canvas.width/2.0;

    return [(event.pageX - this.canvas.offsetLeft - shift)/scale,
            -(event.pageY - this.canvas.offsetTop - shift)/scale];
}

HyperbolicViewport.prototype.internalToScreen = function(preal, pimag, pone) {
    var Br = this.offsetRealNow;
    var Bi = this.offsetImagNow;
    // NOTE: loss of precision for large |(Br,Bi)| values
    var bone = Math.sqrt(1.0 + Br*Br + Bi*Bi);
    var real = -Bi*Bi*preal*pone + 2.0*Bi*Br*pimag*pone + Br*Br*preal*pone + Br*pimag*pimag*bone + Br*preal*preal*bone + Br*bone*(pimag*pimag + preal*preal + 1.0) + preal*(Bi*Bi + Br*Br + 1.0)*pone;
    var imag = Bi*Bi*pimag*pone + 2.0*Bi*Br*preal*pone + Bi*pimag*pimag*bone + Bi*preal*preal*bone + Bi*bone*(pimag*pimag + preal*preal + 1.0) - Br*Br*pimag*pone + pimag*(Bi*Bi + Br*Br + 1.0)*pone;
    var denom = Bi*Bi*pimag*pimag + Bi*Bi*preal*preal + 2.0*Bi*pimag*bone*pone + Br*Br*pimag*pimag + Br*Br*preal*preal + 2.0*Br*preal*bone*pone + (Bi*Bi + Br*Br + 1.0)*(pimag*pimag + preal*preal + 1.0);

    real /= denom;
    imag /= denom;

    return [this.rotationCosNow*real - this.rotationSinNow*imag, this.rotationCosNow*imag + this.rotationSinNow*real];
}

HyperbolicViewport.prototype.updateOffset = function(Fr, Fi) {
    var Pr = this.finger1Real;
    var Pi = this.finger1Imag;
    var pone = Math.sqrt(Pr*Pr + Pi*Pi + 1.0);

    // compute a new offset (dBr,dBi) assuming that the initial offset was zero: this is a change in offset
    var dBr = -(Fi*Pr + Fr*Pi)*(-Fi*pone + Pi - (Fi*Pr + Fr*Pi)*(-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone))/((-Fi*Pi + Fr*Pr - pone)*(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)*(Fi*Pr + Fr*Pi)/(-Fi*Pi + Fr*Pr - pone) - pone)) + (-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone);
    var dBi = (-Fi*pone + Pi - (Fi*Pr + Fr*Pi)*(-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone))/(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)*(Fi*Pr + Fr*Pi)/(-Fi*Pi + Fr*Pr - pone) - pone);

    // NOTE: loss of precision for large |(dBr,dBi)| values
    var dBoneMinus = Math.sqrt(1.0 - dBr*dBr - dBi*dBi);
    [dBr, dBi] = [dBr/dBoneMinus, dBi/dBoneMinus];

    var Rr = Math.cos(this.rotation);
    var Ri = Math.sin(this.rotation);
    var Br = this.offsetReal;
    var Bi = this.offsetImag;

    var dBone = Math.sqrt(1.0 + dBr*dBr + dBi*dBi);
    var Bone = Math.sqrt(1.0 + Br*Br + Bi*Bi);
    var real = -Bi*Bi*Ri*dBi*dBone - Bi*Bi*Rr*dBr*dBone - 2.0*Bi*Br*Ri*dBr*dBone + 2.0*Bi*Br*Rr*dBi*dBone + Br*Br*Ri*dBi*dBone + Br*Br*Rr*dBr*dBone + Br*Ri*Ri*Bone*dBone*dBone + Br*Rr*Rr*Bone*dBone*dBone + Br*dBi*dBi*Bone + Br*dBr*dBr*Bone + Ri*dBi*Bone*Bone*dBone + Rr*dBr*Bone*Bone*dBone;
    var imag = -Bi*Bi*Ri*dBr*dBone + Bi*Bi*Rr*dBi*dBone + 2.0*Bi*Br*Ri*dBi*dBone + 2.0*Bi*Br*Rr*dBr*dBone + Bi*Ri*Ri*Bone*dBone*dBone + Bi*Rr*Rr*Bone*dBone*dBone + Bi*dBi*dBi*Bone + Bi*dBr*dBr*Bone + Br*Br*Ri*dBr*dBone - Br*Br*Rr*dBi*dBone - Ri*dBr*Bone*Bone*dBone + Rr*dBi*Bone*Bone*dBone;
    var denom = Bi*Bi*dBi*dBi + Bi*Bi*dBr*dBr - 2.0*Bi*Ri*dBr*Bone*dBone + 2.0*Bi*Rr*dBi*Bone*dBone + Br*Br*dBi*dBi + Br*Br*dBr*dBr + 2.0*Br*Ri*dBi*Bone*dBone + 2.0*Br*Rr*dBr*Bone*dBone + Ri*Ri*Bone*Bone*dBone*dBone + Rr*Rr*Bone*Bone*dBone*dBone;
    denom = Math.sqrt(denom*denom - real*real - imag*imag);

    var offsetRealNow = real/denom;
    var offsetImagNow = imag/denom;
    if (offsetRealNow*offsetRealNow + offsetImagNow*offsetImagNow < this.NUMERICAL_STABILITY_THRESHOLD*this.NUMERICAL_STABILITY_THRESHOLD) {
        this.offsetRealNow = offsetRealNow;
        this.offsetImagNow = offsetImagNow;
    }

    real = -2.0*Bi*Bi*Ri*dBi*dBr + Bi*Bi*Rr*dBi*dBi - Bi*Bi*Rr*dBr*dBr + 2.0*Bi*Br*Ri*dBi*dBi - 2.0*Bi*Br*Ri*dBr*dBr + 4.0*Bi*Br*Rr*dBi*dBr + Bi*Ri*Ri*dBi*Bone*dBone + Bi*Rr*Rr*dBi*Bone*dBone + Bi*dBi*Bone*dBone + 2.0*Br*Br*Ri*dBi*dBr - Br*Br*Rr*dBi*dBi + Br*Br*Rr*dBr*dBr + Br*Ri*Ri*dBr*Bone*dBone + Br*Rr*Rr*dBr*Bone*dBone + Br*dBr*Bone*dBone + Rr*Bone*Bone*dBone*dBone;
    imag = -Bi*Bi*Ri*dBi*dBi + Bi*Bi*Ri*dBr*dBr - 2.0*Bi*Bi*Rr*dBi*dBr - 4.0*Bi*Br*Ri*dBi*dBr + 2.0*Bi*Br*Rr*dBi*dBi - 2.0*Bi*Br*Rr*dBr*dBr - Bi*Ri*Ri*dBr*Bone*dBone - Bi*Rr*Rr*dBr*Bone*dBone - Bi*dBr*Bone*dBone + Br*Br*Ri*dBi*dBi - Br*Br*Ri*dBr*dBr + 2.0*Br*Br*Rr*dBi*dBr + Br*Ri*Ri*dBi*Bone*dBone + Br*Rr*Rr*dBi*Bone*dBone + Br*dBi*Bone*dBone + Ri*Bone*Bone*dBone*dBone;

    this.rotationNow = Math.atan2(imag, real);

    this.draw();
}

HyperbolicViewport.prototype.draw = function() {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    var VIEW_THRESHOLD2 = this.VIEW_THRESHOLD*this.VIEW_THRESHOLD;
    var MAX_STRAIGHT_LINE_LENGTH2 = this.MAX_STRAIGHT_LINE_LENGTH*this.MAX_STRAIGHT_LINE_LENGTH;

    var shift = this.canvas.width/2.0;
    var scale = this.zoom*this.canvas.width/2.0;

    this.rotationCosNow = Math.cos(this.rotationNow);
    this.rotationSinNow = Math.sin(this.rotationNow);

    this.service.beginDrawableLoop(this.offsetReal, this.offsetImag, this.DOWNLOAD_THRESHOLD);
    var drawable;
    while (drawable = this.service.nextDrawable()) {
        var styleClass = drawable["class"];
        if (styleClass == undefined) {
            styleClass = this.service.styles["default"];
        } else {
            styleClass = this.service.styles[styleClass];
        }

        if (drawable["type"] == "polygon") {
            var points = [];
            var filledges = [];
            var drawedges = [];
            var willDraw = false;

            for (var j in drawable["d"]) {
                var px, py, pc, x1, y1, x2, y2;

                px = drawable["d"][j][0];
                py = drawable["d"][j][1];
                pc = Math.sqrt(1.0 + px*px + py*py);
                [x1, y1] = this.internalToScreen(px, py, pc);

                var jnext = parseInt(j) + 1;
                if (j == drawable["d"].length - 1) { jnext = 0; }

                px = drawable["d"][jnext][0];
                py = drawable["d"][jnext][1];
                pc = Math.sqrt(1.0 + px*px + py*py);
                [x2, y2] = this.internalToScreen(px, py, pc);

                if (x1*x1 + y1*y1 < VIEW_THRESHOLD2  ||
                    x2*x2 + y2*y2 < VIEW_THRESHOLD2) {
                    willDraw = true;
                }

                var options = drawable["d"][j][2];
                if (options == undefined) {
                    options = "";
                } else {
                    options = options.toLowerCase();
                }

                var drawLine = (options.indexOf("l") != -1);
                if (options.indexOf("p") != -1) {
                    points.push([x1*scale + shift, -y1*scale + shift]);
                }

                var denom = x1*y2 - x2*y1;
                var dist2 = (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2);

                if (Math.abs(denom) > 1e-10  &&  dist2 > MAX_STRAIGHT_LINE_LENGTH2) {
                    var a = (-x1*x1*y2 + x2*x2*y1 - y1*y1*y2 + y1*y2*y2 + y1 - y2)/denom;
                    var b = (x1*x1*x2 - x1*x2*x2 - x1*y2*y2 - x1 + x2*y1*y1 + x2)/denom;
                    var cx = -0.5*a;
                    var cy = -0.5*b;
                    var r2 = -1 + 0.25*(a*a + b*b);
                    var phi1 = -Math.atan2(y1 - cy, x1 - cx);
                    var phi2 = -Math.atan2(y2 - cy, x2 - cx);

                    var deltaphi = phi1 - phi2;
                    while (deltaphi >= Math.PI) { deltaphi -= 2*Math.PI; }
                    while (deltaphi < -Math.PI) { deltaphi += 2*Math.PI; }

                    var edge = ["a", cx*scale + shift, -cy*scale + shift, Math.sqrt(r2)*scale, phi1, phi2, (deltaphi > 0)];
                    filledges.push(edge);
                    if (drawLine) {
                        drawedges.push(["m", x1*scale + shift, -y1*scale + shift]);
                        drawedges.push(edge);
                    }
                } else {
                    var edge1 = ["m", x1*scale + shift, -y1*scale + shift];
                    var edge2 = ["l", x2*scale + shift, -y2*scale + shift];

                    filledges.push(edge1);
                    filledges.push(edge2);
                    if (drawLine) {
                        drawedges.push(edge1);
                        drawedges.push(edge2);
                    }
                }
            }

            if (willDraw) {
                // clip the filling to the polygon
                var fillStyle = drawable["fillStyle"];
                if (fillStyle == undefined) { fillStyle = styleClass.fillStyle; }

                if (fillStyle != "none") {
                    this.context.save();
                    this.context.fillStyle = fillStyle;

                    this.context.beginPath();
                    for (var j in filledges) {
                        if (filledges[j][0] == "a") {
                            this.context.arc(filledges[j][1], filledges[j][2], filledges[j][3], filledges[j][4], filledges[j][5], filledges[j][6]);
                        } else if (filledges[j][0] == "l") {
                            this.context.lineTo(filledges[j][1], filledges[j][2]);
                        } else if (filledges[j][0] == "m") {
                            this.context.moveTo(filledges[j][1], filledges[j][2]);
                        }
                    }
                    this.context.clip();
                    
                    // fill the polygon
                    this.context.beginPath();
                    for (var j in filledges) {
                        if (filledges[j][0] == "a") {
                            this.context.arc(filledges[j][1], filledges[j][2], filledges[j][3], filledges[j][4], filledges[j][5], filledges[j][6]);
                        } else if (filledges[j][0] == "l") {
                            this.context.lineTo(filledges[j][1], filledges[j][2]);
                        } else if (filledges[j][0] == "m") {
                            this.context.moveTo(filledges[j][1], filledges[j][2]);
                        }
                    }
                    this.context.fill();
                    this.context.restore();
                }

                // draw a line around it
                this.context.save();

                var strokeStyle = drawable["strokeStyle"];
                if (strokeStyle == undefined) { strokeStyle = styleClass.strokeStyle; }
                this.context.strokeStyle = strokeStyle;

                var lineWidth = drawable["lineWidth"];
                if (lineWidth == undefined) { lineWidth = styleClass.lineWidth; }
                this.context.lineWidth = lineWidth;

                var lineCap = drawable["lineCap"];
                if (lineCap == undefined) { lineCap = styleClass.lineCap; }
                this.context.lineCap = lineCap;

                var lineJoin = drawable["lineJoin"];
                if (lineJoin == undefined) { lineJoin = styleClass.lineJoin; }
                this.context.lineJoin = lineJoin;

                var miterLimit = drawable["miterLimit"];
                if (miterLimit == undefined) { miterLimit = styleClass.miterLimit; }
                this.context.miterLimit = miterLimit;

                this.context.beginPath();
                for (var j in drawedges) {
                    if (drawedges[j][0] == "a") {
                        this.context.arc(drawedges[j][1], drawedges[j][2], drawedges[j][3], drawedges[j][4], drawedges[j][5], drawedges[j][6]);
                    } else if (drawedges[j][0] == "l") {
                        this.context.lineTo(drawedges[j][1], drawedges[j][2]);
                    } else if (drawedges[j][0] == "m") {
                        this.context.moveTo(drawedges[j][1], drawedges[j][2]);
                    }
                }
                this.context.stroke();
                this.context.restore();

                // draw the points
                this.context.save();

                var pointFill = drawable["pointFill"];
                if (pointFill == undefined) { pointFill = styleClass.pointFill; }
                this.context.fillStyle = pointFill;

                var pointRadius = drawable["pointFill"];
                if (pointRadius == undefined) { pointRadius = styleClass.pointRadius; }

                for (var j in points) {
                    this.context.beginPath();
                    this.context.arc(points[j][0], points[j][1], pointRadius, 0.0, 2*Math.PI);
                    this.context.fill();
                }

                this.context.restore();
            }
        }

        if (drawable["type"] == "text") {
            var px, py, pc, ax, ay, upx, upy;
            px = drawable["ax"];
            py = drawable["ay"];
            pc = Math.sqrt(1.0 + px*px + py*py);
            [ax, ay] = this.internalToScreen(px, py, pc);

            px = drawable["upx"];
            py = drawable["upy"];
            pc = Math.sqrt(1.0 + px*px + py*py);
            [upx, upy] = this.internalToScreen(px, py, pc);

            var size = this.FONT_SCALE * Math.sqrt(Math.pow(upy - ay, 2) + Math.pow(upx - ax, 2));
            if (size > this.MIN_TEXT_SIZE) {
                var fillStyle = drawable["fillStyle"];
                if (fillStyle == undefined) { fillStyle = styleClass.fillStyle; }
                this.context.fillStyle = fillStyle;

                var textAlign = drawable["textAlign"];
                if (textAlign == undefined) { textAlign = styleClass.textAlign; }
                this.context.textAlign = textAlign;

                var textBaseline = drawable["textBaseline"];
                if (textBaseline == undefined) { textBaseline = styleClass.textBaseline; }
                this.context.textBaseline = textBaseline;

                var font = drawable["font"];
                if (font == undefined) { font = styleClass.font; }
                this.context.font = font;

                this.context.save();
                this.context.translate(ax*scale + shift, -ay*scale + shift);
                this.context.rotate(-Math.atan2(upy - ay, upx - ax) + Math.PI/2.0);
                this.context.scale(size, size);
                this.context.fillText(drawable["d"], 0.0, 0.0);
                this.context.restore();
            }
        }
    }

    // draw the world-circle
    this.context.fillStyle = this.options["rimColor"];
    this.context.beginPath();
    this.context.arc(shift, shift, scale, 0.0, 2.0*Math.PI);
    this.context.arc(shift, shift, this.VIEW_THRESHOLD*scale, 2.0*Math.PI, 0.0, true);
    this.context.fill();

    this.context.strokeStyle = this.options["lineColor"];
    this.context.beginPath();
    this.context.arc(shift, shift, scale, 0.0, 2.0*Math.PI);
    this.context.stroke();
    this.context.beginPath();
    this.context.arc(shift, shift, this.VIEW_THRESHOLD*scale, 2.0*Math.PI, 0.0, true);
    this.context.stroke();
}
