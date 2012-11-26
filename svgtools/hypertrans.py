#!/usr/bin/env python

from math import *

def halfPlane_to_hyperShadow(px, py):
    sqrtplus = sqrt(px*px + py*py + 2.0*py + 1.0)
    sqrtminus = sqrt(px*px + py*py - 2.0*py + 1.0)
    sinheta = sqrt((sqrtplus + sqrtminus)/(sqrtplus - sqrtminus))/2.0 - sqrt((sqrtplus - sqrtminus)/(sqrtminus + sqrtplus))/2.0

    denom = sqrt(pow(2.0 * px, 2) + pow(px*px + py*py - 1.0, 2))
    if px == 0.0 and py == 1.0:
        cosphi = 0.0
        sinphi = 1.0
    else:
        cosphi = (2.0 * px)/denom
        sinphi = (px*px + py*py - 1.0)/denom

    pxout = sinheta * cosphi
    pyout = sinheta * sinphi
    return pxout, pyout

def hyperShadow_to_halfPlane(px, py):
    pone = sqrt(px*px + py*py + 1.0)
    denom = 2.0*(px*px + py*py) + 1.0 - 2.0*py*pone
    numerx = 2.0*px*pone
    numery = 1.0
    return numerx/denom, numery/denom

def poincareDisk_to_hyperShadow(px, py):
    pone = sqrt(1.0 - px*px - py*py)
    return px/pone, py/pone

def hyperShadow_to_poincareDisk(px, py):
    pone = sqrt(px*px + py*py + 1.0)
    return px/pone, py/pone

def internalToScreen(preal, pimag, Br, Bi, angle):
    pone = sqrt(1.0 + preal*preal + pimag*pimag)

    bone = sqrt(1.0 + Br*Br + Bi*Bi)
    real = -Bi*Bi*preal*pone + 2.0*Bi*Br*pimag*pone + Br*Br*preal*pone + Br*pimag*pimag*bone + Br*preal*preal*bone + Br*bone*(pimag*pimag + preal*preal + 1.0) + preal*(Bi*Bi + Br*Br + 1.0)*pone
    imag = Bi*Bi*pimag*pone + 2.0*Bi*Br*preal*pone + Bi*pimag*pimag*bone + Bi*preal*preal*bone + Bi*bone*(pimag*pimag + preal*preal + 1.0) - Br*Br*pimag*pone + pimag*(Bi*Bi + Br*Br + 1.0)*pone
    denom = Bi*Bi*pimag*pimag + Bi*Bi*preal*preal + 2.0*Bi*pimag*bone*pone + Br*Br*pimag*pimag + Br*Br*preal*preal + 2.0*Br*preal*bone*pone + (Bi*Bi + Br*Br + 1.0)*(pimag*pimag + preal*preal + 1.0)

    real /= denom
    imag /= denom

    rotationCosNow = cos(angle)
    rotationSinNow = sin(angle)
    return rotationCosNow*real - rotationSinNow*imag, rotationCosNow*imag + rotationSinNow*real

def updateCoordinates(Br, Bi, dBr, dBi, Rr, Ri):
    dBone = sqrt(1.0 + dBr*dBr + dBi*dBi)
    Bone = sqrt(1.0 + Br*Br + Bi*Bi)
    real = -Bi*Bi*Ri*dBi*dBone - Bi*Bi*Rr*dBr*dBone - 2.0*Bi*Br*Ri*dBr*dBone + 2.0*Bi*Br*Rr*dBi*dBone + Br*Br*Ri*dBi*dBone + Br*Br*Rr*dBr*dBone + Br*Ri*Ri*Bone*dBone*dBone + Br*Rr*Rr*Bone*dBone*dBone + Br*dBi*dBi*Bone + Br*dBr*dBr*Bone + Ri*dBi*Bone*Bone*dBone + Rr*dBr*Bone*Bone*dBone
    imag = -Bi*Bi*Ri*dBr*dBone + Bi*Bi*Rr*dBi*dBone + 2.0*Bi*Br*Ri*dBi*dBone + 2.0*Bi*Br*Rr*dBr*dBone + Bi*Ri*Ri*Bone*dBone*dBone + Bi*Rr*Rr*Bone*dBone*dBone + Bi*dBi*dBi*Bone + Bi*dBr*dBr*Bone + Br*Br*Ri*dBr*dBone - Br*Br*Rr*dBi*dBone - Ri*dBr*Bone*Bone*dBone + Rr*dBi*Bone*Bone*dBone
    denom = Bi*Bi*dBi*dBi + Bi*Bi*dBr*dBr - 2.0*Bi*Ri*dBr*Bone*dBone + 2.0*Bi*Rr*dBi*Bone*dBone + Br*Br*dBi*dBi + Br*Br*dBr*dBr + 2.0*Br*Ri*dBi*Bone*dBone + 2.0*Br*Rr*dBr*Bone*dBone + Ri*Ri*Bone*Bone*dBone*dBone + Rr*Rr*Bone*Bone*dBone*dBone
    denom = sqrt(denom*denom - real*real - imag*imag)

    outBr = real/denom
    outBi = imag/denom

    real = -2.0*Bi*Bi*Ri*dBi*dBr + Bi*Bi*Rr*dBi*dBi - Bi*Bi*Rr*dBr*dBr + 2.0*Bi*Br*Ri*dBi*dBi - 2.0*Bi*Br*Ri*dBr*dBr + 4.0*Bi*Br*Rr*dBi*dBr + Bi*Ri*Ri*dBi*Bone*dBone + Bi*Rr*Rr*dBi*Bone*dBone + Bi*dBi*Bone*dBone + 2.0*Br*Br*Ri*dBi*dBr - Br*Br*Rr*dBi*dBi + Br*Br*Rr*dBr*dBr + Br*Ri*Ri*dBr*Bone*dBone + Br*Rr*Rr*dBr*Bone*dBone + Br*dBr*Bone*dBone + Rr*Bone*Bone*dBone*dBone
    imag = -Bi*Bi*Ri*dBi*dBi + Bi*Bi*Ri*dBr*dBr - 2.0*Bi*Bi*Rr*dBi*dBr - 4.0*Bi*Br*Ri*dBi*dBr + 2.0*Bi*Br*Rr*dBi*dBi - 2.0*Bi*Br*Rr*dBr*dBr - Bi*Ri*Ri*dBr*Bone*dBone - Bi*Rr*Rr*dBr*Bone*dBone - Bi*dBr*Bone*dBone + Br*Br*Ri*dBi*dBi - Br*Br*Ri*dBr*dBr + 2.0*Br*Br*Rr*dBi*dBr + Br*Ri*Ri*dBi*Bone*dBone + Br*Rr*Rr*dBi*Bone*dBone + Br*dBi*Bone*dBone + Ri*Bone*Bone*dBone*dBone
    outangle = atan2(imag, real)

    return outBr, outBi, outangle
