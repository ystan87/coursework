package com.pc.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.SQLException;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.sql.DataSource;

import org.junit.Test;

public class DBInit {
	protected Connection connect = null;

	protected DataSource ds;

	protected void initDBStandalone() throws Exception {
		if (this.connect != null) {
			return;
		}
		// This will load the MySQL driver, each DB has its own driver
		Class.forName("com.mysql.jdbc.Driver");
		// Setup the connection with the DB
		connect = DriverManager.getConnection("jdbc:mysql://localhost/iuwork?" + "user=username&password=password&serverTimezone=UTC");
	}

	protected void initDBWebContext() throws SQLException {
		try {
			Context ctx = new InitialContext();
			ds = (DataSource) ctx.lookup("java:comp/env/jdbc/iuwork");
			connect = ds.getConnection();
		} catch (NamingException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
			throw e;
		}
	}
	
	protected void initDB() throws Exception {
		this.initDBWebContext();
	}

	@Test
	/**
	 * Test initDBStandalone() method
	 * @throws Exception
	 */
	public void testInitDB() throws Exception{
		this.initDBStandalone();
	}
	
}
