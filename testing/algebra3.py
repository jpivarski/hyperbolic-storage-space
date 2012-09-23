from sympy import Symbol, solve, sqrt, exp, sin, cos, tan, I, re, im
from sympy.printing.ccode import ccode

pone = Symbol("pone", "real")   # it doesn't really belive that they're real...
Br = Symbol("Br", "real")
Bi = Symbol("Bi", "real")
dBr = Symbol("dBr", "real")
dBi = Symbol("dBi", "real")
Pr = Symbol("Pr", "real")
Pi = Symbol("Pi", "real")
Fr = Symbol("Fr", "real")
Fi = Symbol("Fi", "real")
Rr = Symbol("Rr", "real")
Ri = Symbol("Ri", "real")

# print re(((Pr + I*Pi) + (Br + I*Bi)*pone) / ((Br - I*Bi)*(Pr + I*Pi) + pone)).simplify()

# numerator
print ccode((((Pr + I*Pi) + (Br + I*Bi)*sqrt(Pr*Pr + Pi*Pi + 1)) * ((Br + I*Bi)*(Pr - I*Pi) + sqrt(Pr*Pr + Pi*Pi + 1))).expand())
# I*Bi*Bi*Pi*pone - Bi*Bi*Pr*pone + 2*Bi*Br*Pi*pone + 2*I*Bi*Br*Pr*pone + I*Bi*Pi*Pi + I*Bi*Pr*Pr + I*Bi*(Pi*Pi + Pr*Pr + 1) - I*Br*Br*Pi*pone + Br*Br*Pr*pone + Br*Pi*Pi + Br*Pr*Pr + Br*(Pi*Pi + Pr*Pr + 1) + I*Pi*pone + Pr*pone

# Real part: -Bi*Bi*Pr*pone + 2*Bi*Br*Pi*pone + Br*Br*Pr*pone + Br*Pi*Pi + Br*Pr*Pr + Br*(Pi*Pi + Pr*Pr + 1) + Pr*pone
# Imag part: I*Bi*Bi*Pi*pone + 2*I*Bi*Br*Pr*pone + I*Bi*Pi*Pi + I*Bi*Pr*Pr + I*Bi*(Pi*Pi + Pr*Pr + 1) - I*Br*Br*Pi*pone + I*Pi*pone

# denominator
print ccode((((Br - I*Bi)*(Pr + I*Pi) + sqrt(Pr*Pr + Pi*Pi + 1)) * ((Br + I*Bi)*(Pr - I*Pi) + sqrt(Pr*Pr + Pi*Pi + 1))).expand())
# Bi*Bi*Pi*Pi + Bi*Bi*Pr*Pr + 2*Bi*Pi*pone + Br*Br*Pi*Pi + Br*Br*Pr*Pr + 2*Br*Pr*pone + Pi*Pi + Pr*Pr + 1

### START EXTENDING B TO THE WHOLE PLANE

# numerator
print ccode(((sqrt(1 + Br*Br + Bi*Bi)*(Pr + I*Pi) + (Br + I*Bi)*sqrt(Pr*Pr + Pi*Pi + 1)) * ((Br + I*Bi)*(Pr - I*Pi) + sqrt(1 + Br*Br + Bi*Bi)*sqrt(Pr*Pr + Pi*Pi + 1))).expand())
# I*Bi*Bi*Pi*pone - Bi*Bi*Pr*pone + 2*Bi*Br*Pi*pone + 2*I*Bi*Br*Pr*pone + I*Bi*Pi*Pi*bone + I*Bi*Pr*Pr*bone + I*Bi*bone*(Pi*Pi + Pr*Pr + 1) - I*Br*Br*Pi*pone + Br*Br*Pr*pone + Br*Pi*Pi*bone + Br*Pr*Pr*bone + Br*bone*(Pi*Pi + Pr*Pr + 1) + I*Pi*(Bi*Bi + Br*Br + 1)*pone + Pr*(Bi*Bi + Br*Br + 1)*pone

# Real part: -Bi*Bi*Pr*pone + 2*Bi*Br*Pi*pone + Br*Br*Pr*pone + Br*Pi*Pi*bone + Br*Pr*Pr*bone + Br*bone*(Pi*Pi + Pr*Pr + 1) + Pr*(Bi*Bi + Br*Br + 1)*pone
# Imag part: I*Bi*Bi*Pi*pone + 2*I*Bi*Br*Pr*pone + I*Bi*Pi*Pi*bone + I*Bi*Pr*Pr*bone + I*Bi*bone*(Pi*Pi + Pr*Pr + 1) - I*Br*Br*Pi*pone + I*Pi*(Bi*Bi + Br*Br + 1)*pone

# denominator
print ccode((((Br - I*Bi)*(Pr + I*Pi) + sqrt(1 + Br*Br + Bi*Bi)*sqrt(Pr*Pr + Pi*Pi + 1)) * ((Br + I*Bi)*(Pr - I*Pi) + sqrt(1 + Br*Br + Bi*Bi)*sqrt(Pr*Pr + Pi*Pi + 1))).expand())
# Bi*Bi*Pi*Pi + Bi*Bi*Pr*Pr + 2*Bi*Pi*bone*pone + Br*Br*Pi*Pi + Br*Br*Pr*Pr + 2*Br*Pr*bone*pone + (Bi*Bi + Br*Br + 1)*(Pi*Pi + Pr*Pr + 1)

### END EXTENDING B TO THE WHOLE PLANE

######################################################################

solution = solve([Br*Pr*Fr - Br*Pi*Fi + Bi*Pr*Fi + Bi*Pi*Fr - Br*sqrt(Pr*Pr + Pi*Pi + 1) + + Fr*sqrt(Pr*Pr + Pi*Pi + 1) - Pr,
                  Br*Pr*Fi + Br*Pi*Fr - Bi*Pr*Fr + Bi*Pi*Fi - Bi*sqrt(Pr*Pr + Pi*Pi + 1) + Fi*sqrt(Pr*Pr + Pi*Pi + 1) - Pi],
                 [Br, Bi])

print solution[Br]
# -(Fi*Pr + Fr*Pi)*(-Fi*(Pi**2 + Pr**2 + 1)**(1/2) + Pi - (Fi*Pr + Fr*Pi)*(-Fr*(Pi**2 + Pr**2 + 1)**(1/2) + Pr)/(-Fi*Pi + Fr*Pr - (Pi**2 + Pr**2 + 1)**(1/2)))/((-Fi*Pi + Fr*Pr - (Pi**2 + Pr**2 + 1)**(1/2))*(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)**2/(-Fi*Pi + Fr*Pr - (Pi**2 + Pr**2 + 1)**(1/2)) - (Pi**2 + Pr**2 + 1)**(1/2))) + (-Fr*(Pi**2 + Pr**2 + 1)**(1/2) + Pr)/(-Fi*Pi + Fr*Pr - (Pi**2 + Pr**2 + 1)**(1/2))

print solution[Bi]
# (-Fi*(Pi**2 + Pr**2 + 1)**(1/2) + Pi - (Fi*Pr + Fr*Pi)*(-Fr*(Pi**2 + Pr**2 + 1)**(1/2) + Pr)/(-Fi*Pi + Fr*Pr - (Pi**2 + Pr**2 + 1)**(1/2)))/(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)**2/(-Fi*Pi + Fr*Pr - (Pi**2 + Pr**2 + 1)**(1/2)) - (Pi**2 + Pr**2 + 1)**(1/2))

print ccode(solution[Br])
# -(Fi*Pr + Fr*Pi)*(-Fi*pone + Pi - (Fi*Pr + Fr*Pi)*(-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone))/((-Fi*Pi + Fr*Pr - pone)*(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)*(Fi*Pr + Fr*Pi)/(-Fi*Pi + Fr*Pr - pone) - pone)) + (-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone)

print ccode(solution[Bi])
# (-Fi*pone + Pi - (Fi*Pr + Fr*Pi)*(-Fr*pone + Pr)/(-Fi*Pi + Fr*Pr - pone))/(Fi*Pi - Fr*Pr - (Fi*Pr + Fr*Pi)*(Fi*Pr + Fr*Pi)/(-Fi*Pi + Fr*Pr - pone) - pone)

######################################################################

### offset

# numerator
print ccode((((dBr + I*dBi) + (Rr + I*Ri)*(Br + I*Bi)) * ((dBr - I*dBi)*(Br + I*Bi) + (Rr - I*Ri))).expand())
# -Bi*Bi*Ri*dBi - I*Bi*Bi*Ri*dBr + I*Bi*Bi*Rr*dBi - Bi*Bi*Rr*dBr + 2*I*Bi*Br*Ri*dBi - 2*Bi*Br*Ri*dBr + 2*Bi*Br*Rr*dBi + 2*I*Bi*Br*Rr*dBr + I*Bi*Ri*Ri + I*Bi*Rr*Rr + I*Bi*dBi*dBi + I*Bi*dBr*dBr + Br*Br*Ri*dBi + I*Br*Br*Ri*dBr - I*Br*Br*Rr*dBi + Br*Br*Rr*dBr + Br*Ri*Ri + Br*Rr*Rr + Br*dBi*dBi + Br*dBr*dBr + Ri*dBi - I*Ri*dBr + I*Rr*dBi + Rr*dBr

# Real part: -Bi*Bi*Ri*dBi - Bi*Bi*Rr*dBr - 2*Bi*Br*Ri*dBr + 2*Bi*Br*Rr*dBi + Br*Br*Ri*dBi + Br*Br*Rr*dBr + Br*Ri*Ri + Br*Rr*Rr + Br*dBi*dBi + Br*dBr*dBr + Ri*dBi + Rr*dBr

# Imag part: -I*Bi*Bi*Ri*dBr + I*Bi*Bi*Rr*dBi + 2*I*Bi*Br*Ri*dBi + 2*I*Bi*Br*Rr*dBr + I*Bi*Ri*Ri + I*Bi*Rr*Rr + I*Bi*dBi*dBi + I*Bi*dBr*dBr + I*Br*Br*Ri*dBr - I*Br*Br*Rr*dBi - I*Ri*dBr + I*Rr*dBi

# denominator
print ccode((((dBr + I*dBi)*(Br - I*Bi) + (Rr + I*Ri)) * ((dBr - I*dBi)*(Br + I*Bi) + (Rr - I*Ri))).expand())
# Bi*Bi*dBi*dBi + Bi*Bi*dBr*dBr - 2*Bi*Ri*dBr + 2*Bi*Rr*dBi + Br*Br*dBi*dBi + Br*Br*dBr*dBr + 2*Br*Ri*dBi + 2*Br*Rr*dBr + Ri*Ri + Rr*Rr

### rotation

# numerator
print ccode((((Rr + I*Ri) + (dBr + I*dBi)*(Br - I*Bi)) * ((Rr - I*Ri)*(dBr + I*dBi)*(Br - I*Bi) + 1)).expand())
# -I*Bi*Bi*Ri*dBi*dBi - 2*Bi*Bi*Ri*dBi*dBr + I*Bi*Bi*Ri*dBr*dBr + Bi*Bi*Rr*dBi*dBi - 2*I*Bi*Bi*Rr*dBi*dBr - Bi*Bi*Rr*dBr*dBr + 2*Bi*Br*Ri*dBi*dBi - 4*I*Bi*Br*Ri*dBi*dBr - 2*Bi*Br*Ri*dBr*dBr + 2*I*Bi*Br*Rr*dBi*dBi + 4*Bi*Br*Rr*dBi*dBr - 2*I*Bi*Br*Rr*dBr*dBr + Bi*Ri*Ri*dBi - I*Bi*Ri*Ri*dBr + Bi*Rr*Rr*dBi - I*Bi*Rr*Rr*dBr + Bi*dBi - I*Bi*dBr + I*Br*Br*Ri*dBi*dBi + 2*Br*Br*Ri*dBi*dBr - I*Br*Br*Ri*dBr*dBr - Br*Br*Rr*dBi*dBi + 2*I*Br*Br*Rr*dBi*dBr + Br*Br*Rr*dBr*dBr + I*Br*Ri*Ri*dBi + Br*Ri*Ri*dBr + I*Br*Rr*Rr*dBi + Br*Rr*Rr*dBr + I*Br*dBi + Br*dBr + I*Ri + Rr

# Real part: -2*Bi*Bi*Ri*dBi*dBr + Bi*Bi*Rr*dBi*dBi - Bi*Bi*Rr*dBr*dBr + 2*Bi*Br*Ri*dBi*dBi - 2*Bi*Br*Ri*dBr*dBr + 4*Bi*Br*Rr*dBi*dBr + Bi*Ri*Ri*dBi + Bi*Rr*Rr*dBi + Bi*dBi + 2*Br*Br*Ri*dBi*dBr - Br*Br*Rr*dBi*dBi + Br*Br*Rr*dBr*dBr + Br*Ri*Ri*dBr + Br*Rr*Rr*dBr + Br*dBr + Rr

# Imag part: -I*Bi*Bi*Ri*dBi*dBi + I*Bi*Bi*Ri*dBr*dBr - 2*I*Bi*Bi*Rr*dBi*dBr - 4*I*Bi*Br*Ri*dBi*dBr + 2*I*Bi*Br*Rr*dBi*dBi - 2*I*Bi*Br*Rr*dBr*dBr - I*Bi*Ri*Ri*dBr - I*Bi*Rr*Rr*dBr - I*Bi*dBr + I*Br*Br*Ri*dBi*dBi - I*Br*Br*Ri*dBr*dBr + 2*I*Br*Br*Rr*dBi*dBr + I*Br*Ri*Ri*dBi + I*Br*Rr*Rr*dBi + I*Br*dBi + I*Ri

# denominator
print ccode((((Rr + I*Ri)*(dBr - I*dBi)*(Br + I*Bi) + 1) * ((Rr - I*Ri)*(dBr + I*dBi)*(Br - I*Bi) + 1)).expand())
# Bi*Bi*Ri*Ri*dBi*dBi + Bi*Bi*Ri*Ri*dBr*dBr + Bi*Bi*Rr*Rr*dBi*dBi + Bi*Bi*Rr*Rr*dBr*dBr - 2*Bi*Ri*dBr + 2*Bi*Rr*dBi + Br*Br*Ri*Ri*dBi*dBi + Br*Br*Ri*Ri*dBr*dBr + Br*Br*Rr*Rr*dBi*dBi + Br*Br*Rr*Rr*dBr*dBr + 2*Br*Ri*dBi + 2*Br*Rr*dBr + 1

### START EXTENDING B TO THE WHOLE PLANE

# offset numerator
print ccode((((dBr + I*dBi)*sqrt(1 - Br*Br - Bi*Bi) + (Rr + I*Ri)*(Br + I*Bi)*sqrt(1 - dBr*dBr - dBi*dBi)) * ((dBr - I*dBi)*(Br + I*Bi) + (Rr - I*Ri)*sqrt(1 - dBr*dBr - dBi*dBi)*sqrt(1 - Br*Br - Bi*Bi))).expand())
# -Bi*Bi*Ri*dBi*dBone - I*Bi*Bi*Ri*dBr*dBone + I*Bi*Bi*Rr*dBi*dBone - Bi*Bi*Rr*dBr*dBone + 2*I*Bi*Br*Ri*dBi*dBone - 2*Bi*Br*Ri*dBr*dBone + 2*Bi*Br*Rr*dBi*dBone + 2*I*Bi*Br*Rr*dBr*dBone + I*Bi*Ri*Ri*Bone*dBone*dBone + I*Bi*Rr*Rr*Bone*dBone*dBone + I*Bi*dBi*dBi*Bone + I*Bi*dBr*dBr*Bone + Br*Br*Ri*dBi*dBone + I*Br*Br*Ri*dBr*dBone - I*Br*Br*Rr*dBi*dBone + Br*Br*Rr*dBr*dBone + Br*Ri*Ri*Bone*dBone*dBone + Br*Rr*Rr*Bone*dBone*dBone + Br*dBi*dBi*Bone + Br*dBr*dBr*Bone + Ri*dBi*Bone*Bone*dBone - I*Ri*dBr*Bone*Bone*dBone + I*Rr*dBi*Bone*Bone*dBone + Rr*dBr*Bone*Bone*dBone

# Real part: -Bi*Bi*Ri*dBi*dBone - Bi*Bi*Rr*dBr*dBone - 2*Bi*Br*Ri*dBr*dBone + 2*Bi*Br*Rr*dBi*dBone + Br*Br*Ri*dBi*dBone + Br*Br*Rr*dBr*dBone + Br*Ri*Ri*Bone*dBone*dBone + Br*Rr*Rr*Bone*dBone*dBone + Br*dBi*dBi*Bone + Br*dBr*dBr*Bone + Ri*dBi*Bone*Bone*dBone + Rr*dBr*Bone*Bone*dBone

# Imag part: -Bi*Bi*Ri*dBr*dBone + Bi*Bi*Rr*dBi*dBone + 2*Bi*Br*Ri*dBi*dBone + 2*Bi*Br*Rr*dBr*dBone + Bi*Ri*Ri*Bone*dBone*dBone + Bi*Rr*Rr*Bone*dBone*dBone + Bi*dBi*dBi*Bone + Bi*dBr*dBr*Bone + Br*Br*Ri*dBr*dBone - Br*Br*Rr*dBi*dBone - Ri*dBr*Bone*Bone*dBone + Rr*dBi*Bone*Bone*dBone

# offset denominator
print ccode((((dBr + I*dBi)*(Br - I*Bi) + (Rr + I*Ri)*sqrt(1 - dBr*dBr - dBi*dBi)*sqrt(1 - Br*Br - Bi*Bi)) * ((dBr - I*dBi)*(Br + I*Bi) + (Rr - I*Ri)*sqrt(1 - dBr*dBr - dBi*dBi)*sqrt(1 - Br*Br - Bi*Bi))).expand())
# Bi*Bi*dBi*dBi + Bi*Bi*dBr*dBr - 2*Bi*Ri*dBr*Bone*dBone + 2*Bi*Rr*dBi*Bone*dBone + Br*Br*dBi*dBi + Br*Br*dBr*dBr + 2*Br*Ri*dBi*Bone*dBone + 2*Br*Rr*dBr*Bone*dBone + Ri*Ri*Bone*Bone*dBone*dBone + Rr*Rr*Bone*Bone*dBone*dBone

# rotation numerator
print ccode((((Rr + I*Ri)*sqrt(1 - dBr*dBr - dBi*dBi)*sqrt(1 - Br*Br - Bi*Bi) + (dBr + I*dBi)*(Br - I*Bi)) * ((Rr - I*Ri)*(dBr + I*dBi)*(Br - I*Bi) + sqrt(1 - dBr*dBr - dBi*dBi)*sqrt(1 - Br*Br - Bi*Bi))).expand())
# -I*Bi*Bi*Ri*dBi*dBi - 2*Bi*Bi*Ri*dBi*dBr + I*Bi*Bi*Ri*dBr*dBr + Bi*Bi*Rr*dBi*dBi - 2*I*Bi*Bi*Rr*dBi*dBr - Bi*Bi*Rr*dBr*dBr + 2*Bi*Br*Ri*dBi*dBi - 4*I*Bi*Br*Ri*dBi*dBr - 2*Bi*Br*Ri*dBr*dBr + 2*I*Bi*Br*Rr*dBi*dBi + 4*Bi*Br*Rr*dBi*dBr - 2*I*Bi*Br*Rr*dBr*dBr + Bi*Ri*Ri*dBi*Bone*dBone - I*Bi*Ri*Ri*dBr*Bone*dBone + Bi*Rr*Rr*dBi*Bone*dBone - I*Bi*Rr*Rr*dBr*Bone*dBone + Bi*dBi*Bone*dBone - I*Bi*dBr*Bone*dBone + I*Br*Br*Ri*dBi*dBi + 2*Br*Br*Ri*dBi*dBr - I*Br*Br*Ri*dBr*dBr - Br*Br*Rr*dBi*dBi + 2*I*Br*Br*Rr*dBi*dBr + Br*Br*Rr*dBr*dBr + I*Br*Ri*Ri*dBi*Bone*dBone + Br*Ri*Ri*dBr*Bone*dBone + I*Br*Rr*Rr*dBi*Bone*dBone + Br*Rr*Rr*dBr*Bone*dBone + I*Br*dBi*Bone*dBone + Br*dBr*Bone*dBone + I*Ri*Bone*Bone*dBone*dBone + Rr*Bone*Bone*dBone*dBone

# Real part: -2*Bi*Bi*Ri*dBi*dBr + Bi*Bi*Rr*dBi*dBi - Bi*Bi*Rr*dBr*dBr + 2*Bi*Br*Ri*dBi*dBi - 2*Bi*Br*Ri*dBr*dBr + 4*Bi*Br*Rr*dBi*dBr + Bi*Ri*Ri*dBi*Bone*dBone + Bi*Rr*Rr*dBi*Bone*dBone + Bi*dBi*Bone*dBone + 2*Br*Br*Ri*dBi*dBr - Br*Br*Rr*dBi*dBi + Br*Br*Rr*dBr*dBr + Br*Ri*Ri*dBr*Bone*dBone + Br*Rr*Rr*dBr*Bone*dBone + Br*dBr*Bone*dBone + Rr*Bone*Bone*dBone*dBone

# Imag part: -Bi*Bi*Ri*dBi*dBi + Bi*Bi*Ri*dBr*dBr - 2*Bi*Bi*Rr*dBi*dBr - 4*Bi*Br*Ri*dBi*dBr + 2*Bi*Br*Rr*dBi*dBi - 2*Bi*Br*Rr*dBr*dBr - Bi*Ri*Ri*dBr*Bone*dBone - Bi*Rr*Rr*dBr*Bone*dBone - Bi*dBr*Bone*dBone + Br*Br*Ri*dBi*dBi - Br*Br*Ri*dBr*dBr + 2*Br*Br*Rr*dBi*dBr + Br*Ri*Ri*dBi*Bone*dBone + Br*Rr*Rr*dBi*Bone*dBone + Br*dBi*Bone*dBone + Ri*Bone*Bone*dBone*dBone

# rotation denominator
print ccode((((Rr + I*Ri)*(dBr - I*dBi)*(Br + I*Bi) + sqrt(1 - dBr*dBr - dBi*dBi)*sqrt(1 - Br*Br - Bi*Bi)) * ((Rr - I*Ri)*(dBr + I*dBi)*(Br - I*Bi) + sqrt(1 - dBr*dBr - dBi*dBi)*sqrt(1 - Br*Br - Bi*Bi))).expand())
# Bi*Bi*Ri*Ri*dBi*dBi + Bi*Bi*Ri*Ri*dBr*dBr + Bi*Bi*Rr*Rr*dBi*dBi + Bi*Bi*Rr*Rr*dBr*dBr - 2*Bi*Ri*dBr*Bone*dBone + 2*Bi*Rr*dBi*Bone*dBone + Br*Br*Ri*Ri*dBi*dBi + Br*Br*Ri*Ri*dBr*dBr + Br*Br*Rr*Rr*dBi*dBi + Br*Br*Rr*Rr*dBr*dBr + 2*Br*Ri*dBi*Bone*dBone + 2*Br*Rr*dBr*Bone*dBone + Bone*Bone*dBone*dBone

### END EXTENDING B TO THE WHOLE PLANE

######################################################################

# ((1 - I*bbar)*a*eff + (-bee + I))/((I - bbar)*a*eff + (-I*bee + 1))

Br = Symbol("Br", "real")
Bi = Symbol("Bi", "real")
Fr = Symbol("Fr", "real")  # a cos(phi)
Fi = Symbol("Fi", "real")  # a sin(phi)
a = Symbol("a", "real")
phi = Symbol("phi", "real")

# numerator
print ccode((((1 - I*(Br - I*Bi))*(Fr + I*Fi) + (-(Br + I*Bi) + I)) * ((-I - (Br + I*Bi))*(Fr - I*Fi) + (I*(Br - I*Bi) + 1))).expand())

# I*Bi*Bi*Fi*Fi + I*Bi*Bi*Fr*Fr - 2*Bi*Bi*Fr - I*Bi*Bi + 4*Bi*Br*Fi + I*Br*Br*Fi*Fi + I*Br*Br*Fr*Fr + 2*Br*Br*Fr - I*Br*Br - 2*Br*Fi*Fi - 2*Br*Fr*Fr - 2*Br - I*Fi*Fi - I*Fr*Fr + 2*Fr + I

# Real part: -2*Bi*Bi*Fr + 4*Bi*Br*Fi + 2*Br*Br*Fr - 2*Br*Fi*Fi - 2*Br*Fr*Fr - 2*Br + 2*Fr
print ccode((-2*Bi*Bi*a*cos(phi) + 4*Bi*Br*a*sin(phi) + 2*Br*Br*a*cos(phi) - 2*Br*a*sin(phi)*a*sin(phi) - 2*Br*a*cos(phi)*a*cos(phi) - 2*Br + 2*a*cos(phi)).simplify())
# -2*Bi*Bi*a*cos(phi) + 4*Bi*Br*a*sin(phi) + 2*Br*Br*a*cos(phi) - 2*Br*a*a - 2*Br + 2*a*cos(phi)

# Imag part: I*Bi*Bi*Fi*Fi + I*Bi*Bi*Fr*Fr - I*Bi*Bi + I*Br*Br*Fi*Fi + I*Br*Br*Fr*Fr - I*Br*Br - I*Fi*Fi - I*Fr*Fr + I
print ccode((I*Bi*Bi*a*sin(phi)*a*sin(phi) + I*Bi*Bi*a*cos(phi)*a*cos(phi) - I*Bi*Bi + I*Br*Br*a*sin(phi)*a*sin(phi) + I*Br*Br*a*cos(phi)*a*cos(phi) - I*Br*Br - I*a*sin(phi)*a*sin(phi) - I*a*cos(phi)*a*cos(phi) + I).simplify())
# I*(Bi*Bi*a*a - Bi*Bi + Br*Br*a*a - Br*Br - a*a + 1)

# denominator 
print ccode((((I - (Br - I*Bi))*(Fr + I*Fi) + (-I*(Br + I*Bi) + 1)) * ((-I - (Br + I*Bi))*(Fr - I*Fi) + (I*(Br - I*Bi) + 1))).expand())

# Bi*Bi*Fi*Fi - 2*Bi*Bi*Fi + Bi*Bi*Fr*Fr + Bi*Bi - 4*Bi*Br*Fr + 2*Bi*Fi*Fi - 4*Bi*Fi + 2*Bi*Fr*Fr + 2*Bi + Br*Br*Fi*Fi + 2*Br*Br*Fi + Br*Br*Fr*Fr + Br*Br - 4*Br*Fr + Fi*Fi - 2*Fi + Fr*Fr + 1

print ccode((Bi*Bi*a*sin(phi)*a*sin(phi) - 2*Bi*Bi*a*sin(phi) + Bi*Bi*a*cos(phi)*a*cos(phi) + Bi*Bi - 4*Bi*Br*a*cos(phi) + 2*Bi*a*sin(phi)*a*sin(phi) - 4*Bi*a*sin(phi) + 2*Bi*a*cos(phi)*a*cos(phi) + 2*Bi + Br*Br*a*sin(phi)*a*sin(phi) + 2*Br*Br*a*sin(phi) + Br*Br*a*cos(phi)*a*cos(phi) + Br*Br - 4*Br*a*cos(phi) + a*sin(phi)*a*sin(phi) - 2*a*sin(phi) + a*cos(phi)*a*cos(phi) + 1).simplify())
# Bi*Bi*a*a - 2*Bi*Bi*a*sin(phi) + Bi*Bi - 4*Bi*Br*a*cos(phi) + 2*Bi*a*a - 4*Bi*a*sin(phi) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*sin(phi) + Br*Br - 4*Br*a*cos(phi) + a*a - 2*a*sin(phi) + 1


# derivative of x
print ((-2*Bi*Bi*a*cos(phi) + 4*Bi*Br*a*sin(phi) + 2*Br*Br*a*cos(phi) - 2*Br*a*a - 2*Br + 2*a*cos(phi)) / (Bi*Bi*a*a - 2*Bi*Bi*a*sin(phi) + Bi*Bi - 4*Bi*Br*a*cos(phi) + 2*Bi*a*a - 4*Bi*a*sin(phi) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*sin(phi) + Br*Br - 4*Br*a*cos(phi) + a*a - 2*a*sin(phi) + 1)).diff(phi)
# (2*Bi**2*a*sin(phi) + 4*Bi*Br*a*cos(phi) - 2*Br**2*a*sin(phi) - 2*a*sin(phi))/(Bi**2*a**2 - 2*Bi**2*a*sin(phi) + Bi**2 - 4*Bi*Br*a*cos(phi) + 2*Bi*a**2 - 4*Bi*a*sin(phi) + 2*Bi + Br**2*a**2 + 2*Br**2*a*sin(phi) + Br**2 - 4*Br*a*cos(phi) + a**2 - 2*a*sin(phi) + 1) + (-2*Bi**2*a*cos(phi) + 4*Bi*Br*a*sin(phi) + 2*Br**2*a*cos(phi) - 2*Br*a**2 - 2*Br + 2*a*cos(phi))*(2*Bi**2*a*cos(phi) - 4*Bi*Br*a*sin(phi) + 4*Bi*a*cos(phi) - 2*Br**2*a*cos(phi) - 4*Br*a*sin(phi) + 2*a*cos(phi))/(Bi**2*a**2 - 2*Bi**2*a*sin(phi) + Bi**2 - 4*Bi*Br*a*cos(phi) + 2*Bi*a**2 - 4*Bi*a*sin(phi) + 2*Bi + Br**2*a**2 + 2*Br**2*a*sin(phi) + Br**2 - 4*Br*a*cos(phi) + a**2 - 2*a*sin(phi) + 1)**2

# derivative of y
print ((Bi*Bi*a*a - Bi*Bi + Br*Br*a*a - Br*Br - a*a + 1) / (Bi*Bi*a*a - 2*Bi*Bi*a*sin(phi) + Bi*Bi - 4*Bi*Br*a*cos(phi) + 2*Bi*a*a - 4*Bi*a*sin(phi) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*sin(phi) + Br*Br - 4*Br*a*cos(phi) + a*a - 2*a*sin(phi) + 1)).diff(phi)
# (Bi**2*a**2 - Bi**2 + Br**2*a**2 - Br**2 - a**2 + 1)*(2*Bi**2*a*cos(phi) - 4*Bi*Br*a*sin(phi) + 4*Bi*a*cos(phi) - 2*Br**2*a*cos(phi) - 4*Br*a*sin(phi) + 2*a*cos(phi))/(Bi**2*a**2 - 2*Bi**2*a*sin(phi) + Bi**2 - 4*Bi*Br*a*cos(phi) + 2*Bi*a**2 - 4*Bi*a*sin(phi) + 2*Bi + Br**2*a**2 + 2*Br**2*a*sin(phi) + Br**2 - 4*Br*a*cos(phi) + a**2 - 2*a*sin(phi) + 1)**2

######################################################################

from cassius import *
import math

def func(phi, a=0.9, Br=-0.3, Bi=0.95):
    Fr = a*math.cos(phi)
    Fi = a*math.sin(phi)

    # denom = Bi*Bi*Fi*Fi - 2*Bi*Bi*Fi + Bi*Bi*Fr*Fr + Bi*Bi - 4*Bi*Br*Fr + 2*Bi*Fi*Fi - 4*Bi*Fi + 2*Bi*Fr*Fr + 2*Bi + Br*Br*Fi*Fi + 2*Br*Br*Fi + Br*Br*Fr*Fr + Br*Br - 4*Br*Fr + Fi*Fi - 2*Fi + Fr*Fr + 1
    # x = -2*Bi*Bi*Fr + 4*Bi*Br*Fi + 2*Br*Br*Fr - 2*Br*Fi*Fi - 2*Br*Fr*Fr - 2*Br + 2*Fr
    # y = Bi*Bi*Fi*Fi + Bi*Bi*Fr*Fr - Bi*Bi + Br*Br*Fi*Fi + Br*Br*Fr*Fr - Br*Br - Fi*Fi - Fr*Fr + 1

    denom = Bi*Bi*a*a - 2*Bi*Bi*a*math.sin(phi) + Bi*Bi - 4*Bi*Br*a*math.cos(phi) + 2*Bi*a*a - 4*Bi*a*math.sin(phi) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*math.sin(phi) + Br*Br - 4*Br*a*math.cos(phi) + a*a - 2*a*math.sin(phi) + 1
    x = -2*Bi*Bi*a*math.cos(phi) + 4*Bi*Br*a*math.sin(phi) + 2*Br*Br*a*math.cos(phi) - 2*Br*a*a - 2*Br + 2*a*math.cos(phi)
    y = Bi*Bi*a*a - Bi*Bi + Br*Br*a*a - Br*Br - a*a + 1

    return x/denom, y/denom

Br = 0.0
Bi = 0.0

xlist = []
ylist = []
for i in xrange(10000 + 1):
    phi = 2.*math.pi*i/10000
    x, y = func(phi, Br=Br, Bi=Bi)
    xlist.append(x)
    ylist.append(y)

xlist2 = []
ylist2 = []

phi = math.atan2((Bi**2 + 2*Bi - Br**2 + 1), (2*Bi*Br + 2*Br))
x1, y1 = func(phi, Br=Br, Bi=Bi)
xlist2.append(x1)
ylist2.append(y1)

phi = math.atan2(-(Bi**2 + 2*Bi - Br**2 + 1), -(2*Bi*Br + 2*Br))
x2, y2 = func(phi, Br=Br, Bi=Bi)
xlist2.append(x2)
ylist2.append(y2)

x3, y3 = (x1 + x2)/2., (y1 + y2)/2.
xlist2.append(x3)
ylist2.append(y3)

view(Overlay(Scatter(x=xlist, y=ylist, marker=None, connector="unsorted"), Scatter(x=xlist2, y=ylist2)))

######################################################################

# view(Overlay(Curve("(-2*Bi*Bi*a*cos(x) + 4*Bi*Br*a*sin(x) + 2*Br*Br*a*cos(x) - 2*Br*a*a - 2*Br + 2*a*cos(x)) / (Bi*Bi*a*a - 2*Bi*Bi*a*sin(x) + Bi*Bi - 4*Bi*Br*a*cos(x) + 2*Bi*a*a - 4*Bi*a*sin(x) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*sin(x) + Br*Br - 4*Br*a*cos(x) + a*a - 2*a*sin(x) + 1)", 0., 2.*math.pi, namespace={"Br": 0.3, "Bi": 0.5, "a": 0.95}, linecolor="red"), Curve("(Bi*Bi*a*a - Bi*Bi + Br*Br*a*a - Br*Br - a*a + 1) / (Bi*Bi*a*a - 2*Bi*Bi*a*sin(x) + Bi*Bi - 4*Bi*Br*a*cos(x) + 2*Bi*a*a - 4*Bi*a*sin(x) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*sin(x) + Br*Br - 4*Br*a*cos(x) + a*a - 2*a*sin(x) + 1)", 0., 2.*math.pi, namespace={"Br": 0.3, "Bi": 0.5, "a": 0.95}, linecolor="blue"), xmin=1., xmax=1.5))

# view(Curve("(Bi*Bi*a*a - Bi*Bi + Br*Br*a*a - Br*Br - a*a + 1) / (Bi*Bi*a*a - 2*Bi*Bi*a*sin(x) + Bi*Bi - 4*Bi*Br*a*cos(x) + 2*Bi*a*a - 4*Bi*a*sin(x) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*sin(x) + Br*Br - 4*Br*a*cos(x) + a*a - 2*a*sin(x) + 1)", 1.1, 1.3, namespace={"Br": 0.3, "Bi": 0.5, "a": 0.95}, linecolor="blue", ymin=10, ymax=12))

# view(Overlay(Curve("0", 0., 2.*math.pi), Curve("(Bi**2*a**2 - Bi**2 + Br**2*a**2 - Br**2 - a**2 + 1)*(2*Bi**2*a*cos(x) - 4*Bi*Br*a*sin(x) + 4*Bi*a*cos(x) - 2*Br**2*a*cos(x) - 4*Br*a*sin(x) + 2*a*cos(x))/(Bi**2*a**2 - 2*Bi**2*a*sin(x) + Bi**2 - 4*Bi*Br*a*cos(x) + 2*Bi*a**2 - 4*Bi*a*sin(x) + 2*Bi + Br**2*a**2 + 2*Br**2*a*sin(x) + Br**2 - 4*Br*a*cos(x) + a**2 - 2*a*sin(x) + 1)**2", 0., 2.*math.pi, namespace={"Br": 0.3, "Bi": 0.5, "a": 0.95}, linecolor="blue"), ymin=-0.1, ymax=0.1))

# view(Overlay(Curve("0", 1.1, 1.3),
#              Curve("(Bi**2*a**2 - Bi**2 + Br**2*a**2 - Br**2 - a**2 + 1)*(2*Bi**2*a*cos(x) - 4*Bi*Br*a*sin(x) + 4*Bi*a*cos(x) - 2*Br**2*a*cos(x) - 4*Br*a*sin(x) + 2*a*cos(x))/(Bi**2*a**2 - 2*Bi**2*a*sin(x) + Bi**2 - 4*Bi*Br*a*cos(x) + 2*Bi*a**2 - 4*Bi*a*sin(x) + 2*Bi + Br**2*a**2 + 2*Br**2*a*sin(x) + Br**2 - 4*Br*a*cos(x) + a**2 - 2*a*sin(x) + 1)**2", 1.1, 1.3, namespace={"Br": 0.3, "Bi": 0.5, "a": 0.95}, linecolor="blue"),
#              Curve("cos(x)*(Bi**2 + 2*Bi - Br**2 + 1) + sin(x)*(-2*Bi*Br - 2*Br)", 1.1, 1.3, namespace={"Br": 0.3, "Bi": 0.5, "a": 0.95}, linecolor="red"), ymin=-0.1, ymax=0.1))

# "(Bi**2*cos(x) - 2*Bi*Br*sin(x) + 2*Bi*cos(x) - Br**2*cos(x) - 2*Br*sin(x) + cos(x))"

# view(Overlay(Curve("cos(x)*(Bi**2 + 2*Bi - Br**2 + 1)", 0., 2.*math.pi, namespace={"Br": 0.3, "Bi": 0.5, "a": 0.95}), Curve("sin(x)*(2*Bi*Br + 2*Br)", 0., 2.*math.pi, namespace={"Br": 0.3, "Bi": 0.5, "a": 0.95})))

# print eval("math.atan2((Bi**2 + 2*Bi - Br**2 + 1), (2*Bi*Br + 2*Br))", {"Br": 0.3, "Bi": 0.5, "a": 0.95, "math": math})
# print eval("2.*math.pi - math.atan2((Bi**2 + 2*Bi - Br**2 + 1), -(2*Bi*Br + 2*Br))", {"Br": 0.3, "Bi": 0.5, "a": 0.95, "math": math})

######################################################################

# xlist = []
# ylist = []
# for i in xrange(-9, 10):
#     z = 1j

#     Br = 0.
#     Bi = 0.1*i
#     # denom = 1. - Br*Br - Bi*Bi
    
#     transformed = (z*(-1 - Bi) - Br) / (z*(-Br) + (-1 + Bi))

#     xlist.append(transformed.real)
#     ylist.append(transformed.imag)

# view(Scatter(x=xlist, y=ylist))

Br = 0.
Bi = 0.23495827345
scatters = []
for i in xrange(-19, 20):
    xlist = []
    ylist = []
    for j in xrange(-19, 20):
        z = 0.1*j + 2**(0.1*i/math.log(2))*1j
        xlist.append(z.real)
        ylist.append(z.imag)
    scatters.append(Scatter(x=xlist, y=ylist, marker=None, connector="unsorted"))

    xlist = []
    ylist = []
    for j in xrange(-19, 20):
        z = 0.1*j + 2**(0.1*i/math.log(2))*1j
        z2 = (z*(-1 - Bi) - Br) / (z*(-Br) + (-1 + Bi))
        xlist.append(z2.real)
        ylist.append(z2.imag)
    scatters.append(Scatter(x=xlist, y=ylist, marker=None, connector="unsorted", linecolor="red"))

view(Overlay(*scatters))

view(Overlay(Curve("exp(x)", 0, 10), Curve("2**(x/log(2))", 0, 10, linecolor="red", linestyle="dashed", linewidth=2)))

######################################################################

denom = (Pr**2 + Pi**2)*Br**2 + 2*Pr*Br*(1 - Bi) + (1 - Bi)**2
numer = (Pr**2 + Pi**2)*Br*(Bi - 1) - (Pr + I*Pi)*(Bi - 1)**2 + (Pr - I*Pi)*Br**2 + Br*(Bi - 1)

print numer.expand()
# -I*Bi**2*Pi - Bi**2*Pr + Bi*Br*Pi**2 + Bi*Br*Pr**2 + Bi*Br + 2*I*Bi*Pi + 2*Bi*Pr - I*Br**2*Pi + Br**2*Pr - Br*Pi**2 - Br*Pr**2 - Br - I*Pi - Pr

# Real part: -Bi*Bi*Pr + Bi*Br*Pi*Pi + Bi*Br*Pr*Pr + Bi*Br + 2*Bi*Pr + Br*Br*Pr - Br*Pi*Pi - Br*Pr*Pr - Br - Pr
# Imag part: -I*Bi*Bi*Pi + 2*I*Bi*Pi - I*Br*Br*Pi - I*Pi
