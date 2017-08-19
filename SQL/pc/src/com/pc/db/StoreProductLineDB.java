package com.pc.db;

import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.PreparedStatement;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Test;

import com.pc.bo.StoreProductLineBo;
import com.pc.vo.ProductLineVo;
import com.pc.vo.StoreProductLineVo;
import com.pc.vo.StoreVo;

public class StoreProductLineDB extends DBInit {
	private String getStoreStatment(String storeId) {
		StringBuilder getStoreStmt = new StringBuilder();
		getStoreStmt.append("select distinct str.Id, str.Name, str.Address");
		getStoreStmt.append(" from store_productline spl, store str, productline pl");
		getStoreStmt.append(" where spl.Store_Id = '");
		getStoreStmt.append(storeId);
		getStoreStmt.append("'");
		getStoreStmt.append(" and str.Id = spl.Store_Id");
		getStoreStmt.append(" and pl.Id = spl.ProductLine_Id;");
		System.out.println(getStoreStmt.toString());
		return getStoreStmt.toString();
	}

	@Test
	public void testGetStoreStatment() throws Exception {
		StoreProductLineDB dbConnection = new StoreProductLineDB();
		dbConnection.getStoreStatment("6");
	}

	private String getProductLineStatment(String storeId) {
		StringBuilder getStoreStmt = new StringBuilder();
		getStoreStmt.append("select pl.Id, pl.Name");
		getStoreStmt.append(" from store_productline spl, store str, productline pl");
		getStoreStmt.append(" where spl.Store_Id = '");
		getStoreStmt.append(storeId);
		getStoreStmt.append("'");
		getStoreStmt.append(" and str.Id = spl.Store_Id");
		getStoreStmt.append(" and pl.Id = spl.ProductLine_Id;");
		System.out.println(getStoreStmt.toString());
		return getStoreStmt.toString();
	}

	@Test
	public void testGetProductLineStatment() throws Exception {
		StoreProductLineDB dbConnection = new StoreProductLineDB();
		dbConnection.getProductLineStatment("6");
	}

	public JSONArray getAllProductLines(StoreVo storeVo) throws Exception {
		this.initDB();
		Statement statement = this.connect.createStatement();
		ResultSet resultSet = statement.executeQuery(this.getProductLineStatment(storeVo.getId()));
		JSONArray allProductlines = StoreProductLineBo.retrieveAllProductlines(resultSet);
		connect.close();
		return allProductlines;
	}

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testGetAllProductLines() throws Exception {
		StoreProductLineDB dbConnection = new StoreProductLineDB();
		StoreVo storeVo = new StoreVo();
		storeVo.setId("6");
		System.out.println(dbConnection.getAllProductLines(storeVo));
	}

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testUpdateStoreProductLine() throws Exception {
		StoreProductLineVo storeProductLineVo = new StoreProductLineVo();
		StoreVo storeVo = new StoreVo();
		storeVo.setId("1");
		storeProductLineVo.setStoreVo(storeVo);
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId("1");
		//storeProductLineVo.addProductLine(productLineVo);
		ProductLineVo productLineVo1 = new ProductLineVo();
		productLineVo1.setId("2");
		storeProductLineVo.addProductLine(productLineVo1);
		StoreProductLineDB dbConnection = new StoreProductLineDB();
		dbConnection.updateStoreProductLine(storeProductLineVo);
	}

	/**
	 * 
	 * @param storeplVo
	 * @throws Exception
	 */
	public void updateStoreProductLine(StoreProductLineVo storeProductLineVo) throws Exception {
		System.out.println(storeProductLineVo);
		JSONArray allPls = this.getAllProductLines(storeProductLineVo.getStoreVo());
		//find out which product lines have been unchanged and which ones are added
		this.initDB();
		StoreProductLineVo updateStorePLSQL = StoreProductLineBo.generateStorePLUpdateSQL(allPls, storeProductLineVo);
		this.connect.setAutoCommit(false);
		//Statement stmt = this.connect.createStatement();
		// Set auto-commit to false
		this.connect.setAutoCommit(false);	
		//add DMLS
		for (String[] delRequest : updateStorePLSQL.getDeleteStoreplSQLs()) {
			PreparedStatement sql = this.connect.prepareStatement(delRequest[0]);
			sql.setString(1, delRequest[1]);
			sql.setString(2, delRequest[2]);
			sql.executeUpdate();
		}
		for (String[] crtRequest : updateStorePLSQL.getCreateStoreplSQLs()) {
			PreparedStatement sql = this.connect.prepareStatement(crtRequest[0]);
			sql.setString(1, crtRequest[1]);
			sql.setString(2, crtRequest[2]);
			sql.executeUpdate();
		}
		// Create an int[] to hold returned values
		//stmt.executeBatch();
//		System.out.println("updated " + count.toString() + " records.");

		//Explicitly commit statements to apply changes
		this.connect.commit();	
		connect.close();	
		System.out.println("Store Product Lines updated in DB");
	}
}
