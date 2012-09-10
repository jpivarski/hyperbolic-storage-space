from sympy import Symbol, solve
from sympy.printing.ccode import ccode

Br = Symbol("Br")
Bi = Symbol("Bi")
z1r = Symbol("z1r")
z1i = Symbol("z1i")
f1r = Symbol("f1r")
f1i = Symbol("f1i")

solution = solve([Br*( f1r*z1r - f1i*z1i - 1) + Bi*(f1i*z1r + f1r*z1i) + (f1r - z1r),
                  Bi*(-f1r*z1r + f1i*z1i - 1) + Br*(f1i*z1r + f1r*z1i) + (f1i - z1i)], [Br, Bi])

print solution[Br]
# (-fi**2*zr - fr**2*zr + fr*zi**2 + fr*zr**2 - fr + zr)/(fi**2*zi**2 + fi**2*zr**2 + fr**2*zi**2 + fr**2*zr**2 - 1)

print solution[Bi]
# (-fi**2*zi + fi*zi**2 + fi*zr**2 - fi - fr**2*zi + zi)/(fi**2*zi**2 + fi**2*zr**2 + fr**2*zi**2 + fr**2*zr**2 - 1)

print ccode(solution[Br])
# (-fi*fi*zr - fr*fr*zr + fr*zi*zi + fr*zr*zr - fr + zr)/(fi*fi*zi*zi + fi*fi*zr*zr + fr*fr*zi*zi + fr*fr*zr*zr - 1)

print ccode(solution[Bi])
# (-fi*fi*zi + fi*zi*zi + fi*zr*zr - fi - fr*fr*zi + zi)/(fi*fi*zi*zi + fi*fi*zr*zr + fr*fr*zi*zi + fr*fr*zr*zr - 1)

Br = Symbol("Br")
Bi = Symbol("Bi")
Rr = Symbol("Rr")
Ri = Symbol("Ri")
z1r = Symbol("z1r")
z1i = Symbol("z1i")
f1r = Symbol("f1r")
f1i = Symbol("f1i")
z2r = Symbol("z2r")
z2i = Symbol("z2i")
f2r = Symbol("f2r")
f2i = Symbol("f2i")

eqn1 = f1r*Br*z1r + f1i*Bi*z1r + f1r*Bi*z1i - f1i*Br*z1i + f1r - z1r*Rr - Br*Rr + z1i*Ri + Bi*Ri
eqn2 = -f1r*Bi*z1r + f1i*Br*z1r + f1r*Br*z1i + f1i*Bi*z1i + f1i - z1i*Rr - Bi*Rr - z1r*Ri - Br*Ri
eqn3 = f2r*Br*z2r + f2i*Bi*z2r + f2r*Bi*z2i - f2i*Br*z2i + f2r - z2r*Rr - Br*Rr + z2i*Ri + Bi*Ri
eqn4 = -f2r*Bi*z2r + f2i*Br*z2r + f2r*Br*z2i + f2i*Bi*z2i + f2i - z2i*Rr - Bi*Rr - z2r*Ri - Br*Ri

solution2 = solve([eqn1, eqn2, eqn3, eqn4, Rr*Rr + Ri*Ri - 1], [Br, Bi, Rr, Ri])

solution2 = solve([eqn1.subs(Br, solution[Br]).subs(Bi, solution[Bi]), eqn2.subs(Br, solution[Br]).subs(Bi, solution[Bi]), eqn3.subs(Br, solution[Br]).subs(Bi, solution[Bi]), eqn4.subs(Br, solution[Br]).subs(Bi, solution[Bi]), Rr*Rr + Ri*Ri - 1], [Rr, Ri])

#################################################

a = Symbol("a")
b = Symbol("b")
x1 = Symbol("x1")
y1 = Symbol("y1")
x2 = Symbol("x2")
y2 = Symbol("y2")

solution = solve([x1**2 + y1**2 + a*x1 + b*y1 + 1, x2**2 + y2**2 + a*x2 + b*y2 + 1], [a, b])

print ccode(solution[a])
# (-x1*x1*y2 + x2*x2*y1 - y1*y1*y2 + y1*y2*y2 + y1 - y2)/(x1*y2 - x2*y1)

print ccode(solution[b])
# (x1*x1*x2 - x1*x2*x2 - x1*y2*y2 - x1 + x2*y1*y1 + x2)/(x1*y2 - x2*y1)

import random
from math import *
for i in xrange(1000):
    mag1 = random.uniform(0, 1)
    mag2 = random.uniform(0, 1)
    phi1 = random.uniform(-pi, pi)
    phi2 = random.uniform(-pi, pi)
    x1_ = mag1*cos(phi1)
    y1_ = mag1*sin(phi1)
    x2_ = mag2*cos(phi2)
    y2_ = mag2*sin(phi2)
    a_ = solution[a].subs(x1, x1_).subs(y1, y1_).subs(x2, x2_).subs(y2, y2_)
    b_ = solution[b].subs(x1, x1_).subs(y1, y1_).subs(x2, x2_).subs(y2, y2_)
    if -1. + 0.25*(a_**2 + a_**2) <= 0.:
        raise Exception("%g %g %g %g -> %g %g -> %g" % (x1_, y1_, x2_, y2_, a_, b_, -1. + 0.25*(a_**2 + a_**2)))

#################################################

x0 = Symbol("x0")
y0 = Symbol("y0")
x1 = Symbol("x1")
y1 = Symbol("y1")
x2 = Symbol("x2")
y2 = Symbol("y2")
c2 = Symbol("c2")

solution = solve([x1**2 - 2*x1*x0 + y1**2 - 2*y1*y0 - 1/2,
                  x2**2 - 2*x2*x0 + y2**2 - 2*y2*y0 - 1/2], [x0, y0])

print ccode(solution[x0])
# (x1*x1*y2 - x2*x2*y1 + y1*y1*y2 - y1*y2*y2)/(2*(x1*y2 - x2*y1))

print ccode(solution[y0])
# (-x1*x1*x2 + x1*x2*x2 + x1*y2*y2 - x2*y1*y1)/(2*(x1*y2 - x2*y1))
