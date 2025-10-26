-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema inicio_de_sesion_y_registro
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `inicio_de_sesion_y_registro` ;

-- -----------------------------------------------------
-- Schema inicio_de_sesion_y_registro
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `inicio_de_sesion_y_registro` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `inicio_de_sesion_y_registro` ;

-- -----------------------------------------------------
-- Table `inicio_de_sesion_y_registro`.`usuarios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `inicio_de_sesion_y_registro`.`usuarios` ;

CREATE TABLE IF NOT EXISTS `inicio_de_sesion_y_registro`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `apellido` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `fecha_nacimiento` DATE NULL DEFAULT NULL,
  `genero` ENUM('masculino', 'femenino', 'otro') NULL DEFAULT NULL,
  `acepta_terminos` TINYINT(1) NULL DEFAULT '0',
  `fecha_registro` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
