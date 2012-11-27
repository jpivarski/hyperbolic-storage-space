import sys
import jpype

libjvm = "/usr/lib/jvm/java-6-sun/jre/lib/amd64/server/libjvm.so"
classpath = "/home/pivarski/fun/projects/hyperbolic-storage-space/HyperbolicStorage.jar"

jpype.startJVM(libjvm, "-Djava.class.path=%s" % classpath)

try:
    DatabaseInterface = jpype.JClass("org.hyperbolicstorage.DatabaseInterface")
    databaseInterface = DatabaseInterface("/var/www/babudb")

    databaseInterface.insert(10, 8, -22, 1.0, 0.0, 1.0, "one")
    databaseInterface.insert(10, 6, -3, 2.0, 0.0, 1.0, "two")
    databaseInterface.insert(-4, 5, 7, 3.3, 0.0, 1.0, "three")
    databaseInterface.insert(10, 8, 99, 4.4, 0.0, 1.0, "four")
    databaseInterface.insert(10, 5, 0, 5.0, 0.0, 1.0, "five")

    print databaseInterface.getOne(10, 8, -22)
    print databaseInterface.getOne(10, 6, -3)
    print databaseInterface.getOne(-4, 5, 7)
    print databaseInterface.getOne(10, 8, 99)
    print databaseInterface.getOne(10, 5, 0)
    print databaseInterface.getOne(-4, 5, 0)

    print databaseInterface.getRange(10, 0, 8)
    print databaseInterface.getRange(10, 0, 9)

    databaseInterface.close()

except jpype.JavaException as exception:
    sys.stderr.write(exception.stacktrace())
    sys.stderr.write("\n")
    sys.exit(-1)
