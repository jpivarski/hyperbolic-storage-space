package org.hyperbolicstorage;

import java.lang.Math;
import java.awt.geom.Point2D;
import java.io.PrintWriter;

public class GeographicalTiles {
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

    protected static boolean printPoint(PrintWriter printWriter, Point2D.Double p, String options, boolean comma) {
        if (!comma) {
            comma = true;
        } else {
            printWriter.print(",");
        }

        if (options == null) {
            printWriter.print(String.format("[%g,%g]", p.x, p.y));
        }
        else {
            printWriter.print(String.format("[%g,%g,\"%s\"]", p.x, p.y, options));
        }

        return comma;
    }

    public static boolean printGrid(PrintWriter printWriter, boolean comma) {
        for (int row = -8;  row <= 8;  row++) {
            double size = Math.pow(2, row);
            for (int col = -4;  col <= 4;  col++) {
                if (!comma) {
                    comma = true;
                } else {
                    printWriter.print(",");
                }

                printWriter.print("{\"type\": \"polygon\", \"d\": [");
                boolean comma2 = false;

                comma2 = printPoint(printWriter, halfPlane_to_hyperShadow(new Point2D.Double(size*(col), size)), "L", comma2);
                comma2 = printPoint(printWriter, halfPlane_to_hyperShadow(new Point2D.Double(size*(col+0.5), size)), "L", comma2);
                comma2 = printPoint(printWriter, halfPlane_to_hyperShadow(new Point2D.Double(size*(col+1), size)), "L", comma2);
                comma2 = printPoint(printWriter, halfPlane_to_hyperShadow(new Point2D.Double(size*(col+1), 2*size)), null, comma2);

                printWriter.println("]}");
            }
        }

        return comma;
    }
}
