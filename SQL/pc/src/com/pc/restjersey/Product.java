package com.pc.restjersey;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.json.JSONObject;


@Path("/product1")
public class Product {
	@GET
	@Produces(MediaType.APPLICATION_JSON)  
	public Response defaultPath() {
		JSONObject jsonObject = new JSONObject();
		jsonObject.put("result", new String[] { "Product 1", "Product 2", "Product 3" });
		return Response.status(200).entity(""+jsonObject).build();
	}

	@Path("{id}")
	@GET
	@Produces("application/json")
	public Response convertCtoFfromInput(@PathParam("term") String term) {
		JSONObject jsonObject = new JSONObject();
		jsonObject.put("result", new String[] {"DB Result", "Product 1", "Product 2", "Product 3" });
		return Response.status(200).entity(""+jsonObject).build();
	}

}
