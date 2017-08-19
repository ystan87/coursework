package com.pc.vo;

import java.math.BigDecimal;

public class ProductVo {
	private String id;
	private String name;
	private BigDecimal price;
	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public BigDecimal getPrice() {
		return price;
	}
	public void setPrice(BigDecimal price) {
		this.price = price;
	}
	@Override
	public String toString() {
		return "ProductVo [id=" + id + ", name=" + name + ", price=" + price + "]";
	}
}
