package org.hyperbolicstorage;

import java.lang.Math;
import java.awt.geom.Point2D;

import java.io.OutputStream;
import java.io.IOException;

public class GeographicalTiles {
    protected static class Circle {
        Point2D.Double center;
        double radius;
    }

    protected static class IndexRange {
        long min;
        long max;
    }

    protected static double LOG2 = Math.log(2);

    private GeographicalTiles() { }

    public static Point2D.Double halfPlane_to_hyperShadow(Point2D.Double p) {
        double x = p.getX();
        double y = p.getY();

        double sqrtplus = Math.sqrt(x*x + y*y + 2.0*y + 1.0);
        double sqrtminus = Math.sqrt(x*x + y*y - 2.0*y + 1.0);
        double sinheta = Math.sqrt((sqrtplus + sqrtminus)/(sqrtplus - sqrtminus))/2.0 - Math.sqrt((sqrtplus - sqrtminus)/(sqrtminus + sqrtplus))/2.0;

        double denom = Math.sqrt(Math.pow(2.0 * x, 2) + Math.pow(x*x + y*y - 1.0, 2));
        double cosphi = (2.0 * x)/denom;
        double sinphi = (x*x + y*y - 1.0)/denom;
        if (x == 0.0  &&  y == 1.0) {
            cosphi = 0.0;
            sinphi = 1.0;
        }

        double px = sinheta * cosphi;
        double py = sinheta * sinphi;

        return new Point2D.Double(px, py);
    }

    protected static Circle centralCircle(Point2D.Double offset, double a) {
        // NOTE: loss of precision for large |(offset.x,offset.y)| values

        double Bone = Math.sqrt(1.0 + offset.x*offset.x + offset.y*offset.y);
        double Br = offset.x/Bone;
        double Bi = offset.y/Bone;

        double p1 = Math.atan2((Bi*Bi + 2*Bi - Br*Br + 1), (2*Bi*Br + 2*Br));
        double d1 = Bi*Bi*a*a - 2*Bi*Bi*a*Math.sin(p1) + Bi*Bi - 4*Bi*Br*a*Math.cos(p1) + 2*Bi*a*a - 4*Bi*a*Math.sin(p1) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*Math.sin(p1) + Br*Br - 4*Br*a*Math.cos(p1) + a*a - 2*a*Math.sin(p1) + 1;
        double x1 = (-2*Bi*Bi*a*Math.cos(p1) + 4*Bi*Br*a*Math.sin(p1) + 2*Br*Br*a*Math.cos(p1) - 2*Br*a*a - 2*Br + 2*a*Math.cos(p1))/d1;
        double y1 = (Bi*Bi*a*a - Bi*Bi + Br*Br*a*a - Br*Br - a*a + 1)/d1;

        double p2 = Math.atan2(-(Bi*Bi + 2*Bi - Br*Br + 1), -(2*Bi*Br + 2*Br));
        double d2 = Bi*Bi*a*a - 2*Bi*Bi*a*Math.sin(p2) + Bi*Bi - 4*Bi*Br*a*Math.cos(p2) + 2*Bi*a*a - 4*Bi*a*Math.sin(p2) + 2*Bi + Br*Br*a*a + 2*Br*Br*a*Math.sin(p2) + Br*Br - 4*Br*a*Math.cos(p2) + a*a - 2*a*Math.sin(p2) + 1;
        double x2 = (-2*Bi*Bi*a*Math.cos(p2) + 4*Bi*Br*a*Math.sin(p2) + 2*Br*Br*a*Math.cos(p2) - 2*Br*a*a - 2*Br + 2*a*Math.cos(p2))/d2;
        double y2 = (Bi*Bi*a*a - Bi*Bi + Br*Br*a*a - Br*Br - a*a + 1)/d2;

        Circle output = new Circle();
        output.center = new Point2D.Double((x1 + x2)/2.0, (y1 + y2)/2.0);
        output.radius = Math.abs(y2 - y1)/2.0;
        return output;
    }

    protected static IndexRange latitudeRange(Circle visible) {
        double ymin = visible.center.y - visible.radius;
        double ymax = visible.center.y + visible.radius;

        IndexRange output = new IndexRange();
        output.min = (long)Math.floor(Math.log(ymin)/LOG2);
        output.max = (long)Math.ceil(Math.log(ymax)/LOG2);
        return output;
    }

    protected static IndexRange longitudeRange(Circle visible, long latitude) {
        double y = Math.pow(2, latitude);
        double discr = Math.pow(visible.radius, 2) - Math.pow(y - visible.center.y, 2);
        if (discr <= 0) { return null; }
        discr = Math.sqrt(discr);

        double xmin = visible.center.x - discr;
        double xmax = visible.center.x + discr;

        IndexRange output = new IndexRange();
        output.min = (long)Math.floor(xmin/y);
        output.max = (long)Math.ceil(xmax/y);
        return output;
    }

    protected static boolean writePoint(OutputStream stream, Point2D.Double p, String options, boolean comma) throws IOException {
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
        Circle visible = centralCircle(new Point2D.Double(offsetx, offsety), radius);
        IndexRange latitudes = latitudeRange(visible);

        for (long latitude = latitudes.min;  latitude <= latitudes.max;  latitude++) {
            IndexRange longitudes = longitudeRange(visible, latitude);
            if (longitudes == null) { continue; }

            double size = Math.pow(2, latitude);
            for (long longitude = longitudes.min;  longitude <= longitudes.max;  longitude++) {
                if (!comma) {
                    comma = true;
                } else {
                    stream.write(",".getBytes());
                }

                stream.write("{\"type\": \"polygon\", \"d\": [".getBytes());
                boolean comma2 = false;

                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new Point2D.Double(size*(longitude), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new Point2D.Double(size*(longitude+0.5), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new Point2D.Double(size*(longitude+1), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new Point2D.Double(size*(longitude+1), 2*size)), null, comma2);

                stream.write("]}\n".getBytes());
            }
        }

        return comma;
    }
}
