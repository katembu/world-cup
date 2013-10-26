-- MySQL dump 10.13  Distrib 5.5.34, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: world_cup
-- ------------------------------------------------------
-- Server version	5.5.34-0ubuntu0.13.10.1

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
-- Table structure for table `tournament_countries`
--

DROP TABLE IF EXISTS `tournament_countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tournament_countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `group` varchar(1) NOT NULL,
  `position` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tournament_countries`
--

LOCK TABLES `tournament_countries` WRITE;
/*!40000 ALTER TABLE `tournament_countries` DISABLE KEYS */;
INSERT INTO `tournament_countries` VALUES (1,'Brazil','A',1),(2,'Japan','A',2),(3,'Australia','A',3),(4,'Iran','A',4),(5,'South Korea','B',1),(6,'Netherlands','B',2),(7,'Italy','B',3),(8,'Costa Rica','B',4),(9,'United States','C',1),(10,'Argentina','C',2),(11,'Belgium','C',3),(12,'Switzerland','C',4),(13,'Germany','D',1),(14,'Colombia','D',2),(15,'Russia','D',3),(16,'Bosnia and Herzegovina','D',4),(17,'England','E',1),(18,'Spain','E',2),(19,'Chile','E',3),(20,'Ecuador','E',4),(21,'Honduras','F',1),(22,'Greece','F',2),(23,'France','F',3),(24,'Portugal','F',4),(25,'Ukraine','G',1),(26,'Sweden','G',2),(27,'Iceland','G',3),(28,'Romania','G',4),(29,'Croatia','H',1),(30,'Denmark','H',2),(31,'Mexico','H',3),(32,'Finland','H',4);
/*!40000 ALTER TABLE `tournament_countries` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-10-26 10:44:19
