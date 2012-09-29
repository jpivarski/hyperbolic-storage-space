import jpype

libjvm = "/usr/lib/jvm/java-6-openjdk-amd64/jre/lib/amd64/server/libjvm.so"
classpath = "/home/pivarski/fun/projects/hyperbolic-storage-space/HyperbolicStorage.jar"

jpype.startJVM(libjvm, "-Djava.class.path=%s" % classpath)

DatabaseInterface = jpype.JClass("org.hyperbolicstorage.DatabaseInterface")

jpype.shutdownJVM()
