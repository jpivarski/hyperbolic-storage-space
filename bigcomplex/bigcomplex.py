#!/usr/bin/env python

import math

class BigComplex(object):
    bits = 31  # which is log(2**31, 10) = 9.33 digits
    twos = None
    overtwos = None
    twopi = 2.*math.pi
    overtwopi = 0.5/math.pi

    @classmethod
    def init(__class__):
        __class__.twos = [float(2**n) for n in xrange(0, __class__.bits)]
        __class__.overtwos = [1./float(2**n) for n in xrange(0, __class__.bits)]

    def __init__(self, mag, numer, denomexp):
        self.mag = mag
        self.numer = numer
        self.denomexp = denomexp

    ### loses precision when converting to and from plain numbers (at the level of BigComplex.bits)

    def frompolar(self, r, phi):
        # switch to [0, 2pi)
        while phi < 0.: phi += self.twopi
        while phi >= self.twopi: phi -= self.twopi

        self.mag = r
        self.denomexp = (self.bits - 1)
        self.numer = int(round(phi * self.overtwopi * self.twos[self.denomexp]))

    def topolar(self):
        numer = self.numer
        denomexp = self.denomexp

        # switch to [-pi, pi)
        while numer >= (1 << (denomexp - 1)):
            numer -= (1 << denomexp)

        positive = (numer >= 0)
        if not positive:
            numer = -numer
            
        # reduce precision
        while denomexp >= self.bits:
            numer = numer >> self.bits
            denomexp -= self.bits

        if not positive:
            numer = -numer
        return self.mag, numer * self.overtwos[denomexp] * self.twopi
            
    def fromcoord(self, real, imag):
        r = math.sqrt(real**2 + imag**2)
        phi = math.atan2(imag, real)
        self.frompolar(r, phi)

    def tocoord(self):
        r, phi = self.topolar()
        return r*math.cos(phi), r*math.sin(phi)

    def fromcomplex(self, z):
        self.fromcoord(z.real, z.imag)

    def tocomplex(self):
        real, imag = self.tocoord()
        return real + imag*1j

    ### multiplications of BigComplexes in internal representation are lossless

    def __mul__(self, other):
        mag = self.mag * other.mag
        numer = (self.numer << other.denomexp) + (other.numer << self.denomexp)
        denomexp = self.denomexp + other.denomexp
        return BigComplex(mag, numer, denomexp)

    def __div__(self, other):
        mag = self.mag / other.mag
        numer = (self.numer << other.denomexp) - (other.numer << self.denomexp)
        denomexp = self.denomexp + other.denomexp
        return BigComplex(mag, numer, denomexp)

    ### addition and subtraction are just careful about big cancellations (self and other nearly collinear)

    def __add__(self, other):
        # strategy: rotate self and other such that self is on the real axis,
        #           add them as phasors, and then rotate back

        # difference is otherphi - selfphi to remove the self angle
        diff_numer = (other.numer << self.denomexp) - (self.numer << other.denomexp)
        diff_denomexp = other.denomexp + self.denomexp

        # switch to [-pi, pi)
        while diff_numer >= (1 << (diff_denomexp - 1)):
            diff_numer -= (1 << diff_denomexp)

        positive = (diff_numer >= 0)
        if not positive:
            diff_numer = -diff_numer

        # reduce precision in diffphi
        while diff_denomexp >= self.bits:
            diff_numer = diff_numer >> self.bits
            diff_denomexp -= self.bits

        if not positive:
            diff_numer = -diff_numer
        diffphi = diff_numer * self.overtwos[diff_denomexp] * self.twopi

        # get the polar coordinates of the rotated phasor
        mag = math.sqrt((self.mag + other.mag*math.cos(diffphi))**2 + (other.mag*math.sin(diffphi))**2)
        phi = math.atan2(other.mag*math.sin(diffphi), self.mag + other.mag*math.cos(diffphi))

        # convert it to a BigComplex in [0, 2pi)
        while phi < 0.: phi += self.twopi
        while phi >= self.twopi: phi -= self.twopi
        denomexp = (self.bits - 1)
        numer = int(round(phi * self.overtwopi * self.twos[denomexp]))

        # rotate back (add the self angle back in)
        numer = (self.numer << denomexp) + (numer << self.denomexp)
        denomexp += self.denomexp

        return BigComplex(mag, numer, denomexp)

    def __neg__(self):
        # add pi to the angle
        numer = self.numer + (1 << (self.denomexp - 1))
        return BigComplex(self.mag, numer, self.denomexp)

    def __sub__(self, other):
        return self + (-other)

    def conjugate(self):
        # negate the angle
        numer = -self.numer
        # add 2pi until it's within [0, 2pi)
        while numer < 0:
            numer += (1 << self.denomexp)
        return BigComplex(self.mag, numer, self.denomexp)

BigComplex.init()

def frompolar(r, phi):
    output = BigComplex.__new__(BigComplex)
    output.frompolar(r, phi)
    return output

def fromcoord(real, imag):
    output = BigComplex.__new__(BigComplex)
    output.fromcoord(real, imag)
    return output

def fromcomplex(z):
    output = BigComplex.__new__(BigComplex)
    output.fromcomplex(z)
    return output

def topolar(bigComplex):
    return bigComplex.topolar()

def tocoord(bigComplex):
    return bigComplex.tocoord()

def tocomplex(bigComplex):
    return bigComplex.tocomplex()

def conjugate(bigComplex):
    return bigComplex.conjugate()

######################################################################

import random

for i in xrange(1000000):
    x = random.gauss(0, 1) + random.gauss(0, 1)*1j
    y = random.gauss(0, 1) + random.gauss(0, 1)*1j
    z = random.gauss(0, 1) + random.gauss(0, 1)*1j
    if abs((x * y * z) - (tocomplex(fromcomplex(x) * fromcomplex(y) * fromcomplex(z)))) > 1e-6:
        raise Exception

for i in xrange(1000000):
    x = random.gauss(0, 1) + random.gauss(0, 1)*1j
    y = random.gauss(0, 1) + random.gauss(0, 1)*1j
    z = random.gauss(0, 1) + random.gauss(0, 1)*1j
    if abs((x + y + z) - (tocomplex(fromcomplex(x) + fromcomplex(y) + fromcomplex(z)))) > 1e-6:
        raise Exception

for i in xrange(1000000):
    x = random.gauss(0, 1) + random.gauss(0, 1)*1j
    y = random.gauss(0, 1) + random.gauss(0, 1)*1j
    z = random.gauss(0, 1) + random.gauss(0, 1)*1j
    if abs((x + y - z) - (tocomplex(fromcomplex(x) + fromcomplex(y) - fromcomplex(z)))) > 1e-6:
        raise Exception

for i in xrange(1000000):
    x = random.gauss(0, 1) + random.gauss(0, 1)*1j
    y = random.gauss(0, 1) + random.gauss(0, 1)*1j
    z = random.gauss(0, 1) + random.gauss(0, 1)*1j
    if abs((x * y - z) - (tocomplex(fromcomplex(x) * fromcomplex(y) - fromcomplex(z)))) > 1e-6:
        raise Exception

for i in xrange(1000000):
    x = random.gauss(0, 1) + random.gauss(0, 1)*1j
    y = random.gauss(0, 1) + random.gauss(0, 1)*1j
    z = random.gauss(0, 1) + random.gauss(0, 1)*1j
    if abs((x.conjugate() * y - z) - (tocomplex(fromcomplex(x).conjugate() * fromcomplex(y) - fromcomplex(z)))) > 1e-6:
        raise Exception
