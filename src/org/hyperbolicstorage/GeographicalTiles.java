package org.hyperbolicstorage;

import java.lang.Math;
import java.math.BigInteger;
import java.math.BigDecimal;
import java.math.RoundingMode;

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
    protected static BigDecimal ZERO = BigDecimal.ZERO;
    protected static BigDecimal ONE = BigDecimal.ONE;
    protected static BigDecimal TWO = BigDecimal.ONE.add(BigDecimal.ONE);
    protected static BigDecimal HALF = new BigDecimal(BigInteger.valueOf(5), 1);
    protected static BigDecimal ONE_POINT_FIVE = new BigDecimal(BigInteger.valueOf(15), 1);
    protected static BigDecimal ONE_POINT_SEVEN = new BigDecimal(BigInteger.valueOf(17), 1);

    public static class BigPoint2D {
        BigDecimal x;
        BigDecimal y;

        public BigPoint2D(BigDecimal x, BigDecimal y) {
            this.x = x;
            this.y = y;
        }

        public BigPoint2D(double x, double y) {
            this.x = new BigDecimal(x);
            this.y = new BigDecimal(y);
        }

        public double xValue() { return x.doubleValue(); }
        public double yValue() { return y.doubleValue(); }
    }

    private GeographicalTiles() { }

    public static BigDecimal sqrt(BigDecimal x, int iterations, int precision) {
        if (x.compareTo(ZERO) == 0) {
            return x;
        }

        BigDecimal result = BigDecimal.valueOf(java.lang.Math.sqrt(x.doubleValue()));
        for (int i = 0;  i < iterations;  i++) {
            result = result.subtract((result.pow(2).subtract(x)).divide(result.multiply(TWO), precision, RoundingMode.HALF_UP));
        }
        return result;
    }

    public static BigPoint2D halfPlane_to_hyperShadow(BigPoint2D p) {
        int iterations = 10;
        int precision = 1000;

        BigDecimal sqrtplus = sqrt(p.x.pow(2).add(p.y.pow(2)).add(p.y.multiply(TWO)).add(ONE), iterations, precision);
        BigDecimal sqrtminus = sqrt(p.x.pow(2).add(p.y.pow(2)).subtract(p.y.multiply(TWO)).add(ONE), iterations, precision);

        BigDecimal sinheta = sqrt((sqrtplus.add(sqrtminus)).divide(sqrtplus.subtract(sqrtminus), precision, RoundingMode.HALF_UP), iterations, precision).divide(TWO, precision, RoundingMode.HALF_UP).subtract(sqrt((sqrtplus.subtract(sqrtminus)).divide(sqrtminus.add(sqrtplus), precision, RoundingMode.HALF_UP), iterations, precision).divide(TWO, precision, RoundingMode.HALF_UP));

        BigDecimal denom = sqrt(p.x.multiply(TWO).pow(2).add((p.x.pow(2).add(p.y.pow(2)).subtract(ONE)).pow(2)), iterations, precision);

        BigDecimal cosphi;
        BigDecimal sinphi;
        if (p.x.compareTo(ZERO) == 0  &&  p.y.compareTo(ONE) == 0) {
            cosphi = ZERO;
            sinphi = ONE;
        }
        else {
            cosphi = p.x.multiply(TWO).divide(denom, precision, RoundingMode.HALF_UP);
            sinphi = (p.x.pow(2).add(p.y.pow(2)).subtract(ONE)).divide(denom, precision, RoundingMode.HALF_UP);
        }

        BigDecimal px = sinheta.multiply(cosphi);
        BigDecimal py = sinheta.multiply(sinphi);

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

            BigDecimal size;
            if (latitude > 999999999) {
                continue;
            }
            else if (latitude >= 0) {
                size = TWO.pow(latitude);
            }
            else if (latitude < -999999999) {
                continue;
            }
            else {
                size = HALF.pow(-latitude);
            }

            BigDecimal size1p5 = size.multiply(ONE_POINT_FIVE);
            BigDecimal size1p7 = size.multiply(ONE_POINT_SEVEN);

            for (long longitude = longitudes.min;  longitude <= longitudes.max;  longitude++) {
                if (!comma) {
                    comma = true;
                } else {
                    stream.write(",".getBytes());
                }

                stream.write("{\"type\": \"polygon\", \"class\": \"grid\", \"d\": [".getBytes());
                boolean comma2 = false;

                BigDecimal longitudeBD = BigDecimal.valueOf(longitude);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new BigPoint2D(size.multiply(longitudeBD), size)), "L", comma2);
                longitudeBD = longitudeBD.add(HALF);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new BigPoint2D(size.multiply(longitudeBD), size)), "L", comma2);
                longitudeBD = longitudeBD.add(HALF);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new BigPoint2D(size.multiply(longitudeBD), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new BigPoint2D(size.multiply(longitudeBD), size.multiply(TWO))), null, comma2);

                stream.write("]}\n".getBytes());

                longitudeBD = longitudeBD.subtract(HALF);
                BigPoint2D boxCenter = halfPlane_to_hyperShadow(new BigPoint2D(size.multiply(longitudeBD), size1p5));
                BigPoint2D box1up = halfPlane_to_hyperShadow(new BigPoint2D(size.multiply(longitudeBD), size1p7));

                stream.write(String.format(",{\"type\": \"text\", \"class\": \"gridText\", \"textBaseline\": \"bottom\", \"d\": \"%d\", \"ax\": %g, \"ay\": %g, \"upx\": %g, \"upy\": %g}\n", latitude, boxCenter.xValue(), boxCenter.yValue(), box1up.xValue(), box1up.yValue()).getBytes());

                stream.write(String.format(",{\"type\": \"text\", \"class\": \"gridText\", \"textBaseline\": \"top\", \"d\": \"%d\", \"ax\": %g, \"ay\": %g, \"upx\": %g, \"upy\": %g}\n", longitude, boxCenter.xValue(), boxCenter.yValue(), box1up.xValue(), box1up.yValue()).getBytes());
            }
        }

        return comma;
    }
}
