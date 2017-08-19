package com.pc.bo;

import java.math.BigDecimal;

import java.util.ArrayList;
import java.util.List;

import java.sql.ResultSet;
import java.sql.SQLException;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Test;

import com.pc.vo.ProductLineProductVo;
import com.pc.vo.ProductLineVo;
import com.pc.vo.ProductVo;
import com.pc.vo.StoreProductLineVo;
import com.pc.vo.StoreVo;

public class ProductLineProductBo {
	@Test
	public void testToPojo() {
		String content = "{\"Id\":\"1\",\"ProductIds\":[\"2\"]}";
		System.out.println(StoreProductLineBo.toPOJO(content));
	}
	
	public static ProductLineProductVo toPOJO(String content) {
		ProductLineProductVo productLineProductVo = new ProductLineProductVo();
		System.out.println(content);
		JSONObject obj = new JSONObject(content);
		String id = obj.getString("Id");
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId(id);
		productLineProductVo.setProductLineVo(productLineVo);
		JSONArray productLinesjson = obj.getJSONArray("ProductIds");

		for (int plCount=0; plCount < productLinesjson.length(); plCount++) {
			ProductVo productVo = new ProductVo();
			productVo.setId(productLinesjson.getString(plCount));
			productLineProductVo.addProduct(productVo);
		}
		return productLineProductVo;
	}
	

	
	@Test
	public void testGeneratePLProductsUpdateSQL() 
			throws SQLException, Exception {
		String content = "[{\"Id\":\"oldTestPL2\"},{\"Id\":\"oldTestPL2\"}]";
		JSONArray from = new JSONArray("[{\"Id\":\"oldTestPL1\"},{\"Id\":\"oldTestPL2\"}]");
		System.out.println(from.toString());
		ProductLineProductVo to = new ProductLineProductVo();
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId("TestPL");
		productLineVo.setName("TestPLName");
		ProductVo productVo = new ProductVo();
		productVo.setId("newTestProduct1");
		productVo.setName("newTestProductName1");
		productVo.setPrice(new BigDecimal(0));
		ProductVo productVo2 = new ProductVo();
		productVo2.setId("newTestProduct2");
		productVo2.setName("newTestProductName2");
		productVo2.setPrice(new BigDecimal(1));
		to.setProductLineVo(productLineVo);
		to.addProduct(productVo);
		to.addProduct(productVo2);
		System.out.println(to.toString());
		ProductLineProductVo testResult = generatePLProductsUpdateSQL(from, to);
		int nTest = 0;
		for (String[] delTestStringArray : testResult.getDeletePLProductSQLs()) {
			if(delTestStringArray[1].equals("TestPL"))
				if(delTestStringArray[2].equals("oldTestPL1") || delTestStringArray[2].equals("oldTestPL2"))
					nTest += 1;
			/*System.out.print("Delete: ");
			for (String delTestString: delTestStringArray)
				System.out.print(", " + delTestString);
			System.out.println("");*/
		}
		assert nTest==2:"delete statement string failed";
		for (String[] crtTestStringArray : testResult.getCreatePLProductSQLs()) {
			if(crtTestStringArray[1].equals("TestPL"))
				if(crtTestStringArray[2].equals("newTestProduct1") || crtTestStringArray[2].equals("newTestProduct2"))
					nTest += 1;
			/*System.out.print("Create: ");
			for (String crtTestString: crtTestStringArray)
				System.out.print(", " + crtTestString);
			System.out.println("");*/
		}
		assert nTest==4:"create statement string failed";
		
	}

	public static ProductLineProductVo generatePLProductsUpdateSQL(JSONArray from, ProductLineProductVo to) 
			throws Exception {
		ProductLineProductVo productLineProductVo = new ProductLineProductVo();
		List<String> createPlList = new ArrayList<>();
		List<String> removePlList = new ArrayList<>();
		for (int plCount=0; plCount < from.length(); plCount++) {
			//from.getString(plCount)
			boolean removed = true;
			for (ProductVo productVo: to.getProducts()){
				if ((from.getJSONObject(plCount).getString("Id")).equals(productVo.getId())) {
					removed = false;
					break;
				}
			}
			if (removed) {
				removePlList.add(from.getJSONObject(plCount).getString("Id"));
			}
		}
		System.out.println("remove PLs: " + removePlList);
		if (removePlList.size() != 0) {
			for (int count = 0; count < removePlList.size(); count++) {
				String[] deletePLProdSQL = {
						"DELETE FROM `iuwork`.`productline_product` WHERE ProductLine_Id = ? and Product_Id = ?",
						to.getProductLineVo().getId(),
						removePlList.get(count) };
				/*deletePLProdSQL.append(to.getProductLineVo().getId());
				deletePLProdSQL.append("' and Product_Id = '");
				deletePLProdSQL.append(removePlList.get(count));
				deletePLProdSQL.append("';");*/
				//System.out.println(deletePLProdSQL.toString());
				//String delString = new String(deletePLProdSQL.toString());
				productLineProductVo.addDeleteStoreplSQL(deletePLProdSQL);
			}
		}
		
		//find new PLs
		for (ProductVo productVo : to.getProducts()) {
			boolean added = true;
			for (int plCount=0; plCount < from.length(); plCount++) {
				if ((from.getJSONObject(plCount).getString("Id")).equals(productVo.getId())) {
					added = false;
					break;
				}
			}
			if (added) {
				createPlList.add(productVo.getId());
			}			
		}
		System.out.println("create PLs: " + createPlList);
		if (createPlList.size() != 0) {
			for (int count = 0; count < createPlList.size(); count++) {
				String[] createPLProdSQL = {
						"INSERT INTO `iuwork`.`productline_product` (`ProductLine_Id`, `Product_Id`) VALUES (?, ?)",
						to.getProductLineVo().getId(),
						createPlList.get(count) };
				/*createPLProdSQL.append(to.getProductLineVo().getId());
				createPLProdSQL.append("', '");
				createPLProdSQL.append(createPlList.get(count));
				createPLProdSQL.append("');");*/
				//System.out.println(createPLProdSQL.toString());
				//String createString = new String(createPLProdSQL.toString());
				productLineProductVo.addCreateStoreplSQL(createPLProdSQL);
			}
		}
		
		return productLineProductVo;
	}
	
	public static JSONArray retrieveAllProducts(ResultSet resultSet) {

		JSONArray result = new JSONArray();
		try {
			while (resultSet.next()) {
				JSONObject productJson = new JSONObject();
				productJson.put("Id", resultSet.getString("Id"));
				productJson.put("Name", resultSet.getString("Name"));
				productJson.put("Price", resultSet.getBigDecimal("Price"));
				result.put(productJson);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return result;
	}
		
}
