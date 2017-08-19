package com.pc.db;

import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.PreparedStatement;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Test;

import com.pc.vo.StoreVo;
import com.pc.bo.StoreBo;

/**
 * The class has all supporting CURD operations for
 * the Store entity in the DB
 * @author Damodar Panigrahi and Yee Sern Tan
 *
 */
public class StoreDB extends DBInit{

	/**
	 * Returns a list of all the stores in the DB
	 * @return
	 * @throws Exception
	 */
	public JSONArray getAllStores() throws Exception {
		this.initDB();
		Statement statement = this.connect.createStatement();
		ResultSet resultSet = statement.executeQuery("select * from store;");
		JSONArray allStores = StoreBo.retrieveAllStores(resultSet);
		connect.close();
		return allStores;
	}
	
	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testGetAllStores() throws Exception {
		StoreDB dbConnection = new StoreDB();
		System.out.println(dbConnection.getAllStores());
	}
	
	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testInsertStore() throws Exception {
		StoreVo storeVo = new StoreVo();
		storeVo.setId(""+java.util.UUID.randomUUID());
		storeVo.setName("Digital Store");
		storeVo.setAddress("Newpark Mall, CA");
		StoreDB dbConnection = new StoreDB();
		dbConnection.insertStore(storeVo);
	}
	
	/**
	 * 
	 * @param storeVo
	 * @throws Exception
	 */
	public void insertStore(StoreVo storeVo) throws Exception {
		this.initDB();
		PreparedStatement storeInsertDML = this.connect.prepareStatement(
				"INSERT INTO `iuwork`.`store` (`Id`, `Name`, `Address`) "
				+ "VALUES (?, ?, ?)");
		storeInsertDML.setString(1, storeVo.getId());
		storeInsertDML.setString(2, storeVo.getName());
		storeInsertDML.setString(3, storeVo.getAddress());
		/*storeInsertDML.append(storeVo.getId());
		storeInsertDML.append("', '");
		storeInsertDML.append(storeVo.getName());
		storeInsertDML.append("', '");
		storeInsertDML.append(storeVo.getAddress());
		storeInsertDML.append("');");*/
		System.out.println(storeInsertDML.toString());
		storeInsertDML.executeUpdate();
		connect.close();
		//Statement statement = this.connect.createStatement();
		//statement.executeUpdate(storeInsertDML.toString());
		System.out.println("Store inserted into DB");
	}

	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testUpdateStore() throws Exception {
		StoreVo storeVo = new StoreVo();
		storeVo.setId("1");
		storeVo.setName("Digital Store");
		storeVo.setAddress("Newpark Mall, CA " + java.util.UUID.randomUUID());
		StoreDB dbConnection = new StoreDB();
		dbConnection.updateStore(storeVo);
	}	
	
	/**
	 * 
	 * @param storeVo
	 * @throws Exception
	 */
	public void updateStore(StoreVo storeVo) throws Exception {
		this.initDB();
		PreparedStatement storeUpdateDML = this.connect.prepareStatement(
				"UPDATE `iuwork`.`store` SET `Name` = ?, `Address` = ? WHERE `Id`= ?");
		storeUpdateDML.setString(1, storeVo.getName());
		storeUpdateDML.setString(2, storeVo.getAddress());
		storeUpdateDML.setString(3, storeVo.getId());
		/*storeUpdateDML.append(storeVo.getName());
		storeUpdateDML.append("', `Address` = '");
		storeUpdateDML.append(storeVo.getAddress());
		storeUpdateDML.append("' WHERE `Id`= '");
		storeUpdateDML.append(storeVo.getId());
		storeUpdateDML.append("';");*/
		System.out.println(storeUpdateDML.toString());
		storeUpdateDML.executeUpdate();
		connect.close();
		//Statement statement = this.connect.createStatement();
		//statement.executeUpdate(storeUpdateDML.toString());
		System.out.println("Store updated in DB");
	}	
	
	@Test
	/**
	 * 
	 * @throws Exception
	 */
	public void testDeleteStore() throws Exception {
		StoreVo storeVo = new StoreVo();
		storeVo.setId("3");
		StoreDB dbConnection = new StoreDB();
		dbConnection.deleteStore(storeVo);
	}	
	
	/**
	 * 
	 * @param storeVo
	 * @throws Exception
	 */
	public void deleteStore(StoreVo storeVo) throws Exception {
		this.initDB();
		PreparedStatement storeDeleteDML = this.connect.prepareStatement(
				"DELETE FROM `iuwork`.`store` WHERE `Id`= ?");
		storeDeleteDML.setString(1, storeVo.getId());
		/*storeDeleteDML.append(storeVo.getId());
		storeDeleteDML.append("';");*/
		System.out.println(storeDeleteDML.toString());
		try {
			storeDeleteDML.executeUpdate();
			//statement.executeUpdate(produceDeleteDML.toString());
		} catch (Throwable e) {
			System.out.println("Can't delete the store with id:" + storeVo.getId());
			throw new Exception("Can't delete the store with id:" + storeVo.getId());
		}
		connect.close();
		//Statement statement = this.connect.createStatement();
		//statement.executeUpdate(storeDeleteDML.toString());
		System.out.println("Store deleted in DB");
	}	
}
