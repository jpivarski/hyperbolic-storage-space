package org.hyperbolicstorage;

import org.hyperbolicstorage.DatabaseInterface;
import org.hyperbolicstorage.GeographicalTiles;

import java.io.PrintWriter;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
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
	response.setContentType("application/json");
        PrintWriter printWriter = response.getWriter();

        printWriter.print("{\"fillstyle\": \"none\", \"lineWidth\": 1.5, \"drawables\": [");
        boolean comma = false;

        comma = GeographicalTiles.printGrid(printWriter, comma);

        printWriter.println("]}");
        printWriter.close();

    }
}
