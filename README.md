For a live demonstration of this project and a conversational background on the idea of hyperbolic spaces, see http://www.coffeeshopphysics.com/articles/2012-12/22_lost_in_hyperbolia/

Package contents
================

The two main parts of this package are `WebContent/HyperbolicViewport.js`, which is an in-browser viewer of pictures drawn in a hyperbolic space, and the Java code in `src` (package `org.hyperbolicstorage`), which serves those images to the client.  The user scrolls through the image with the mouse or fingers (two fingers rotate and zoom) and the server supplies new image elements as needed.  It is essentially a web mapping service for hyperbolic spaces, rather than the spherical Earth.

The image elements are transferred as vector-based JSON items.  Images cannot be raster tiles (like Google Earth, for instance) because non-linear transformations on images would be too expensive.  The JSON items have a de-factor format (*FIXME:* document it) that can be extended in the future.  It is inspired by SVG, but with much less coverage.

GitHub seems to think this project is 60% Python, 20% Javascript, and 20% Java.  The "real" parts of the project are the Javascript client and Java server; the many Python scripts were for testing and building the examples.  The testing directory is a mess of early work, mostly symbolic calculations.  The `svgtools` directory has a growing (meaning "incomplete") set of tools for converting between SVG, JSON items, and among coordinate systems.  The `svgtools/examples` directory has image bits in SVG and messier scripts intended just to convert those images.  The top level of `svgtools` should one day be widely useful.

Coordinate systems
==================

The viewer presents a hyperbolic plane in the Poincare disk projection, which maps the whole infinite plane to the inside of a large circle.  This coordinate system is consistently referred to as `poincareDisk` in the code.

The client's internal representation is what I call the hyperbolic shadow, `hyperShadow` in the code.  A 2-D hyperbolic space can be represented on a hyperboloid in 3-D Euclidean space, a solution to x^2 + y^2 - z^2 = 1 and z > 0.  If you project all of those points directly down to the x-y plane (that is, just ignore z), that's the hyperbolic shadow.  It differs from the Poincare disk in that the hyperbolic plane is mapped to the whole x-y plane, as though you replaced `tanh` in the Poincare disk with `sinh`.  This makes it easily convertable to the Poincare disk while not scrunching most of the image data into the tiny sliver between 0.99999 and 1.0.  It's for numerical stability.

Some source images were drawn in the Poincare half-plane model, `halfPlane` in the code.  Additionally, the server assigns image elements to tiles which are simply equal-sized squares in the half-plane model ("equal-sized" in the hyperbolic metric, not as they appear in the half-plane model).  The tiles are used as database keys for quick look-up, but the image elements are still in the hyperbolic shadow (because they are stored as uninterpreted JSON text).

*FIXME:* add some mathematical documentation on how the transformations were derived and which function does what.

*NOTE:* because complex numbers are so useful for the transformations (conversions among all three coordinate systems, as well as user scrolling and rotations, are Mobius transformations), the words `real` and `imag` are used interchangeably with `x` and `y`.  Also, `B` is used interchangeably with `offset` (since the second argument of a Mobius transformation controls scrolling in the hyperbolic plane) and `R` is used interchangeably with rotation.

Third party libraries
=====================

None required--- if you want to use the browser only, with no server.  The server uses BabuDB as an embedded database, which is available as a jar file.  Details:

   * *BabuDB:*  This is an embedded non-SQL database.  It is possible to use the viewer client without a server (static JSON), in which case BabuDB wouldn't be needed.  It's also possible to write Java code to auto-generate image elements, rather than retrieve them, and that would be another way to get around using a database (the `dungeon.html` example partly does this).  However, I've had good experience with BabuDB.  See http://code.google.com/p/babudb/ for more.
   * The Python scripts use JPype to control Java code (byte-level manipulation of the JVM).  While this is a convenient way to access things, it's not strictly needed to use the hyperbolic client-server.
   * Some early calculations were worked out in Sympy.

Summary of testing
==================

Tested on Firefox, Chrome, and Safari, Linux, Mac, and iPad 2.  It looks the same on all these platforms, but the Firefox-Linux combination is very, very, very slow (whether the Linux machine is real or virtual).  The iPad 2 should be limited to small numbers of image elements (`escher.html` is too much for it, but `clock.html` works great).  Internet Explorer and Windows have not been tested.

Alternatives considered
=======================

Several design choices were considered but eventually rejected due to poor performance:

   * *SVG vs. HTML5 canvas:* Since the graphics are vector-based, SVG seemed like an obvious choice at first.  In practice, though, transformations of the same images took about 10 times longer with SVG on several browsers, and I traced it to SVG calls with a profiler.  Perhaps reconfiguring the DOM is an expensive operation.  I never explicitly tested WebGL (I found out about it too late in the developement process), but I strongly suspect that most browser-operating system combinations use either WebGL or some hardware acceleration when HTML5 canvas routines are called, because one particular combination, Firefox on Linux, is many times slower for the same graphics.
   * *infinite precision arithmetic:* since they involve exponentials (indirectly through sinh and cosh), hyperbolic transformations have problems with numerical precision.  I tried infinite precision libraries on both the Javascript side and the Java side, but the slow-down in performance was never offset by an improvement in precision.  The transformation involves square roots, so it can't be purely done with infinite-precision rationals.
   * *server sends recentered graphics:* Currently, the server does not interpret the JSON graphical elements, it just passes them as raw bytes.  If the calculation could be done in Java with higher precision than is normally available to Javascript, then it could be valuable for the server to recenter its output and instruct the client to accept a new origin.  The thing that stopped me on this one is that I couldn't solve the mathematical problem of recentering, since the server does its work in `halfPlane` coordinates and the JSON items are in `hyperShadow`.  This would only be useful if there were a way to do the calculations in higher-than-double precision in Java (addition/subtraction, multiplication, division, and square roots).
