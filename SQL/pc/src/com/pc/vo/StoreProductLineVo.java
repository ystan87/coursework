package com.pc.vo;

import java.util.ArrayList;
import java.util.List;

//import java.sql.PreparedStatement;

public class StoreProductLineVo {
	private StoreVo storeVo;
	private List<ProductLineVo> productLines = new ArrayList<>();
	private List<String[]> deleteStoreplSQLs = new ArrayList<>();
	private List<String[]> createStoreplSQLs = new ArrayList<>();
	
	public StoreVo getStoreVo() {
		return storeVo;
	}
	public void setStoreVo(StoreVo storeVo) {
		this.storeVo = storeVo;
	}
	public List<ProductLineVo> getProductLines() {
		return productLines;
	}
	public void setProductLines(List<ProductLineVo> productLines) {
		this.productLines = productLines;
	}
	public void addProductLine(ProductLineVo productLineVo) {
		this.productLines.add(productLineVo);
	}
	
	@Override
	public String toString() {
		return "StoreProductLineVo [storeVo=" + storeVo + ", productLines=" + productLines + 
				", delList=" + deleteStoreplSQLs + ", createList=" + createStoreplSQLs + "]";
	}
	public List<String[]> getDeleteStoreplSQLs() {
		return deleteStoreplSQLs;
	}
	public void addDeleteStoreplSQL(String[] deleteStoreplSQL) {
		this.deleteStoreplSQLs.add(deleteStoreplSQL);
	}
	public List<String[]> getCreateStoreplSQLs() {
		return createStoreplSQLs;
	}
	public void addCreateStoreplSQL(String[] createStoreplSQL) {
		this.createStoreplSQLs.add(createStoreplSQL);
	}

}
