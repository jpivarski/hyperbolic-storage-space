//////////////////////////////////////////// HyperbolicMappingService -> HyperbolicMapFromJSON

function HyperbolicMapFromJSON(data) {
    data = JSON.parse(data);

    this.drawables = data["drawables"];
    if (this.drawables == undefined) { this.drawables = []; }

    this.fillStyle = data["fillStyle"];
    if (this.fillStyle == undefined) { this.fillStyle = "none"; }

    this.strokeStyle = data["strokeStyle"];
    if (this.strokeStyle == undefined) { this.strokeStyle = "#000000"; }

    this.lineWidth = data["lineWidth"];
    if (this.lineWidth == undefined) { this.lineWidth = 1.0; }

    this.lineCap = data["lineCap"];
    if (this.lineCap == undefined) { this.lineCap = "butt"; }

    this.lineJoin = data["lineJoin"];
    if (this.lineJoin == undefined) { this.lineJoin = "miter"; }

    this.miterLimit = data["miterLimit"];
    if (this.miterLimit == undefined) { this.miterLimit = 10.0; }

    this.pointRadius = data["pointRadius"];
    if (this.pointRadius == undefined) { this.pointRadius = 3.5; }

    this.pointFill = data["pointFill"];
    if (this.pointFill == undefined) { this.pointFill = "#000000"; }

    for (var i in this.drawables) {
        if (this.drawables[i]["type"] == "polygon") {
            for (var j in this.drawables[i]["d"]) {
                this.convertPoint(this.drawables[i]["d"][j]);
            }
        }
    }
}

HyperbolicMapFromJSON.prototype.convertPoint = function(point) {
    // var x = point[0];
    // var y = point[1];

    // var r = Math.sqrt(x*x + y*y);
    // var sinhr = 0.5*(Math.exp(r/2.0) - Math.exp(-r/2.0));
    // var coshr = 0.5*(Math.exp(r/2.0) + Math.exp(-r/2.0));

    // if (r == 0.0) {
    //         point[0] = 0.0;
    //         point[1] = 0.0;
    // }
    // else {
    //         point[0] = sinhr*x/r;
    //         point[1] = sinhr*y/r;
    // }

    var eta = point[0];
    var phi = point[1];
    var sinhr = 0.5*(Math.exp(eta) - Math.exp(-eta));
    var coshr = 0.5*(Math.exp(eta) + Math.exp(-eta));

    point[0] = sinhr*Math.cos(phi);
    point[1] = sinhr*Math.sin(phi);

    point.splice(2, 0, coshr);
}

HyperbolicMapFromJSON.prototype.loadDrawables = function(offset, callback) {
    this.i = 0;
}

HyperbolicMapFromJSON.prototype.nextDrawable = function() {
    return this.drawables[this.i++];
}

//////////////////////////////////////////// HyperbolicViewport

function HyperbolicViewport(service, elem, width, height) {
    this.MAX_STRAIGHT_LINE_LENGTH = 0.1;
    this.THRESHOLD = 0.95;

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

        if (x*x + y*y < hyperbolicViewport.THRESHOLD*hyperbolicViewport.THRESHOLD) {
            hyperbolicViewport.isMouseDown = true;
        }

    }; }(this));

    document.addEventListener("mousemove", function(hyperbolicViewport) { return function(event) {
        if (hyperbolicViewport.isMouseDown) {
            var x, y;
            [x, y] = hyperbolicViewport.mousePosition(event);
            if (x*x + y*y < hyperbolicViewport.THRESHOLD*hyperbolicViewport.THRESHOLD) {
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
    }; }(this));
}

HyperbolicViewport.prototype.mousePosition = function(event) {
    var shift = this.canvas.width/2.0;
    var scale = this.zoom*this.canvas.width/2.0;

    return [(event.pageX - this.canvas.offsetLeft - shift)/scale,
            -(event.pageY - this.canvas.offsetTop - shift)/scale];
}

HyperbolicViewport.prototype.internalToScreen = function(preal, pimag, pone) {
    var Br = this.offsetRealNow;
    var Bi = this.offsetImagNow;

    // START EXPANDING B TO THE WHOLE PLANE
    // // compute a Mobius transformation composed with the internal -> screen transformation
    // // F = (P + B*sqrt(|P|^2 + 1))/(conj(B)*P + sqrt(|P|^2 + 1))
    // var real = -Bi*Bi*preal*pone + 2.0*Bi*Br*pimag*pone + Br*Br*preal*pone + Br*pimag*pimag + Br*preal*preal + Br*(pimag*pimag + preal*preal + 1.0) + preal*pone;
    // var imag = Bi*Bi*pimag*pone + 2.0*Bi*Br*preal*pone + Bi*pimag*pimag + Bi*preal*preal + Bi*(pimag*pimag + preal*preal + 1.0) - Br*Br*pimag*pone + pimag*pone;
    // var denom = Bi*Bi*pimag*pimag + Bi*Bi*preal*preal + 2.0*Bi*pimag*pone + Br*Br*pimag*pimag + Br*Br*preal*preal + 2.0*Br*preal*pone + pimag*pimag + preal*preal + 1.0;

    // F = ((1+|B|^2)*P + B*sqrt(|P|^2 + 1))/(conj(B)*P + (1+|B|^2)*sqrt(|P|^2 + 1))
    var bone = Math.sqrt(1.0 + Br*Br + Bi*Bi);
    var real = -Bi*Bi*preal*pone + 2.0*Bi*Br*pimag*pone + Br*Br*preal*pone + Br*pimag*pimag*bone + Br*preal*preal*bone + Br*bone*(pimag*pimag + preal*preal + 1.0) + preal*(Bi*Bi + Br*Br + 1.0)*pone;
    var imag = Bi*Bi*pimag*pone + 2.0*Bi*Br*preal*pone + Bi*pimag*pimag*bone + Bi*preal*preal*bone + Bi*bone*(pimag*pimag + preal*preal + 1.0) - Br*Br*pimag*pone + pimag*(Bi*Bi + Br*Br + 1.0)*pone;
    var denom = Bi*Bi*pimag*pimag + Bi*Bi*preal*preal + 2.0*Bi*pimag*bone*pone + Br*Br*pimag*pimag + Br*Br*preal*preal + 2.0*Br*preal*bone*pone + (Bi*Bi + Br*Br + 1.0)*(pimag*pimag + preal*preal + 1.0);
    // END EXPANDING B TO THE WHOLE PLANE

    real /= denom;
    imag /= denom;

    return [this.rotationCosNow*real - this.rotationSinNow*imag, this.rotationCosNow*imag + this.rotationSinNow*real];
}

HyperbolicViewport.prototype.updateOffset = function(Fr, Fi) {
    var Pr = this.finger1Real;
    var Pi = this.finger1Imag;
    var pone = Math.sqrt(Pr*Pr + Pi*Pi + 1.0);

    // compute a new offset (dBr, dBi) assuming that the initial offset was zero: this is a change in offset
    // F = (P + B*sqrt(|P|^2 + 1))/(conj(B)*P + sqrt(|P|^2 + 1)) solved for B (I used sympy)
    var dBr = -(Fi*Pr + Fr*Pi)*(-Fi*pone + Pi - (Fi*Pr + Fr*Pi)*(-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone))/((-Fi*Pi + Fr*Pr - pone)*(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)*(Fi*Pr + Fr*Pi)/(-Fi*Pi + Fr*Pr - pone) - pone)) + (-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone);
    var dBi = (-Fi*pone + Pi - (Fi*Pr + Fr*Pi)*(-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone))/(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)*(Fi*Pr + Fr*Pi)/(-Fi*Pi + Fr*Pr - pone) - pone);

    // START EXPANDING B TO THE WHOLE PLANE
    var dBoneMinus = Math.sqrt(1.0 - dBr*dBr - dBi*dBi);
    [dBr, dBi] = [dBr/dBoneMinus, dBi/dBoneMinus];
    // END EXPANDING B TO THE WHOLE PLANE

    var Rr = Math.cos(this.rotation);
    var Ri = Math.sin(this.rotation);
    var Br = this.offsetReal;
    var Bi = this.offsetImag;

    // START EXPANDING B TO THE WHOLE PLANE
    // // compose the old offset with the new offset
    // // Bprime = (dB + R*B)/(dB*conj(B) + R)
    // var real = -Bi*Bi*Ri*dBi - Bi*Bi*Rr*dBr - 2.0*Bi*Br*Ri*dBr + 2.0*Bi*Br*Rr*dBi + Br*Br*Ri*dBi + Br*Br*Rr*dBr + Br*Ri*Ri + Br*Rr*Rr + Br*dBi*dBi + Br*dBr*dBr + Ri*dBi + Rr*dBr;
    // var imag = -Bi*Bi*Ri*dBr + Bi*Bi*Rr*dBi + 2.0*Bi*Br*Ri*dBi + 2.0*Bi*Br*Rr*dBr + Bi*Ri*Ri + Bi*Rr*Rr + Bi*dBi*dBi + Bi*dBr*dBr + Br*Br*Ri*dBr - Br*Br*Rr*dBi - Ri*dBr + Rr*dBi;
    // var denom = Bi*Bi*dBi*dBi + Bi*Bi*dBr*dBr - 2.0*Bi*Ri*dBr + 2.0*Bi*Rr*dBi + Br*Br*dBi*dBi + Br*Br*dBr*dBr + 2.0*Br*Ri*dBi + 2.0*Br*Rr*dBr + Ri*Ri + Rr*Rr;
    var dBone = Math.sqrt(1.0 + dBr*dBr + dBi*dBi);
    var Bone = Math.sqrt(1.0 + Br*Br + Bi*Bi);
    var real = -Bi*Bi*Ri*dBi*dBone - Bi*Bi*Rr*dBr*dBone - 2.0*Bi*Br*Ri*dBr*dBone + 2.0*Bi*Br*Rr*dBi*dBone + Br*Br*Ri*dBi*dBone + Br*Br*Rr*dBr*dBone + Br*Ri*Ri*Bone*dBone*dBone + Br*Rr*Rr*Bone*dBone*dBone + Br*dBi*dBi*Bone + Br*dBr*dBr*Bone + Ri*dBi*Bone*Bone*dBone + Rr*dBr*Bone*Bone*dBone;
    var imag = -Bi*Bi*Ri*dBr*dBone + Bi*Bi*Rr*dBi*dBone + 2.0*Bi*Br*Ri*dBi*dBone + 2.0*Bi*Br*Rr*dBr*dBone + Bi*Ri*Ri*Bone*dBone*dBone + Bi*Rr*Rr*Bone*dBone*dBone + Bi*dBi*dBi*Bone + Bi*dBr*dBr*Bone + Br*Br*Ri*dBr*dBone - Br*Br*Rr*dBi*dBone - Ri*dBr*Bone*Bone*dBone + Rr*dBi*Bone*Bone*dBone;
    var denom = Bi*Bi*dBi*dBi + Bi*Bi*dBr*dBr - 2.0*Bi*Ri*dBr*Bone*dBone + 2.0*Bi*Rr*dBi*Bone*dBone + Br*Br*dBi*dBi + Br*Br*dBr*dBr + 2.0*Br*Ri*dBi*Bone*dBone + 2.0*Br*Rr*dBr*Bone*dBone + Ri*Ri*Bone*Bone*dBone*dBone + Rr*Rr*Bone*Bone*dBone*dBone;
    denom = Math.sqrt(denom*denom - real*real - imag*imag);
    // END EXPANDING B TO THE WHOLE PLANE

    this.offsetRealNow = real/denom;
    this.offsetImagNow = imag/denom;

    // START EXPANDING B TO THE WHOLE PLANE
    // // also compose to get a new rotation
    // // Rprime = (R + dB*conj(B))/(R*dB*B + 1)
    // real = -2.0*Bi*Bi*Ri*dBi*dBr + Bi*Bi*Rr*dBi*dBi - Bi*Bi*Rr*dBr*dBr + 2.0*Bi*Br*Ri*dBi*dBi - 2.0*Bi*Br*Ri*dBr*dBr + 4.0*Bi*Br*Rr*dBi*dBr + Bi*Ri*Ri*dBi + Bi*Rr*Rr*dBi + Bi*dBi + 2.0*Br*Br*Ri*dBi*dBr - Br*Br*Rr*dBi*dBi + Br*Br*Rr*dBr*dBr + Br*Ri*Ri*dBr + Br*Rr*Rr*dBr + Br*dBr + Rr;
    // imag = -Bi*Bi*Ri*dBi*dBi + Bi*Bi*Ri*dBr*dBr - 2.0*Bi*Bi*Rr*dBi*dBr - 4.0*Bi*Br*Ri*dBi*dBr + 2.0*Bi*Br*Rr*dBi*dBi - 2.0*Bi*Br*Rr*dBr*dBr - Bi*Ri*Ri*dBr - Bi*Rr*Rr*dBr - Bi*dBr + Br*Br*Ri*dBi*dBi - Br*Br*Ri*dBr*dBr + 2.0*Br*Br*Rr*dBi*dBr + Br*Ri*Ri*dBi + Br*Rr*Rr*dBi + Br*dBi + Ri;
    // // denom = Bi*Bi*Ri*Ri*dBi*dBi + Bi*Bi*Ri*Ri*dBr*dBr + Bi*Bi*Rr*Rr*dBi*dBi + Bi*Bi*Rr*Rr*dBr*dBr - 2.0*Bi*Ri*dBr + 2.0*Bi*Rr*dBi + Br*Br*Ri*Ri*dBi*dBi + Br*Br*Ri*Ri*dBr*dBr + Br*Br*Rr*Rr*dBi*dBi + Br*Br*Rr*Rr*dBr*dBr + 2.0*Br*Ri*dBi + 2.0*Br*Rr*dBr + 1.0;
    real = -2.0*Bi*Bi*Ri*dBi*dBr + Bi*Bi*Rr*dBi*dBi - Bi*Bi*Rr*dBr*dBr + 2.0*Bi*Br*Ri*dBi*dBi - 2.0*Bi*Br*Ri*dBr*dBr + 4.0*Bi*Br*Rr*dBi*dBr + Bi*Ri*Ri*dBi*Bone*dBone + Bi*Rr*Rr*dBi*Bone*dBone + Bi*dBi*Bone*dBone + 2.0*Br*Br*Ri*dBi*dBr - Br*Br*Rr*dBi*dBi + Br*Br*Rr*dBr*dBr + Br*Ri*Ri*dBr*Bone*dBone + Br*Rr*Rr*dBr*Bone*dBone + Br*dBr*Bone*dBone + Rr*Bone*Bone*dBone*dBone;
    imag = -Bi*Bi*Ri*dBi*dBi + Bi*Bi*Ri*dBr*dBr - 2.0*Bi*Bi*Rr*dBi*dBr - 4.0*Bi*Br*Ri*dBi*dBr + 2.0*Bi*Br*Rr*dBi*dBi - 2.0*Bi*Br*Rr*dBr*dBr - Bi*Ri*Ri*dBr*Bone*dBone - Bi*Rr*Rr*dBr*Bone*dBone - Bi*dBr*Bone*dBone + Br*Br*Ri*dBi*dBi - Br*Br*Ri*dBr*dBr + 2.0*Br*Br*Rr*dBi*dBr + Br*Ri*Ri*dBi*Bone*dBone + Br*Rr*Rr*dBi*Bone*dBone + Br*dBi*Bone*dBone + Ri*Bone*Bone*dBone*dBone;
    // denom = Bi*Bi*Ri*Ri*dBi*dBi + Bi*Bi*Ri*Ri*dBr*dBr + Bi*Bi*Rr*Rr*dBi*dBi + Bi*Bi*Rr*Rr*dBr*dBr - 2.0*Bi*Ri*dBr*Bone*dBone + 2.0*Bi*Rr*dBi*Bone*dBone + Br*Br*Ri*Ri*dBi*dBi + Br*Br*Ri*Ri*dBr*dBr + Br*Br*Rr*Rr*dBi*dBi + Br*Br*Rr*Rr*dBr*dBr + 2.0*Br*Ri*dBi*Bone*dBone + 2.0*Br*Rr*dBr*Bone*dBone + Bone*Bone*dBone*dBone;
    // END EXPANDING B TO THE WHOLE PLANE

    this.rotationNow = Math.atan2(imag, real);  // Math.atan2(imag/denom, real/denom);

    this.draw();
}

HyperbolicViewport.prototype.draw = function() {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    var THRESHOLD2 = this.THRESHOLD*this.THRESHOLD;
    var MAX_STRAIGHT_LINE_LENGTH2 = this.MAX_STRAIGHT_LINE_LENGTH*this.MAX_STRAIGHT_LINE_LENGTH;

    var shift = this.canvas.width/2.0;
    var scale = this.zoom*this.canvas.width/2.0;

    this.rotationCosNow = Math.cos(this.rotationNow);
    this.rotationSinNow = Math.sin(this.rotationNow);

    // draw the world-circle
    this.context.beginPath();
    this.context.arc(shift, shift, scale, 0.0, 2.0*Math.PI);
    this.context.stroke();

    this.service.loadDrawables();
    var drawable;
    while (drawable = this.service.nextDrawable()) {
        if (drawable["type"] == "polygon") {
            var points = [];
            var filledges = [];
            var drawedges = [];
            var willDraw = false;

            for (var j in drawable["d"]) {
                var px, py, pc, x1, y1, x2, y2;

                px = drawable["d"][j][0];
                py = drawable["d"][j][1];
                pc = drawable["d"][j][2];
                [x1, y1] = this.internalToScreen(px, py, pc);

                var jnext = parseInt(j) + 1;
                if (j == drawable["d"].length - 1) { jnext = 0; }

                px = drawable["d"][jnext][0];
                py = drawable["d"][jnext][1];
                pc = drawable["d"][jnext][2];
                [x2, y2] = this.internalToScreen(px, py, pc);

                if (x1*x1 + y1*y1 < THRESHOLD2  ||
                    x2*x2 + y2*y2 < THRESHOLD2) {
                    willDraw = true;
                }

                var options = drawable["d"][j][3];
                if (options == undefined) { options = ""; }
                else { options = options.toLowerCase(); }

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
                }
                else {
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
                if (fillStyle == undefined) { fillStyle = this.service.fillStyle; }

                if (fillStyle != "none") {
                    this.context.save();
                    this.context.fillStyle = fillStyle;

                    this.context.beginPath();
                    for (var j in filledges) {
                        if (filledges[j][0] == "a") {
                            this.context.arc(filledges[j][1], filledges[j][2], filledges[j][3], filledges[j][4], filledges[j][5], filledges[j][6]);
                        }
                        else if (filledges[j][0] == "l") {
                            this.context.lineTo(filledges[j][1], filledges[j][2]);
                        }
                        else if (filledges[j][0] == "m") {
                            this.context.moveTo(filledges[j][1], filledges[j][2]);
                        }
                    }
                    this.context.clip();
                    
                    // fill the polygon
                    this.context.beginPath();
                    for (var j in filledges) {
                        if (filledges[j][0] == "a") {
                            this.context.arc(filledges[j][1], filledges[j][2], filledges[j][3], filledges[j][4], filledges[j][5], filledges[j][6]);
                        }
                        else if (filledges[j][0] == "l") {
                            this.context.lineTo(filledges[j][1], filledges[j][2]);
                        }
                        else if (filledges[j][0] == "m") {
                            this.context.moveTo(filledges[j][1], filledges[j][2]);
                        }
                    }
                    this.context.fill();
                    this.context.restore();
                }

                // draw a line around it
                this.context.save();

                var strokeStyle = drawable["strokeStyle"];
                if (strokeStyle == undefined) { strokeStyle = this.service.strokeStyle; }
                this.context.strokeStyle = strokeStyle;

                var lineWidth = drawable["lineWidth"];
                if (lineWidth == undefined) { lineWidth = this.service.lineWidth; }
                this.context.lineWidth = lineWidth;

                var lineCap = drawable["lineCap"];
                if (lineCap == undefined) { lineCap = this.service.lineCap; }
                this.context.lineCap = lineCap;

                var lineJoin = drawable["lineJoin"];
                if (lineJoin == undefined) { lineJoin = this.service.lineJoin; }
                this.context.lineJoin = lineJoin;

                var miterLimit = drawable["miterLimit"];
                if (miterLimit == undefined) { miterLimit = this.service.miterLimit; }
                this.context.miterLimit = miterLimit;

                this.context.beginPath();
                for (var j in drawedges) {
                    if (drawedges[j][0] == "a") {
                        this.context.arc(drawedges[j][1], drawedges[j][2], drawedges[j][3], drawedges[j][4], drawedges[j][5], drawedges[j][6]);
                    }
                    else if (drawedges[j][0] == "l") {
                        this.context.lineTo(drawedges[j][1], drawedges[j][2]);
                    }
                    else if (drawedges[j][0] == "m") {
                        this.context.moveTo(drawedges[j][1], drawedges[j][2]);
                    }
                }
                this.context.stroke();
                this.context.restore();

                // draw the points
                this.context.save();

                var pointFill = drawable["pointFill"];
                if (pointFill == undefined) { pointFill = this.service.pointFill; }
                this.context.fillStyle = pointFill;

                var pointRadius = drawable["pointFill"];
                if (pointRadius == undefined) { pointRadius = this.service.pointRadius; }

                for (var j in points) {
                    this.context.beginPath();
                    this.context.arc(points[j][0], points[j][1], pointRadius, 0.0, 2*Math.PI);
                    this.context.fill();
                }

                this.context.restore();
            }
        }
    }
}
