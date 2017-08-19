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

import com.pc.db.StoreDB;
import com.pc.util.StoreTestJson;
import com.pc.vo.StoreVo;

@Path("/store")
public class StoreAPI {
	@GET
	@Produces(MediaType.APPLICATION_JSON)
	public Response defaultPath() throws Exception {
		JSONArray jsonObject = (new StoreDB().getAllStores());
		return Response.status(200).entity("" + jsonObject).build();
	}

	@Path("/test")
	@GET
	@Produces(MediaType.APPLICATION_JSON)
	public Response defaultTestPath() {
		JSONArray jsonObject = StoreTestJson.getTestStore();
		return Response.status(200).entity("" + jsonObject).build();
	}

	@POST
	@Path("/post")
	@Consumes(MediaType.APPLICATION_FORM_URLENCODED)
	@Produces(MediaType.APPLICATION_JSON)
	public Response createStore(@FormParam("Id") String id, @FormParam("Name") String name,
			@FormParam("Address") String address) throws Exception {
		StoreVo storeVo = new StoreVo();
		storeVo.setId("" + java.util.UUID.randomUUID());
		storeVo.setName(name);
		storeVo.setAddress(address);
		// System.out.println(storeVo);
		(new StoreDB()).insertStore(storeVo);
		JSONObject obj = new JSONObject();
		obj.put("Id", storeVo.getId());
		obj.put("Name", storeVo.getName());
		obj.put("Address", storeVo.getAddress());
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
		String address = obj.getString("Address");
		String id = obj.getString("Id");
		StoreVo storeVo = new StoreVo();
		storeVo.setId(id);
		storeVo.setName(name);
		storeVo.setAddress(address);
		 System.out.println(storeVo);
		(new StoreDB()).updateStore(storeVo);
		return Response.status(201).entity("" + obj).build();
	}

	@DELETE
	@Path("/delete")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public Response deleteStore(String content) throws Exception {
		JSONObject obj = new JSONObject(content);
		String name = obj.getString("Name");
		String address = obj.getString("Address");
		String id = obj.getString("Id");
		StoreVo storeVo = new StoreVo();
		storeVo.setId(id);
		storeVo.setName(name);
		storeVo.setAddress(address);
		System.out.println(storeVo);
		(new StoreDB()).deleteStore(storeVo);
		return Response.status(201).entity("" + obj).build();
	}	
}
