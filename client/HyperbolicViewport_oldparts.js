//////////////////////////////////////////// transformations

function add([areal, aimag], [breal, bimag]) {
    return [areal + breal, aimag + bimag];
}   

function sub([areal, aimag], [breal, bimag]) {
    return [areal - breal, aimag - bimag];
}   

function mult([areal, aimag], [breal, bimag]) {
    var amag = Math.sqrt(areal*areal + aimag*aimag);
    var aphi = Math.atan2(aimag, areal);
    var bmag = Math.sqrt(breal*breal + bimag*bimag);
    var bphi = Math.atan2(bimag, breal);

    var mag = amag * bmag;
    var phi = aphi + bphi;

    return [mag*Math.cos(phi), mag*Math.sin(phi)];
}   

function div([areal, aimag], [breal, bimag]) {
    var amag = Math.sqrt(areal*areal + aimag*aimag);
    var aphi = Math.atan2(aimag, areal);
    var bmag = Math.sqrt(breal*breal + bimag*bimag);
    var bphi = Math.atan2(bimag, breal);

    var mag = amag / bmag;
    var phi = aphi - bphi;

    return [mag*Math.cos(phi), mag*Math.sin(phi)];
}   

function conj([real, imag]) {
    return [real, -imag];
}   

// function internalToScreen([preal, pimag], [oreal, oimag], [cos, sin]) {
//     var radscale = Math.sqrt(preal*preal + pimag*pimag + 1.0) + 1.0;
//     var alpha = preal + oreal*radscale;
//     var beta = pimag + oimag*radscale;
//     var gamma = oreal*preal + oimag*pimag + radscale;
//     var delta = oreal*pimag - oimag*preal;
//     var factor = 1.0/(gamma*gamma + delta*delta);
//     var resultR = factor*(alpha*gamma + beta*delta);
//     var resultI = factor*(beta*gamma - alpha*delta);
//     return [cos*resultR - sin*resultI, cos*resultI + sin*resultR];
// }

HyperbolicViewport.prototype.updateOffset = function(x, y) {
    var fx, fy;
    [fx, fy] = this.finger1;

    var real = (-y*y*fx - x*x*fx + x*fy*fy + x*fx*fx - x + fx)/(y*y*fy*fy + y*y*fx*fx + x*x*fy*fy + x*x*fx*fx - 1.0);
    var imag = (-y*y*fy + y*fy*fy + y*fx*fx - y - x*x*fy + fy)/(y*y*fy*fy + y*y*fx*fx + x*x*fy*fy + x*x*fx*fx - 1.0);

    var offsetDelta = [real, imag];
    var rotation = [Math.cos(this.rotation), Math.sin(this.rotation)];

    this.offsetNow = div(add(offsetDelta, mult(rotation, this.offset)),
	       add(mult(offsetDelta, conj(this.offset)), rotation));

    rotation = div(add(rotation, mult(offsetDelta, conj(this.offset))),
		   add(mult(rotation, mult(conj(offsetDelta), this.offset)), [1.0, 0.0]));

    this.rotationNow = Math.atan2(rotation[1], rotation[0]);

    // this.offsetNow = offsetDelta.add(this.rotation.multiply(this.offset)).divide(offsetDelta.multiply(this.offset.conjugate()).add(this.rotation));
    // this.rotationNow = this.rotation.add(offsetDelta.multiply(this.offset.conjugate())).divide(this.rotation.multiply(offsetDelta.conjugate()).multiply(this.offset).add(BigComplex.ONE));
    // this.rotationNow.r = 1.0;

    this.draw();
}

    // this.context.setTransform(1.0, 0.0, 0.0, 1.0, 0.0, 0.0);
    // this.context.translate((1.0 - this.zoom)*this.canvas.width/2.0, (1.0 - this.zoom)*this.canvas.width/2.0);
    // this.context.scale(scale, -scale);
    // this.context.translate(1.0, -1.0);
    // this.context.rotate(this.rotation);

	    var x, y;
	    [x, y] = this.internalToScreen(poly[j]);
	    this.context.beginPath();
	    this.context.arc(x*scale + shift, -y*scale + shift, 3.0, 0.0, 2*Math.PI);
	    this.context.fill();

