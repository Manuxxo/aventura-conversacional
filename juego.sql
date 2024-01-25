-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         5.5.60 - MySQL Community Server (GPL)
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para juego
CREATE DATABASE IF NOT EXISTS `juego` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_spanish_ci */;
USE `juego`;

-- Volcando estructura para tabla juego.jugador
CREATE TABLE IF NOT EXISTS `jugador` (
  `idjugador` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  `puntuacion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idjugador`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.jugador: ~0 rows (aproximadamente)

-- Volcando estructura para tabla juego.objeto
CREATE TABLE IF NOT EXISTS `objeto` (
  `idobjeto` int(11) NOT NULL AUTO_INCREMENT,
  `idsala` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idobjeto`),
  KEY `idobjeto` (`idobjeto`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.objeto: ~9 rows (aproximadamente)
INSERT INTO `objeto` (`idobjeto`, `idsala`) VALUES
	(1, 2),
	(2, 2),
	(3, 1),
	(4, 3),
	(5, 4),
	(6, 3),
	(7, 1),
	(8, 4),
	(9, 2);

-- Volcando estructura para tabla juego.partida
CREATE TABLE IF NOT EXISTS `partida` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `objetos` varchar(255) COLLATE latin1_spanish_ci DEFAULT NULL,
  `puntuacion` int(11) DEFAULT NULL,
  `idsala` varchar(255) COLLATE latin1_spanish_ci DEFAULT NULL,
  `salavisitada` varchar(50) COLLATE latin1_spanish_ci DEFAULT NULL,
  `monedas` int(11) DEFAULT NULL,
  `nombre` varchar(50) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.partida: ~2 rows (aproximadamente)
INSERT INTO `partida` (`id`, `objetos`, `puntuacion`, `idsala`, `salavisitada`, `monedas`, `nombre`) VALUES
	(2, 'llave candelabro ', 100, '2', '1 0 1 0 0 ', 100, 'Manu');

-- Volcando estructura para tabla juego.personaje
CREATE TABLE IF NOT EXISTS `personaje` (
  `idpersonaje` int(11) NOT NULL,
  `idsala` int(11) DEFAULT NULL,
  PRIMARY KEY (`idpersonaje`),
  KEY `idpersonaje` (`idpersonaje`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.personaje: ~3 rows (aproximadamente)
INSERT INTO `personaje` (`idpersonaje`, `idsala`) VALUES
	(1, 3),
	(2, 4),
	(3, 4);

-- Volcando estructura para tabla juego.record
CREATE TABLE IF NOT EXISTS `record` (
  `nombrejugador` varchar(50) COLLATE latin1_spanish_ci DEFAULT NULL,
  `puntuacion` int(11) DEFAULT NULL,
  `idjugador` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.record: ~1 rows (aproximadamente)
INSERT INTO `record` (`nombrejugador`, `puntuacion`, `idjugador`) VALUES
	('Manu', 101, 1);

-- Volcando estructura para tabla juego.sala
CREATE TABLE IF NOT EXISTS `sala` (
  `idsala` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(1000) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`idsala`),
  KEY `id` (`idsala`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.sala: ~5 rows (aproximadamente)
INSERT INTO `sala` (`idsala`, `descripcion`) VALUES
	(1, 'Te encuentras en una enorme sala llena de columnas , no hay apenas luz, el olor es desagradable, algo anda cerca'),
	(2, 'Has entrado en salon, de esta enorme fortaleza, es amplio y muy luminoso, a lo lejo se aprecia un par de puertas'),
	(3, 'Estas en una mazmorra llena de esqueletos de antiguos inquilinos, el suelo es tierra y parece estar mojado'),
	(4, 'Bienvenido a la tienda de esta fortaleza, el tendero estara encantado de hacer tratos contigo'),
	(5, 'Has llegado a una habitacion , quizas sea el fin de todo o comiezo de algo nuevo, se ve una puerta al final, pero parece cerrada');

-- Volcando estructura para tabla juego.salida
CREATE TABLE IF NOT EXISTS `salida` (
  `idsalida` int(11) NOT NULL AUTO_INCREMENT,
  `idsala` int(11) NOT NULL DEFAULT '0',
  `salida` varchar(10) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  `idsalasalida` int(11) DEFAULT NULL,
  PRIMARY KEY (`idsalida`),
  KEY `idsalida` (`idsalida`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.salida: ~9 rows (aproximadamente)
INSERT INTO `salida` (`idsalida`, `idsala`, `salida`, `idsalasalida`) VALUES
	(1, 1, 'sur', 3),
	(2, 1, 'este', 2),
	(3, 2, 'este', 5),
	(4, 2, 'oeste', 1),
	(5, 2, 'sur', 4),
	(6, 3, 'norte', 1),
	(7, 4, 'norte', 2),
	(8, 5, 'este', 0),
	(9, 5, 'oeste', 2);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
