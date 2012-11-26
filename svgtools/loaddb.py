#!/usr/bin/env python

import sys
import json

import jpype

libjvm = "/usr/lib/jvm/java-6-sun/jre/lib/amd64/server/libjvm.so"
classpath = "/home/pivarski/fun/projects/hyperbolic-storage-space/HyperbolicStorage.jar"
jpype.startJVM(libjvm, "-Djava.class.path=%s" % classpath)

depth = 0.0

try:
    DatabaseInterface = jpype.JClass("org.hyperbolicstorage.DatabaseInterface")
    databaseInterface = DatabaseInterface("/var/www/babudb")

    GeographicalTiles = jpype.JClass("org.hyperbolicstorage.GeographicalTiles")
    Point2D = jpype.JClass("org.hyperbolicstorage.GeographicalTiles$Point2D")
    IndexPair = jpype.JClass("org.hyperbolicstorage.GeographicalTiles$IndexPair")

    for drawableString in sys.stdin.xreadlines():
        drawableString = drawableString.strip()
        drawable = json.loads(drawableString)

        if drawable["type"] == "polygon":
            x = 0.0
            y = 0.0
            N = 0.0
            for item in drawable["d"]:
                x += item[0]
                y += item[1]
                N += 1.0
            x /= N
            y /= N

        elif drawable["type"] == "text":
            x = drawable["ax"]
            y = drawable["ay"]
        
        tileIndex = GeographicalTiles.tileIndex(GeographicalTiles.hyperShadow_to_halfPlane(Point2D(x, y)))
        
        databaseInterface.insert(tileIndex.latitude, tileIndex.longitude, hash(drawableString), depth, drawableString)
        depth += 1.0

    databaseInterface.close()

except jpype.JavaException as exception:
    sys.stderr.write(exception.stacktrace())
    sys.stderr.write("\n")
    sys.exit(-1)
