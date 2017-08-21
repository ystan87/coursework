Final Project for course: SQL and NoSQL

A working prototypical MySQL web-project is developed for product line management. MySQL connects to the Tomcat server via JDBC. Server backend code is developed with Java, making RestFUL calls to the browser front-end, aided by Rest Jersey API. The server can be discovered via JNDI. The front-end code is written in HTML5, Javascript and CSS. The plugin jQuery is used with Javascript.

Server configuration is found under folder apache-tomcat-8.5.16 . Jar files will need to be copied into the lib folder for server. The jar dependencies can be obtained using Maven, as configured in file pom.xml.

Browsers tested include Chrome and Firefox. The webpage provides an interface for CRUD operations on the database.

The DDL of this RDBMS is generated with MySQLWorkbench. (The MWB file is the project in MySQLWorkbench.) The entities are store, product, and product line, where many-to-many relationships exist between the first and third, and the second and third. Bridge tables are formed to convert each many-to-many relationship into two one-to-many relationship.

Ajax converts CRUD requests to the Java code, this interface calls the business layer, and calls to the database is done with the data access layer. Unit testing is done with JUnit.

To replicate this project, the folder pc can be imported into an Eclipse project under Java EE Dynamic Web Project. The project is built with Maven, and the resultant war file can be deployed.
