package com.pc.restjersey;
import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.json.JSONArray;

import com.pc.bo.StoreProductLineBo;
import com.pc.db.StoreProductLineDB;
import com.pc.vo.StoreProductLineVo;
import com.pc.vo.StoreVo;

@Path("/storepl")
public class StoreProductLineAPI {
	@Path("/pl")
	@GET
	@Produces(MediaType.APPLICATION_JSON)
	public Response getAllProductLines(@QueryParam("Id") String id) throws Exception {
		StoreVo storeVo = new StoreVo();
		storeVo.setId(id);
		System.out.println(storeVo);
		JSONArray jsonObject = (new StoreProductLineDB().getAllProductLines(storeVo));
		return Response.status(200).entity("" + jsonObject).build();
	}
	
	@PUT
	@Path("/put")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public Response updateStoreProductLineRel(String content) throws Exception {
		StoreProductLineVo storeProductLineVo = StoreProductLineBo.toPOJO(content);
		new StoreProductLineDB().updateStoreProductLine(storeProductLineVo);
		return Response.status(200).entity("").build();
	}
	
}
