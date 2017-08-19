package com.pc.db;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.PreparedStatement;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Test;

import com.pc.bo.ProductLineProductBo;
import com.pc.vo.ProductLineProductVo;
import com.pc.vo.ProductLineVo;
import com.pc.vo.ProductVo;

public class ProductLineProductDB  extends DBInit {
	//currently not used
	private String getProductLineStatement(String productLineID) {
		StringBuilder getStoreStmt = new StringBuilder();
		getStoreStmt.append("select distinct pl.Id, pl.Name");
		getStoreStmt.append(" from productline_product plp, productline pl, product prod ");
		getStoreStmt.append(" where plp.ProductLine_Id =  '");
		getStoreStmt.append(productLineID);
		getStoreStmt.append("'");
		getStoreStmt.append(" and plp.ProductLine_Id = pl.Id");
		getStoreStmt.append(" and plp.Product_Id = prod.Id;");
		System.out.println(getStoreStmt.toString());
		return getStoreStmt.toString();
	}

	@Test
	public void testGetProductLineStatement() throws Exception {
		ProductLineProductDB dbConnection = new ProductLineProductDB();
		dbConnection.getProductLineStatement("1");
	}

	/**
	 * 
	 * @throws SQLException, Exception
	 */
	private PreparedStatement getProductsStatement(String productLineID) throws SQLException, Exception {
		String s = new String( "select prod.Id, prod.Name, prod.Price" +
				" from productline_product plp, productline pl, product prod where plp.ProductLine_Id = ?" +
				" and plp.ProductLine_Id = pl.Id and plp.Product_Id = prod.Id");
		this.initDB();
		System.out.println(this.connect.toString());
		PreparedStatement getStoreStmt = this.connect.prepareStatement(s);
		getStoreStmt.setString(1, productLineID);
		/*try {
			getStoreStmt = this.connect.prepareStatement(s);
			getStoreStmt.setString(1, productLineID);
		} catch (SQLException e) {
			System.out.println("SQLException in " + s);
		}*/
		
		System.out.println(getStoreStmt.toString());
		return getStoreStmt;
	}

	@Test
	public void testGetProductLineStatment() throws Exception {
		ProductLineProductDB dbConnection = new ProductLineProductDB();
		dbConnection.getProductsStatement("1");
		connect.close();
	}	
	
	public JSONArray getAllProducts(ProductLineVo productLineVo) throws Exception {
		//this.initDB();
		//Statement statement = this.connect.createStatement();
		ResultSet resultSet = this.getProductsStatement(productLineVo.getId()).executeQuery();
		//ResultSet resultSet = statement.executeQuery(this.getProductsStatement(productLineVo.getId()));
		JSONArray allProducts = ProductLineProductBo.retrieveAllProducts(resultSet);
		connect.close();
		return allProducts;
	}

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testGetAllProductLines() throws Exception {
		ProductLineProductDB dbConnection = new ProductLineProductDB();
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId("1");
		System.out.println(dbConnection.getAllProducts(productLineVo));
	}

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testUpdatePLProducts() throws Exception {
		ProductLineProductVo productLineProductVo = new ProductLineProductVo();
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId("1");
		productLineProductVo.setProductLineVo(productLineVo);
		ProductVo productVo = new ProductVo();
		productVo.setId("1");
		productLineProductVo.addProduct(productVo);
		ProductVo productVo1 = new ProductVo();
		productVo1.setId("4");
		productLineProductVo.addProduct(productVo1);
		ProductLineProductDB dbConnection = new ProductLineProductDB();
		dbConnection.updatePLProducts(productLineProductVo);
	}

	/**
	 * 
	 * @param storeplVo
	 * @throws Exception
	 */
	public void updatePLProducts(ProductLineProductVo productLineProductVo) throws Exception {
		JSONArray allProducts = this.getAllProducts(productLineProductVo.getProductLineVo());
		//find out which product  have been unchanged and which ones are added
		this.initDB();
		ProductLineProductVo updatePLProdVo = ProductLineProductBo.generatePLProductsUpdateSQL(allProducts, productLineProductVo);
		System.out.println("sql stmts:" + updatePLProdVo);
		//Statement stmt = this.connect.createStatement();
		// Set auto-commit to false
		this.connect.setAutoCommit(false);	
		//add DMLS
		for (String[] delRequest: updatePLProdVo.getDeletePLProductSQLs()) {
			PreparedStatement sql = connect.prepareStatement(delRequest[0]);
			sql.setString(1, delRequest[1]);
			sql.setString(2, delRequest[2]);
			sql.executeUpdate();
		}
		for (String[] crtRequest : updatePLProdVo.getCreatePLProductSQLs()) {
			PreparedStatement sql = connect.prepareStatement(crtRequest[0]);
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
		System.out.println("Store Product updated in DB");
	}

	public static void main(String[] args) throws Exception{
		ProductLineProductVo productLineProductVo = new ProductLineProductVo();
		ProductLineVo productLineVo = new ProductLineVo();
		productLineVo.setId("1");
		productLineProductVo.setProductLineVo(productLineVo);
		ProductVo productVo = new ProductVo();
		productVo.setId("1");
		productLineProductVo.addProduct(productVo);
		ProductVo productVo1 = new ProductVo();
		productVo1.setId("2");
		productLineProductVo.addProduct(productVo1);
		ProductLineProductDB productLineProductDB = new ProductLineProductDB();
		productLineProductDB.updatePLProducts(productLineProductVo);
	}	
}
