package org.hyperbolicstorage;

import org.hyperbolicstorage.DatabaseInterface;
import org.hyperbolicstorage.GeographicalTiles;

import java.io.OutputStream;
import java.io.ByteArrayOutputStream;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletOutputStream;
import java.io.IOException;

public class HyperbolicMapServlet extends HttpServlet {
    // static DatabaseInterface databaseInterface = null;

    // static {
    //     try {
    //         databaseInterface = new DatabaseInterface("/tmp/babudb");
    //     }
    //     catch (IOException exception) {
    //         System.err.println("HyperbolicMapServlet: Failed to create database connection");
    //         exception.printStackTrace(System.err);
    //     }
    // }

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        processRequest(request, response);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        processRequest(request, response);
    }

    protected void processRequest(HttpServletRequest request, HttpServletResponse response) throws IOException {
	// request.getParameter("");

        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        stream.write("{\"fillstyle\": \"none\", \"lineWidth\": 1.5, \"drawables\": [".getBytes());
        boolean comma = false;
        comma = GeographicalTiles.writeGrid(stream, comma);
        stream.write("]}\n".getBytes());

	response.setContentType("application/json;charset=UTF-8");
        response.setContentLength(stream.size());
	ServletOutputStream servletOutputStream = response.getOutputStream();
        servletOutputStream.write(stream.toByteArray());
        servletOutputStream.close();
    }
}
