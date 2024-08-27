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
-- Table structure for table `atividades_nao_programadas`
--

DROP TABLE IF EXISTS `atividades_nao_programadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `atividades_nao_programadas` (
  `id_atividade_nao_prog` int NOT NULL AUTO_INCREMENT,
  `nome_atividade` varchar(50) NOT NULL,
  `justificativa` varchar(500) NOT NULL,
  `horas_totais` int NOT NULL,
  `classificacao` set('ensino','pesquisa','extensao') NOT NULL,
  `horas_ensino` int NOT NULL DEFAULT '0',
  `horas_pesquisa` int NOT NULL DEFAULT '0',
  `horas_extensao` int NOT NULL DEFAULT '0',
  `ano` year NOT NULL,
  `id_relatorio` int NOT NULL,
  `email_grupo_pet` varchar(50) NOT NULL,  -- Changed from int to varchar(50)
  PRIMARY KEY (`id_atividade_nao_prog`),
  KEY `id_relatorio` (`id_relatorio`),
  KEY `email_grupo_pet` (`email_grupo_pet`),
  CONSTRAINT `atividades_nao_programadas_ibfk_1` FOREIGN KEY (`id_relatorio`) REFERENCES `relatorios` (`id_relatorio`),
  CONSTRAINT `atividades_nao_programadas_ibfk_2` FOREIGN KEY (`email_grupo_pet`) REFERENCES `grupos_pet` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atividades_nao_programadas`
--

LOCK TABLES `atividades_nao_programadas` WRITE;
/*!40000 ALTER TABLE `atividades_nao_programadas` DISABLE KEYS */;
/*!40000 ALTER TABLE `atividades_nao_programadas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `atividades_programadas`
--

DROP TABLE IF EXISTS `atividades_programadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `atividades_programadas` (
  `id_atividade_prog` int NOT NULL AUTO_INCREMENT,
  `nome_atividade` varchar(50) NOT NULL,
  `realizacao` enum('nao','parcial','total') NOT NULL,
  `horas_totais` int NOT NULL,
  `classificacao` set('ensino','pesquisa','extensao') DEFAULT NULL,
  `horas_ensino` int NOT NULL DEFAULT '0',
  `horas_pesquisa` int NOT NULL DEFAULT '0',
  `horas_extensao` int NOT NULL DEFAULT '0',
  `ano` year NOT NULL,
  `id_relatorio` int NOT NULL,
  `email_grupo_pet` varchar(50) NOT NULL,  -- Changed from int to varchar(50)
  PRIMARY KEY (`id_atividade_prog`),
  KEY `id_relatorio` (`id_relatorio`),
  KEY `email_grupo_pet` (`email_grupo_pet`),
  CONSTRAINT `atividades_programadas_ibfk_1` FOREIGN KEY (`id_relatorio`) REFERENCES `relatorios` (`id_relatorio`),
  CONSTRAINT `atividades_programadas_ibfk_2` FOREIGN KEY (`email_grupo_pet`) REFERENCES `grupos_pet` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atividades_programadas`
--

LOCK TABLES `atividades_programadas` WRITE;
/*!40000 ALTER TABLE `atividades_programadas` DISABLE KEYS */;
/*!40000 ALTER TABLE `atividades_programadas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupos_pet`
--

DROP TABLE IF EXISTS `grupos_pet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos_pet` (
  `nome` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `instagram` varchar(100) DEFAULT NULL,
  `pagina` varchar(100) DEFAULT NULL,
  `nof_bolsistas` int NOT NULL,
  `nof_voluntarios` int NOT NULL,
  `endereco` varchar(100) DEFAULT NULL,
  `campus` enum('Araranguá','Florianópolis','Curitibanos','Joinvile','Blumenau') NOT NULL,
  `centro` enum('CTS','CTE','CCR','CTC','CCB','CTJ','CCA','CCE','CCS','CCJ','CDS','CED','CFH','CFM','CSE','PROGRAD') NOT NULL,
  `email_tutor` varchar(50) DEFAULT NULL,/*todo remove this default, it should be not null*/
  PRIMARY KEY (`email`),
  KEY `email_tutor` (`email_tutor`),
  CONSTRAINT `grupos_pet_ibfk_1` FOREIGN KEY (`email_tutor`) REFERENCES `usuarios` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos_pet`
--

LOCK TABLES `grupos_pet` WRITE;
/*!40000 ALTER TABLE `grupos_pet` DISABLE KEYS */;
/*!40000 ALTER TABLE `grupos_pet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relatorios`
--

DROP TABLE IF EXISTS `relatorios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `relatorios` (
  `id_relatorio` int NOT NULL AUTO_INCREMENT,
  `cond_infra` enum('melhorou','manteve','piorou') NOT NULL,
  `desc_infra` varchar(500) NOT NULL,
  `cond_equip` enum('melhorou','manteve','piorou') NOT NULL,
  `desc_equip` varchar(500) NOT NULL,
  `cond_custeio` enum('sim','nao') NOT NULL,
  `desc_custeio` varchar(500) NOT NULL,
  `publico_alvo_dentro` varchar(1000) NOT NULL,
  `publico_alvo_fora` varchar(1000) NOT NULL,
  `cont_permanencia` varchar(1000) NOT NULL,
  `cont_inclusao` varchar(1000) NOT NULL,
  `desc_articulacao_politica` varchar(1000) NOT NULL,
  `desc_articulacao_atividades` varchar(1000) NOT NULL,
  `ano` year NOT NULL,
  `id_grupo` varchar(50) NOT NULL,  -- Changed from int to varchar(50)
  PRIMARY KEY (`id_relatorio`),
  KEY `id_grupo` (`id_grupo`),
  CONSTRAINT `relatorios_ibfk_1` FOREIGN KEY (`id_grupo`) REFERENCES `grupos_pet` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relatorios`
--

LOCK TABLES `relatorios` WRITE;
/*!40000 ALTER TABLE `relatorios` DISABLE KEYS */;
/*!40000 ALTER TABLE `relatorios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `email` varchar(50) NOT NULL,
  `senha` varchar(60) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `membro_claa` enum('nao','suplente','titular') NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
