package com.pc.restjersey;

import java.math.BigDecimal;

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

import com.pc.db.ProductDB;
import com.pc.vo.ProductVo;

@Path("/product")
public class ProductAPI {
	@GET
	@Produces(MediaType.APPLICATION_JSON)
	public Response defaultPath() throws Exception {
		JSONArray jsonObject = (new ProductDB().getAllProducts());
		return Response.status(200).entity("" + jsonObject).build();
	}

	@POST
	@Path("/post")
	@Consumes(MediaType.APPLICATION_FORM_URLENCODED)
	@Produces(MediaType.APPLICATION_JSON)
	public Response createProduct(@FormParam("Id") String id, @FormParam("Name") String name,
			@FormParam("Price") BigDecimal price) throws Exception {
		ProductVo productVo = new ProductVo();
		productVo.setId("" + java.util.UUID.randomUUID());
		productVo.setName(name);
		productVo.setPrice(price);;
		System.out.println(productVo);
		(new ProductDB()).insertProduct(productVo);;
		JSONObject obj = new JSONObject();
		obj.put("Id", productVo.getId());
		obj.put("Name", productVo.getName());
		obj.put("Price", productVo.getPrice());
		return Response.status(201).entity("" + obj).build();
	}	
	
	@PUT
	@Path("/put")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public Response updateProduct(String content) throws Exception {
		JSONObject obj = new JSONObject(content);
		String name = obj.getString("Name");
		String price = obj.getString("Price");
		String id = obj.getString("Id");
		ProductVo productVo = new ProductVo();
		productVo.setId(id);
		productVo.setName(name);
		productVo.setPrice(new BigDecimal(price));
		System.out.println(productVo);
		(new ProductDB()).updateProduct(productVo);
		return Response.status(201).entity("" + obj).build();
	}

	@DELETE
	@Path("/delete")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public Response deleteProduct(String content) throws Exception {
		JSONObject obj = new JSONObject(content);
		String id = obj.getString("Id");
		ProductVo productVo = new ProductVo();
		productVo.setId(id);
		System.out.println(productVo);
		try {
			(new ProductDB()).deleteProduct(productVo);
		} catch (Exception e) {
			JSONObject jsonObject = new JSONObject();
			jsonObject.put("Error", "Can't delete product. First, remove the relationship between ProductLine and Product.");
			return Response.status(500).entity("" + jsonObject).build();
		}
		return Response.status(201).entity("" + obj).build();
	}	
}
