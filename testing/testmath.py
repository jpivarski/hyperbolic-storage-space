import sys
import jpype
import random

libjvm = "/usr/lib/jvm/java-6-openjdk-amd64/jre/lib/amd64/server/libjvm.so"
classpath = "/home/pivarski/fun/projects/hyperbolic-storage-space/HyperbolicStorage.jar"

jpype.startJVM(libjvm, "-Djava.class.path=%s" % classpath)

try:
    GeographicalTiles = jpype.JClass("org.hyperbolicstorage.GeographicalTiles")

    for i in xrange(100000):
        x = random.gauss(0, 1)
        y = abs(random.gauss(0, 1))
        GeographicalTiles.halfPlane_to_hyperShadow(x, y)

except jpype.JavaException as exception:
    sys.stderr.write(exception.stacktrace())
    sys.stderr.write("\n")
    sys.exit(-1)
