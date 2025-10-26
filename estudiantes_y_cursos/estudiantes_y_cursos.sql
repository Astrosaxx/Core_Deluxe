-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema esquema_estudiantes_cursos
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema_estudiantes_cursos` ;

-- -----------------------------------------------------
-- Schema esquema_estudiantes_cursos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema_estudiantes_cursos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `esquema_estudiantes_cursos` ;

-- -----------------------------------------------------
-- Table `esquema_estudiantes_cursos`.`cursos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `esquema_estudiantes_cursos`.`cursos` ;

CREATE TABLE IF NOT EXISTS `esquema_estudiantes_cursos`.`cursos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `esquema_estudiantes_cursos`.`estudiantes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `esquema_estudiantes_cursos`.`estudiantes` ;

CREATE TABLE IF NOT EXISTS `esquema_estudiantes_cursos`.`estudiantes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `edad` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `curso_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `curso_id` (`curso_id` ASC) VISIBLE,
  CONSTRAINT `estudiantes_ibfk_1`
    FOREIGN KEY (`curso_id`)
    REFERENCES `esquema_estudiantes_cursos`.`cursos` (`id`)
    ON DELETE SET NULL)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- Poblar datos de ejemplo para esquema_estudiantes_cursos

START TRANSACTION;

USE `esquema_estudiantes_cursos`;

-- =====================================================
-- CURSOS
-- =====================================================
INSERT INTO `cursos` (`id`, `nombre`)
VALUES
  (1, 'Matemáticas I'),
  (2, 'Lenguaje y Comunicación'),
  (3, 'Ciencias Naturales'),
  (4, 'Historia y Geografía'),
  (5, 'Inglés Intermedio'),
  (6, 'Programación Básica');

ALTER TABLE `cursos` AUTO_INCREMENT = 7;

-- =====================================================
-- ESTUDIANTES
-- =====================================================
INSERT INTO `estudiantes` (`id`, `nombre`, `apellido`, `edad`, `curso_id`)
VALUES
  (1,  'Sofía',   'González', 15, 1),  
  (2,  'Matías',  'Pérez',    16, 2),  
  (3,  'Antonia', 'Muñoz',    14, 3),  
  (4,  'Benjamín','Rojas',    17, 4), 
  (5,  'Isidora', 'Contreras',16, 5),
  (6,  'Diego',   'Castro',   15, 6),  
  (7,  'Camila',  'Hernández',14, 1),  
  (8,  'Joaquín', 'Vargas',   18, 2), 
  (9,  'Valentina','Morales', 17, NULL),
  (10, 'Lucas',   'Fuentes',  16, 6),  
  (11, 'Martina', 'Rivera',   15, 5), 
  (12, 'Tomás',   'Silva',    14, NULL); 

ALTER TABLE `estudiantes` AUTO_INCREMENT = 13;

COMMIT;
