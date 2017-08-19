-- MySQL dump 10.13  Distrib 5.6.35, for Win64 (x86_64)
--
-- Host: localhost    Database: iuwork
-- ------------------------------------------------------
-- Server version	5.6.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `Id` varchar(50) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Price` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('026c9c7a-4a08-4f6a-98c4-157b88fc17ba','Valdi Spoon',5.25),('1','Alibaba',5.50),('1fe3baa1-b295-470f-9645-ce5df1f522a1','Nike',4.50),('2','Amazon',6.50),('3','Walmart',5.00),('4','Walmart Clothes',5.00),('c1c9c94b-1365-4875-9b74-011297002752','Alibaba Shoe',4.50),('ffa41997-8214-41c0-a812-5590b246ed03','Walmart Show',4.00);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productline`
--

DROP TABLE IF EXISTS `productline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productline` (
  `Id` varchar(50) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productline`
--

LOCK TABLES `productline` WRITE;
/*!40000 ALTER TABLE `productline` DISABLE KEYS */;
INSERT INTO `productline` VALUES ('1','Shoes'),('1ff29327-ff88-4fe9-b37c-1c3de3516ced','Male Perfume'),('2','Watch'),('232cfb35-62b5-4036-80d9-e9c427cb78fb','Lights'),('23e1ba88-e209-46a4-9e45-55846db71452','Female Shoes'),('249d8d29-fe5e-4e54-8e1d-526d90520db3','Male Cloths'),('3','Spoon'),('3ed1724b-8550-4716-a978-a250dc22b519','Glass'),('4','Utencils'),('48041c46-4152-4de8-b6d7-e0faceb83ab1','Plates'),('4daebdb8-7972-4aff-99a9-45c8e4b5b0de','Male Watch'),('be993b38-ad15-43f4-a38f-af8800781b77','Men Shoes');
/*!40000 ALTER TABLE `productline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productline_product`
--

DROP TABLE IF EXISTS `productline_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productline_product` (
  `ProductLine_Id` varchar(50) NOT NULL,
  `Product_Id` varchar(50) NOT NULL,
  KEY `fk_ProductLine_Product_ProductLine1_idx` (`ProductLine_Id`),
  KEY `fk_ProductLine_Product_Product1_idx` (`Product_Id`),
  CONSTRAINT `fk_ProductLine_Product_Product1` FOREIGN KEY (`Product_Id`) REFERENCES `product` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_ProductLine_Product_ProductLine1` FOREIGN KEY (`ProductLine_Id`) REFERENCES `productline` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productline_product`
--

LOCK TABLES `productline_product` WRITE;
/*!40000 ALTER TABLE `productline_product` DISABLE KEYS */;
INSERT INTO `productline_product` VALUES ('1','1'),('1','4'),('1','1fe3baa1-b295-470f-9645-ce5df1f522a1');
/*!40000 ALTER TABLE `productline_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store` (
  `Id` varchar(50) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Address` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store`
--

LOCK TABLES `store` WRITE;
/*!40000 ALTER TABLE `store` DISABLE KEYS */;
INSERT INTO `store` VALUES ('1','Digital Store','Newpark Mall, CA'),('2','Retail Store','Main Road, OH'),('3','Cloth Store','Boston Globe, IL'),('322e8a62-fe8e-49bf-98d3-149bea114320','Bus Store','Fort, WI'),('4','Shoe Store','Boomberg, NY'),('5','Watch Store','Tampa, FL'),('6','Kitchen Store','Lot full, MI'),('6efd1015-aa15-4f02-b1fe-0eeefb2f6613','Perfume Store1','Las Vagas, NV'),('7','General Store','Someplace, ID'),('9ab7ca3f-5fc8-4eba-a168-50b6dee26c32','Jacket Store','Alabama, AL'),('c93ed219-ec7d-45cf-b9c0-8d1c6ce329f5','Watch Store','Seattle, WI'),('df522a9a-77b1-4b31-af8f-0b6a74435603','Food Store','Boston, MA');
/*!40000 ALTER TABLE `store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_productline`
--

DROP TABLE IF EXISTS `store_productline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_productline` (
  `Store_Id` varchar(50) NOT NULL,
  `ProductLine_Id` varchar(50) NOT NULL,
  KEY `fk_Store_ProductLine_Store_idx` (`Store_Id`),
  KEY `fk_Store_ProductLine_ProductLine1_idx` (`ProductLine_Id`),
  CONSTRAINT `fk_Store_ProductLine_ProductLine1` FOREIGN KEY (`ProductLine_Id`) REFERENCES `productline` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Store_ProductLine_Store` FOREIGN KEY (`Store_Id`) REFERENCES `store` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_productline`
--

LOCK TABLES `store_productline` WRITE;
/*!40000 ALTER TABLE `store_productline` DISABLE KEYS */;
INSERT INTO `store_productline` VALUES ('6','3'),('6','4'),('1','2'),('2','1ff29327-ff88-4fe9-b37c-1c3de3516ced'),('3','249d8d29-fe5e-4e54-8e1d-526d90520db3'),('6','3ed1724b-8550-4716-a978-a250dc22b519'),('6efd1015-aa15-4f02-b1fe-0eeefb2f6613','1ff29327-ff88-4fe9-b37c-1c3de3516ced'),('4','1'),('2','232cfb35-62b5-4036-80d9-e9c427cb78fb'),('2','23e1ba88-e209-46a4-9e45-55846db71452'),('1','23e1ba88-e209-46a4-9e45-55846db71452');
/*!40000 ALTER TABLE `store_productline` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-08  0:11:47
