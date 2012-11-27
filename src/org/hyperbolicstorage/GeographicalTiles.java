package org.hyperbolicstorage;

import org.hyperbolicstorage.DatabaseInterface;

import java.lang.Math;
import java.lang.Double;
import java.lang.Long;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import java.util.Map;
import java.util.HashMap;
import java.util.Collections;
import java.io.OutputStream;
import java.io.IOException;

public class GeographicalTiles {
    public static class IndexRange {
        int min;
        int max;
    }
    public static class IndexRangeL {
        long min;
        long max;
    }
    public static class IndexPair {
        int latitude;
        long longitude;
    }

    public static class Circle {
        double centerx;
        double centery;
        double radius;
    }

    protected static double LOG2 = Math.log(2);

    public static class Point2D {
        double x;
        double y;

        public Point2D(double x, double y) {
            this.x = x;
            this.y = y;
        }
    }

    private GeographicalTiles() { }

    public static Point2D halfPlane_to_hyperShadow(Point2D p) {
        double sqrtplus = Math.sqrt(p.x*p.x + p.y*p.y + 2.0*p.y + 1.0);
        double sqrtminus = Math.sqrt(p.x*p.x + p.y*p.y - 2.0*p.y + 1.0);
        double sinheta = Math.sqrt((sqrtplus + sqrtminus)/(sqrtplus - sqrtminus))/2.0 - Math.sqrt((sqrtplus - sqrtminus)/(sqrtminus + sqrtplus))/2.0;

        double denom = Math.sqrt(Math.pow(2.0 * p.x, 2) + Math.pow(p.x*p.x + p.y*p.y - 1.0, 2));
        double cosphi;
        double sinphi;
        if (p.x == 0.0  &&  p.y == 1.0) {
            cosphi = 0.0;
            sinphi = 1.0;
        }
        else {
            cosphi = (2.0 * p.x)/denom;
            sinphi = (p.x*p.x + p.y*p.y - 1.0)/denom;
        }

        double px = sinheta * cosphi;
        double py = sinheta * sinphi;

        return new Point2D(px, py);
    }

    public static Point2D hyperShadow_to_halfPlane(Point2D p) {
        double pone = Math.sqrt(p.x*p.x + p.y*p.y + 1.0);
        double denom = 2.0*(p.x*p.x + p.y*p.y) + 1.0 - 2.0*p.y*pone;
        double numerx = 2.0*p.x*pone;
        double numery = 1.0;
        return new Point2D(numerx/denom, numery/denom);
    }

    public static IndexPair tileIndex(Point2D halfPlane) {
        IndexPair output = new IndexPair();
        output.latitude = (int)Math.floor(Math.log(halfPlane.y)/LOG2);
        output.longitude = (long)Math.floor(halfPlane.x * Math.pow(2, -output.latitude));
        return output;
    }

    public static Circle centralCircle(double offsetx, double offsety, double a) {
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

    public static IndexRange latitudeRange(Circle visible) {
        double ymin = visible.centery - visible.radius;
        double ymax = visible.centery + visible.radius;

        IndexRange output = new IndexRange();
        output.min = (int)Math.floor(Math.log(ymin)/LOG2);
        output.max = (int)Math.ceil(Math.log(ymax)/LOG2);
        return output;
    }

    public static IndexRangeL longitudeRange(Circle visible, long latitude) {
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

    protected static boolean writePoint(OutputStream stream, Point2D p, String options, boolean comma) throws IOException {
        if (!comma) {
            comma = true;
        } else {
            stream.write(",".getBytes());
        }

        if (options == null) {
            stream.write(String.format("[%.18e,%.18e]", p.x, p.y).getBytes());
        }
        else {
            stream.write(String.format("[%.18e,%.18e,\"%s\"]", p.x, p.y, options).getBytes());
        }

        return comma;
    }

    public static boolean writeGrid(OutputStream stream, boolean comma, double offsetx, double offsety, double radius) throws IOException {
        Circle visible = centralCircle(offsetx, offsety, radius);
        IndexRange latitudes = latitudeRange(visible);

        for (int latitude = latitudes.min;  latitude <= latitudes.max;  latitude++) {
            IndexRangeL longitudes = longitudeRange(visible, latitude);
            if (longitudes == null) { continue; }

            double size = Math.pow(2, latitude);
            for (long longitude = longitudes.min;  longitude <= longitudes.max;  longitude++) {
                if (!comma) {
                    comma = true;
                } else {
                    stream.write(",".getBytes());
                }

                stream.write("{\"type\": \"polygon\", \"class\": \"grid\", \"d\": [".getBytes());
                boolean comma2 = false;

                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new Point2D(size*(longitude), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new Point2D(size*(longitude+0.5), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new Point2D(size*(longitude+1), size)), "L", comma2);
                comma2 = writePoint(stream, halfPlane_to_hyperShadow(new Point2D(size*(longitude+1), 2.0*size)), null, comma2);

                stream.write("]}\n".getBytes());

                Point2D boxCenter = halfPlane_to_hyperShadow(new Point2D(size*(longitude+0.5), 1.5*size));
                Point2D box1up = halfPlane_to_hyperShadow(new Point2D(size*(longitude+0.5), 1.7*size));

                stream.write(String.format(",{\"type\": \"text\", \"class\": \"gridText\", \"textBaseline\": \"bottom\", \"d\": \"%d\", \"ax\": %.18e, \"ay\": %.18e, \"upx\": %.18e, \"upy\": %.18e}\n", latitude, boxCenter.x, boxCenter.y, box1up.x, box1up.y).getBytes());

                stream.write(String.format(",{\"type\": \"text\", \"class\": \"gridText\", \"textBaseline\": \"top\", \"d\": \"%d\", \"ax\": %.18e, \"ay\": %.18e, \"upx\": %.18e, \"upy\": %.18e}\n", longitude, boxCenter.x, boxCenter.y, box1up.x, box1up.y).getBytes());
            }
        }

        return comma;
    }

    public static boolean writeDrawables(OutputStream stream, boolean comma, double offsetx, double offsety, double radius, DatabaseInterface databaseInterface) throws IOException {
        Circle visible = centralCircle(offsetx, offsety, radius);
        IndexRange latitudes = latitudeRange(visible);

        List<DatabaseInterface.DepthDrawable> depthDrawables = new ArrayList<DatabaseInterface.DepthDrawable>();

        for (int latitude = latitudes.min;  latitude <= latitudes.max;  latitude++) {
            IndexRangeL longitudes = longitudeRange(visible, latitude);
            if (longitudes == null) { continue; }

            depthDrawables.addAll(databaseInterface.getRange(latitude, longitudes.min, longitudes.max));
        }

        Collections.sort(depthDrawables);

        Set<Long> idsSeen = new HashSet<Long>();
        Map<Double,Circle> circles = new HashMap<Double,Circle>();   // drawings tend to reuse limits; cache them

        for (DatabaseInterface.DepthDrawable depthDrawable : depthDrawables) {
            // ids to draw must be unique (DB doesn't guarantee that because it's geographically distributed)
            if (idsSeen.contains(depthDrawable.id)) { continue; }   // only draw the deepest one
            idsSeen.add(depthDrawable.id);

            if (depthDrawable.minRadius != 0.0) {
                Circle thisCircle;
                if (circles.containsKey(depthDrawable.minRadius)) {
                    thisCircle = circles.get(depthDrawable.minRadius);
                }
                else {
                    thisCircle = centralCircle(offsetx, offsety, depthDrawable.minRadius);
                    circles.put(depthDrawable.minRadius, thisCircle);
                }

                // if this drawable is within the radius, DON'T draw it (this is the minRadius threshold)
                boolean good = true;
                IndexRange thisLatitudes = latitudeRange(thisCircle);
                if (thisLatitudes.min <= depthDrawable.latitude  &&  depthDrawable.latitude <= thisLatitudes.max) {
                    IndexRangeL thisLongitudes = longitudeRange(thisCircle, depthDrawable.latitude);
                    if (thisLongitudes != null  &&  thisLongitudes.min <= depthDrawable.longitude  &&  depthDrawable.longitude <= thisLongitudes.max) {
                        good = false;
                    }
                }

                if (!good) { continue; }
            }

            if (depthDrawable.maxRadius != 1.0) {
                Circle thisCircle;
                if (circles.containsKey(depthDrawable.maxRadius)) {
                    thisCircle = circles.get(depthDrawable.maxRadius);
                }
                else {
                    thisCircle = centralCircle(offsetx, offsety, depthDrawable.maxRadius);
                    circles.put(depthDrawable.maxRadius, thisCircle);
                }

                // if this drawable isn't within the radius, don't draw it (it's too far away, exceeds maxRadius)
                boolean good = false;
                IndexRange thisLatitudes = latitudeRange(thisCircle);
                if (thisLatitudes.min <= depthDrawable.latitude  &&  depthDrawable.latitude <= thisLatitudes.max) {
                    IndexRangeL thisLongitudes = longitudeRange(thisCircle, depthDrawable.latitude);
                    if (thisLongitudes != null  &&  thisLongitudes.min <= depthDrawable.longitude  &&  depthDrawable.longitude <= thisLongitudes.max) {
                        good = true;
                    }
                }

                if (!good) { continue; }
            }

            if (!comma) {
                comma = true;
            } else {
                stream.write(",".getBytes());
            }
            stream.write(depthDrawable.drawable.getBytes());
        }
        return comma;
    }
}
