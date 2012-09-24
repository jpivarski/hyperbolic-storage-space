package org.hyperbolicstorage;

import java.io.PrintWriter;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;

public class HyperbolicMapServlet extends HttpServlet {

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        processRequest(request, response);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        processRequest(request, response);
    }

    protected void processRequest(HttpServletRequest request, HttpServletResponse response) throws IOException {
	// request.getParameter("");
	// response.setContentType("application/json");
        // PrintWriter printWriter = response.getWriter();
        // printWriter.println("");
        // printWriter.close();

        PrintWriter printWriter = response.getWriter();
        printWriter.println("hello");
        printWriter.close();
        
    }
}
