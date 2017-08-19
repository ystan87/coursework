package com.pc.bo;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Test;

import com.pc.vo.ProductLineVo;
import com.pc.vo.StoreProductLineVo;
import com.pc.vo.StoreVo;

public class StoreProductLineBo {
	
	@Test
	public void testToPojo() {
		String content = "{\"Id\":\"1\",\"ProductLineIds\":[\"2\"]}";
		System.out.println(StoreProductLineBo.toPOJO(content));
	}
	
	public static StoreProductLineVo toPOJO(String content) {
		StoreProductLineVo storeProductLineVo = new StoreProductLineVo();
		System.out.println(content);
		JSONObject obj = new JSONObject(content);
		String id = obj.getString("Id");
		StoreVo storeVo = new StoreVo();
		storeVo.setId(id);
		storeProductLineVo.setStoreVo(storeVo);
		JSONArray productLinesjson = obj.getJSONArray("ProductLineIds");

		for (int plCount=0; plCount < productLinesjson.length(); plCount++) {
			ProductLineVo productLineVo = new ProductLineVo();
			productLineVo.setId(productLinesjson.getString(plCount));
			storeProductLineVo.addProductLine(productLineVo);
		}
		return storeProductLineVo;
	}
	
	@Test
	public void testGenerateStorePLUpdateSQL() 
			throws SQLException, Exception {
		String content = "[{\"Id\":\"oldTestPL2\"},{\"Id\":\"oldTestPL2\"}]";
		JSONArray from = new JSONArray("[{\"Id\":\"oldTestPL1\"},{\"Id\":\"oldTestPL2\"}]");
		System.out.println(from.toString());
		StoreProductLineVo to = new StoreProductLineVo();
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId("newTestPL1");
		productLineVo.setName("newTestPLName1");
		ProductLineVo productLineVo2 = new ProductLineVo();
		productLineVo2.setId("newTestPL2");
		productLineVo2.setName("newTestPLName2");
		StoreVo storeVo = new StoreVo();
		storeVo.setId("TestStore");
		storeVo.setName("TestStoreName");
		storeVo.setAddress("TestStoreAddress");
		to.setStoreVo(storeVo);
		to.addProductLine(productLineVo);
		to.addProductLine(productLineVo2);
		System.out.println(to.toString());
		StoreProductLineVo testResult = generateStorePLUpdateSQL(from, to);
		int nTest = 0;
		for (String[] delTestStringArray : testResult.getDeleteStoreplSQLs()) {
			if(delTestStringArray[1].equals("TestStore"))
				if(delTestStringArray[2].equals("oldTestPL1") || delTestStringArray[2].equals("oldTestPL2"))
					nTest += 1;
			/*System.out.print("Delete: ");
			for (String delTestString: delTestStringArray)
				System.out.print(", " + delTestString);
			System.out.println("");*/
		}
		assert nTest==2:"delete statement string failed";
		for (String[] crtTestStringArray : testResult.getCreateStoreplSQLs()) {
			if(crtTestStringArray[1].equals("TestStore"))
				if(crtTestStringArray[2].equals("newTestPL1") || crtTestStringArray[2].equals("newTestPL2"))
					nTest += 1;
			/*System.out.print("Create: ");
			for (String crtTestString: crtTestStringArray)
				System.out.print(", " + crtTestString);
			System.out.println("");*/
		}
		assert nTest==4:"create statement string failed";
		
	}
	
	public static StoreProductLineVo generateStorePLUpdateSQL(JSONArray from, StoreProductLineVo to) 
			throws SQLException, Exception{
		StoreProductLineVo storeProductLineVo = new StoreProductLineVo();
		List<String> createPlList = new ArrayList<>();
		List<String> removePlList = new ArrayList<>();
		for (int plCount=0; plCount < from.length(); plCount++) {
			//from.getString(plCount)
			boolean removed = true;
			for (ProductLineVo productLineVo: to.getProductLines()){
				if ((from.getJSONObject(plCount).getString("Id")).equals(productLineVo.getId())) {
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
				String[] deleteStoreplSQL = {
						"DELETE FROM `iuwork`.`store_productline` WHERE Store_Id = ? and ProductLine_Id = ?",
						to.getStoreVo().getId(),
						removePlList.get(count)};
				/*deleteStoreplSQL.append(to.getStoreVo().getId());
				deleteStoreplSQL.append("' and ProductLine_Id = '");
				deleteStoreplSQL.append(removePlList.get(count));
				deleteStoreplSQL.append("';");*/
				//System.out.println(deleteStoreplSQL.toString());
				//String delString = new String(deleteStoreplSQL.toString());
				storeProductLineVo.addDeleteStoreplSQL(deleteStoreplSQL);
			}
		}
		
		//find new PLs
		for (ProductLineVo productLineVo : to.getProductLines()) {
			boolean added = true;
			for (int plCount=0; plCount < from.length(); plCount++) {
				if ((from.getJSONObject(plCount).getString("Id")).equals(productLineVo.getId())) {
					added = false;
					break;
				}
			}
			if (added) {
				createPlList.add(productLineVo.getId());
			}			
		}
		System.out.println("create PLs: " + createPlList);
		if (createPlList.size() != 0) {
			for (int count = 0; count < createPlList.size(); count++) {
				String[] createStoreplSQL = {
						"INSERT INTO `iuwork`.`store_productline` (`Store_Id`, `ProductLine_Id`) VALUES (?, ?)",
						to.getStoreVo().getId(),
						createPlList.get(count) };
				/*createStoreplSQL.append(to.getStoreVo().getId());
				createStoreplSQL.append("', '");
				createStoreplSQL.append(createPlList.get(count));
				createStoreplSQL.append("');");*/
				//System.out.println(createStoreplSQL.toString());
				//String createString = new String(createStoreplSQL.toString());
				storeProductLineVo.addCreateStoreplSQL(createStoreplSQL);
			}
		}
		
		return storeProductLineVo;
	}
	
	public static JSONArray retrieveAllProductlines(ResultSet resultSet) {

		JSONArray result = new JSONArray();
		try {
			while (resultSet.next()) {
				JSONObject productJson = new JSONObject();
				productJson.put("Id", resultSet.getString("Id"));
				productJson.put("Name", resultSet.getString("Name"));
				result.put(productJson);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return result;
	}
	
	public static void main(String[] args) {
		String content = "{\"Id\":\"1\",\"ProductLineIds\":[\"2\"]}";
		System.out.println(StoreProductLineBo.toPOJO(content));		
	}
}
