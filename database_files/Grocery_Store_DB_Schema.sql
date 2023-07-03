CREATE DATABASE  IF NOT EXISTS `grocery_store` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `grocery_store`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: grocery_store
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Fruits'),(2,'Vegetables'),(3,'Dairy'),(4,'Meat'),(5,'Bakery'),(6,'Beverages'),(7,'Snacks'),(8,'Personal Care'),(9,'Rice');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_details`
--

DROP TABLE IF EXISTS `order_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_details` (
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` double NOT NULL,
  `total_price` double NOT NULL,
  PRIMARY KEY (`order_id`,`product_id`),
  KEY `fk_product_id_idx` (`product_id`),
  CONSTRAINT `fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON UPDATE RESTRICT,
  CONSTRAINT `fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_details`
--

LOCK TABLES `order_details` WRITE;
/*!40000 ALTER TABLE `order_details` DISABLE KEYS */;
INSERT INTO `order_details` VALUES (1,1,2,60),(2,3,3,1.5),(2,5,2,2.3),(2,7,1,5.99),(3,6,1,2.29),(3,7,1,5.99),(3,15,2,2.98),(3,17,1,1.5),(4,6,1,2.29),(4,7,1,5.99),(5,7,1,5.99),(5,15,2,2.98),(5,17,1,1.5),(5,23,4,5.16),(6,3,3,1.5),(6,4,8,1.6),(7,3,3,1.5),(7,4,3,0.6),(7,6,1,2.29),(7,7,1,5.99),(8,1,1,30),(8,3,2,1),(8,6,1,2.29),(8,7,1,5.99),(9,14,3,4.2),(9,16,2,2.78),(9,17,1,1.5),(10,15,3,4.47),(10,20,3,10.5);
/*!40000 ALTER TABLE `order_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) NOT NULL,
  `total_amount` double NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'Vidhi',60,'2023-06-15 00:00:00'),(2,'Anuhya',9.79,'2023-06-15 10:00:00'),(3,'Naga Sai',12.76,'2023-06-15 10:00:00'),(4,'Mousami',8.28,'2023-05-26 08:30:00'),(5,'Fallon',15.63,'2023-06-14 14:26:00'),(6,'Jenny',3.1,'2023-05-20 15:36:00'),(7,'Carol',10.38,'2023-05-24 20:01:00'),(8,'Blake',39.28,'2023-05-26 19:22:00'),(9,'Hope',8.48,'2023-06-14 14:26:00'),(10,'Hayley',14.97,'2023-06-21 16:29:00');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `unit_of_measure_id` int NOT NULL,
  `price_per_unit` double NOT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`product_id`),
  KEY `fk_unit_of_measure_id_idx` (`unit_of_measure_id`),
  CONSTRAINT `fk_unit_of_measure_id` FOREIGN KEY (`unit_of_measure_id`) REFERENCES `unit_of_measures` (`unit_of_measure_id`) ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Toothpaste',1,30,8),(2,'Rice',2,50,9),(3,'Apple',1,0.5,1),(4,'Banana',1,0.2,1),(5,'Honey Mango',1,1.15,1),(6,'Golden Pineapple',1,2.29,1),(7,'Watermelon',1,5.99,1),(8,'Raspberry',1,0.2,1),(9,'Dragon Fruit',1,5.99,1),(10,'Avocado',1,0.99,1),(11,'Carrot',2,0.3,2),(12,'Cucumber',1,0.79,2),(13,'Sweet Potato',2,1.09,2),(14,'Roma Tomatoes',2,1.4,2),(15,'Sweet Onions',2,1.49,2),(16,'Red Onions',2,1.39,2),(17,'Milk',4,1.5,3),(18,'Lactose Free Milk',5,5.69,3),(19,'Low Fat Milk',5,2.77,3),(20,'Chicken Breast',2,3.5,4),(21,'Chicken Drumsticks',2,0.99,4),(22,'Chicken Bone-in Chicken Wings',2,3.49,4),(23,'Bone-In Chicken Thighs',2,1.29,4),(24,'Bread',1,1.2,5),(25,'Orange Juice',5,6.5,6),(26,'Water',4,0.5,6),(27,'Long Grain Enriched Rice',2,1.5,9),(28,'Organic Long Grain Enriched Rice',2,21.5,9),(29,'Short Grain Sushi Rice',2,2.79,9),(30,'Brown Rice',2,2.99,9);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unit_of_measures`
--

DROP TABLE IF EXISTS `unit_of_measures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unit_of_measures` (
  `unit_of_measure_id` int NOT NULL AUTO_INCREMENT,
  `unit_of_measure_name` varchar(45) NOT NULL,
  PRIMARY KEY (`unit_of_measure_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unit_of_measures`
--

LOCK TABLES `unit_of_measures` WRITE;
/*!40000 ALTER TABLE `unit_of_measures` DISABLE KEYS */;
INSERT INTO `unit_of_measures` VALUES (1,'Each'),(2,'Pound'),(3,'kilogram'),(4,'Liter'),(5,'Gallon'),(6,'Ounce');
/*!40000 ALTER TABLE `unit_of_measures` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-22 10:08:10