CREATE DATABASE  IF NOT EXISTS `sdnet` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sdnet`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sdnet
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `customer_addresses`
--

DROP TABLE IF EXISTS `customer_addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `city` varchar(50) DEFAULT NULL,
  `village` varchar(50) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `building` varchar(50) DEFAULT NULL,
  `floor` varchar(10) DEFAULT NULL,
  `type` enum('home','work','other') DEFAULT 'home',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_addresses`
--

LOCK TABLES `customer_addresses` WRITE;
/*!40000 ALTER TABLE `customer_addresses` DISABLE KEYS */;
INSERT INTO `customer_addresses` VALUES (1,'2013','برجا-قشفا',NULL,'قشفا بناية ابو حمزة',NULL,NULL,'home','2025-11-26 18:01:34'),(2,'2014',NULL,NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(3,'2015',NULL,NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(4,'2016',NULL,NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(5,'2017',NULL,NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(6,'2018','برجا-فتيحات1',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(7,'2019','برجا-فتيحات1',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(8,'2020',NULL,NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(9,'hm1000','برجا-معبور','شارع العام',NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(10,'hm1001','برجا-فتيحات1',NULL,'ناية محمد منصور اخر ط يمين',NULL,NULL,'home','2025-11-26 18:01:34'),(11,'hm1003','برجا-مرج برجا',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(12,'hm1007','برجا-تلة ابو عارف',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(13,'hm1008','منشية',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(14,'hm1009','برجا-معبور','شارع العام','يناية عبد الكريم حمدو بلوك تاني ط 2 بالوج',NULL,NULL,'home','2025-11-26 18:01:34'),(15,'hm1011','برجا-قشفا',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(16,'hm1012','برجا-روس',NULL,'برجا-مرج برجا----',NULL,NULL,'home','2025-11-26 18:01:34'),(17,'hm1014','سعديات',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(18,'hm1015','برجا-فتيحات1',NULL,'فوق ام رمزي ط 2 يمين',NULL,NULL,'home','2025-11-26 18:01:34'),(19,'hm1016','برجا-مرج برجا',NULL,'بناية هاشم ط3 يمين',NULL,NULL,'home','2025-11-26 18:01:34'),(20,'hm1017','برجا-فتيحات1',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(21,'hm1018','برجا-عريض',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(22,'hm1019','برجا-بطنة',NULL,'فوق محل الصاج مدخل الثاني اخر ط شمال',NULL,NULL,'home','2025-11-26 18:01:34'),(23,'hm1020','منشية',NULL,'منشية حي العرب فوق قسامر كانجو',NULL,NULL,'home','2025-11-26 18:01:34'),(24,'hm1021','برجا-معبور','شارع العام',NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(25,'hm1022','بعاصير',NULL,'ناية محمد عبدالله ط اةل شمال',NULL,NULL,'home','2025-11-26 18:01:34'),(26,'hm1023','برجا-كروم',NULL,'فوق عاطف سليم ط3 يمين',NULL,NULL,'home','2025-11-26 18:01:34'),(27,'hm1025','برجا-فتيحات2',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(28,'hm1026','برجا-فتيحات1',NULL,'بناية الارامل ط ارضي شمال',NULL,NULL,'home','2025-11-26 18:01:34'),(29,'hm1027','برجا-كروم',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(30,'hm1028','برجا-فتيحات1',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(31,'hm1031','منشية',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34'),(32,'hm1032','منشية',NULL,'ضيعة حي السراي بيت الزعرت ارضي',NULL,NULL,'home','2025-11-26 18:01:34'),(33,'hm1033','برجا-حقرون',NULL,'ن قبل مفرق العمدة يمين اخر ط شمال',NULL,NULL,'home','2025-11-26 18:01:34'),(34,'hm1034','برجا-فتيحات1',NULL,NULL,NULL,NULL,'home','2025-11-26 18:01:34');
/*!40000 ALTER TABLE `customer_addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_subscriptions`
--

DROP TABLE IF EXISTS `customer_subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_subscriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_username` varchar(100) NOT NULL,
  `service_code` varchar(50) NOT NULL,
  `amount` decimal(10,2) NOT NULL DEFAULT '0.00',
  `billing_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `emp_manager` varchar(45) DEFAULT NULL,
  `subscription_status` tinyint DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_subscriptions`
--

LOCK TABLES `customer_subscriptions` WRITE;
/*!40000 ALTER TABLE `customer_subscriptions` DISABLE KEYS */;
INSERT INTO `customer_subscriptions` VALUES (1,'2013','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(2,'2014','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(3,'2015','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(4,'2016','000001',50.00,'2025-11-26 00:00:00','dak',1,'2025-11-26 18:01:34','2025-11-26 18:02:28'),(5,'2017','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(6,'2018','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(7,'2019','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(8,'2020','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(9,'hm1000','000002',27.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(10,'hm1001','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(11,'hm1003','000002',27.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(12,'hm1007','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(13,'hm1008','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(14,'hm1009','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(15,'hm1011','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(16,'hm1012','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(17,'hm1014','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(18,'hm1015','000002',27.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(19,'hm1016','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(20,'hm1017','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(21,'hm1018','000004',32.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(22,'hm1019','000005',25.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(23,'hm1020','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(24,'hm1021','000006',35.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(25,'hm1022','000001',0.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(26,'hm1023','000002',27.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(27,'hm1025','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(28,'hm1026','000004',32.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(29,'hm1027','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(30,'hm1028','000006',35.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(31,'hm1031','000007',40.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(32,'hm1032','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(33,'hm1033','000002',27.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34'),(34,'hm1034','000003',30.00,'2025-11-26 18:01:34','import_excel',NULL,'2025-11-26 18:01:34','2025-11-26 18:01:34');
/*!40000 ALTER TABLE `customer_subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `username` varchar(50) NOT NULL,
  `customer_status` tinyint DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`,`updated_at`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'وسلم اهل','','2013',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(2,'محل','','2014',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(3,'راوتر مكتب الشباب','','2015',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(4,'2016','','2016',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(5,'وسام بيت 2','','2017',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(6,'لابتوب محل','','2018',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(7,'دكانة الحاح','','2019',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(8,'لابتوب','','2020',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(9,'وسام حوحو','','hm1000',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(10,'مصطفى اصلان','','hm1001',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(11,'معمل بلاستك','','hm1003',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(12,'جاد الجعيد','','hm1007',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(13,'حسين حمزة','','hm1008',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(14,'عمران هناية','','hm1009',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(15,'ناصر رمضان','','hm1011',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(16,'خضر لمع','','hm1012',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(17,'بيت العم عيتاني','','hm1014',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(18,'محمود الاحمد','','hm1015',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(19,'غوش بيز','','hm1016',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(20,'احمد ليا','','hm1017',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(21,'كمال دمج','','hm1018',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(22,'سليمان بشاشة','','hm1019',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(23,'نسرين العرب','','hm1020',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(24,'la cite','','hm1021',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(25,'حسين لابتوب','','hm1022',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(26,'علي ديب (كروم)','','hm1023',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(27,'علي خلوف','','hm1025',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(28,'احمد العيكل','','hm1026',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(29,'محمد ناصر كروم','','hm1027',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(30,'عفيف حرب','','hm1028',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(31,'خليفة منشية','','hm1031',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(32,'حسن عيتاني','','hm1032',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(33,'سمر ادلبي (حقرون)','','hm1033',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34'),(34,'ابو عامر (جار حاييك)','','hm1034',NULL,'123456','2025-11-26 18:01:34','2025-11-26 18:01:34');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emp_cust_relation`
--

DROP TABLE IF EXISTS `emp_cust_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emp_cust_relation` (
  `idemp_cust_relation` int NOT NULL AUTO_INCREMENT,
  `emp_username` varchar(45) DEFAULT NULL,
  `cust_username` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idemp_cust_relation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emp_cust_relation`
--

LOCK TABLES `emp_cust_relation` WRITE;
/*!40000 ALTER TABLE `emp_cust_relation` DISABLE KEYS */;
/*!40000 ALTER TABLE `emp_cust_relation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_salary`
--

DROP TABLE IF EXISTS `employee_salary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_salary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_username` varchar(100) NOT NULL,
  `salary_month` date NOT NULL,
  `base_salary` decimal(12,2) DEFAULT NULL,
  `payment` decimal(12,2) DEFAULT NULL,
  `bonus` decimal(12,2) DEFAULT NULL,
  `deductions` decimal(12,2) DEFAULT NULL,
  `net_salary` decimal(12,2) NOT NULL,
  `currency` enum('USD','LBP') NOT NULL DEFAULT 'LBP',
  `payment_method` enum('cash','card','bank','other') NOT NULL DEFAULT 'cash',
  `notes` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_salary_month` (`salary_month`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_salary`
--

LOCK TABLES `employee_salary` WRITE;
/*!40000 ALTER TABLE `employee_salary` DISABLE KEYS */;
/*!40000 ALTER TABLE `employee_salary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `city` varchar(50) DEFAULT NULL,
  `village` varchar(50) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `building` varchar(50) DEFAULT NULL,
  `floor` varchar(10) DEFAULT NULL,
  `type` enum('home','work','other') NOT NULL DEFAULT 'home',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_employees_mobile` (`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'mohamed el dakdouki','71771420','dak','71771420','barja','kroum',NULL,NULL,NULL,'home','2025-11-26 18:02:14','2025-11-26 18:02:14');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expense_categories`
--

DROP TABLE IF EXISTS `expense_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expense_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expense_categories`
--

LOCK TABLES `expense_categories` WRITE;
/*!40000 ALTER TABLE `expense_categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `expense_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `expense_date` date NOT NULL,
  `category` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `amount` decimal(12,2) NOT NULL,
  `payment_method` enum('cash','card','bank','other') NOT NULL DEFAULT 'cash',
  `supplier_name` varchar(100) DEFAULT NULL,
  `employee_name` varchar(100) DEFAULT NULL,
  `receipt_number` varchar(50) DEFAULT NULL,
  `notes` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_expense_date` (`expense_date`),
  KEY `idx_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `idservice` int NOT NULL AUTO_INCREMENT,
  `service_code` varchar(50) NOT NULL,
  `service_name` varchar(100) NOT NULL,
  `service_price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `service_currency` varchar(3) NOT NULL,
  `service_status` varchar(10) NOT NULL DEFAULT 'active',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idservice`),
  UNIQUE KEY `service_code` (`service_code`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'000001','000001',0.00,'USD','1','2025-11-26 18:01:34','2025-11-26 18:01:34'),(2,'000002','000002',27.00,'USD','1','2025-11-26 18:01:34','2025-11-26 18:01:34'),(3,'000003','000003',30.00,'USD','1','2025-11-26 18:01:34','2025-11-26 18:01:34'),(4,'000004','000004',32.00,'USD','1','2025-11-26 18:01:34','2025-11-26 18:01:34'),(5,'000005','000005',25.00,'USD','1','2025-11-26 18:01:34','2025-11-26 18:01:34'),(6,'000006','000006',35.00,'USD','1','2025-11-26 18:01:34','2025-11-26 18:01:34'),(7,'000007','000007',40.00,'USD','1','2025-11-26 18:01:34','2025-11-26 18:01:34');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier_addresses`
--

DROP TABLE IF EXISTS `supplier_addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier_addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `supplier_code` varchar(50) NOT NULL,
  `city` varchar(50) DEFAULT NULL,
  `village` varchar(50) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `building` varchar(50) DEFAULT NULL,
  `floor` varchar(10) DEFAULT NULL,
  `type` enum('office','warehouse','other') NOT NULL DEFAULT 'office',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_supplier_addresses_code` (`supplier_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier_addresses`
--

LOCK TABLES `supplier_addresses` WRITE;
/*!40000 ALTER TABLE `supplier_addresses` DISABLE KEYS */;
/*!40000 ALTER TABLE `supplier_addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `supplier_name` varchar(150) NOT NULL,
  `contact_person` varchar(100) DEFAULT NULL,
  `mobile` varchar(20) NOT NULL,
  `supplier_code` varchar(50) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_suppliers_code` (`supplier_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_detail`
--

DROP TABLE IF EXISTS `transaction_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_number` varchar(50) NOT NULL,
  `payment_date` date NOT NULL,
  `payment` decimal(12,2) NOT NULL,
  `net_amount` decimal(12,2) DEFAULT NULL,
  `currency` varchar(10) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_invoice_number` (`invoice_number`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_detail`
--

LOCK TABLES `transaction_detail` WRITE;
/*!40000 ALTER TABLE `transaction_detail` DISABLE KEYS */;
INSERT INTO `transaction_detail` VALUES (1,'4','2025-11-26',20.00,30.00,'USD','2025-11-26 18:22:01','2025-11-26 18:22:01'),(2,'4','2025-11-26',20.00,30.00,'USD','2025-11-26 19:52:31','2025-11-26 19:52:31');
/*!40000 ALTER TABLE `transaction_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_master`
--

DROP TABLE IF EXISTS `transaction_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_master` (
  `idtransaction_master` bigint NOT NULL AUTO_INCREMENT,
  `customer_username` varchar(45) DEFAULT NULL,
  `invoice_number` bigint DEFAULT NULL,
  `invoiced` tinyint DEFAULT '0',
  `invoice_date` datetime DEFAULT NULL,
  `payment_status` tinyint DEFAULT '0',
  `amount` decimal(19,9) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idtransaction_master`),
  UNIQUE KEY `invoice_number_UNIQUE` (`invoice_number`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_master`
--

LOCK TABLES `transaction_master` WRITE;
/*!40000 ALTER TABLE `transaction_master` DISABLE KEYS */;
INSERT INTO `transaction_master` VALUES (1,'2013',1,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(2,'2014',2,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(3,'2015',3,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(4,'2016',4,1,'2025-11-26 18:04:18',0,50.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(5,'2017',5,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(6,'2018',6,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(7,'2019',7,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(8,'2020',8,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(9,'hm1000',9,1,'2025-11-26 18:04:18',0,27.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(10,'hm1001',10,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(11,'hm1003',11,1,'2025-11-26 18:04:18',0,27.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(12,'hm1007',12,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(13,'hm1008',13,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(14,'hm1009',14,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(15,'hm1011',15,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(16,'hm1012',16,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(17,'hm1014',17,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(18,'hm1015',18,1,'2025-11-26 18:04:18',0,27.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(19,'hm1016',19,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(20,'hm1017',20,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(21,'hm1018',21,1,'2025-11-26 18:04:18',0,32.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(22,'hm1019',22,1,'2025-11-26 18:04:18',0,25.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(23,'hm1020',23,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(24,'hm1021',24,1,'2025-11-26 18:04:18',0,35.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(25,'hm1022',25,1,'2025-11-26 18:04:18',0,0.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(26,'hm1023',26,1,'2025-11-26 18:04:18',0,27.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(27,'hm1025',27,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(28,'hm1026',28,1,'2025-11-26 18:04:18',0,32.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(29,'hm1027',29,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(30,'hm1028',30,1,'2025-11-26 18:04:18',0,35.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(31,'hm1031',31,1,'2025-11-26 18:04:18',0,40.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(32,'hm1032',32,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(33,'hm1033',33,1,'2025-11-26 18:04:18',0,27.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18'),(34,'hm1034',34,1,'2025-11-26 18:04:18',0,30.000000000,'2025-11-26 18:04:18','2025-11-26 18:04:18');
/*!40000 ALTER TABLE `transaction_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `idusers` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `fullname` varchar(45) DEFAULT NULL,
  `password_hash` text NOT NULL,
  `mobile` varchar(45) DEFAULT NULL,
  `app_token` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idusers`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'dak','mohamed el dakdouki','$2a$12$uRiGUtuaVU1SwWAT6ebbL.EqYtJPE5TgVkr8ONIC8vz/OExDOxYNS','1','1','2025-11-15 13:22:40','2025-11-22 11:40:31');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-26 21:22:48
