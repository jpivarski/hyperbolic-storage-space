package org.hyperbolicstorage;

import java.lang.Math;
// import java.math.BigInteger;
// import java.math.BigDecimal;
// import java.math.RoundingMode;

import java.io.OutputStream;
import java.io.IOException;

public class GeographicalTiles {
    protected static class IndexRange {
        int min;
        int max;
    }
    protected static class IndexRangeL {
        long min;
        long max;
    }

    protected static class Circle {
        double centerx;
        double centery;
        double radius;
    }

    protected static double LOG2 = Math.log(2);
    // protected static BigDecimal ZERO = BigDecimal.ZERO;
    // protected static BigDecimal ONE = BigDecimal.ONE;
    // protected static BigDecimal TWO = BigDecimal.ONE.add(BigDecimal.ONE);
    // protected static BigDecimal HALF = new BigDecimal(BigInteger.valueOf(5), 1);
    // protected static BigDecimal ONE_POINT_FIVE = new BigDecimal(BigInteger.valueOf(15), 1);
    // protected static BigDecimal ONE_POINT_SEVEN = new BigDecimal(BigInteger.valueOf(17), 1);

    public static class BigPoint2D {
        // BigDecimal x;
        // BigDecimal y;

        // public BigPoint2D(BigDecimal x, BigDecimal y) {
        //     this.x = x;
        //     this.y = y;
        // }

        double x;
        double y;

        public BigPoint2D(double x, double y) {
            // this.x = new BigDecimal(x);
            // this.y = new BigDecimal(y);
            this.x = x;
            this.y = y;
        }

        // public double xValue() { return x.doubleValue(); }
        // public double yValue() { return y.doubleValue(); }

        public double xValue() { return x; }
        public double yValue() { return y; }
    }

    private GeographicalTiles() { }

    public static BigPoint2D halfPlane_to_hyperShadow(BigPoint2D p) {
        double sqrtplus = Math.sqrt(p.x*p.x + p.y*p.y + 2.0*p.y + 1.0);
        double sqrtminus = Math.sqrt(p.x*p.x + p.y*p.y - 2.0*p.y + 1.0);
        double sinheta = Math.sqrt((sqrtplus + sqrtminus)/(sqrtplus - sqrtminus))/2.0 - Math.sqrt((sqrtplus - sqrtminus)/(sqrtminus + sqrtplus))/2.0;

        double denom = Math.sqrt(Math.pow(2.0 * p.x, 2) + Math.pow(p.x*p.x + p.y*p.y - 1.0, 2));
        double cosphi;
        double sinphi;
        if (p.x == 0.0 && p.y == 1.0) {
            cosphi = 0.0;
            sinphi = 1.0;
        }
        else {
            cosphi = (2.0 * p.x)/denom;
            sinphi = (p.x*p.x + p.y*p.y - 1.0)/denom;
        }

        double px = sinheta * cosphi;
        double py = sinheta * sinphi;

        return new BigPoint2D(px, py);
    }

    protected static Circle centralCircle(double offsetx, double offsety, double a) {
        // NOTE: loss of precision for large |(offset.x,offset.y)| values

        double Bone = Math.sqrt(1.0 + offsetx*offsetx + offsety*offsety);
        double Br = offsetx/Bone;
        double Bi = offsety/Bone;

        double p1 = Math.atan2((Bi*Bi + 2*Bi - Br*Br + 1), (2*Bi*Br + 2*Br));
        double d1 = Bi*Bi*a*a - 2*Bi*Bi*a*Math.sin(p1) + Bi*Bi - 4*Bi*Br*a*Math.cos(p1) + 2*Bi*a*a - 4*Bi*a*Math.sin(p1) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*Math.sin(p1) + Br*Br - 4*Br*a*Math.cos(p1) + a*a - 2*a*Math.sin(p1) + 1;
        double x1 = (-2*Bi*Bi*a*Math.cos(p1) + 4*Bi*Br*a*Math.sin(p1) + 2*Br*Br*a*Math.cos(p1) - 2*Br*a*a - 2*Br + 2*a*Math.cos(p1))/d1;
        double y1 = (Bi*Bi*a*a - Bi*Bi + Br*Br*a*a - Br*Br - a*a + 1)/d1;

        double p2 = Math.atan2(-(Bi*Bi + 2*Bi - Br*Br + 1), -(2*Bi*Br + 2*Br));
        double d2 = Bi*Bi*a*a - 2*Bi*Bi*a*Math.sin(p2) + Bi*Bi - 4*Bi*Br*a*Math.cos(p2) + 2*Bi*a*a - 4*Bi*a*Math.sin(p2) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*Math.sin(p2) + Br*Br - 4*Br*a*Math.cos(p2) + a*a - 2*a*Math.sin(p2) + 1;
        double x2 = (-2*Bi*Bi*a*Math.cos(p2) + 4*Bi*Br*a*Math.sin(p2) + 2*Br*Br*a*Math.cos(p2) - 2*Br*a*a - 2*Br + 2*a*Math.cos(p2))/d2;
        double y2 = (Bi*Bi*a*a - Bi*Bi + Br*Br*a*a - Br*Br - a*a + 1)/d2;

        Circle output = new Circle();
        output.centerx = (x1 + x2)/2.0;
        output.centery = (y1 + y2)/2.0;
        output.radius = Math.abs(y2 - y1)/2.0;
        return output;
    }

    protected static IndexRange latitudeRange(Circle visible) {
        double ymin = visible.centery - visible.radius;
        double ymax = visible.centery + visible.radius;

        IndexRange output = new IndexRange();
        output.min = (int)Math.floor(Math.log(ymin)/LOG2);
        output.max = (int)Math.ceil(Math.log(ymax)/LOG2);
        return output;
    }

    protected static IndexRangeL longitudeRange(Circle visible, long latitude) {
        double y = Math.pow(2, latitude);
        double discr = Math.pow(visible.radius, 2) - Math.pow(y - visible.centery, 2);
        if (discr <= 0) { return null; }
        discr = Math.sqrt(discr);

        double xmin = visible.centerx - discr;
        double xmax = visible.centerx + discr;

        IndexRangeL output = new IndexRangeL();
        output.min = (long)Math.floor(xmin/y);
        output.max = (long)Math.ceil(xmax/y);
        return output;
    }

    protected static boolean writePoint(OutputStream stream, BigPoint2D p, String options, boolean comma) throws IOException {
        if (!comma) {
            comma = true;
        } else {
            stream.write(",".getBytes());
        }

        if (options == null) {
            stream.write(String.format("[%g,%g]", p.x, p.y).getBytes());
        }
        else {
            stream.write(String.format("[%g,%g,\"%s\"]", p.x, p.y, options).getBytes());
        }

        return comma;
    }

    public static boolean writeGrid(OutputStream stream, boolean comma, double offsetx, double offsety, double radius) throws IOException {
        Circle visible = centralCircle(offsetx, offsety, radius);
        IndexRange latitudes = latitudeRange(visible);

        for (int latitude = latitudes.min;  latitude <= latitudes.max;  latitude++) {
            IndexRangeL longitudes = longitudeRange(visible, latitude);
            if (longitudes == null) { continue; }

            // BigDecimal size;
            // if (latitude > 999999999) {
            //     continue;
            // }
            // else if (latitude >= 0) {
            //     size = TWO.pow(latitude);
            // }
            // else if (latitude < -999999999) {
            //     continue;
            // }
            // else {
            //     size = HALF.pow(-latitude);
            // }
            double size = Math.pow(2, latitude);

            // BigDecimal size1p5 = size.multiply(ONE_POINT_FIVE);
            // BigDecimal size1p7 = size.multiply(ONE_POINT_SEVEN);

            for (long longitude = longitudes.min;  longitude <= longitudes.max;  longitude++) {
                if (!comma) {
                    comma = true;
                } else {
                    stream.write(",".getBytes());
                }

                stream.write("{\"type\": \"polygon\", \"class\": \"grid\", \"d\": [".getBytes());
                boolean comma2 = false;

                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new BigPoint2D(size*(longitude), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new BigPoint2D(size*(longitude+0.5), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new BigPoint2D(size*(longitude+1), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new BigPoint2D(size*(longitude+1), 2.0*size)), null, comma2);

                stream.write("]}\n".getBytes());

                BigPoint2D boxCenter = halfPlane_to_hyperShadow(new BigPoint2D(size*(longitude+0.5), 1.5*size));
                BigPoint2D box1up = halfPlane_to_hyperShadow(new BigPoint2D(size*(longitude+0.5), 1.7*size));

                stream.write(String.format(",{\"type\": \"text\", \"class\": \"gridText\", \"textBaseline\": \"bottom\", \"d\": \"%d\", \"ax\": %.18e, \"ay\": %.18e, \"upx\": %.18e, \"upy\": %.18e}\n", latitude, boxCenter.xValue(), boxCenter.yValue(), box1up.xValue(), box1up.yValue()).getBytes());

                stream.write(String.format(",{\"type\": \"text\", \"class\": \"gridText\", \"textBaseline\": \"top\", \"d\": \"%d\", \"ax\": %.18e, \"ay\": %.18e, \"upx\": %.18e, \"upy\": %.18e}\n", longitude, boxCenter.xValue(), boxCenter.yValue(), box1up.xValue(), box1up.yValue()).getBytes());
            }
        }

        return comma;
    }
}
