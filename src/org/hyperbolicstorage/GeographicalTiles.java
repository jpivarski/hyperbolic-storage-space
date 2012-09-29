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

        double phi = Math.atan2(x*x + y*y - 1.0, 2.0 * x);




    }



    public static String printGrid(PrintWriter printWriter, String comma) {
        for (int row = -15;  row <= 15;  row++) {
            double size = Math.pow(2, row);
            for (int col = -4;  col <= 4;  col++) {
                



            }
        }

        return comma;
    }
}
