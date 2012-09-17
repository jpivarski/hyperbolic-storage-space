function BigComplex(r, numer, denomexp) {
    this.r = r;
    this.numer = numer;
    this.denomexp = denomexp;
}

BigComplex.prototype.DEFAULT_BITS = dbits;  // from jsbn.min.js
BigComplex.prototype.TWOPI = 2*Math.PI;
BigComplex.prototype.OVERTWOPI = 0.5/Math.PI;

function fromPolar(r, phi) {
    // switch to [0, 2pi)
    while (phi < 0) { phi += BigComplex.prototype.TWOPI; }
    while (phi >= BigComplex.prototype.TWOPI) { phi -= BigComplex.prototype.TWOPI; }

    var denomexp = BigComplex.prototype.DEFAULT_BITS - 1;

    var numer = nbv(Math.round(phi * BigComplex.prototype.OVERTWOPI * (1 << denomexp)));

    return new BigComplex(r, numer, denomexp);
}

function fromCoord(real, imag) {
    var r = Math.sqrt(real*real + imag*imag);
    var phi = Math.atan2(imag, real);
    return fromPolar(r, phi);
}

BigComplex.prototype.toPolar = function() {
    var numer = this.numer;

    // switch to [-pi, pi)
    // (if greater than denom/2, subtract denom; in this space, 1 unit represents 2pi)
    if (numer.compareTo(BigInteger.ONE.shiftLeft(this.denomexp - 1)) >= 0) {
	numer = numer.subtract(BigInteger.ONE.shiftLeft(this.denomexp));
    }
    
    return [this.r, (numer / BigInteger.ONE.shiftLeft(this.denomexp)) * this.TWOPI];
}

BigComplex.prototype.arg = function() {
    return (this.numer / BigInteger.ONE.shiftLeft(this.denomexp)) * this.TWOPI;
}

BigComplex.prototype.toCoord = function() {
    var r, phi;
    [r, phi] = this.toPolar();
    return [r*Math.cos(phi), r*Math.sin(phi)];
}

BigComplex.prototype.toString = function() {
    var real, imag;
    [real, imag] = this.toCoord();
    return real.toPrecision(5) + "+" + imag.toPrecision(5) + "j";
}

BigComplex.prototype.scale = function(real) {
    return new BigComplex(this.r * real, this.numer, this.denomexp);
}

BigComplex.prototype.multiply = function(other) {
    var r = this.r * other.r;
    var numer = this.numer.shiftLeft(other.denomexp).add(other.numer.shiftLeft(this.denomexp));
    var denomexp = this.denomexp + other.denomexp;
    return new BigComplex(r, numer, denomexp);
}

BigComplex.prototype.divide = function(other) {
    var r = this.r / other.r;
    var numer = this.numer.shiftLeft(other.denomexp).subtract(other.numer.shiftLeft(this.denomexp));
    var denomexp = this.denomexp + other.denomexp;
    return new BigComplex(r, numer, denomexp);
}

BigComplex.prototype.add = function(other) {
    // the internal representation is polar, so addition is hard
    // this algorithm is designed for high precision in the case of large cancellations between this and other
    // we only calculate trig functions of the angle *between* this and other (calculated to full precision)

    // we first rotate to a frame in which this.toPolar()[1] would be zero
    var diff_numer = other.numer.shiftLeft(this.denomexp).subtract(this.numer.shiftLeft(other.denomexp));
    var diff_denomexp = other.denomexp + this.denomexp;

    // then switch this angle to [-pi, pi)
    // (if greater than denom/2, subtract denom; in this space, 1 unit represents 2pi)
    if (diff_numer.compareTo(BigInteger.ONE.shiftLeft(diff_denomexp - 1)) >= 0) {
	diff_numer = diff_numer.subtract(BigInteger.ONE.shiftLeft(diff_denomexp));
    }

    var diff_phi = (diff_numer / BigInteger.ONE.shiftLeft(diff_denomexp)) * this.TWOPI;

    // calculate the sum using components
    var real = this.r + other.r*Math.cos(diff_phi);
    var imag = other.r*Math.sin(diff_phi);
    var result = fromPolar(Math.sqrt(real*real + imag*imag), Math.atan2(imag, real));

    // rotate back to the original frame
    result.numer = this.numer.shiftLeft(result.denomexp).add(result.numer.shiftLeft(this.denomexp));
    result.denomexp += this.denomexp;

    return result;
}

BigComplex.prototype.negate = function() {
    // in this space, 1/2 unit represents pi
    var pi = BigInteger.ONE.shiftLeft(this.denomexp - 1);
    var numer;
    
    if (this.numer.compareTo(pi) > 0) {    // if the angle is greater than pi, add pi
	numer = this.numer.add(pi);
    }
    else {    // otherwise, subtract pi
	numer = this.numer.subtract(pi);
    }
    return new BigComplex(this.r, numer, this.denomexp);
}

BigComplex.prototype.subtract = function(other) {
    return this.add(other.negate());
}

BigComplex.prototype.conjugate = function() {
    // negate the angle
    var numer = this.numer.negate();

    // add 2pi until it's within [0, 2pi)
    while (numer.compareTo(BigInteger.ZERO) < 0) {
	numer = numer.add(BigInteger.ONE.shiftLeft(this.denomexp));
    }

    return new BigComplex(this.r, numer, this.denomexp);
}

BigComplex.ZERO = fromPolar(0.0, 0.0);
BigComplex.ONE = fromPolar(1.0, 0.0);
