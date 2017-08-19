package com.pc.bo;

import org.json.JSONArray;
import org.json.JSONObject;

import java.sql.ResultSet;
import java.sql.SQLException;

public class StoreBo {
	
	public static JSONArray retrieveAllStores(ResultSet resultSet) {

		JSONArray result = new JSONArray();
		try {
			while (resultSet.next()) {
				JSONObject storeVo = new JSONObject();
				storeVo.put("Id", resultSet.getString("Id"));
				storeVo.put("Name", resultSet.getString("Name"));
				storeVo.put("Address", resultSet.getString("Address"));
				result.put(storeVo);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return result;
	}

}
