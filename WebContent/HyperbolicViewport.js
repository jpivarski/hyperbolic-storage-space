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
        this.font = "14pt sans-serif";
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
                   "grid": new HyperbolicStyleClass("none", "#538bf5"),
                   "gridText": new HyperbolicStyleClass("#538bf5", "none")
                  };

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
                   "grid": new HyperbolicStyleClass("none", "#538bf5"),
                   "gridText": new HyperbolicStyleClass("#538bf5", "none")
                  };
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
    this.VIEW_THRESHOLD = 0.95;
    this.DOWNLOAD_THRESHOLD = 0.97;
    this.FONT_SCALE = 0.05;
    this.MIN_TEXT_SIZE = 0.5;   // 1.0 for limited browsers

    this.options = {};
    for (prop in this.defaultOptions) {
        this.options[prop] = this.defaultOptions[prop];
    }
    if (options != null) {
        for (prop in options) {
            this.options[prop] = options[prop];
        }
    }

    this.offsetReal = 0.0;
    this.offsetImag = 0.0;
    this.zoom = 0.95;
    this.rotation = 0.0;

    this.offsetRealNow = this.offsetReal;
    this.offsetImagNow = this.offsetImag;
    this.zoomNow = this.zoom;
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

    if (this.options["backgroundImage"] == null) {
        this.backgroundImage == null;
    }
    else if (typeof this.options["backgroundImage"] == "string") {
        this.backgroundImage = new Image();
        this.backgroundImage.src = this.options["backgroundImage"];
    }
    else {
        this.backgroundImage = this.options["backgroundImage"];
    }

    if (this.options["shellImage"] == null) {
        this.shellImage = null;
    }
    else if (typeof this.options["shellImage"] == "string") {
        this.shellImage = new Image();
        this.shellImage.src = this.options["shellImage"];
    }
    else {
        this.shellImage = this.options["shellImage"];
    }

    this.draw();
    if (this.backgroundImage != null  &&  !this.backgroundImage.complete) {
        this.backgroundImage.onload = function(hyperbolicViewport) { return function() { hyperbolicViewport.draw(); } }(this);
    }
    if (this.shellImage != null  &&  !this.shellImage.complete) {
        this.shellImage.onload = function(hyperbolicViewport) { return function() { hyperbolicViewport.draw(); } }(this);
    }

    this.isMouseScrolling = false;
    this.isMouseRotating = false;
    this.isTwoFingerTransformation = false;
    this.finger1Id = null;
    this.finger1Real = null;
    this.finger1Imag = null;
    this.finger2Id = null;
    this.finger2Real = null;
    this.finger2Imag = null;
    this.fingersAngle = null;
    this.fingersSeparation = null;

    this.canvas.addEventListener("mousedown", function(hyperbolicViewport) { return function(event) {
        var tmp = hyperbolicViewport.mousePosition(event);
        var x = tmp[0];
        var y = tmp[1];

        var rad2 = x*x + y*y;
        if (rad2 < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
            hyperbolicViewport.finger1Real = x/Math.sqrt(1.0 - x*x - y*y);
            hyperbolicViewport.finger1Imag = y/Math.sqrt(1.0 - x*x - y*y);
            hyperbolicViewport.isMouseScrolling = true;
        }
        else if (rad2 < 1.0) {
            hyperbolicViewport.finger1Real = x;
            hyperbolicViewport.finger1Imag = y;
            hyperbolicViewport.isMouseRotating = true;
        }

    }; }(this));

    this.canvas.addEventListener("mousemove", function(hyperbolicViewport) { return function(event) {
        if (hyperbolicViewport.isMouseScrolling) {
            var tmp = hyperbolicViewport.mousePosition(event);
            var x = tmp[0];
            var y = tmp[1];
            if (x*x + y*y < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
                hyperbolicViewport.updateOffset(x, y);
            }
        }

        else if (hyperbolicViewport.isMouseRotating) {
            var tmp = hyperbolicViewport.mousePosition(event);
            var x = tmp[0];
            var y = tmp[1];
            hyperbolicViewport.updateRotation(x, y);
        }

    }; }(this));

    this.canvas.addEventListener("mouseup", function(hyperbolicViewport) { return function(event) {
        hyperbolicViewport.offsetReal = hyperbolicViewport.offsetRealNow;
        hyperbolicViewport.offsetImag = hyperbolicViewport.offsetImagNow;
        hyperbolicViewport.zoom = hyperbolicViewport.zoomNow;
        hyperbolicViewport.rotation = hyperbolicViewport.rotationNow;
        hyperbolicViewport.isMouseScrolling = false;
        hyperbolicViewport.isMouseRotating = false;
        hyperbolicViewport.finger1Id = null;
        hyperbolicViewport.finger1Real = null;
        hyperbolicViewport.finger1Imag = null;
        hyperbolicViewport.finger2Id = null;
        hyperbolicViewport.finger2Real = null;
        hyperbolicViewport.finger2Imag = null;
        hyperbolicViewport.fingersAngle = null;
        hyperbolicViewport.fingersSeparation = null;

        hyperbolicViewport.service.downloadDrawables(hyperbolicViewport.offsetReal, hyperbolicViewport.offsetImag, hyperbolicViewport.DOWNLOAD_THRESHOLD, true, hyperbolicViewport);

    }; }(this));

    this.canvas.addEventListener("touchstart", function(hyperbolicViewport) { return function(event) {
        event.preventDefault();
        if (event.targetTouches.length == 1  &&  event.changedTouches.length == 1) {
            var tmp = hyperbolicViewport.fingerPosition(event.targetTouches[0]);
            var x = tmp[0];
            var y = tmp[1];

            var rad2 = x*x + y*y;
            if (rad2 < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
                hyperbolicViewport.finger1Id = event.targetTouches[0].identifier;
                hyperbolicViewport.finger1Real = x/Math.sqrt(1.0 - x*x - y*y);
                hyperbolicViewport.finger1Imag = y/Math.sqrt(1.0 - x*x - y*y);
                hyperbolicViewport.isMouseScrolling = true;
            }
        }
        else if (hyperbolicViewport.isMouseScrolling  &&  event.targetTouches.length == 2) {
            var tmp = hyperbolicViewport.fingerPosition(event.changedTouches[0]);
            var x2 = tmp[0];
            var y2 = tmp[1];

            var oldtouch = null;
            if (event.targetTouches[0].identifier != event.changedTouches[0].identifier) {
                oldtouch = event.targetTouches[0];
            }
            else {
                oldtouch = event.targetTouches[1];
            }
            tmp = hyperbolicViewport.fingerPosition(oldtouch);
            var x1 = tmp[0];
            var y1 = tmp[1];

            var rad2_1 = x1*x1 + y1*y1;
            var rad2_2 = x2*x2 + y2*y2;
            if (rad2_1 < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD  &&  rad2_2 < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
                hyperbolicViewport.offsetReal = hyperbolicViewport.offsetRealNow;
                hyperbolicViewport.offsetImag = hyperbolicViewport.offsetImagNow;
                hyperbolicViewport.zoom = hyperbolicViewport.zoomNow;
                hyperbolicViewport.rotation = hyperbolicViewport.rotationNow;

                hyperbolicViewport.finger1Real = x1/Math.sqrt(1.0 - x1*x1 - y1*y1);
                hyperbolicViewport.finger1Imag = y1/Math.sqrt(1.0 - x1*x1 - y1*y1);
                
                hyperbolicViewport.finger2Id = event.changedTouches[0].identifier;
                hyperbolicViewport.finger2Real = x2/Math.sqrt(1.0 - x2*x2 - y2*y2);
                hyperbolicViewport.finger2Imag = y2/Math.sqrt(1.0 - x2*x2 - y2*y2);

                hyperbolicViewport.fingersAngle = Math.atan2(y1 - y2, x1 - x2);
                hyperbolicViewport.fingersSeparation = Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));

                hyperbolicViewport.isMouseScrolling = false;
                hyperbolicViewport.isTwoFingerTransformation = true;
            }
        }
        else if (event.targetTouches.length == 2  &&  event.changedTouches.length == 2) {
            var tmp = hyperbolicViewport.fingerPosition(event.changedTouches[0]);
            var x1 = tmp[0];
            var y1 = tmp[1];
            tmp = hyperbolicViewport.fingerPosition(event.changedTouches[1]);
            var x2 = tmp[0];
            var y2 = tmp[1];

            var rad2_1 = x1*x1 + y1*y1;
            var rad2_2 = x2*x2 + y2*y2;
            if (rad2_1 < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD  &&  rad2_2 < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
                hyperbolicViewport.finger1Id = event.changedTouches[0].identifier;
                hyperbolicViewport.finger1Real = x1/Math.sqrt(1.0 - x1*x1 - y1*y1);
                hyperbolicViewport.finger1Imag = y1/Math.sqrt(1.0 - x1*x1 - y1*y1);
                hyperbolicViewport.finger2Id = event.changedTouches[1].identifier;
                hyperbolicViewport.finger2Real = x2/Math.sqrt(1.0 - x2*x2 - y2*y2);
                hyperbolicViewport.finger2Imag = y2/Math.sqrt(1.0 - x2*x2 - y2*y2);

                hyperbolicViewport.fingersAngle = Math.atan2(y1 - y2, x1 - x2);
                hyperbolicViewport.fingersSeparation = Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));

                hyperbolicViewport.isTwoFingerTransformation = true;
            }
        }
    }; }(this));

    this.canvas.addEventListener("touchmove", function(hyperbolicViewport) { return function(event) {
        event.preventDefault();
        if (hyperbolicViewport.isMouseScrolling  &&  event.targetTouches.length == 1  &&  event.changedTouches.length == 1) {
            var tmp = hyperbolicViewport.fingerPosition(event.targetTouches[0]);
            var x = tmp[0];
            var y = tmp[1];
            if (x*x + y*y < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
                hyperbolicViewport.updateOffset(x, y);
            }
        }
        if (hyperbolicViewport.isTwoFingerTransformation  &&  event.targetTouches.length == 2) {
            var touch1 = null;
            var touch2 = null;
            if (event.targetTouches[0].identifier == hyperbolicViewport.finger1Id) {
                touch1 = event.targetTouches[0];
            }
            else if (event.targetTouches[1].identifier == hyperbolicViewport.finger1Id) {
                touch1 = event.targetTouches[1];
            }
            if (event.targetTouches[0].identifier == hyperbolicViewport.finger2Id) {
                touch2 = event.targetTouches[0];
            }
            else if (event.targetTouches[1].identifier == hyperbolicViewport.finger2Id) {
                touch2 = event.targetTouches[1];
            }
            if (touch1 != null  &&  touch2 != null) {
                var tmp = hyperbolicViewport.fingerPosition(touch1);
                var x1 = tmp[0];
                var y1 = tmp[1];
                tmp = hyperbolicViewport.fingerPosition(touch2);
                var x2 = tmp[0];
                var y2 = tmp[1];
                if (x1*x1 + y1*y1 < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD  &&  x2*x2 + y2*y2 < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
                    hyperbolicViewport.updateTransformation(x1, y1, x2, y2);
                }
            }
        }
    }; }(this));

    this.canvas.addEventListener("touchend", function(hyperbolicViewport) { return function(event) {
        event.preventDefault();
        if (event.targetTouches.length == 0) {
            hyperbolicViewport.offsetReal = hyperbolicViewport.offsetRealNow;
            hyperbolicViewport.offsetImag = hyperbolicViewport.offsetImagNow;
            hyperbolicViewport.zoom = hyperbolicViewport.zoomNow;
            hyperbolicViewport.rotation = hyperbolicViewport.rotationNow;
            hyperbolicViewport.isMouseScrolling = false;
            hyperbolicViewport.isTwoFingerTransformation = false;
            hyperbolicViewport.finger1Id = null;
            hyperbolicViewport.finger1Real = null;
            hyperbolicViewport.finger1Imag = null;
            hyperbolicViewport.finger2Id = null;
            hyperbolicViewport.finger2Real = null;
            hyperbolicViewport.finger2Imag = null;
            hyperbolicViewport.fingersAngle = null;
            hyperbolicViewport.fingersSeparation = null;

            hyperbolicViewport.service.downloadDrawables(hyperbolicViewport.offsetReal, hyperbolicViewport.offsetImag, hyperbolicViewport.DOWNLOAD_THRESHOLD, true, hyperbolicViewport);
        }

        else if (event.targetTouches.length == 1) {
            var tmp = hyperbolicViewport.fingerPosition(event.targetTouches[0]);
            var x = tmp[0];
            var y = tmp[1];

            var rad2 = x*x + y*y;
            if (rad2 < hyperbolicViewport.VIEW_THRESHOLD*hyperbolicViewport.VIEW_THRESHOLD) {
                hyperbolicViewport.offsetReal = hyperbolicViewport.offsetRealNow;
                hyperbolicViewport.offsetImag = hyperbolicViewport.offsetImagNow;
                hyperbolicViewport.zoom = hyperbolicViewport.zoomNow;
                hyperbolicViewport.rotation = hyperbolicViewport.rotationNow;

                hyperbolicViewport.finger1Id = event.targetTouches[0].identifier;
                hyperbolicViewport.finger1Real = x/Math.sqrt(1.0 - x*x - y*y);
                hyperbolicViewport.finger1Imag = y/Math.sqrt(1.0 - x*x - y*y);

                hyperbolicViewport.isMouseScrolling = true;
                hyperbolicViewport.isTwoFingerTransformation = false;
            }
        }
    }; }(this));
}

HyperbolicViewport.prototype.defaultOptions = {"allowZoom": true, "allowRotate": true, "minZoom": 0.5, "maxZoom": null, "rimStrokeStyle": "#000000", "rimFillStyle": "#f5d6ab", "backgroundColor": "#ffffff", "backgroundImage": null, "shellImage": null, "shellImageScale": 1.0};

HyperbolicViewport.prototype.mousePosition = function(event) {
    var shiftx = this.canvas.width/2.0;
    var shifty = this.canvas.height/2.0;
    var scale = this.zoom*this.canvas.width/2.0;

    return [(event.pageX - this.canvas.offsetLeft - shiftx)/scale,
            -(event.pageY - this.canvas.offsetTop - shifty)/scale];
}

HyperbolicViewport.prototype.fingerPosition = function(touch) {
    var shiftx = this.canvas.width/2.0;
    var shifty = this.canvas.height/2.0;
    var scale = this.zoom*this.canvas.width/2.0;

    return [(touch.pageX - this.canvas.offsetLeft - shiftx)/scale,
            -(touch.pageY - this.canvas.offsetTop - shifty)/scale];
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

HyperbolicViewport.prototype.updateCoordinates = function(Fr, Fi, Pr, Pi, Rr, Ri) {
    var pone = Math.sqrt(Pr*Pr + Pi*Pi + 1.0);

    // compute a new offset (dBr,dBi) assuming that the initial offset was zero: this is a change in offset
    var dBr = -(Fi*Pr + Fr*Pi)*(-Fi*pone + Pi - (Fi*Pr + Fr*Pi)*(-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone))/((-Fi*Pi + Fr*Pr - pone)*(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)*(Fi*Pr + Fr*Pi)/(-Fi*Pi + Fr*Pr - pone) - pone)) + (-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone);
    var dBi = (-Fi*pone + Pi - (Fi*Pr + Fr*Pi)*(-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone))/(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)*(Fi*Pr + Fr*Pi)/(-Fi*Pi + Fr*Pr - pone) - pone);

    // NOTE: loss of precision for large |(dBr,dBi)| values
    var dBoneMinus = Math.sqrt(1.0 - dBr*dBr - dBi*dBi);
    dBr = dBr/dBoneMinus;
    dBi = dBi/dBoneMinus;

    var Br = this.offsetReal;
    var Bi = this.offsetImag;

    var dBone = Math.sqrt(1.0 + dBr*dBr + dBi*dBi);
    var Bone = Math.sqrt(1.0 + Br*Br + Bi*Bi);
    var real = -Bi*Bi*Ri*dBi*dBone - Bi*Bi*Rr*dBr*dBone - 2.0*Bi*Br*Ri*dBr*dBone + 2.0*Bi*Br*Rr*dBi*dBone + Br*Br*Ri*dBi*dBone + Br*Br*Rr*dBr*dBone + Br*Ri*Ri*Bone*dBone*dBone + Br*Rr*Rr*Bone*dBone*dBone + Br*dBi*dBi*Bone + Br*dBr*dBr*Bone + Ri*dBi*Bone*Bone*dBone + Rr*dBr*Bone*Bone*dBone;
    var imag = -Bi*Bi*Ri*dBr*dBone + Bi*Bi*Rr*dBi*dBone + 2.0*Bi*Br*Ri*dBi*dBone + 2.0*Bi*Br*Rr*dBr*dBone + Bi*Ri*Ri*Bone*dBone*dBone + Bi*Rr*Rr*Bone*dBone*dBone + Bi*dBi*dBi*Bone + Bi*dBr*dBr*Bone + Br*Br*Ri*dBr*dBone - Br*Br*Rr*dBi*dBone - Ri*dBr*Bone*Bone*dBone + Rr*dBi*Bone*Bone*dBone;
    var denom = Bi*Bi*dBi*dBi + Bi*Bi*dBr*dBr - 2.0*Bi*Ri*dBr*Bone*dBone + 2.0*Bi*Rr*dBi*Bone*dBone + Br*Br*dBi*dBi + Br*Br*dBr*dBr + 2.0*Br*Ri*dBi*Bone*dBone + 2.0*Br*Rr*dBr*Bone*dBone + Ri*Ri*Bone*Bone*dBone*dBone + Rr*Rr*Bone*Bone*dBone*dBone;
    denom = Math.sqrt(denom*denom - real*real - imag*imag);

    this.offsetRealNow = real/denom;
    this.offsetImagNow = imag/denom;

    real = -2.0*Bi*Bi*Ri*dBi*dBr + Bi*Bi*Rr*dBi*dBi - Bi*Bi*Rr*dBr*dBr + 2.0*Bi*Br*Ri*dBi*dBi - 2.0*Bi*Br*Ri*dBr*dBr + 4.0*Bi*Br*Rr*dBi*dBr + Bi*Ri*Ri*dBi*Bone*dBone + Bi*Rr*Rr*dBi*Bone*dBone + Bi*dBi*Bone*dBone + 2.0*Br*Br*Ri*dBi*dBr - Br*Br*Rr*dBi*dBi + Br*Br*Rr*dBr*dBr + Br*Ri*Ri*dBr*Bone*dBone + Br*Rr*Rr*dBr*Bone*dBone + Br*dBr*Bone*dBone + Rr*Bone*Bone*dBone*dBone;
    imag = -Bi*Bi*Ri*dBi*dBi + Bi*Bi*Ri*dBr*dBr - 2.0*Bi*Bi*Rr*dBi*dBr - 4.0*Bi*Br*Ri*dBi*dBr + 2.0*Bi*Br*Rr*dBi*dBi - 2.0*Bi*Br*Rr*dBr*dBr - Bi*Ri*Ri*dBr*Bone*dBone - Bi*Rr*Rr*dBr*Bone*dBone - Bi*dBr*Bone*dBone + Br*Br*Ri*dBi*dBi - Br*Br*Ri*dBr*dBr + 2.0*Br*Br*Rr*dBi*dBr + Br*Ri*Ri*dBi*Bone*dBone + Br*Rr*Rr*dBi*Bone*dBone + Br*dBi*Bone*dBone + Ri*Bone*Bone*dBone*dBone;
    this.rotationNow = Math.atan2(imag, real);
}

HyperbolicViewport.prototype.updateOffset = function(x, y) {
    this.updateCoordinates(x, y, hyperbolicViewport.finger1Real, hyperbolicViewport.finger1Imag, Math.cos(hyperbolicViewport.rotation), Math.sin(hyperbolicViewport.rotation));
    this.draw();
}

HyperbolicViewport.prototype.updateRotation = function(x, y) {
    var oldphi = Math.atan2(this.finger1Imag, this.finger1Real);
    var newphi = Math.atan2(y, x);

    this.rotationNow = (newphi - oldphi) + this.rotation;

    this.draw();
}

HyperbolicViewport.prototype.updateTransformation = function(x1, y1, x2, y2) {
    var centerx = (this.finger1Real + this.finger2Real)/2.0;
    var centery = (this.finger1Imag + this.finger2Imag)/2.0;

    var scale = 1.;
    var angle = 0.;
    if (this.options["allowZoom"]) {
        scale = Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2)) / this.fingersSeparation;
    }
    if (this.options["allowRotate"]) {
        angle = Math.atan2(y1 - y2, x1 - x2) - this.fingersAngle;
    }

    if (this.options["minZoom"] != null) {
        if (scale * this.zoom < this.options["minZoom"]) {
            scale = this.options["minZoom"] / this.zoom;
        }
    }
    if (this.options["maxZoom"] != null) {
        if (scale * this.zoom > this.options["maxZoom"]) {
            scale = this.options["maxZoom"] / this.zoom;
        }
    }

    var centerxPrime = scale*(Math.cos(angle)*centerx - Math.sin(angle)*centery);
    var centeryPrime = scale*(Math.sin(angle)*centerx + Math.cos(angle)*centery);

    this.zoomNow = scale * this.zoom;
    this.updateCoordinates((x1 + x2)/2.0, (y1 + y2)/2.0, centerxPrime, centeryPrime, Math.cos(this.rotation + angle), Math.sin(this.rotation + angle));
    this.draw();
}

HyperbolicViewport.prototype.draw = function() {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    var VIEW_THRESHOLD2 = this.VIEW_THRESHOLD*this.VIEW_THRESHOLD;
    var MAX_STRAIGHT_LINE_LENGTH2 = this.MAX_STRAIGHT_LINE_LENGTH*this.MAX_STRAIGHT_LINE_LENGTH;

    var shiftx = this.canvas.width/2.0;
    var shifty = this.canvas.height/2.0;
    var scale = this.zoomNow*this.canvas.width/2.0;

    this.rotationCosNow = Math.cos(this.rotationNow);
    this.rotationSinNow = Math.sin(this.rotationNow);

    if (this.backgroundImage != null  &&  this.backgroundImage.complete) {
        if (2.0*scale < Math.sqrt(this.canvas.width*this.canvas.width + this.canvas.height*this.canvas.height)) {
            var width, height;
            if (this.canvas.width < this.canvas.height) {
                height = this.canvas.height;
                width = this.canvas.height * this.backgroundImage.width/this.backgroundImage.height;
            }
            else {
                width = this.canvas.width;
                height = this.canvas.width * this.backgroundImage.height/this.backgroundImage.width;
            }

            this.context.drawImage(this.backgroundImage, (this.canvas.width - width)/2.0, (this.canvas.height - height)/2.0, width, height);
        }        
    }

    if (this.shellImage != null  &&  this.shellImage.complete) {
        if (2.0*scale < Math.sqrt(this.canvas.width*this.canvas.width + this.canvas.height*this.canvas.height)) {
            var width = this.options["shellImageScale"]*this.zoomNow*this.canvas.width;
            var height = this.options["shellImageScale"]*this.zoomNow*this.canvas.width*this.shellImage.height/this.shellImage.width;

            this.context.translate(this.canvas.width/2.0, this.canvas.height/2.0);
            this.context.rotate(-this.rotationNow);
            this.context.drawImage(this.shellImage, -width/2.0, -height/2.0, width, height);
            this.context.rotate(this.rotationNow);
            this.context.translate(-this.canvas.width/2.0, -this.canvas.height/2.0);
        }
    }

    this.context.fillStyle = this.options["backgroundColor"];
    this.context.beginPath();
    this.context.arc(shiftx, shifty, scale, 0.0, 2.0*Math.PI);
    this.context.fill();

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
                var px = drawable["d"][j][0];
                var py = drawable["d"][j][1];
                var pc = Math.sqrt(1.0 + px*px + py*py);
                var tmp = this.internalToScreen(px, py, pc);
                var x1 = tmp[0];
                var y1 = tmp[1];

                var jnext = parseInt(j) + 1;
                if (j == drawable["d"].length - 1) { jnext = 0; }

                px = drawable["d"][jnext][0];
                py = drawable["d"][jnext][1];
                pc = Math.sqrt(1.0 + px*px + py*py);
                tmp = this.internalToScreen(px, py, pc);
                var x2 = tmp[0];
                var y2 = tmp[1];

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
                    points.push([x1*scale + shiftx, -y1*scale + shifty]);
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

                    var edge = ["a", cx*scale + shiftx, -cy*scale + shifty, Math.sqrt(r2)*scale, phi1, phi2, (deltaphi > 0)];
                    filledges.push(edge);
                    if (drawLine) {
                        drawedges.push(["m", x1*scale + shiftx, -y1*scale + shifty]);
                        drawedges.push(edge);
                    }
                } else {
                    var edge1 = ["m", x1*scale + shiftx, -y1*scale + shifty];
                    var edge2 = ["l", x2*scale + shiftx, -y2*scale + shifty];

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
            var px = drawable["ax"];
            var py = drawable["ay"];
            var pc = Math.sqrt(1.0 + px*px + py*py);
            var tmp = this.internalToScreen(px, py, pc);
            var ax = tmp[0];
            var ay = tmp[1];

            px = drawable["upx"];
            py = drawable["upy"];
            pc = Math.sqrt(1.0 + px*px + py*py);
            tmp = this.internalToScreen(px, py, pc);
            var upx = tmp[0];
            var upy = tmp[1];

            var size = scale * this.FONT_SCALE * Math.sqrt(Math.pow(upy - ay, 2) + Math.pow(upx - ax, 2));
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
                this.context.translate(ax*scale + shiftx, -ay*scale + shifty);
                this.context.rotate(-Math.atan2(upy - ay, upx - ax) + Math.PI/2.0);
                this.context.scale(size, size);
                this.context.fillText(drawable["d"], 0.0, 0.0);
                this.context.restore();
            }
        }
    }

    // draw the world-circle
    if (this.options["rimFillStyle"] != "none") {
        this.context.fillStyle = this.options["rimFillStyle"];
        this.context.beginPath();
        this.context.arc(shiftx, shifty, scale, 0.0, 2.0*Math.PI);
        this.context.arc(shiftx, shifty, this.VIEW_THRESHOLD*scale, 2.0*Math.PI, 0.0, true);
        this.context.fill();
    }

    if (this.options["rimStrokeStyle"] != "none") {
        this.context.strokeStyle = this.options["rimStrokeStyle"];
        this.context.beginPath();
        this.context.arc(shiftx, shifty, scale, 0.0, 2.0*Math.PI);
        this.context.stroke();
        this.context.beginPath();
        this.context.arc(shiftx, shifty, this.VIEW_THRESHOLD*scale, 2.0*Math.PI, 0.0, true);
        this.context.stroke();
    }
}
