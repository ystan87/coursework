package com.pc.db;

import java.math.BigDecimal;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.PreparedStatement;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Test;

import com.pc.vo.ProductVo;

import com.pc.bo.ProductLineProductBo;

public class ProductDB extends DBInit {
	/**
	 * Returns a list of all the ProductLines in the DB
	 * 
	 * @return
	 * @throws Exception
	 */
	public JSONArray getAllProducts() throws Exception {
		this.initDB();
		Statement statement = this.connect.createStatement();
		ResultSet resultSet = statement.executeQuery("select * from product;");
		JSONArray allProducts = ProductLineProductBo.retrieveAllProducts(resultSet);
		connect.close();
		return allProducts;
	}

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testGetAllProducts() throws Exception {
		ProductDB dbConnection = new ProductDB();
		System.out.println(dbConnection.getAllProducts());
	}

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testInsertProduct() throws Exception {
		ProductVo productVo = new ProductVo();
		productVo.setId("" + java.util.UUID.randomUUID());
		productVo.setName("Nike");
		productVo.setPrice(new BigDecimal("4.50"));
		ProductDB dbConnection = new ProductDB();
		dbConnection.insertProduct(productVo);
	}

	/**
	 * 
	 * @param storeVo
	 * @throws Exception
	 */
	public void insertProduct(ProductVo productVo) throws Exception {
		this.initDB();
		PreparedStatement productInsertDML = this.connect.prepareStatement(
				"INSERT INTO `iuwork`.`product` (`Id`, `Name`, `Price`) VALUES (?, ?, ?)");
		productInsertDML.setString(1, productVo.getId());
		productInsertDML.setString(2, productVo.getName());
		productInsertDML.setBigDecimal(3, productVo.getPrice());
		/*productInsertDML.append(storeVo.getId());
		productInsertDML.append("', '");
		productInsertDML.append(storeVo.getName());
		productInsertDML.append("', ");
		productInsertDML.append(storeVo.getPrice());
		productInsertDML.append(");");
		*/
		System.out.println(productInsertDML.toString());
		productInsertDML.executeUpdate();
		connect.close();
		//Statement statement = this.connect.createStatement();
		//statement.executeUpdate(productInsertDML.toString());
		System.out.println("Product inserted into DB");
	}

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testUpdateProduct() throws Exception {
		ProductVo productVo = new ProductVo();
		productVo.setId("1");
		productVo.setName("Alibaba " + java.util.UUID.randomUUID());
		productVo.setPrice(new BigDecimal("6.25"));
		ProductDB dbConnection = new ProductDB();
		dbConnection.updateProduct(productVo);
	}

	/**
	 * 
	 * @param productVo
	 * @throws Exception
	 */
	public void updateProduct(ProductVo productVo) throws Exception {
		this.initDB();
		PreparedStatement productUpdateDML = this.connect.prepareStatement(
				"UPDATE `iuwork`.`product` SET `Name` = ?, `Price` = ? WHERE `Id`= ?");
		productUpdateDML.setString(1, productVo.getName());
		productUpdateDML.setBigDecimal(2, productVo.getPrice());
		productUpdateDML.setString(3, productVo.getId());
		System.out.println(productUpdateDML.toString());
		productUpdateDML.executeUpdate();
		connect.close();
		/*productUpdateDML.append(productVo.getName());
		productUpdateDML.append("'");
		productUpdateDML.append(productVo.getPrice());
		productUpdateDML.append("'");
		productUpdateDML.append(productVo.getId());
		productUpdateDML.append("';");
		System.out.println(productUpdateDML.toString());
		Statement statement = this.connect.createStatement();
		statement.executeUpdate(productUpdateDML.toString());*/
		System.out.println("Product updated in DB");
	}

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testDeleteProduct() throws Exception {
		ProductVo productVo = new ProductVo();
		productVo.setId("4");
		ProductDB dbConnection = new ProductDB();
		dbConnection.deleteProduct(productVo);
	}

	/**
	 * 
	 * @param productVo
	 * @throws Exception
	 */
	public void deleteProduct(ProductVo productVo) throws Exception {
		this.initDB();
		PreparedStatement produceDeleteDML = this.connect.prepareStatement("DELETE FROM `iuwork`.`product` WHERE `Id`=?");
		produceDeleteDML.setString(1, productVo.getId());
		/*produceDeleteDML.append(productVo.getId());
		produceDeleteDML.append("';");*/
		System.out.println(produceDeleteDML.toString());
		//Statement statement = this.connect.createStatement();
		try {
			produceDeleteDML.executeUpdate();
			//statement.executeUpdate(produceDeleteDML.toString());
		} catch (Throwable e) {
			System.out.println("Can't delete the produt with id:" + productVo.getId());
			throw new Exception("Can't delete the produt with id:" + productVo.getId());
		}
		connect.close();
		System.out.println("Product deleted in DB");
	}
}
