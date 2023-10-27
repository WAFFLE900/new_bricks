-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 34.81.186.58    Database: bricksdata
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.20.04.2

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
-- Table structure for table `delete`
--

DROP TABLE IF EXISTS `delete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delete` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int unsigned NOT NULL,
  `user_id` int unsigned NOT NULL,
  `delete_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `delete_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`),
  CONSTRAINT `delete_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delete`
--

LOCK TABLES `delete` WRITE;
/*!40000 ALTER TABLE `delete` DISABLE KEYS */;
/*!40000 ALTER TABLE `delete` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `groups` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `groups_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups_member`
--

DROP TABLE IF EXISTS `groups_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `groups_member` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `group_member_identity` varchar(20) DEFAULT NULL,
  `group_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `groups_member_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `groups_member_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups_member`
--

LOCK TABLES `groups_member` WRITE;
/*!40000 ALTER TABLE `groups_member` DISABLE KEYS */;
/*!40000 ALTER TABLE `groups_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mention`
--

DROP TABLE IF EXISTS `mention`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mention` (
  `notification_id` int unsigned NOT NULL,
  `notification_recipient_id` int unsigned NOT NULL,
  `notification_isRead` tinyint(1) NOT NULL,
  PRIMARY KEY (`notification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mention`
--

LOCK TABLES `mention` WRITE;
/*!40000 ALTER TABLE `mention` DISABLE KEYS */;
INSERT INTO `mention` VALUES (1,2,0),(2,3,1),(3,1,1);
/*!40000 ALTER TABLE `mention` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `notification_content` varchar(300) NOT NULL,
  `notification_sender_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (2,'notice1',1),(4,'notice2',2),(7,'notice3',3);
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `problem`
--

DROP TABLE IF EXISTS `problem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `problem` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `problem_content` varchar(300) DEFAULT NULL,
  `problem_sovled` tinyint(1) DEFAULT NULL,
  `user_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `problem_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `problem`
--

LOCK TABLES `problem` WRITE;
/*!40000 ALTER TABLE `problem` DISABLE KEYS */;
/*!40000 ALTER TABLE `problem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_type` varchar(20) DEFAULT NULL,
  `project_image` varchar(20) DEFAULT NULL,
  `project_name` varchar(20) NOT NULL,
  `project_trashcan` tinyint(1) DEFAULT '0',
  `project_ended` tinyint(1) DEFAULT '0',
  `user_id` int unsigned NOT NULL,
  `project_edit` tinyint(1) NOT NULL,
  `project_visible` tinyint(1) NOT NULL,
  `project_comment` tinyint(1) NOT NULL,
  `project_creation_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `project_edit_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (29,'學校','test1.jpg','培訓社課',1,0,1,0,0,0,'2023-05-17 20:02:32','2023-05-21 16:58:22'),(30,'學校','test2.jpg','社團發展計劃',1,0,1,0,0,0,'2023-05-17 20:02:32','2023-02-21 16:58:22'),(31,'學校','test3.jpg','社團產物保管',1,1,1,0,0,0,'2023-05-17 20:02:32','2023-05-21 16:58:22'),(32,'未分類','test2.jpg','社團經費管理',1,1,1,0,0,0,'2023-05-17 20:02:32','2023-05-28 20:24:12'),(33,'學校','test3.jpg','社團財務管理',1,1,2,0,0,0,'2023-05-17 20:02:32','2023-03-21 16:58:22'),(34,'學校','test2.jpg','垃圾桶',0,1,1,0,0,0,'2023-05-17 20:02:32','2023-05-24 19:59:49'),(35,'學校','test2.jpg','垃圾桶',0,0,1,0,0,0,'2023-05-17 20:02:32','2023-05-21 16:58:22'),(36,'學校','test2.jpg','已結束',0,0,1,0,0,0,'2023-05-17 20:02:32','2023-05-21 16:58:22'),(37,'normal','test4.jpg','7點22分的測試',1,1,3,0,0,0,'2023-05-24 20:00:06','2023-05-24 20:00:06'),(38,'normal','test4.jpg','7點22分的測試',1,1,3,0,0,0,'2023-05-24 20:02:56','2023-05-24 20:02:56'),(39,'normal','test4.jpg','7點22分的測試',1,1,3,0,0,0,'2023-05-24 20:03:06','2023-05-24 20:03:06'),(40,'normal','test4.jpg','7點22分的測試',1,1,3,0,0,0,'2023-05-24 20:03:11','2023-05-24 20:03:11'),(41,'normal','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-24 20:06:02','2023-05-24 20:06:02'),(42,'normal','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:39:45','2023-05-25 02:39:45'),(43,'normal','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:03','2023-05-25 02:40:03'),(44,'normal','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:03','2023-05-25 02:40:03'),(45,'normal','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:04','2023-05-25 02:40:04'),(46,'2707','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:04','2023-05-25 02:40:04'),(47,'normal AND 1809=5613','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:06','2023-05-25 02:40:06'),(48,'normal AND 3540=3540','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:06','2023-05-25 02:40:06'),(49,'-7173','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:10','2023-05-25 02:40:10'),(50,'-5266) OR 4094=6153#','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:10','2023-05-25 02:40:10'),(51,'-5359) OR 1239=1239#','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:10','2023-05-25 02:40:10'),(52,'-9688\' OR 5097=9795#','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:11','2023-05-25 02:40:11'),(53,'-8148\' OR 1239=1239#','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:11','2023-05-25 02:40:11'),(54,'-4202 OR 4362=5612#','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:11','2023-05-25 02:40:11'),(55,'-9794 OR 1239=1239#','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:11','2023-05-25 02:40:11'),(56,'0','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:29','2023-05-25 02:40:29'),(57,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:29','2023-05-25 02:40:29'),(58,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:34','2023-05-25 02:40:34'),(59,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:34','2023-05-25 02:40:34'),(60,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:34','2023-05-25 02:40:34'),(61,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:34','2023-05-25 02:40:34'),(62,NULL,'test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:43','2023-05-25 02:40:43'),(63,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:43','2023-05-25 02:40:43'),(64,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:47','2023-05-25 02:40:47'),(65,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:47','2023-05-25 02:40:47'),(66,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:47','2023-05-25 02:40:47'),(67,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:47','2023-05-25 02:40:47'),(68,'0','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:55','2023-05-25 02:40:55'),(69,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:55','2023-05-25 02:40:55'),(70,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:59','2023-05-25 02:40:59'),(71,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:40:59','2023-05-25 02:40:59'),(72,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:00','2023-05-25 02:41:00'),(73,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:00','2023-05-25 02:41:00'),(74,'ELT(1691=4826,4826)','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:02','2023-05-25 02:41:02'),(75,'ELT(8738=8738,8607)','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:02','2023-05-25 02:41:02'),(76,'(5318=8325)*8325','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:02','2023-05-25 02:41:02'),(77,'(4678=4678)*9697','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:02','2023-05-25 02:41:02'),(78,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:16','2023-05-25 02:41:16'),(79,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:20','2023-05-25 02:41:20'),(80,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:24','2023-05-25 02:41:24'),(81,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:29','2023-05-25 02:41:29'),(82,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:34','2023-05-25 02:41:34'),(83,'1','test4.jpg','7點22分的測試',1,1,1,0,0,0,'2023-05-25 02:41:35','2023-05-25 02:41:35'),(84,'學校','test5.jpg','8點32分的測試',0,1,3,0,0,0,'2023-05-28 20:33:31','2023-05-28 20:33:31'),(85,'學校','test6.jpg','8點33分的測試',0,1,1,0,0,0,'2023-05-28 20:33:55','2023-05-28 20:33:55');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_sort`
--

DROP TABLE IF EXISTS `project_sort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_sort` (
  `type_id` int NOT NULL,
  `project_type` varchar(20) NOT NULL,
  `project_type_sort` int NOT NULL,
  `user_id` int unsigned NOT NULL,
  `project_ended` tinyint(1) NOT NULL,
  PRIMARY KEY (`type_id`),
  KEY `project_sort_fk_idx` (`user_id`),
  CONSTRAINT `project_sort_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_sort`
--

LOCK TABLES `project_sort` WRITE;
/*!40000 ALTER TABLE `project_sort` DISABLE KEYS */;
INSERT INTO `project_sort` VALUES (1,'未分類',1,1,0),(2,'學校',3,1,0),(3,'學校',2,2,0),(4,'未分類',1,2,0),(5,'實習',2,1,0),(6,'測試',4,1,0),(7,'測試2',4,1,0),(8,'測試3',6,1,0),(9,'測試5',7,1,0);
/*!40000 ALTER TABLE `project_sort` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `record`
--

DROP TABLE IF EXISTS `record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `record` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `record_date` date DEFAULT NULL,
  `record_department` varchar(50) DEFAULT NULL,
  `record_attendances` int unsigned DEFAULT NULL,
  `record_place` varchar(50) DEFAULT NULL,
  `record_host_name` varchar(50) DEFAULT NULL,
  `user_id` int unsigned NOT NULL,
  `project_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `record_ibfk_project` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `record_ibfk_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
/*!40000 ALTER TABLE `record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search_history`
--

DROP TABLE IF EXISTS `search_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_history` (
  `id` int NOT NULL,
  `user_id` int unsigned NOT NULL,
  `search_content` varchar(100) DEFAULT NULL,
  `search_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `history_fk_idx` (`user_id`),
  CONSTRAINT `history_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_history`
--

LOCK TABLES `search_history` WRITE;
/*!40000 ALTER TABLE `search_history` DISABLE KEYS */;
INSERT INTO `search_history` VALUES (1,3,'search1','2023-05-29 16:49:10'),(2,3,'search1','2023-05-29 17:01:05'),(3,2,'search1','2023-05-29 17:07:08'),(4,2,'search2','2023-05-29 17:05:50'),(5,2,'search3','2023-05-29 17:05:54'),(6,1,'search1','2023-05-29 17:10:21'),(7,1,'search2','2023-05-29 17:10:05'),(8,1,'search3','2023-05-29 17:10:11');
/*!40000 ALTER TABLE `search_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_textBox`
--

DROP TABLE IF EXISTS `tag_textBox`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag_textBox` (
  `tag_id` int NOT NULL,
  `textBox_id` int NOT NULL,
  PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag_textBox`
--

LOCK TABLES `tag_textBox` WRITE;
/*!40000 ALTER TABLE `tag_textBox` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag_textBox` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `textBox`
--

DROP TABLE IF EXISTS `textBox`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `textBox` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `textBox_content` varchar(300) DEFAULT NULL,
  `record_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `textBox`
--

LOCK TABLES `textBox` WRITE;
/*!40000 ALTER TABLE `textBox` DISABLE KEYS */;
/*!40000 ALTER TABLE `textBox` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_email` varchar(64) NOT NULL,
  `user_password` varchar(128) NOT NULL,
  `user_name` varchar(16) NOT NULL,
  `user_purpose` varchar(10) DEFAULT NULL,
  `user_identity` varchar(10) DEFAULT NULL,
  `user_otherTool` varchar(100) DEFAULT NULL,
  `user_avatar` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_email` (`user_email`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'test1@gmail.com','test1password','test1user','1','學生','Notion,Asana,Google 雲端',''),(2,'test2@gmail.com','test2password','test2user','','','',''),(3,'test3@gmail.com','test3password','test3user','營隊','學生','Notion,Asana,Google 雲端',''),(4,'test4@gmail.com','test4password',' test4user','營隊','學生','Notion,Asana,Google 雲端',NULL),(5,'test5@gmail.com','a6759ef8b1e48d78c7e62944bc5e7a2cd0e65fdf003713e871c00172f2d8e77b',' test5user','營隊','學生','Notion,Asana,Google 雲端',NULL),(17,'1@2','a7cc881e8bafd9441bf2b96dc55dee596c6ac139744a3343bac3f16bb4b80915',' 1@2','課堂作業','高中職 (含) 以下','Google 雲端',NULL),(18,'test6@gmail.com','5f7adc73392764002b5efdf972d1872cf5949731f71b32cb6542352d815cf744',' test6user','營隊','學生','Notion,Asana,Google 雲端',NULL),(19,'sdfghjkl;@d','6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b',' yghjkl','營隊','高中職 (含) 以下','Trello',NULL),(20,'test17@gmail.com','46203c818f3d9a78cdc749eabb075f25fc96b87586f851242542bc6c1f0781bf',' test17',NULL,NULL,NULL,NULL),(21,'test18@gmail.com','58a7983073db9298cf236d398ffa90a54972be5ceda30f22f619eb63dab7250c',' test18user',NULL,NULL,NULL,NULL),(22,'test121@gmail.com','481ead938fad7d8ccdef10efcb514306f7cb859c707d62002dd77531962e7078',' test121','社團,競賽','高中職 (含) 以下','Notion,Trello',NULL),(23,'test123@gmail.com','3e5c3896cfe5340eeb788eeea9e48f54185df5bbfd4939f7d7b4621d0b02d8d1',' test123','社團,競賽','高中職 (含) 以下','Google 雲端,Evernote',NULL),(24,'test20@gmail.com','8485623d5aa7e185c5feda0b9e76b475238bb5d13115bff2d5280c552343969f',' test20','營隊,社團','博士','Notion',NULL);
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

-- Dump completed on 2023-06-05 13:25:39
