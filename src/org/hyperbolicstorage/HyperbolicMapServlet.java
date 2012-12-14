package org.hyperbolicstorage;

import org.hyperbolicstorage.DatabaseInterface;
import org.hyperbolicstorage.GeographicalTiles;

import java.lang.Float;
import java.util.List;
import java.io.OutputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletOutputStream;
import javax.servlet.ServletException;

public class HyperbolicMapServlet extends HttpServlet {
    DatabaseInterface databaseInterface = null;

    public void init() throws ServletException {
        try {
            databaseInterface = new DatabaseInterface(getInitParameter("dbPath"));
        }
        catch (IOException exception) {
            // throw new ServletException("HyperbolicMapLoader: Failed to create database connection");
            throw new ServletException(getInitParameter("dbPath"));
        }
    }

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        processRequest(request, response);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        processRequest(request, response);
    }

    protected void processRequest(HttpServletRequest request, HttpServletResponse response) throws IOException {
	String Bx = request.getParameter("Bx");
	String By = request.getParameter("By");
	String a = request.getParameter("a");

        double offsetx, offsety, radius;
        if (Bx == null) {
            offsetx = 0.0;
        } else {
            offsetx = Float.parseFloat(Bx);
        }
        if (By == null) {
            offsety = 0.0;
        } else {
            offsety = Float.parseFloat(By);
        }
        if (a == null) {
            radius = 0.99;
        } else {
            radius = Float.parseFloat(a);
        }

        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        stream.write("[".getBytes());
        boolean comma = false;
        // comma = GeographicalTiles.writeGrid(stream, comma, offsetx, offsety, radius);
        comma = GeographicalTiles.writeDrawables(stream, comma, offsetx, offsety, radius, databaseInterface);
        stream.write("]\n".getBytes());

	response.setContentType("application/json;charset=UTF-8");
        response.setContentLength(stream.size());
	ServletOutputStream servletOutputStream = response.getOutputStream();
        servletOutputStream.write(stream.toByteArray());
        servletOutputStream.close();
    }
}
