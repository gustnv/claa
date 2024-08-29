-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: claa
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `unscheduled_activities`
--

DROP TABLE IF EXISTS `unscheduled_activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unscheduled_activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `justification` varchar(1000) NOT NULL,
  `total_hours` int NOT NULL,
  `teaching_hours` int NOT NULL,
  `research_hours` int NOT NULL,
  `extension_hours` int NOT NULL,
  `report_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_id` (`report_id`),
  CONSTRAINT `unscheduled_activities_ibfk_1` FOREIGN KEY (`report_id`) REFERENCES `reports` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scheduled_activities`
--

DROP TABLE IF EXISTS `scheduled_activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scheduled_activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `carrying_out` enum('not','partial','full') NOT NULL,
  `total_hours` int NOT NULL,
  `teaching_hours` int NOT NULL DEFAULT '0',
  `research_hours` int NOT NULL DEFAULT '0',
  `extension_hours` int NOT NULL DEFAULT '0',
  `report_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_id` (`report_id`),
  CONSTRAINT `scheduled_activities_ibfk_1` FOREIGN KEY (`report_id`) REFERENCES `reports` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `groups` (
  `email` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `instagram` varchar(100) DEFAULT NULL,
  `webpage` varchar(100) DEFAULT NULL,
  `nof_scholarships` int NOT NULL,
  `nof_volunteers` int NOT NULL,
  `address` varchar(100) NOT NULL,
  `campus` enum('Araranguá','Florianópolis','Curitibanos','Joinville','Blumenau') NOT NULL,
  `center` enum('CTS','CTE','CCR','CTC','CCB','CTJ','CCA','CCE','CCS','CCJ','CDS','CED','CHF','CFM','CSE') NOT NULL,
  `email_tutor` varchar(100) NOT NULL,
  PRIMARY KEY (`email`),
  KEY `email_tutor` (`email_tutor`),
  CONSTRAINT `groups_ibfk_1` FOREIGN KEY (`email_tutor`) REFERENCES `users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `activities_articulation` varchar(1000) NOT NULL,
  `politics_articulation` varchar(1000) NOT NULL,
  `selection_students` varchar(1000) NOT NULL,
  `permanence_students` varchar(1000) NOT NULL,
  `ufsc_target_public` varchar(1000) NOT NULL,
  `society_target_public` varchar(1000) NOT NULL,
  `infrastructure_condition` enum('better','equal','worse') NOT NULL,
  `infrastructure_description` varchar(500) NOT NULL,
  `tools_condition` enum('better','equal','worse') NOT NULL,
  `tools_description` varchar(500) NOT NULL,
  `costing_condition` enum('yes','no') NOT NULL,
  `costing_description` varchar(500) NOT NULL,
  `year` year NOT NULL,
  `group_email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `group_email` (`group_email`),
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`group_email`) REFERENCES `groups` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `email` varchar(100) NOT NULL,
  `password` varchar(60) NOT NULL,
  `name` varchar(100) NOT NULL,
  `status_claa` enum('no','substitute','holder') NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for tables
--

LOCK TABLES 
  `unscheduled_activities` WRITE, 
  `scheduled_activities` WRITE, 
  `groups` WRITE, 
  `reports` WRITE, 
  `users` WRITE;

/*!40000 ALTER TABLE `unscheduled_activities` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduled_activities` DISABLE KEYS */;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

/*!40000 ALTER TABLE `unscheduled_activities` ENABLE KEYS */;
/*!40000 ALTER TABLE `scheduled_activities` ENABLE KEYS */;
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
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
