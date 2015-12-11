-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: lpari_db
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

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
-- Table structure for table `Location_tweet`
--

DROP TABLE IF EXISTS `Location_tweet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Location_tweet` (
  `location_name` varchar(64) NOT NULL,
  `country_code` char(4) NOT NULL,
  `idTweet` bigint(30) NOT NULL,
  `frequency` int(11) DEFAULT NULL,
  KEY `fk_Location_tweet_Locations_table1_idx` (`location_name`,`country_code`),
  KEY `fk_Location_tweet_Tweets_table1_idx` (`idTweet`),
  CONSTRAINT `fk_Location_tweet_Locations_table1` FOREIGN KEY (`location_name`, `country_code`) REFERENCES `Locations_table` (`location_name`, `country_code`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Location_tweet_Tweets_table1` FOREIGN KEY (`idTweet`) REFERENCES `Tweets_table` (`idTweet`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Location_tweet`
--

LOCK TABLES `Location_tweet` WRITE;
/*!40000 ALTER TABLE `Location_tweet` DISABLE KEYS */;
/*!40000 ALTER TABLE `Location_tweet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Locations_table`
--

DROP TABLE IF EXISTS `Locations_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Locations_table` (
  `location_name` varchar(64) NOT NULL,
  `country_code` char(4) NOT NULL,
  `region_code` varchar(64) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  PRIMARY KEY (`location_name`,`country_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Locations_table`
--

LOCK TABLES `Locations_table` WRITE;
/*!40000 ALTER TABLE `Locations_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `Locations_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tweets_table`
--

DROP TABLE IF EXISTS `Tweets_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tweets_table` (
  `idTweet` bigint(30) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `text` varchar(200) DEFAULT NULL,
  `favorited` tinyint(4) DEFAULT NULL,
  `favoritedCount` int(11) DEFAULT NULL,
  `truncated` tinyint(4) DEFAULT NULL,
  `retweetCount` int(11) DEFAULT NULL,
  `retweeted` tinyint(4) DEFAULT NULL,
  `gato` int(11) DEFAULT NULL,
  `aroa` int(11) DEFAULT NULL,
  `RT` int(11) DEFAULT NULL,
  `URL` int(11) DEFAULT NULL,
  `idUser` bigint(30) NOT NULL,
  PRIMARY KEY (`idTweet`),
  KEY `fk_Tweets_table_Users_table_idx` (`idUser`),
  CONSTRAINT `fk_Tweets_table_Users_table` FOREIGN KEY (`idUser`) REFERENCES `Users_table` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tweets_table`
--

LOCK TABLES `Tweets_table` WRITE;
/*!40000 ALTER TABLE `Tweets_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `Tweets_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_location`
--

DROP TABLE IF EXISTS `User_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User_location` (
  `idUser` bigint(30) NOT NULL,
  `country_code` char(4) DEFAULT NULL,
  `region_code` varchar(64) DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  PRIMARY KEY (`idUser`),
  CONSTRAINT `fk_User_location_Users_table1` FOREIGN KEY (`idUser`) REFERENCES `Users_table` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_location`
--

LOCK TABLES `User_location` WRITE;
/*!40000 ALTER TABLE `User_location` DISABLE KEYS */;
/*!40000 ALTER TABLE `User_location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users_table`
--

DROP TABLE IF EXISTS `Users_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users_table` (
  `idUser` bigint(30) NOT NULL,
  `screen_name` varchar(255) DEFAULT NULL,
  `time_zone` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `followers_count` int(11) DEFAULT NULL,
  `region` varchar(64) DEFAULT NULL,
  `geo_enabled` tinyint(1) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `Chile` tinyint(1) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `friends_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`idUser`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users_table`
--

LOCK TABLES `Users_table` WRITE;
/*!40000 ALTER TABLE `Users_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `Users_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-10 22:55:36
