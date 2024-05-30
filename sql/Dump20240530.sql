-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 104.199.143.218    Database: bricksdata
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.20.04.1

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
  `project_edit` tinyint(1) NOT NULL DEFAULT '0',
  `project_visible` tinyint(1) NOT NULL DEFAULT '0',
  `project_comment` tinyint(1) NOT NULL DEFAULT '0',
  `project_creation_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `project_edit_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (86,'學校','test1.jpg','Bricks 專案開發',0,1,25,0,0,0,'2024-03-21 10:40:09','2024-05-26 06:10:03'),(87,'','test2.jpg','專案會議記錄',0,1,25,0,0,0,'2024-03-21 10:41:06','2024-05-27 07:23:04'),(89,'實習','test11.jpg','工研院專案',1,0,25,0,0,0,'2024-04-14 03:20:21','2024-04-19 09:22:11'),(92,'','test11.jpg','資料科學作業',0,0,25,0,0,0,'2024-05-27 07:28:06','2024-05-27 07:28:06');
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
  `record_name` varchar(100) NOT NULL,
  `record_date` date DEFAULT NULL,
  `record_department` varchar(50) DEFAULT NULL,
  `record_place` varchar(50) DEFAULT NULL,
  `record_attendees_name` varchar(100) DEFAULT NULL,
  `record_absentees_name` varchar(100) DEFAULT NULL,
  `record_recorder_name` varchar(50) DEFAULT NULL,
  `record_trashcan` tinyint(1) DEFAULT '0',
  `record_creation_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `record_update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int unsigned NOT NULL,
  `project_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `record_name_UNIQUE` (`record_name`),
  KEY `user_id` (`user_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `record_ibfk_project` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `record_ibfk_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
INSERT INTO `record` VALUES (3,'會議記錄一','2024-03-28','BE','達賢702','Tommy,Benson,Thomas,Asp',NULL,'Thomas',0,'2024-04-04 10:55:51','2024-05-23 10:58:14',25,86),(4,'test',NULL,NULL,NULL,NULL,NULL,NULL,0,'2024-05-23 10:32:00','2024-05-23 10:56:28',25,86),(6,'會議記錄二','2023-12-21','後端','四維堂',NULL,NULL,NULL,0,'2024-05-30 06:16:49','2024-05-30 06:16:49',34,86);
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
  `tag_class` varchar(5) NOT NULL,
  `tag_creation_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (1,'CI/CD','','2024-03-28 09:34:10'),(2,'資料庫','','2024-03-28 09:34:11'),(3,'test','1','2024-05-23 11:49:45');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_textBox`
--

DROP TABLE IF EXISTS `tag_textBox`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag_textBox` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `textBox_id` int unsigned NOT NULL,
  `tag_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tagtextBox_ibfk_texBox_idx` (`textBox_id`),
  KEY `tagTextBox_ibfk_tag_idx` (`tag_id`),
  CONSTRAINT `tagTextBox_ibfk_tag` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tagTextBox_ibfk_textBox` FOREIGN KEY (`textBox_id`) REFERENCES `textBox` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag_textBox`
--

LOCK TABLES `tag_textBox` WRITE;
/*!40000 ALTER TABLE `tag_textBox` DISABLE KEYS */;
INSERT INTO `tag_textBox` VALUES (3,6,2),(4,6,1);
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
  `record_id` int unsigned NOT NULL,
  `textBox_update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `textBox_ibfk_record_idx` (`record_id`),
  CONSTRAINT `textBox_ibfk_record` FOREIGN KEY (`record_id`) REFERENCES `record` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `textBox`
--

LOCK TABLES `textBox` WRITE;
/*!40000 ALTER TABLE `textBox` DISABLE KEYS */;
INSERT INTO `textBox` VALUES (6,'完成前後端串接',3,'2024-05-23 11:07:48');
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
  `user_password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_name` varchar(16) NOT NULL,
  `user_purpose` varchar(10) DEFAULT NULL,
  `user_identity` varchar(10) DEFAULT NULL,
  `user_otherTool` varchar(100) DEFAULT NULL,
  `user_avatar` varchar(20) DEFAULT NULL,
  `user_session` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_email` (`user_email`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (25,'bricksBE@gmail.com','63d3420fbf1aeb870892e81e97895543a672c5b39cb585dbf768f111b4ffabfd','bricksBE','社團','學生','Notion,Asana,Google 雲端',NULL,NULL),(26,'bricksdemo@gmail.com','65d17d0165363c4fa5e7cfaa43e80ab49bf62310476b4b7ee546e5a289d2c6cc','bricks','社團','學生','Notion,Asana,Google 雲端',NULL,NULL),(27,'tommycat100@gmail.com',NULL,'tommy lin',NULL,NULL,NULL,NULL,NULL),(28,'tommycatyoutub@gmail.com',NULL,'林品榮',NULL,NULL,NULL,NULL,NULL),(29,'brickstest@gmail.com','65d17d0165363c4fa5e7cfaa43e80ab49bf62310476b4b7ee546e5a289d2c6cc','bricksuser',NULL,NULL,NULL,NULL,NULL),(30,'test7@gmail.com','0f20e29dfa12cd0cfd095b8addfcfd96820bf47096e7628a9230c16b79851c45','test7user',NULL,NULL,NULL,NULL,NULL),(31,'123@gmail.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','123',NULL,NULL,NULL,NULL,NULL),(32,'456@gmail.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','759',NULL,NULL,NULL,NULL,NULL),(33,'789@gmail.com','35a9e381b1a27567549b5f8a6f783c167ebf809f1c4d6a9e367240484d8ce281','762',NULL,NULL,NULL,NULL,NULL),(34,'741@gmail.com','75f7313c20144e39edcf57a14733d074aee0c482320d5178ee0ef2f2608c2996','741',NULL,NULL,NULL,NULL,NULL),(35,'963@gmail.com','b22eb34537f6f6753da6e0dc05713be0ccc35ef12dae0f6bf19b5206d373af33','456',NULL,NULL,NULL,NULL,NULL),(36,'256@gmail.com','b3a8e0e1f9ab1bfe3a36f231f676f78bb30a519d2b21e6c530c0eee8ebb4a5d0','45',NULL,NULL,NULL,NULL,NULL),(37,'test5@gmail.com','0f20e29dfa12cd0cfd095b8addfcfd96820bf47096e7628a9230c16b79851c45','test7user',NULL,NULL,NULL,NULL,NULL),(38,'12@gmail.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','123',NULL,NULL,NULL,NULL,NULL),(39,'123@123','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','123',NULL,NULL,NULL,NULL,NULL),(40,'bricksBE_test@gmail.com','a4fa78a0018980c1203a96cbfbc31ce732c7eefd0a6837033d0fe8189250e4c3','BE_test',NULL,NULL,NULL,NULL,NULL),(41,'109302061@g.nccu.edu.tw','cfe0576e018a93ef9e276e14f4a54c0fa4d5533f0594f434310bb9788047ba64','tim',NULL,NULL,NULL,NULL,NULL),(42,'Bricks_BE@gmail.com','994e1a9dc5e174d8127770b22297c85f081cee5d937c160e9281b776c54ec95a','test',NULL,NULL,NULL,NULL,NULL);
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

-- Dump completed on 2024-05-30 14:52:53
