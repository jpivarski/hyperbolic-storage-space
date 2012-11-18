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
