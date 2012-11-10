import sympy
from sympy import I, conjugate
from sympy.printing.ccode import ccode

B = sympy.Symbol("B")
# R = sympy.Symbol("R")

# toDisk = (Rr + I*Ri)*(Br + I*Bi)
# toDisk = R*B
toDisk = B

toHalfPlane = (toDisk + I)/(I*toDisk + 1)

twiceImag = toHalfPlane - toHalfPlane.conjugate()

highPoint = toHalfPlane + twiceImag/2
# highPoint = toHalfPlane + I

backToDisk = (-highPoint + I)/(I*highPoint - 1)

# backToScreen = R.conjugate()*(backToDisk - B)/(-B.conjugate()*backToDisk + 1)
backToScreen = (backToDisk - B)/(-B.conjugate()*backToDisk + 1)

tmp = backToScreen.simplify()

print ccode(tmp)
# (-B + (-2*(B*R + I)/(I*B*R + 1) + (conjugate(B)*conjugate(R) - I)/(-I*conjugate(B)*conjugate(R) + 1) + I)/(I*(2*(B*R + I)/(I*B*R + 1) - (conjugate(B)*conjugate(R) - I)/(-I*conjugate(B)*conjugate(R) + 1)) - 1))*conjugate(R)/(1 - (-2*(B*R + I)/(I*B*R + 1) + (conjugate(B)*conjugate(R) - I)/(-I*conjugate(B)*conjugate(R) + 1) + I)*conjugate(B)/(I*(2*(B*R + I)/(I*B*R + 1) - (conjugate(B)*conjugate(R) - I)/(-I*conjugate(B)*conjugate(R) + 1)) - 1))
# other sign: (B + (-2*(B + I)/(I*B + 1) + I + (conjugate(B) - I)/(-I*conjugate(B) + 1))/(I*(2*(B + I)/(I*B + 1) - (conjugate(B) - I)/(-I*conjugate(B) + 1)) - 1))/(1 + (-2*(B + I)/(I*B + 1) + I + (conjugate(B) - I)/(-I*conjugate(B) + 1))*conjugate(B)/(I*(2*(B + I)/(I*B + 1) - (conjugate(B) - I)/(-I*conjugate(B) + 1)) - 1))
# just I: (B - (B + I)/((I*B + 1)*(I*((B + I)/(I*B + 1) + I) - 1)))/(-(B + I)*conjugate(B)/((I*B + 1)*(I*((B + I)/(I*B + 1) + I) - 1)) + 1)

# numer = (-B + (-2*(B*R + I)/(I*B*R + 1) + (conjugate(B)*conjugate(R) - I)/(-I*conjugate(B)*conjugate(R) + 1) + I)/(I*(2*(B*R + I)/(I*B*R + 1) - (conjugate(B)*conjugate(R) - I)/(-I*conjugate(B)*conjugate(R) + 1)) - 1))*conjugate(R)
# denom = (1 - (-2*(B*R + I)/(I*B*R + 1) + (conjugate(B)*conjugate(R) - I)/(-I*conjugate(B)*conjugate(R) + 1) + I)*conjugate(B)/(I*(2*(B*R + I)/(I*B*R + 1) - (conjugate(B)*conjugate(R) - I)/(-I*conjugate(B)*conjugate(R) + 1)) - 1))
# numer = (-B + (-2*(B + I)/(I*B + 1) + I + (conjugate(B) - I)/(-I*conjugate(B) + 1))/(I*(2*(B + I)/(I*B + 1) - (conjugate(B) - I)/(-I*conjugate(B) + 1)) - 1))
# denom = (1 - (-2*(B + I)/(I*B + 1) + I + (conjugate(B) - I)/(-I*conjugate(B) + 1))*conjugate(B)/(I*(2*(B + I)/(I*B + 1) - (conjugate(B) - I)/(-I*conjugate(B) + 1)) - 1))
# numer = (B + (-2*(B + I)/(I*B + 1) + I + (conjugate(B) - I)/(-I*conjugate(B) + 1))/(I*(2*(B + I)/(I*B + 1) - (conjugate(B) - I)/(-I*conjugate(B) + 1)) - 1))
# denom = (1 + (-2*(B + I)/(I*B + 1) + I + (conjugate(B) - I)/(-I*conjugate(B) + 1))*conjugate(B)/(I*(2*(B + I)/(I*B + 1) - (conjugate(B) - I)/(-I*conjugate(B) + 1)) - 1))
# numer = (B - (B + I)/((I*B + 1)*(I*((B + I)/(I*B + 1) + I) - 1)))
# denom = (-(B + I)*conjugate(B)/((I*B + 1)*(I*((B + I)/(I*B + 1) + I) - 1)) + 1)
# numer = (-B - (B + I)/((I*B + 1)*(I*((B + I)/(I*B + 1) + I) - 1)))
# denom = ((B + I)*conjugate(B)/((I*B + 1)*(I*((B + I)/(I*B + 1) + I) - 1)) + 1)
numer = (-B + (-3*(B + I)/(2*(I*B + 1)) + I + (conjugate(B) - I)/(2*(-I*conjugate(B) + 1)))/(I*(3*(B + I)/(2*(I*B + 1)) - (conjugate(B) - I)/(2*(-I*conjugate(B) + 1))) - 1))
denom = (1 - (-3*(B + I)/(2*(I*B + 1)) + I + (conjugate(B) - I)/(2*(-I*conjugate(B) + 1)))*conjugate(B)/(I*(3*(B + I)/(2*(I*B + 1)) - (conjugate(B) - I)/(2*(-I*conjugate(B) + 1))) - 1))
print (numer/denom - tmp).simplify()

numer, denom = numer * denom.conjugate(), denom * denom.conjugate()

br = sympy.Symbol("br")
bi = sympy.Symbol("bi")

# numer2 = (-(br+I*bi) + ((-2*(br+I*bi) - 2*I)/(I*(br+I*bi) + 1) + I + ((br-I*bi) - I)/(-I*(br-I*bi) + 1))/(I*((2*(br+I*bi) + 2*I)/(I*(br+I*bi) + 1) - ((br-I*bi) - I)/(-I*(br-I*bi) + 1)) - 1))*(-(br+I*bi)*(((br+I*bi) + I)/(I*(br+I*bi) + 1) - I + (-2*(br-I*bi) + 2*I)/(-I*(br-I*bi) + 1))/(-I*(-((br+I*bi) + I)/(I*(br+I*bi) + 1) + (2*(br-I*bi) - 2*I)/(-I*(br-I*bi) + 1)) - 1) + 1)
# denom2 = (1 - ((-2*(br+I*bi) - 2*I)/(I*(br+I*bi) + 1) + I + ((br-I*bi) - I)/(-I*(br-I*bi) + 1))*(br-I*bi)/(I*((2*(br+I*bi) + 2*I)/(I*(br+I*bi) + 1) - ((br-I*bi) - I)/(-I*(br-I*bi) + 1)) - 1))*(-(br+I*bi)*(((br+I*bi) + I)/(I*(br+I*bi) + 1) - I + (-2*(br-I*bi) + 2*I)/(-I*(br-I*bi) + 1))/(-I*(-((br+I*bi) + I)/(I*(br+I*bi) + 1) + (2*(br-I*bi) - 2*I)/(-I*(br-I*bi) + 1)) - 1) + 1)

# numer2 = ((br+I*bi) + ((-2*(br+I*bi) - 2*I)/(I*(br+I*bi) + 1) + I + ((br-I*bi) - I)/(-I*(br-I*bi) + 1))/(I*((2*(br+I*bi) + 2*I)/(I*(br+I*bi) + 1) - ((br-I*bi) - I)/(-I*(br-I*bi) + 1)) - 1))*((br+I*bi)*(((br+I*bi) + I)/(I*(br+I*bi) + 1) - I + (-2*(br-I*bi) + 2*I)/(-I*(br-I*bi) + 1))/(-I*(-((br+I*bi) + I)/(I*(br+I*bi) + 1) + (2*(br-I*bi) - 2*I)/(-I*(br-I*bi) + 1)) - 1) + 1)
# denom2 = (1 + ((-2*(br+I*bi) - 2*I)/(I*(br+I*bi) + 1) + I + ((br-I*bi) - I)/(-I*(br-I*bi) + 1))*(br-I*bi)/(I*((2*(br+I*bi) + 2*I)/(I*(br+I*bi) + 1) - ((br-I*bi) - I)/(-I*(br-I*bi) + 1)) - 1))*((br+I*bi)*(((br+I*bi) + I)/(I*(br+I*bi) + 1) - I + (-2*(br-I*bi) + 2*I)/(-I*(br-I*bi) + 1))/(-I*(-((br+I*bi) + I)/(I*(br+I*bi) + 1) + (2*(br-I*bi) - 2*I)/(-I*(br-I*bi) + 1)) - 1) + 1)

# numer2 = ((br+I*bi) - ((br+I*bi) + I)/((I*(br+I*bi) + 1)*(I*(((br+I*bi) + I)/(I*(br+I*bi) + 1) + I) - 1)))*((br+I*bi)*(-(br-I*bi) + I)/((-I*(-I + ((br-I*bi) - I)/(-I*(br-I*bi) + 1)) - 1)*(-I*(br-I*bi) + 1)) + 1)
# denom2 = ((br+I*bi)*(-(br-I*bi) + I)/((-I*(-I + ((br-I*bi) - I)/(-I*(br-I*bi) + 1)) - 1)*(-I*(br-I*bi) + 1)) + 1)*((-(br+I*bi) - I)*(br-I*bi)/((I*(br+I*bi) + 1)*(I*(((br+I*bi) + I)/(I*(br+I*bi) + 1) + I) - 1)) + 1)

# numer2 = (-(br+I*bi) - ((br+I*bi) + I)/((I*(br+I*bi) + 1)*(I*(((br+I*bi) + I)/(I*(br+I*bi) + 1) + I) - 1)))*((br+I*bi)*((br-I*bi) - I)/((-I*(-I + ((br-I*bi) - I)/(-I*(br-I*bi) + 1)) - 1)*(-I*(br-I*bi) + 1)) + 1)
# denom2 = ((br+I*bi)*((br-I*bi) - I)/((-I*(-I + ((br-I*bi) - I)/(-I*(br-I*bi) + 1)) - 1)*(-I*(br-I*bi) + 1)) + 1)*(((br+I*bi) + I)*(br-I*bi)/((I*(br+I*bi) + 1)*(I*(((br+I*bi) + I)/(I*(br+I*bi) + 1) + I) - 1)) + 1)

numer2 = (-(br+I*bi) + ((-3*(br+I*bi) - 3*I)/(2*I*(br+I*bi) + 2) + I + ((br-I*bi) - I)/(-2*I*(br-I*bi) + 2))/(I*((3*(br+I*bi) + 3*I)/(2*I*(br+I*bi) + 2) - ((br-I*bi) - I)/(-2*I*(br-I*bi) + 2)) - 1))*(-(br+I*bi)*(((br+I*bi) + I)/(2*I*(br+I*bi) + 2) - I + (-3*(br-I*bi) + 3*I)/(-2*I*(br-I*bi) + 2))/(-I*(-((br+I*bi) + I)/(2*I*(br+I*bi) + 2) + (3*(br-I*bi) - 3*I)/(-2*I*(br-I*bi) + 2)) - 1) + 1)
denom2 = (1 - ((-3*(br+I*bi) - 3*I)/(2*I*(br+I*bi) + 2) + I + ((br-I*bi) - I)/(-2*I*(br-I*bi) + 2))*(br-I*bi)/(I*((3*(br+I*bi) + 3*I)/(2*I*(br+I*bi) + 2) - ((br-I*bi) - I)/(-2*I*(br-I*bi) + 2)) - 1))*(-(br+I*bi)*(((br+I*bi) + I)/(2*I*(br+I*bi) + 2) - I + (-3*(br-I*bi) + 3*I)/(-2*I*(br-I*bi) + 2))/(-I*(-((br+I*bi) + I)/(2*I*(br+I*bi) + 2) + (3*(br-I*bi) - 3*I)/(-2*I*(br-I*bi) + 2)) - 1) + 1)

numer2 = numer2.simplify()
denom2 = denom2.simplify()

###############

# print ccode(numer2)
# # 2*(I*pow(bi, 6) + 2*pow(bi, 5)*br - 2*I*pow(bi, 5) + I*pow(bi, 4)*pow(br, 2) - 2*pow(bi, 4)*br - I*pow(bi, 4) + 4*pow(bi, 3)*pow(br, 3) - 4*I*pow(bi, 3)*pow(br, 2) - 4*pow(bi, 3)*br + 4*I*pow(bi, 3) - I*pow(bi, 2)*pow(br, 4) - 4*pow(bi, 2)*pow(br, 3) + 2*I*pow(bi, 2)*pow(br, 2) + 4*pow(bi, 2)*br - I*pow(bi, 2) + 2*bi*pow(br, 5) - 2*I*bi*pow(br, 4) - 4*bi*pow(br, 3) + 4*I*bi*pow(br, 2) + 2*bi*br - 2*I*bi - I*pow(br, 6) - 2*pow(br, 5) + 3*I*pow(br, 4) + 4*pow(br, 3) - 3*I*pow(br, 2) - 2*br + I)
# test0 = 2*(I*(bi**6) + 2*(bi**5)*br - 2*I*(bi**5) + I*(bi**4)*(br**2) - 2*(bi**4)*br - I*(bi**4) + 4*(bi**3)*(br**3) - 4*I*(bi**3)*(br**2) - 4*(bi**3)*br + 4*I*(bi**3) - I*(bi**2)*(br**4) - 4*(bi**2)*(br**3) + 2*I*(bi**2)*(br**2) + 4*(bi**2)*br - I*(bi**2) + 2*bi*(br**5) - 2*I*bi*(br**4) - 4*bi*(br**3) + 4*I*bi*(br**2) + 2*bi*br - 2*I*bi - I*(br**6) - 2*(br**5) + 3*I*(br**4) + 4*(br**3) - 3*I*(br**2) - 2*br + I)

# # Real part: 2*(2*pow(bi, 5)*br - 2*pow(bi, 4)*br + 4*pow(bi, 3)*pow(br, 3) - 4*pow(bi, 3)*br - 4*pow(bi, 2)*pow(br, 3) + 4*pow(bi, 2)*br + 2*bi*pow(br, 5) - 4*bi*pow(br, 3) + 2*bi*br - 2*pow(br, 5) + 4*pow(br, 3) - 2*br)
# test1 = 2*(2*(bi**5)*br - 2*(bi**4)*br + 4*(bi**3)*(br**3) - 4*(bi**3)*br - 4*(bi**2)*(br**3) + 4*(bi**2)*br + 2*bi*(br**5) - 4*bi*(br**3) + 2*bi*br - 2*(br**5) + 4*(br**3) - 2*br)

# # Imag part: 2*(I*pow(bi, 6) - 2*I*pow(bi, 5) + I*pow(bi, 4)*pow(br, 2) - I*pow(bi, 4) - 4*I*pow(bi, 3)*pow(br, 2) + 4*I*pow(bi, 3) - I*pow(bi, 2)*pow(br, 4) + 2*I*pow(bi, 2)*pow(br, 2) - I*pow(bi, 2) - 2*I*bi*pow(br, 4) + 4*I*bi*pow(br, 2) - 2*I*bi - I*pow(br, 6) + 3*I*pow(br, 4) - 3*I*pow(br, 2) + I)
# # Imag part: 2*(pow(bi, 6) - 2*pow(bi, 5) + pow(bi, 4)*pow(br, 2) - pow(bi, 4) - 4*pow(bi, 3)*pow(br, 2) + 4*pow(bi, 3) - pow(bi, 2)*pow(br, 4) + 2*pow(bi, 2)*pow(br, 2) - pow(bi, 2) - 2*bi*pow(br, 4) + 4*bi*pow(br, 2) - 2*bi - pow(br, 6) + 3*pow(br, 4) - 3*pow(br, 2) + 1)

# test2 = 2*(I*(bi**6) - 2*I*(bi**5) + I*(bi**4)*(br**2) - I*(bi**4) - 4*I*(bi**3)*(br**2) + 4*I*(bi**3) - I*(bi**2)*(br**4) + 2*I*(bi**2)*(br**2) - I*(bi**2) - 2*I*bi*(br**4) + 4*I*bi*(br**2) - 2*I*bi - I*(br**6) + 3*I*(br**4) - 3*I*(br**2) + I)

# print test0 - test1 - test2

# print ccode(denom2)
# # 4*(pow(bi, 6) - 2*pow(bi, 5) + 3*pow(bi, 4)*pow(br, 2) - pow(bi, 4) - 4*pow(bi, 3)*pow(br, 2) + 4*pow(bi, 3) + 3*pow(bi, 2)*pow(br, 4) - 2*pow(bi, 2)*pow(br, 2) - pow(bi, 2) - 2*bi*pow(br, 4) + 4*bi*pow(br, 2) - 2*bi + pow(br, 6) - pow(br, 4) - pow(br, 2) + 1)
# testdenom = 4*((bi**6) - 2*(bi**5) + 3*(bi**4)*(br**2) - (bi**4) - 4*(bi**3)*(br**2) + 4*(bi**3) + 3*(bi**2)*(br**4) - 2*(bi**2)*(br**2) - (bi**2) - 2*bi*(br**4) + 4*bi*(br**2) - 2*bi + (br**6) - (br**4) - (br**2) + 1)

# print ((test1 + test2)/testdenom - numer2/denom2).simplify()

###############

# print ccode(numer2)
# # 2*(I*pow(bi, 6) + 2*pow(bi, 5)*br + 3*I*pow(bi, 5) + I*pow(bi, 4)*pow(br, 2) + 3*pow(bi, 4)*br - 3*I*pow(bi, 4) + 4*pow(bi, 3)*pow(br, 3) + 6*I*pow(bi, 3)*pow(br, 2) - 6*pow(bi, 3)*br - 2*I*pow(bi, 3) - I*pow(bi, 2)*pow(br, 4) + 6*pow(bi, 2)*pow(br, 3) - 2*pow(bi, 2)*br - 3*I*pow(bi, 2) + 2*bi*pow(br, 5) + 3*I*bi*pow(br, 4) - 6*bi*pow(br, 3) - 2*I*bi*pow(br, 2) + 3*I*bi - I*pow(br, 6) + 3*pow(br, 5) + 3*I*pow(br, 4) - 2*pow(br, 3) - 3*I*pow(br, 2) + 3*br + I)
# test0 = 2*(I*(bi**6) + 2*(bi**5)*br + 3*I*(bi**5) + I*(bi**4)*(br**2) + 3*(bi**4)*br - 3*I*(bi**4) + 4*(bi**3)*(br**3) + 6*I*(bi**3)*(br**2) - 6*(bi**3)*br - 2*I*(bi**3) - I*(bi**2)*(br**4) + 6*(bi**2)*(br**3) - 2*(bi**2)*br - 3*I*(bi**2) + 2*bi*(br**5) + 3*I*bi*(br**4) - 6*bi*(br**3) - 2*I*bi*(br**2) + 3*I*bi - I*(br**6) + 3*(br**5) + 3*I*(br**4) - 2*(br**3) - 3*I*(br**2) + 3*br + I)

# # Real part: 2*(2*pow(bi, 5)*br + 3*pow(bi, 4)*br + 4*pow(bi, 3)*pow(br, 3) - 6*pow(bi, 3)*br + 6*pow(bi, 2)*pow(br, 3) - 2*pow(bi, 2)*br + 2*bi*pow(br, 5) - 6*bi*pow(br, 3) + 3*pow(br, 5) - 2*pow(br, 3) + 3*br)
# test1 = 2*(2*(bi**5)*br + 3*(bi**4)*br + 4*(bi**3)*(br**3) - 6*(bi**3)*br + 6*(bi**2)*(br**3) - 2*(bi**2)*br + 2*bi*(br**5) - 6*bi*(br**3) + 3*(br**5) - 2*(br**3) + 3*br)

# # Imag part: 2*(I*pow(bi, 6) + 3*I*pow(bi, 5) + I*pow(bi, 4)*pow(br, 2) - 3*I*pow(bi, 4) + 6*I*pow(bi, 3)*pow(br, 2) - 2*I*pow(bi, 3) - I*pow(bi, 2)*pow(br, 4) - 3*I*pow(bi, 2) + 3*I*bi*pow(br, 4) - 2*I*bi*pow(br, 2) + 3*I*bi - I*pow(br, 6) + 3*I*pow(br, 4) - 3*I*pow(br, 2) + I)
# #            2*(pow(bi, 6) + 3*pow(bi, 5) + pow(bi, 4)*pow(br, 2) - 3*pow(bi, 4) + 6*pow(bi, 3)*pow(br, 2) - 2*pow(bi, 3) - pow(bi, 2)*pow(br, 4) - 3*pow(bi, 2) + 3*bi*pow(br, 4) - 2*bi*pow(br, 2) + 3*bi - pow(br, 6) + 3*pow(br, 4) - 3*pow(br, 2) + 1)
# test2 = 2*I*((bi**6) + 3*(bi**5) + (bi**4)*(br**2) - 3*(bi**4) + 6*(bi**3)*(br**2) - 2*(bi**3) - (bi**2)*(br**4) - 3*(bi**2) + 3*bi*(br**4) - 2*bi*(br**2) + 3*bi - (br**6) + 3*(br**4) - 3*(br**2) + 1)

# print ccode(denom2)
# # 4*(pow(bi, 6) + 3*pow(bi, 4)*pow(br, 2) - 2*pow(bi, 3) + 3*pow(bi, 2)*pow(br, 4) - 2*bi*pow(br, 2) + pow(br, 6) + 1)
# testdenom = 4*((bi**6) + 3*(bi**4)*(br**2) - 2*(bi**3) + 3*(bi**2)*(br**4) - 2*bi*(br**2) + (br**6) + 1)

# print ((test1 + test2)/testdenom - numer2/denom2).simplify()

###############

print ccode(numer2)
# (-I*pow(bi, 4) - 2*pow(bi, 3)*br + 4*I*pow(bi, 3) + 2*pow(bi, 2)*br - 2*I*pow(bi, 2) - 2*bi*pow(br, 3) + 8*I*bi*pow(br, 2) + 2*bi*br + 12*I*bi + I*pow(br, 4) + 6*pow(br, 3) - 4*I*pow(br, 2) + 14*br + 3*I)/(pow(bi, 2) - 6*bi + pow(br, 2) + 9)
test0 = (-I*(bi**4) - 2*(bi**3)*br + 4*I*(bi**3) + 2*(bi**2)*br - 2*I*(bi**2) - 2*bi*(br**3) + 8*I*bi*(br**2) + 2*bi*br + 12*I*bi + I*(br**4) + 6*(br**3) - 4*I*(br**2) + 14*br + 3*I)

# Real part: (-2*pow(bi, 3)*br + 2*pow(bi, 2)*br - 2*bi*pow(br, 3) + 2*bi*br + 6*pow(br, 3) + 14*br)
test1 = (-2*(bi**3)*br + 2*(bi**2)*br - 2*bi*(br**3) + 2*bi*br + 6*(br**3) + 14*br)

# Imag part: (-I*pow(bi, 4) + 4*I*pow(bi, 3) - 2*I*pow(bi, 2) + 8*I*bi*pow(br, 2) + 12*I*bi + I*pow(br, 4) - 4*I*pow(br, 2) + 3*I)
#            (-pow(bi, 4) + 4*pow(bi, 3) - 2*pow(bi, 2) + 8*bi*pow(br, 2) + 12*bi + pow(br, 4) - 4*pow(br, 2) + 3)
test2 = (-(bi**4) + 4*(bi**3) - 2*(bi**2) + 8*bi*(br**2) + 12*bi + (br**4) - 4*(br**2) + 3)

print ccode(denom2)
# (pow(bi, 4) + 2*pow(bi, 2)*pow(br, 2) + 6*pow(bi, 2) + pow(br, 4) + 10*pow(br, 2) + 9)
testdenom = ((bi**4) + 2*(bi**2)*(br**2) + 6*(bi**2) + (br**4) + 10*(br**2) + 9)

print ((test1 + I*test2)/testdenom - numer2/denom2).simplify()

###############

print ccode(numer2)
# (-I*pow(bi, 4) - 2*pow(bi, 3)*br - 2*pow(bi, 2)*br + 6*I*pow(bi, 2) - 2*bi*pow(br, 3) + 4*I*bi*pow(br, 2) + 10*bi*br - 8*I*bi + I*pow(br, 4) + 2*pow(br, 3) - 4*I*pow(br, 2) - 6*br + 3*I)
test0 = (-I*(bi**4) - 2*(bi**3)*br - 2*(bi**2)*br + 6*I*(bi**2) - 2*bi*(br**3) + 4*I*bi*(br**2) + 10*bi*br - 8*I*bi + I*(br**4) + 2*(br**3) - 4*I*(br**2) - 6*br + 3*I)

# Real part: (-2*pow(bi, 3)*br - 2*pow(bi, 2)*br - 2*bi*pow(br, 3) + 10*bi*br + 2*pow(br, 3) - 6*br)
test1 = (-2*(bi**3)*br - 2*(bi**2)*br - 2*bi*(br**3) + 10*bi*br + 2*(br**3) - 6*br)

# Imag part: (-I*pow(bi, 4) + 6*I*pow(bi, 2) + 4*I*bi*pow(br, 2) - 8*I*bi + I*pow(br, 4) - 4*I*pow(br, 2) + 3*I)
#            (-pow(bi, 4) + 6*pow(bi, 2) + 4*bi*pow(br, 2) - 8*bi + pow(br, 4) - 4*pow(br, 2) + 3)
test2 = (-(bi**4) + 6*(bi**2) + 4*bi*(br**2) - 8*bi + (br**4) - 4*(br**2) + 3)

print ccode(denom2)
# (pow(bi, 4) + 4*pow(bi, 3) + 2*pow(bi, 2)*pow(br, 2) - 2*pow(bi, 2) + 4*bi*pow(br, 2) - 12*bi + pow(br, 4) - 6*pow(br, 2) + 9)
testdenom = ((bi**4) + 4*(bi**3) + 2*(bi**2)*(br**2) - 2*(bi**2) + 4*bi*(br**2) - 12*bi + (br**4) - 6*(br**2) + 9)

print ((test1 + I*test2)/testdenom - numer2/denom2).simplify()

###############

print ccode(numer2)
# 3*(I*pow(bi, 6) + 2*pow(bi, 5)*br - 2*I*pow(bi, 5) + I*pow(bi, 4)*pow(br, 2) - 2*pow(bi, 4)*br - I*pow(bi, 4) + 4*pow(bi, 3)*pow(br, 3) - 4*I*pow(bi, 3)*pow(br, 2) - 4*pow(bi, 3)*br + 4*I*pow(bi, 3) - I*pow(bi, 2)*pow(br, 4) - 4*pow(bi, 2)*pow(br, 3) + 2*I*pow(bi, 2)*pow(br, 2) + 4*pow(bi, 2)*br - I*pow(bi, 2) + 2*bi*pow(br, 5) - 2*I*bi*pow(br, 4) - 4*bi*pow(br, 3) + 4*I*bi*pow(br, 2) + 2*bi*br - 2*I*bi - I*pow(br, 6) - 2*pow(br, 5) + 3*I*pow(br, 4) + 4*pow(br, 3) - 3*I*pow(br, 2) - 2*br + I)
test0 = 3*(I*pow(bi, 6) + 2*pow(bi, 5)*br - 2*I*pow(bi, 5) + I*pow(bi, 4)*pow(br, 2) - 2*pow(bi, 4)*br - I*pow(bi, 4) + 4*pow(bi, 3)*pow(br, 3) - 4*I*pow(bi, 3)*pow(br, 2) - 4*pow(bi, 3)*br + 4*I*pow(bi, 3) - I*pow(bi, 2)*pow(br, 4) - 4*pow(bi, 2)*pow(br, 3) + 2*I*pow(bi, 2)*pow(br, 2) + 4*pow(bi, 2)*br - I*pow(bi, 2) + 2*bi*pow(br, 5) - 2*I*bi*pow(br, 4) - 4*bi*pow(br, 3) + 4*I*bi*pow(br, 2) + 2*bi*br - 2*I*bi - I*pow(br, 6) - 2*pow(br, 5) + 3*I*pow(br, 4) + 4*pow(br, 3) - 3*I*pow(br, 2) - 2*br + I)

# Real part: 3*(2*pow(bi, 5)*br - 2*pow(bi, 4)*br + 4*pow(bi, 3)*pow(br, 3) - 4*pow(bi, 3)*br - 4*pow(bi, 2)*pow(br, 3) + 4*pow(bi, 2)*br + 2*bi*pow(br, 5) - 4*bi*pow(br, 3) + 2*bi*br - 2*pow(br, 5) + 4*pow(br, 3) - 2*br)
test1 = 3*(2*pow(bi, 5)*br - 2*pow(bi, 4)*br + 4*pow(bi, 3)*pow(br, 3) - 4*pow(bi, 3)*br - 4*pow(bi, 2)*pow(br, 3) + 4*pow(bi, 2)*br + 2*bi*pow(br, 5) - 4*bi*pow(br, 3) + 2*bi*br - 2*pow(br, 5) + 4*pow(br, 3) - 2*br)

# Imag part: 3*(I*pow(bi, 6) - 2*I*pow(bi, 5) + I*pow(bi, 4)*pow(br, 2) - I*pow(bi, 4) - 4*I*pow(bi, 3)*pow(br, 2) + 4*I*pow(bi, 3) - I*pow(bi, 2)*pow(br, 4) + 2*I*pow(bi, 2)*pow(br, 2) - I*pow(bi, 2) - 2*I*bi*pow(br, 4) + 4*I*bi*pow(br, 2) - 2*I*bi - I*pow(br, 6) + 3*I*pow(br, 4) - 3*I*pow(br, 2) + I)
#            3*(pow(bi, 6) - 2*pow(bi, 5) + pow(bi, 4)*pow(br, 2) - pow(bi, 4) - 4*pow(bi, 3)*pow(br, 2) + 4*pow(bi, 3) - pow(bi, 2)*pow(br, 4) + 2*pow(bi, 2)*pow(br, 2) - pow(bi, 2) - 2*bi*pow(br, 4) + 4*bi*pow(br, 2) - 2*bi - pow(br, 6) + 3*pow(br, 4) - 3*pow(br, 2) + 1)
test2 = 3*(pow(bi, 6) - 2*pow(bi, 5) + pow(bi, 4)*pow(br, 2) - pow(bi, 4) - 4*pow(bi, 3)*pow(br, 2) + 4*pow(bi, 3) - pow(bi, 2)*pow(br, 4) + 2*pow(bi, 2)*pow(br, 2) - pow(bi, 2) - 2*bi*pow(br, 4) + 4*bi*pow(br, 2) - 2*bi - pow(br, 6) + 3*pow(br, 4) - 3*pow(br, 2) + 1)

print ccode(denom2)
# 9*(pow(bi, 6) - 2*pow(bi, 5) + 3*pow(bi, 4)*pow(br, 2) - pow(bi, 4) - 4*pow(bi, 3)*pow(br, 2) + 4*pow(bi, 3) + 3*pow(bi, 2)*pow(br, 4) - 2*pow(bi, 2)*pow(br, 2) - pow(bi, 2) - 2*bi*pow(br, 4) + 4*bi*pow(br, 2) - 2*bi + pow(br, 6) - pow(br, 4) - pow(br, 2) + 1)
testdenom = 9*(pow(bi, 6) - 2*pow(bi, 5) + 3*pow(bi, 4)*pow(br, 2) - pow(bi, 4) - 4*pow(bi, 3)*pow(br, 2) + 4*pow(bi, 3) + 3*pow(bi, 2)*pow(br, 4) - 2*pow(bi, 2)*pow(br, 2) - pow(bi, 2) - 2*bi*pow(br, 4) + 4*bi*pow(br, 2) - 2*bi + pow(br, 6) - pow(br, 4) - pow(br, 2) + 1)

print ((test1 + I*test2)/testdenom - numer2/denom2).simplify()
