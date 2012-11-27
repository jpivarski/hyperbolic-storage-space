package org.hyperbolicstorage;

import org.hyperbolicstorage.DatabaseInterface;
import org.hyperbolicstorage.GeographicalTiles;

import java.lang.Float;
import java.lang.Long;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletException;

public class HyperbolicMapLoader extends HttpServlet {
    static DatabaseInterface databaseInterface = null;

    public void init() throws ServletException {
        try {
            databaseInterface = new DatabaseInterface(getInitParameter("dbPath"));
        }
        catch (IOException exception) {
            throw new ServletException("HyperbolicMapLoader: Failed to create database connection");
        }
    }

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        processRequest(request, response);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        processRequest(request, response);
    }

    protected void processRequest(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String command = request.getParameter("command");
        if (command.equals("clearAll")) {
            clearAll(request, response);
        }
        else if (command.equals("addDrawable")) {
            addDrawable(request, response);
        }
        else {
            PrintWriter output = response.getWriter();
            output.println(String.format("<UnrecognizedCommand command=\"%s\" />", command));
        }
    }

    protected void clearAll(HttpServletRequest request, HttpServletResponse response) throws IOException {
        databaseInterface.clearAll();
    }

    protected void addDrawable(HttpServletRequest request, HttpServletResponse response) throws IOException {
        PrintWriter output = response.getWriter();

        String x_ = request.getParameter("x");
        String y_ = request.getParameter("y");
        String z_ = request.getParameter("z");
        String mind_ = request.getParameter("mind");
        String maxd_ = request.getParameter("maxd");
        String id_ = request.getParameter("id");
        String drawable = request.getParameter("drawable");

        if (x_ == null) {
            output.println("<MissingArgument argument=\"x\" />");
            return;
        }
        if (y_ == null) {
            output.println("<MissingArgument argument=\"y\" />");
            return;
        }
        if (z_ == null) {
            output.println("<MissingArgument argument=\"z\" />");
            return;
        }
        if (mind_ == null) {
            mind_ = "0.0";
        }
        if (maxd_ == null) {
            maxd_ = "1.0";
        }
        if (id_ == null) {
            output.println("<MissingArgument argument=\"id\" />");
            return;
        }
        if (drawable == null) {
            output.println("<MissingArgument argument=\"drawable\" />");
            return;
        }

        double x = Float.parseFloat(x_);
        double y = Float.parseFloat(y_);
        double z = Float.parseFloat(z_);
        double mind = Float.parseFloat(mind_);
        double maxd = Float.parseFloat(maxd_);
        long id = Long.parseLong(id_);
        
        GeographicalTiles.Point2D hyperShadow = new GeographicalTiles.Point2D(x, y);
        GeographicalTiles.Point2D halfPlane = GeographicalTiles.hyperShadow_to_halfPlane(hyperShadow);
        GeographicalTiles.IndexPair tileIndex = GeographicalTiles.tileIndex(halfPlane);

        databaseInterface.insert(tileIndex.latitude, tileIndex.longitude, id, z, mind, maxd, drawable);

        output.println(String.format("<Inserted halfPlane=\"%g,%g\" latitude=\"%d\" longitude=\"%d\" />", halfPlane.x, halfPlane.y, tileIndex.latitude, tileIndex.longitude));
    }
}
