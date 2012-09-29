import sympy
import math
import random

x = sympy.Symbol("x")
y = sympy.Symbol("y")

r = sympy.sqrt((x**2 + y**2 - 2*y + 1) / (x**2 + y**2 + 2*y + 1))

print sympy.printing.ccode((sympy.sqrt((1 + r)/(1 - r))/2 - sympy.sqrt((1 - r)/(1 + r))/2).expand())


# sqrtplus = sqrt(x*x + y*y + 2.0*y + 1.0)
# sqrtminus = sqrt(x*x + y*y - 2.0*y + 1.0)

# sqrt((sqrtplus + sqrtminus)/(sqrtplus - sqrtminus)) - sqrt((sqrtplus - sqrtminus)/(sqrtminus + sqrtplus))/2.0






#####

# sqrt(sqrt(x*x/(x*x + y*y + 2*y + 1) + y*y/(x*x + y*y + 2*y + 1) - 2*y/(x*x + y*y + 2*y + 1) + 1.0/(x*x + y*y + 2*y + 1))/(sqrt(x*x/(x*x + y*y + 2*y + 1) + y*y/(x*x + y*y + 2*y + 1) - 2*y/(x*x + y*y + 2*y + 1) + 1.0/(x*x + y*y + 2*y + 1)) + 1) - 1/(sqrt(x*x/(x*x + y*y + 2*y + 1) + y*y/(x*x + y*y + 2*y + 1) - 2*y/(x*x + y*y + 2*y + 1) + 1.0/(x*x + y*y + 2*y + 1)) + 1) + sqrt(x*x/(x*x + y*y + 2*y + 1) + y*y/(x*x + y*y + 2*y + 1) - 2*y/(x*x + y*y + 2*y + 1) + 1.0/(x*x + y*y + 2*y + 1))/(-sqrt(x*x/(x*x + y*y + 2*y + 1) + y*y/(x*x + y*y + 2*y + 1) - 2*y/(x*x + y*y + 2*y + 1) + 1.0/(x*x + y*y + 2*y + 1)) + 1) + 1.0/(-sqrt(x*x/(x*x + y*y + 2*y + 1) + y*y/(x*x + y*y + 2*y + 1) - 2*y/(x*x + y*y + 2*y + 1) + 1.0/(x*x + y*y + 2*y + 1)) + 1))/2

def one(x, y):
    r = math.sqrt((x**2 + y**2 - 2*y + 1.0) / (x**2 + y**2 + 2*y + 1.0))
    return math.sqrt((1.0 + r)/(1.0 - r) - (1.0 - r)/(1.0 + r))/2.0

def two(x, y):
    sqrtplus = math.sqrt(x*x + y*y + 2.0*y + 1.0)
    sqrtminus = math.sqrt(x*x + y*y - 2.0*y + 1.0)
    # return sqrt(sqrt(x*x/plus + y*y/plus - 2.0*y/plus + 1.0/plus)/(sqrt(x*x/plus + y*y/plus - 2.0*y/plus + 1.0/plus) + 1.0) - 1.0/(sqrt(x*x/plus + y*y/plus - 2.0*y/plus + 1.0/plus) + 1.0) + sqrt(x*x/plus + y*y/plus - 2.0*y/plus + 1.0/plus)/(-sqrt(x*x/plus + y*y/plus - 2.0*y/plus + 1.0/plus) + 1.0) + 1.0/(-sqrt(x*x/plus + y*y/plus - 2.0*y/plus + 1.0/plus) + 1.0))/2.0
    # return ((sqrtminus - sqrtplus)/(sqrtminus + sqrtplus) + (sqrtplus + sqrtminus)/(sqrtplus - sqrtminus))/2.0
    return math.sqrt((sqrtplus + sqrtminus)/(sqrtplus - sqrtminus))/2.0 - math.sqrt((sqrtplus - sqrtminus)/(sqrtminus + sqrtplus))/2.0

def four(x, y):
    r = math.sqrt((x**2 + y**2 - 2*y + 1.0) / (x**2 + y**2 + 2*y + 1.0))
    eta = math.atanh(r)
    return math.sinh(eta)

def three(x, y):
    r = math.sqrt((x**2 + y**2 - 2*y + 1.0) / (x**2 + y**2 + 2*y + 1.0))
    eta = 0.5*(math.log((1 + r)/(1 - r)))
    return (math.sqrt((1 + r)/(1 - r)) - math.sqrt((1 - r)/(1 + r)))/2.0

def zero(x, y):
    r = math.sqrt((x**2 + y**2 - 2*y + 1.0) / (x**2 + y**2 + 2*y + 1.0))
    return (math.sqrt((1+r)/(1-r)) - 1.0/math.sqrt((1+r)/(1-r)))/2.0

for i in xrange(10):
    x = random.gauss(0, 0.5)
    y = abs(random.gauss(0, 0.5))
    print one(x, y), zero(x, y) - three(x, y), four(x, y) - three(x, y), two(x, y) - three(x, y)


# plus = x*x + y*y + 2*y + 1
# sqrt(sqrt(x*x/plus + y*y/plus - 2*y/plus + 1.0/plus)/(sqrt(x*x/plus + y*y/plus - 2*y/plus + 1.0/plus) + 1) - 1/(sqrt(x*x/plus + y*y/plus - 2*y/plus + 1.0/plus) + 1) + sqrt(x*x/plus + y*y/plus - 2*y/plus + 1.0/plus)/(-sqrt(x*x/plus + y*y/plus - 2*y/plus + 1.0/plus) + 1) + 1.0/(-sqrt(x*x/plus + y*y/plus - 2*y/plus + 1.0/plus) + 1))/2

# plus = x*x + y*y + 2*y + 1
# sqrtminus = sqrt(x*x + y*y - 2*y + 1)
# sqrt(sqrtminus/(sqrtminus + plus*plus) - plus*plus/(sqrtminus + plus*plus) + sqrtminus/(-sqrtminus + plus*plus) + plus*plus/(-sqrtminus + plus*plus))/2


