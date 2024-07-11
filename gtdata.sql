-- MySQL dump 10.13  Distrib 5.7.43, for Linux (x86_64)
--
-- Host: localhost    Database: gtdata
-- ------------------------------------------------------
-- Server version	5.7.43-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alltimes`
--

DROP TABLE IF EXISTS `alltimes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alltimes` (
  `times` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alltimes`
--

LOCK TABLES `alltimes` WRITE;
/*!40000 ALTER TABLE `alltimes` DISABLE KEYS */;
INSERT INTO `alltimes` VALUES (0);
/*!40000 ALTER TABLE `alltimes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ipban`
--

DROP TABLE IF EXISTS `ipban`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ipban` (
  `ip` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ipban`
--

LOCK TABLES `ipban` WRITE;
/*!40000 ALTER TABLE `ipban` DISABLE KEYS */;
/*!40000 ALTER TABLE `ipban` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `ip` varchar(255) NOT NULL,
  `times` bigint(20) DEFAULT NULL,
  `addtimes` bigint(20) DEFAULT NULL,
  `checked` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `lastusetime` datetime DEFAULT NULL,
  PRIMARY KEY (`ip`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
-- nonono,deleted
--


--
-- Dumping events for database 'gtdata'
--

--
-- Dumping routines for database 'gtdata'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-10 18:03:38
