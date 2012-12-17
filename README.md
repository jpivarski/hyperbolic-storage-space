For a more conversational introduction, a live demonstration of the viewer, and background on hyperbolic spaces, see http://www.coffeeshopphysics.com/articles/FIXME-NOT-WRITTEN-YET

Package contents
================

The two main parts of this package are `WebContent/HyperbolicViewport.js`, which is an in-browser viewer of pictures drawn in a hyperbolic space, and the Java code in `src` (package `org.hyperbolicstorage`), which serves those images to the client.  The user scrolls through the image with the mouse or fingers (two fingers rotate and zoom) and the server supplies new image elements as needed.  It is essentially a web mapping service for hyperbolic spaces, rather than the spherical Earth.

The image elements are transferred as vector-based JSON items.  Images cannot be raster tiles (like Google Earth, for instance) because non-linear transformations on images would be too expensive.  The JSON items have a de-factor format (FIXME: document it) that can be extended in the future.  It is inspired by SVG, but with much less coverage.

GitHub seems to think this project is 60% Python, 20% Javascript, and 20% Java.  The "real" parts of the project are the Javascript client and Java server; the many Python scripts were for testing and building the examples.  The testing directory is a mess of early work, mostly symbolic calculations.  The `svgtools` directory has a growing (meaning "incomplete") set of tools for converting between SVG, JSON items, and among coordinate systems.  The `svgtools/examples` directory has image bits in SVG and messier scripts intended just to convert those images.  The top level of `svgtools` should one day be widely useful.

Coordinate systems
==================

The viewer presents a hyperbolic plane in the Poincare disk projection, which maps the whole infinite plane to the inside of a large circle.  This coordinate system is consistently referred to as `poincareDisk` in the code.

The client's internal representation is what I call the hyperbolic shadow, `hyperShadow` in the code.  A 2-D hyperbolic space can be represented on a hyperboloid in 3-D Euclidean space, a solution to x^2 + y^2 - z^2 = 1 and z > 0.  If you project all of those points directly down to the x-y plane (that is, just ignore z), that's the hyperbolic shadow.  It differs from the Poincare disk in that the hyperbolic plane is mapped to the whole x-y plane, as though you replaced `tanh` in the Poincare disk with `sinh`.  This makes it easily convertable to the Poincare disk while not scrunching most of the image data into the tiny sliver between 0.99999 and 1.0.  It's for numerical stability.

Some source images were drawn in the Poincare half-plane model, `halfPlane` in the code.  Additionally, the server assigns image elements to tiles which are simply equal-sized squares in the half-plane model ("equal-sized" in the hyperbolic metric, not as they appear in the half-plane model).  The tiles are used as database keys for quick look-up, but the image elements are still in the hyperbolic shadow (because they are stored as uninterpreted JSON text).

FIXME: add some mathematical documentation on how the transformations were derived and which function does what.

NOTE: because complex numbers are so useful for the transformations (conversions among all three coordinate systems, as well as user scrolling and rotations, are Mobius transformations), the words `real` and `imag` are used interchangeably with `x` and `y`.  Also, `B` is used interchangeably with `offset` (since the second argument of a Mobius transformation controls scrolling in the hyperbolic plane) and `R` is used interchangeably with rotation.

Third party libraries
=====================

The server uses BabuDB to store image elements.  This is an embedded non-SQL database.  It is possible to use the viewer client without a server (static JSON), in which case BabuDB wouldn't be needed.  It's also possible to write Java code to auto-generate image elements, rather than retrieve them, and that would be another way to get around using a database (the `dungeon.html` example partly does this).  However, I've had good experience with BabuDB.  See http://code.google.com/p/babudb/ for more.

The Python scripts use JPype to control Java code (byte-level manipulation of the JVM).  While this is a convenient way to access things, it's not strictly needed to use the hyperbolic client-server.

Some early calculations were worked out in Sympy.

The Javascript doesn't require any third-party libraries.  (It basically _is_ a library intended for other projects.)  It has been tested on Firefox, Chrome, and Safari, Linux, Mac, and iPad 2.  It looks the same on all these platforms, but the Firefox-Linux combination is very, very, very slow (whether the Linux machine is real or virtual).  The iPad 2 should be limited to small numbers of image elements (`escher.html` is too much for it, but `clock.html` works great).  The Javascript borrows liberally from HTML5 features, so the multitouch support ought to be cross-platform.
