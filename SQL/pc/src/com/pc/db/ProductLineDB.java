package com.pc.db;

import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.PreparedStatement;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Test;

import com.pc.bo.StoreProductLineBo;
import com.pc.vo.ProductLineVo;

public class ProductLineDB  extends DBInit {
	/**
	 * Returns a list of all the ProductLines in the DB
	 * @return
	 * @throws Exception
	 */
	public JSONArray getAllProductLines() throws Exception {
		this.initDB();
		Statement statement = this.connect.createStatement();
		ResultSet resultSet = statement.executeQuery("select * from productline;");
		JSONArray allProductLines = StoreProductLineBo.retrieveAllProductlines(resultSet);
		connect.close();
		return allProductLines;
	}
	
	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testGetAllProductLines() throws Exception {
		ProductLineDB dbConnection = new ProductLineDB();
		System.out.println(dbConnection.getAllProductLines());
	}
	
	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testInsertProductLine() throws Exception {
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId(""+java.util.UUID.randomUUID());
		productLineVo.setName("Soup");
		ProductLineDB dbConnection = new ProductLineDB();
		dbConnection.insertProductLine(productLineVo);
	}
	
	/**
	 * 
	 * @param productLineVo
	 * @throws Exception
	 */
	public void insertProductLine(ProductLineVo productLineVo) throws Exception {
		this.initDB();
		PreparedStatement productLineInsertDML = this.connect.prepareStatement(
				"INSERT INTO `iuwork`.`productline` (`Id`, `Name`) VALUES (?, ?)");
		productLineInsertDML.setString(1, productLineVo.getId());
		productLineInsertDML.setString(2, productLineVo.getName());
		/*productLineInsertDML.append(productLineVo.getId());
		productLineInsertDML.append("', '");
		productLineInsertDML.append(productLineVo.getName());
		productLineInsertDML.append("');");*/
		System.out.println(productLineInsertDML.toString());
		productLineInsertDML.executeUpdate();
		connect.close();
		//Statement statement = this.connect.createStatement();
		//statement.executeUpdate(productLineInsertDML.toString());
		System.out.println("ProductLine inserted into DB");
	}	

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testUpdateProductLine() throws Exception {
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId("1");
		productLineVo.setName("Shoes  " + java.util.UUID.randomUUID());
		ProductLineDB dbConnection = new ProductLineDB();
		dbConnection.updateProductLine(productLineVo);
	}	
	
	/**
	 * 
	 * @param productLineVo
	 * @throws Exception
	 */
	public void updateProductLine(ProductLineVo productLineVo) throws Exception {
		this.initDB();
		PreparedStatement productLineUpdateDML = this.connect.prepareStatement(
				"UPDATE `iuwork`.`productline` SET `Name` = ? WHERE `Id`= ?");
		productLineUpdateDML.setString(1, productLineVo.getName());
		productLineUpdateDML.setString(2, productLineVo.getId());
		/*productLineUpdateDML.append(productLineVo.getName());
		productLineUpdateDML.append("' WHERE `Id`= '");
		productLineUpdateDML.append(productLineVo.getId());
		productLineUpdateDML.append("';");*/
		System.out.println(productLineUpdateDML.toString());
		productLineUpdateDML.executeUpdate();
		connect.close();
		/*Statement statement = this.connect.createStatement();
		statement.executeUpdate(productLineUpdateDML.toString());*/
		System.out.println("ProductLine updated in DB");
	}	

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testDeleteProductLine() throws Exception {
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId("3");
		ProductLineDB dbConnection = new ProductLineDB();
		try{
			dbConnection.deleteProductLine(productLineVo);
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}	
	
	/**
	 * 
	 * @param productLineVo
	 * @throws Exception
	 */
	public void deleteProductLine(ProductLineVo productLineVo) throws Exception {
		this.initDB();
		PreparedStatement productLineDeleteDML = this.connect.prepareStatement(
				"DELETE FROM `iuwork`.`productline` WHERE `Id`=?");
		productLineDeleteDML.setString(1, productLineVo.getId());
		/*productLineDeleteDML.append(productLineVo.getId());
		productLineDeleteDML.append("';");*/
		System.out.println(productLineDeleteDML.toString());
		//Statement statement = this.connect.createStatement();
		try {
			productLineDeleteDML.executeUpdate();
			//statement.executeUpdate(productLineDeleteDML.toString());
		} catch (Throwable e) {
			System.out.println("Can't delete the produtline with id:" + productLineVo.getId());
			throw new Exception("Can't delete the produtline with id:" + productLineVo.getId());
		}
		connect.close();
		System.out.println("Product Line deleted in DB");
	}	
}
