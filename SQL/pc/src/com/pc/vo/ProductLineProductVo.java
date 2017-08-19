package com.pc.vo;

import java.util.ArrayList;
import java.util.List;

public class ProductLineProductVo {
	private ProductLineVo productLineVo;
	private List<ProductVo> products = new ArrayList<>();
	private List<String[]> deletePLProductSQLs = new ArrayList<>();
	private List<String[]> createPLProductSQLs = new ArrayList<>();
	
	public void addProduct(ProductVo productVo) {
		this.products.add(productVo);
	}
	
	@Override
	public String toString() {
		return "ProductLineProductVo [productLineVo=" + productLineVo + ", products=" + products + 
				", delList=" + deletePLProductSQLs + ", createList=" + createPLProductSQLs + "]";
	}
	public List<String[]> getDeletePLProductSQLs() {
		return deletePLProductSQLs;
	}
	public void addDeleteStoreplSQL(String[] deleteStoreplSQL) {
		this.deletePLProductSQLs.add(deleteStoreplSQL);
	}
	public List<String[]> getCreatePLProductSQLs() {
		return createPLProductSQLs;
	}
	public void addCreateStoreplSQL(String[] createStoreplSQL) {
		this.createPLProductSQLs.add(createStoreplSQL);
	}

	public ProductLineVo getProductLineVo() {
		return productLineVo;
	}

	public void setProductLineVo(ProductLineVo productLineVo) {
		this.productLineVo = productLineVo;
	}

	public List<ProductVo> getProducts() {
		return products;
	}

	public void setProducts(List<ProductVo> products) {
		this.products = products;
	}

}
