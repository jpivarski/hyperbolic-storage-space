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

    public static String dungeonPoint(int latitude, long longitude, double x, double y) {
        double size = Math.pow(2, latitude);
        Point2D xy = halfPlane_to_hyperShadow(new Point2D((x + 0.5*longitude)*size, y*size));
        return String.format("%.18e, %.18e", xy.x, xy.y);
    }

    public static boolean writeDungeon(OutputStream stream, boolean comma, double offsetx, double offsety, double radius) throws IOException {
        Circle visible = centralCircle(offsetx, offsety, radius);
        IndexRange latitudes = latitudeRange(visible);

        for (int latitude = latitudes.min;  latitude <= latitudes.max;  latitude++) {
            IndexRangeL longitudes = longitudeRange(visible, latitude);
            if (longitudes == null) { continue; }

            for (long longitude = longitudes.min;  longitude <= longitudes.max;  longitude++) {
                if (!comma) {
                    comma = true;
                } else {
                    stream.write(",".getBytes());
                }

                stream.write(("{\"strokeStyle\": \"none\", \"d\": [[" + dungeonPoint(latitude, longitude, 0.0035722099182922875, 0.8530670239545664) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.018498612152460587, 0.8530670239545664) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.018498612152460587, 0.9815045140589823) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.10255350911754954, 0.9815045140589823) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.10255350911754954, 0.996497212740246) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.001628606195931924, 0.9978996127362316) + ", \"L\"]], \"lineWidth\": 0.28839591, \"type\": \"polygon\", \"fillStyle\": \"#8a8a91\"}\n").getBytes());
                stream.write((",{\"strokeStyle\": \"none\", \"d\": [[" + dungeonPoint(latitude, longitude, 0.41193609447018764, 0.996497212740246) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.41193609447018764, 0.9815045140589823) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.48849859311833194, 0.9815045140589823) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.48849859311833194, 0.8530670239545664) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.5035376889303103, 0.8530670239545664) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.5071218961176088, 0.9984369173501794) + ", \"L\"]], \"lineWidth\": 0.28839591, \"type\": \"polygon\", \"fillStyle\": \"#8a8a91\"}\n").getBytes());
                stream.write((",{\"strokeStyle\": \"none\", \"d\": [[" + dungeonPoint(latitude, longitude, 0.30150372500782857, 0.4964972300439995) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.30150372500782857, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.25400372226806756, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.20619122527819964, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.20619122527819964, 0.4964972300439995) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.2523965265829776, 0.4938455336618855) + ", \"L\"]], \"lineWidth\": 0.28839591, \"type\": \"polygon\", \"fillStyle\": \"#8a8a91\"}\n").getBytes());
                stream.write((",{\"strokeStyle\": \"none\", \"d\": [[" + dungeonPoint(latitude, longitude, 0.502345010425223, 0.5955670321738491) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.48734500956003535, 0.5955670321738491) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.48734500956003535, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.4564075135435035, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.4564075135435035, 0.49645813509720876) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.5095256066421956, 0.4917488378655036) + ", \"L\"]], \"lineWidth\": 0.28839591, \"type\": \"polygon\", \"fillStyle\": \"#8a8a91\"}\n").getBytes());
                stream.write((",{\"d\": [[" + dungeonPoint(latitude, longitude, 0.0035722099182922875, 0.8530670239545664) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.018498612152460587, 0.8530670239545664) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.018498612152460587, 0.9815045140589823) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.10255350911754954, 0.9815045140589823) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.10255350911754954, 0.996497212740246) + "]], \"lineWidth\": 2.5, \"type\": \"polygon\"}\n").getBytes());
                stream.write((",{\"d\": [[" + dungeonPoint(latitude, longitude, 0.41193609447018764, 0.996497212740246) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.41193609447018764, 0.9815045140589823) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.48849859311833194, 0.9815045140589823) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.48849859311833194, 0.8530670239545664) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.5035376889303103, 0.8530670239545664) + "]], \"lineWidth\": 2.5, \"type\": \"polygon\"}\n").getBytes());
                stream.write((",{\"d\": [[" + dungeonPoint(latitude, longitude, 0.30150372500782857, 0.4964972300439995) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.30150372500782857, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.25400372226806756, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.20619122527819964, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.20619122527819964, 0.4964972300439995) + "]], \"lineWidth\": 2.5, \"type\": \"polygon\"}\n").getBytes());
                stream.write((",{\"d\": [[" + dungeonPoint(latitude, longitude, 0.502345010425223, 0.5955670321738491) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.48734500956003535, 0.5955670321738491) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.48734500956003535, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.4564075135435035, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.4564075135435035, 0.49645813509720876) + "]], \"lineWidth\": 2.5, \"type\": \"polygon\"}\n").getBytes());
                stream.write((",{\"strokeStyle\": \"none\", \"d\": [[" + dungeonPoint(latitude, longitude, 0.05172003057688578, 0.4964972300439995) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.05172003057688578, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.017345028594164043, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.017345028594164043, 0.5955670321738491) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.002345027728976404, 0.5955670321738491) + ", \"L\"], [" + dungeonPoint(latitude, longitude, -0.0006596767578118613, 0.49357913661076797) + ", \"L\"]], \"lineWidth\": 0.28839591, \"type\": \"polygon\", \"fillStyle\": \"#8a8a91\"}\n").getBytes());
                stream.write((",{\"d\": [[" + dungeonPoint(latitude, longitude, 0.05172003057688578, 0.4964972300439995) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.05172003057688578, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.017345028594164043, 0.5115045330931111) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.017345028594164043, 0.5955670321738491) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.002345027728976404, 0.5955670321738491) + "]], \"lineWidth\": 2.5, \"type\": \"polygon\"}\n").getBytes());
                stream.write((",{\"d\": [[" + dungeonPoint(latitude, longitude, 0.10704075305011822, 1.0092354284660239) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.25629494685988496, 1.0032300224273947) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.2554908414405744, 0.983246125300285) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.10623664763080756, 0.9892516236255988) + ", \"L\"]], \"lineWidth\": 2.5, \"type\": \"polygon\", \"fillStyle\": \"#803300\"}\n").getBytes());
                stream.write((",{\"d\": [[" + dungeonPoint(latitude, longitude, 0.40697664264386585, 1.0092354284660239) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.25772244883409906, 1.0032300224273947) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.2585265427175741, 0.983246125300285) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.40778073652734087, 0.9892516236255988) + ", \"L\"]], \"lineWidth\": 2.5, \"type\": \"polygon\", \"fillStyle\": \"#803300\"}\n").getBytes());
                stream.write((",{\"d\": [[" + dungeonPoint(latitude, longitude, -0.005836671371557196, 0.599415732999394) + ", \"L\"], [" + dungeonPoint(latitude, longitude, -0.0008492336081111869, 0.7233701897512292) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.01574723461507426, 0.7227023802293312) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.010759716100779177, 0.5987479350133317) + ", \"L\"]], \"lineWidth\": 2.07623076, \"type\": \"polygon\", \"fillStyle\": \"#803300\"}\n").getBytes());
                stream.write((",{\"d\": [[" + dungeonPoint(latitude, longitude, -0.005836671371557196, 0.84851017279009) + ", \"L\"], [" + dungeonPoint(latitude, longitude, -0.0008492336081111869, 0.7245557160382549) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.01574723461507426, 0.7252235140243172) + ", \"L\"], [" + dungeonPoint(latitude, longitude, 0.010759716100779177, 0.8491779707761523) + ", \"L\"]], \"lineWidth\": 2.07623076, \"type\": \"polygon\", \"fillStyle\": \"#803300\"}\n").getBytes());

                if (latitude == 0  &&  longitude == 0) {
                    stream.write(",{\"d\": [[0.09651601137594819, -0.1224181183434036, \"L\"], [0.1194088329663479, -0.1994864147386012, \"L\"], [0.1289179675674319, -0.19684019790209642, \"L\"], [0.1228292874002955, -0.17727100316861366, \"L\"], [0.1324752265202032, -0.17461571274833937, \"L\"], [0.1433086704739346, -0.1990655815354423, \"L\"], [0.21456057666578163, -0.17919223467726886, \"L\"], [0.20846216529457473, -0.1536730102405995, \"L\"], [0.21775042586738794, -0.15111100536863756, \"L\"], [0.22445277010909118, -0.17026635947812543, \"L\"], [0.23407418956415882, -0.16759281952840194, \"L\"], [0.2207778293238709, -0.12958521397511466, \"L\"], [0.2112804652588409, -0.13218582652921376, \"L\"], [0.20812998276808584, -0.12280511396315953, \"L\"], [0.18923734109983936, -0.12795444604858885, \"L\"], [0.17285008904314939, -0.07600476572564897, \"L\"], [0.19683735229866542, -0.056055691019394574, \"L\"], [0.19407487704090887, -0.04706802135138413, \"L\"], [0.14795498980772218, -0.05922594089017514, \"L\"], [0.15059011872749317, -0.06829808345709948, \"L\"], [0.1413734370684053, -0.0707243964519046, \"L\"], [0.15228618143858258, -0.10752955936990792, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#ff9933\"}".getBytes());
                    stream.write(",{\"d\": [[0.21825575416851745, -0.18262415065190313, \"L\"], [0.2114978591443495, -0.16331000040880053, \"L\"], [0.20193802735749738, -0.16595722127759305, \"L\"], [0.2052556326818521, -0.17560288442492739, \"L\"], [0.14795189694949928, -0.1915435637263213, \"L\"], [0.14481988053070002, -0.1817730150156527, \"L\"], [0.1353304482077796, -0.1843998132601014, \"L\"], [0.1415885760664324, -0.20404915086542194, \"L\"], [0.151139566919554, -0.20137744805130478, \"L\"], [0.15438392656671956, -0.2112767080422151, \"L\"], [0.2120693441107128, -0.195081483380456, \"L\"], [0.20863236082811257, -0.1853103022158956, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#006600\"}".getBytes());
                    stream.write(",{\"d\": [[0.1986784465244196, -0.1563713775062255, \"L\"], [0.19232912444931283, -0.13737175540691593, \"L\"], [0.20179791054706578, -0.13478127304539686, \"L\"], [0.2114978591443495, -0.16331000040880053, \"L\"], [0.20193802735749738, -0.16595722127759305, \"L\"], [0.2052556326818521, -0.17560288442492739, \"L\"], [0.14795189694949928, -0.1915435637263213, \"L\"], [0.14481988053070002, -0.1817730150156527, \"L\"], [0.1353304482077796, -0.1843998132601014, \"L\"], [0.1263466473105438, -0.1553837317490925, \"L\"], [0.13574783750560981, -0.152822085451431, \"L\"], [0.14174251191712092, -0.1720638367187477, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#663300\"}".getBytes());
                    stream.write(",{\"d\": [[0.18599013980988258, -0.14944829143455918, \"L\"], [0.17651631059262055, -0.15204892887135885, \"L\"], [0.17965874225456532, -0.16161582408575076, \"L\"], [0.18916258820645596, -0.1589954859363092, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#006600\"}".getBytes());
                    stream.write(",{\"d\": [[0.1481555806167153, -0.15982799440035375, \"L\"], [0.14515562198635085, -0.1502569777691799, \"L\"], [0.15457101773442528, -0.14768818301967726, \"L\"], [0.1576000649949603, -0.15723856190361088, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#663300\"}".getBytes());
                    stream.write(",{\"d\": [[0.1576000649949603, -0.15723856190361088, \"L\"], [0.1481555806167153, -0.15982799440035375, \"L\"], [0.15120878568629, -0.16945638874663582, \"L\"], [0.1606828869261011, -0.16684605457427482, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#006600\"}".getBytes());
                    stream.write(",{\"d\": [[0.17342872003792914, -0.142538649365248, \"L\"], [0.18287307132036248, -0.13995747828878377, \"L\"], [0.18599013980988258, -0.14944829143455918, \"L\"], [0.17651631059262055, -0.15204892887135885, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#663300\"}".getBytes());
                    stream.write(",{\"d\": [[0.18923734109983936, -0.12795444604858885, \"L\"], [0.19867686391201142, -0.12538244843417876, \"L\"], [0.19561027356936447, -0.11603616690020091, \"L\"], [0.1861994949893267, -0.11858988844391502, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#006600\"}".getBytes());
                    stream.write(",{\"d\": [[0.17039499228349458, -0.13308324477164854, \"L\"], [0.1674141755102451, -0.12368103631863736, \"L\"], [0.14867046966210892, -0.12875183093896297, \"L\"], [0.15159479438187992, -0.1381931684056055, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#663300\"}".getBytes());
                    stream.write(",{\"d\": [[0.09793245186795566, -0.09198430893249543, \"L\"], [0.11127593011724801, -0.1388391914115851, \"L\"], [0.12061544475894108, -0.13632358048806525, \"L\"], [0.12345584536772117, -0.1458264216396687, \"L\"], [0.13282865816640751, -0.1432859278778409, \"L\"], [0.12996037679592345, -0.13380396581942566, \"L\"], [0.13931172012141727, -0.131280122847343, \"L\"], [0.1364659761449178, -0.12187096103687052, \"L\"], [0.15513660216947248, -0.11684909489417285, \"L\"], [0.1413734370684053, -0.0707243964519046, \"L\"], [0.11377197109537047, -0.07796256446235664, \"L\"], [0.11635252693284068, -0.08715178113933933, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#006600\"}".getBytes());
                    stream.write(",{\"d\": [[0.2144731315044143, -0.11091142345212872, \"L\"], [0.21140305053848849, -0.10165115249747884, \"L\"], [0.22082840524435224, -0.09909674590732516, \"L\"], [0.206126213670997, -0.053583704316131534, \"L\"], [0.15059011872749317, -0.06829808345709948, \"L\"], [0.16160759209439474, -0.10502978748665288, \"L\"], [0.15228618143858258, -0.10752955936990792, \"L\"], [0.15513660216947248, -0.11684909489417285, \"L\"], [0.16448534304459536, -0.11433040467309903, \"L\"], [0.1674141755102451, -0.12368103631863736, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#663300\"}".getBytes());
                    stream.write(",{\"d\": [[0.12345584536772117, -0.1458264216396687, \"L\"], [0.12061544475894108, -0.13632358048806525, \"L\"], [0.10194083946899839, -0.14135102725230986, \"L\"], [0.10755998699702646, -0.1604975640349655, \"L\"], [0.11695103556125491, -0.15794214652986638, \"L\"], [0.11408852943756619, -0.14836329294728054, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#663300\"}".getBytes());
                    stream.write(",{\"d\": [[0.10312916252977128, -0.11057921863536616, \"L\"], [0.10579706692423951, -0.11994871513587992, \"L\"], [0.11508241419459701, -0.11747479683890477, \"L\"], [0.11238812057794766, -0.10812574260582167, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#663300\"}".getBytes());
                    stream.write(",{\"d\": [[0.10974089884984024, -0.09882492921417553, \"L\"], [0.11238812057794766, -0.10812574260582167, \"L\"], [0.13092257101265178, -0.10320329501280898, \"L\"], [0.13366987464367142, -0.11251252480169052, \"L\"], [0.15228618143858258, -0.10752955936990792, \"L\"], [0.14948549159173247, -0.0982587553924218, \"L\"], [0.14019999011120926, -0.10073389232262375, \"L\"], [0.1374744730280626, -0.09149155164355476, \"L\"], [0.14673368564207495, -0.08903522430168512, \"L\"], [0.14402993671414996, -0.0798575579026118, \"L\"], [0.12557107954970687, -0.08472664061092304, \"L\"], [0.12822324096888615, -0.09394180543842673, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#663300\"}".getBytes());
                    stream.write(",{\"d\": [[0.09960732068226799, -0.06207633335189696, \"L\"], [0.10713996552570747, -0.08957093291760135, \"L\"], [0.11635252693284068, -0.08715178113933933, \"L\"], [0.11377197109537047, -0.07796256446235664, \"L\"], [0.13216547680926663, -0.07314377933269027, \"L\"], [0.12704063889010062, -0.0549696964418738, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#663300\"}".getBytes());
                    stream.write(",{\"d\": [[0.20199297698783625, -0.10419911203879464, \"L\"], [0.19900451982425715, -0.09497066572933788, \"L\"], [0.20838651637573324, -0.09243988179589493, \"L\"], [0.20542258673869465, -0.08327611753260637, \"L\"], [0.19606817896670994, -0.08578990968478648, \"L\"], [0.19034824370885287, -0.06756574180036728, \"L\"], [0.18106120672867804, -0.07003850705437746, \"L\"], [0.18672770284381215, -0.08829676682665137, \"L\"], [0.17740017399598068, -0.09079688266631543, \"L\"], [0.1802818277119852, -0.10001263532790633, \"L\"], [0.18963662196862988, -0.0974948518393034, \"L\"], [0.19259717324281964, -0.10674081899376814, \"L\"]], \"lineWidth\": 2.0, \"type\": \"polygon\", \"fillStyle\": \"#ffff00\"}".getBytes());
                }
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
