package com.pc.restjersey;

import javax.ws.rs.Consumes;
import javax.ws.rs.DELETE;
import javax.ws.rs.FormParam;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.json.JSONArray;
import org.json.JSONObject;

import com.pc.db.ProductLineDB;
import com.pc.vo.ProductLineVo;

@Path("/productline")
public class ProductLineAPI {
	@GET
	@Produces(MediaType.APPLICATION_JSON)
	public Response defaultPath() throws Exception {
		JSONArray jsonObject = (new ProductLineDB().getAllProductLines());
		return Response.status(200).entity("" + jsonObject).build();
	}

	@POST
	@Path("/post")
	@Consumes(MediaType.APPLICATION_FORM_URLENCODED)
	@Produces(MediaType.APPLICATION_JSON)
	public Response createStore(@FormParam("Id") String id, @FormParam("Name") String name) throws Exception {
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId("" + java.util.UUID.randomUUID());
		productLineVo.setName(name);
		// System.out.println(storeVo);
		(new ProductLineDB()).insertProductLine(productLineVo);
		JSONObject obj = new JSONObject();
		obj.put("Id", productLineVo.getId());
		obj.put("Name", productLineVo.getName());
		return Response.status(201).entity("" + obj).build();
	}

	@PUT
	@Path("/put")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public Response updateStore(String content) throws Exception {
//		System.out.println(content);
		JSONObject obj = new JSONObject(content);
		String name = obj.getString("Name");
		String id = obj.getString("Id");
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId(id);
		productLineVo.setName(name);
		System.out.println(productLineVo);
		(new ProductLineDB()).updateProductLine(productLineVo);
		return Response.status(201).entity("" + obj).build();
	}

	@DELETE
	@Path("/delete")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public Response deleteProductLine(String content) throws Exception {
		JSONObject obj = new JSONObject(content);
		String name = obj.getString("Name");
		String id = obj.getString("Id");
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId(id);
		productLineVo.setName(name);
		System.out.println(productLineVo);
		try {
			(new ProductLineDB()).deleteProductLine(productLineVo);
		} catch (Exception e) {
			JSONObject jsonObject = new JSONObject();
			jsonObject.put("Error", "Can't delete product line. First, remove the relationship between Store and ProductLine.");
			return Response.status(500).entity("" + jsonObject).build();
		}
		return Response.status(201).entity("" + obj).build();
	}	
}
