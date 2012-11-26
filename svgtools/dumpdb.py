#!/usr/bin/env python

import sys

import jpype

libjvm = "/usr/lib/jvm/java-6-sun/jre/lib/amd64/server/libjvm.so"
classpath = "/home/pivarski/fun/projects/hyperbolic-storage-space/HyperbolicStorage.jar"
jpype.startJVM(libjvm, "-Djava.class.path=%s" % classpath)

try:
    DatabaseInterface = jpype.JClass("org.hyperbolicstorage.DatabaseInterface")
    databaseInterface = DatabaseInterface("/var/www/babudb")

    GeographicalTiles = jpype.JClass("org.hyperbolicstorage.GeographicalTiles")

    visible = GeographicalTiles.centralCircle(0.0, 0.0, 0.99)
    latitudes = GeographicalTiles.latitudeRange(visible)

    depthDrawables = []
    for latitude in xrange(latitudes.min, latitudes.max + 1):
        longitudes = GeographicalTiles.longitudeRange(visible, latitude)
        if longitudes is None: continue

        depthDrawables.extend(databaseInterface.getRange(latitude, longitudes.min, longitudes.max))

    depthDrawables.sort(lambda a, b: a.compareTo(b))

    for depthDrawable in depthDrawables:
        print depthDrawable.depth, depthDrawable.drawable
        
    databaseInterface.close()

except jpype.JavaException as exception:
    sys.stderr.write(exception.stacktrace())
    sys.stderr.write("\n")
    sys.exit(-1)
