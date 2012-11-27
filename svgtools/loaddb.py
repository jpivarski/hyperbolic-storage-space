#!/usr/bin/env python

import sys
import json

import jpype

libjvm = "/usr/lib/jvm/java-6-sun/jre/lib/amd64/server/libjvm.so"
classpath = "/home/pivarski/fun/projects/hyperbolic-storage-space/HyperbolicStorage.jar"
jpype.startJVM(libjvm, "-Djava.class.path=%s" % classpath)

depth = 0.0
if len(sys.argv) == 4:
    dbLocation = sys.argv[1]
    minRadius, maxRadius = float(sys.argv[2]), float(sys.argv[3])
elif len(sys.argv) == 2:
    dbLocation = sys.argv[1]
    minRadius, maxRadius = 0.0, 1.0
else:
    raise NotImplementedError("arguments are: dbLocation [minRadius maxRadius]")

def hashable(d):
    if isinstance(d, dict):
        output = []
        for key in sorted(d.keys()):
            output.append((key, hashable(d[key])))
        return tuple(output)

    elif isinstance(d, list):
        output = []
        for item in d:
            output.append(hashable(item))
        return tuple(output)

    else:
        return d

try:
    DatabaseInterface = jpype.JClass("org.hyperbolicstorage.DatabaseInterface")
    databaseInterface = DatabaseInterface(dbLocation)

    GeographicalTiles = jpype.JClass("org.hyperbolicstorage.GeographicalTiles")
    Point2D = jpype.JClass("org.hyperbolicstorage.GeographicalTiles$Point2D")
    IndexPair = jpype.JClass("org.hyperbolicstorage.GeographicalTiles$IndexPair")

    for lineNumber, drawableString in enumerate(sys.stdin.xreadlines()):
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
        identifier = drawable.get("id", hash(hashable(drawable)))

        databaseInterface.insert(tileIndex.latitude, tileIndex.longitude, identifier, depth, minRadius, maxRadius, drawableString)
        depth += 1.0

        if lineNumber % 100 == 0:
            print "Filling line %d: %g %g %d %d %d %g %g %g %s" % (lineNumber, x, y, tileIndex.latitude, tileIndex.longitude, identifier, depth, minRadius, maxRadius, drawableString[:100])

    databaseInterface.close()

except jpype.JavaException as exception:
    sys.stderr.write(exception.stacktrace())
    sys.stderr.write("\n")
    sys.exit(-1)
