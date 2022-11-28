-- MariaDB dump 10.19  Distrib 10.9.4-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: huertapp
-- ------------------------------------------------------
-- Server version	10.9.4-MariaDB-1:10.9.4+maria~ubu2204

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
-- Table structure for table `Intercambio`
--

DROP TABLE IF EXISTS `Intercambio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Intercambio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_concretado` tinyint(4) DEFAULT NULL,
  `fecha_intercambio` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Intercambio_has_Usuario`
--

DROP TABLE IF EXISTS `Intercambio_has_Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Intercambio_has_Usuario` (
  `Intercambio_id` int(11) NOT NULL,
  `Usuario_id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`Intercambio_id`,`Usuario_id_usuario`),
  KEY `fk_Intercambio_has_Usuario_Usuario1_idx` (`Usuario_id_usuario`),
  KEY `fk_Intercambio_has_Usuario_Intercambio1_idx` (`Intercambio_id`),
  CONSTRAINT `fk_Intercambio_has_Usuario_Intercambio1` FOREIGN KEY (`Intercambio_id`) REFERENCES `Intercambio` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Intercambio_has_Usuario_Usuario1` FOREIGN KEY (`Usuario_id_usuario`) REFERENCES `Usuario` (`id_usuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Mensaje`
--

DROP TABLE IF EXISTS `Mensaje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Mensaje` (
  `id_mensaje` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(45) DEFAULT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `Intercambio_id` int(11) NOT NULL,
  `Publicaciones_id_publicacion` int(11) NOT NULL,
  PRIMARY KEY (`id_mensaje`),
  KEY `fk_Mensaje_Intercambio1_idx` (`Intercambio_id`),
  KEY `fk_Mensaje_Publicaciones1_idx` (`Publicaciones_id_publicacion`),
  CONSTRAINT `fk_Mensaje_Intercambio1` FOREIGN KEY (`Intercambio_id`) REFERENCES `Intercambio` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Mensaje_Publicaciones1` FOREIGN KEY (`Publicaciones_id_publicacion`) REFERENCES `Publicacion` (`id_publicacion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Publicacion`
--

DROP TABLE IF EXISTS `Publicacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Publicacion` (
  `id_publicacion` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(45) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha_creacion` date DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL COMMENT 'id del usuario que creo la publicacion',
  `foto` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_publicacion`),
  KEY `Publicacion_FK` (`id_usuario`),
  CONSTRAINT `Publicacion_FK` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuario` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fecha_inscripcion` date DEFAULT NULL,
  `activo` tinyint(4) DEFAULT NULL,
  `celular` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Usuario_has_Publicacion`
--

DROP TABLE IF EXISTS `Usuario_has_Publicacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuario_has_Publicacion` (
  `Usuario_id_usuario` int(11) NOT NULL,
  `Publicacion_id_publicacion` int(11) NOT NULL,
  PRIMARY KEY (`Usuario_id_usuario`,`Publicacion_id_publicacion`),
  KEY `fk_Usuario_has_Publicacion_Publicacion1_idx` (`Publicacion_id_publicacion`),
  KEY `fk_Usuario_has_Publicacion_Usuario1_idx` (`Usuario_id_usuario`),
  CONSTRAINT `fk_Usuario_has_Publicacion_Publicacion1` FOREIGN KEY (`Publicacion_id_publicacion`) REFERENCES `Publicacion` (`id_publicacion`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Usuario_has_Publicacion_Usuario1` FOREIGN KEY (`Usuario_id_usuario`) REFERENCES `Usuario` (`id_usuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-28 20:36:49
