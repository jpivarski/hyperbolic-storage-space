import sys
import jpype

libjvm = "/usr/lib/jvm/java-6-openjdk-amd64/jre/lib/amd64/server/libjvm.so"
classpath = "/home/pivarski/fun/projects/hyperbolic-storage-space/HyperbolicStorage.jar"

jpype.startJVM(libjvm, "-Djava.class.path=%s" % classpath)

try:
    DatabaseInterface = jpype.JClass("org.hyperbolicstorage.DatabaseInterface")
    databaseInterface = DatabaseInterface("babudb")

    databaseInterface.insertGeographical("one", "ONE")
    databaseInterface.insertGeographical("two", "TWO")
    databaseInterface.insertGeographical("three", "THREE")
    databaseInterface.insertGeographical("four", "FOUR")

    databaseInterface.deleteGeographical("three")

    print databaseInterface.getGeographical("one")
    print databaseInterface.getGeographical("two")
    print databaseInterface.getGeographical("three")
    print databaseInterface.getGeographical("four")

    databaseInterface.close()

except jpype.JavaException as exception:
    sys.stderr.write(exception.stacktrace())
    sys.stderr.write("\n")
    sys.exit(-1)
