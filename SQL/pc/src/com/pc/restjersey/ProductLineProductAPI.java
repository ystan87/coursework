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

import com.pc.bo.ProductLineProductBo;
import com.pc.db.ProductLineProductDB;
import com.pc.vo.ProductLineProductVo;
import com.pc.vo.ProductLineVo;

@Path("/plproduct")
public class ProductLineProductAPI {
	@Path("/prod")
	@GET
	@Produces(MediaType.APPLICATION_JSON)
	public Response getAllProducts(@QueryParam("Id") String id) throws Exception {
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId(id);
		JSONArray jsonObject = (new ProductLineProductDB().getAllProducts(productLineVo));
		return Response.status(200).entity("" + jsonObject).build();
	}
	
	@PUT
	@Path("/put")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public Response updateProductLineProductRel(String content) throws Exception {
		ProductLineProductVo productLineVo = ProductLineProductBo.toPOJO(content);
		new ProductLineProductDB().updatePLProducts(productLineVo);
		return Response.status(200).entity("").build();
	}
}
