SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema spstest
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `spstest` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `spstest` ;

-- -----------------------------------------------------
-- Table `spstest`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`user` ;

CREATE TABLE IF NOT EXISTS `spstest`.`user` (
  `userid` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `username` VARCHAR(20) NOT NULL,
  `firstname` VARCHAR(45) NULL,
  `lastname` VARCHAR(45) NULL,
  `password` VARCHAR(100) NOT NULL,
  `salt` VARCHAR(100) NOT NULL,
  `datecreated` DATETIME NOT NULL,
  `dateinactive` DATETIME NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`userid`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`usertoken`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`usertoken` ;

CREATE TABLE IF NOT EXISTS `spstest`.`usertoken` (
  `userid` INT NOT NULL,
  `usertoken` VARCHAR(100) NOT NULL,
  `datecreated` DATETIME NOT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`userid`),
  INDEX `fk_usertoken_user_idx` (`userid` ASC),
  UNIQUE INDEX `usertoken_UNIQUE` (`usertoken` ASC),
  CONSTRAINT `fk_usertoken_user`
    FOREIGN KEY (`userid`)
    REFERENCES `spstest`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`sessionstatustyp`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`sessionstatustyp` ;

CREATE TABLE IF NOT EXISTS `spstest`.`sessionstatustyp` (
  `sessionstatustypcd` VARCHAR(5) NOT NULL,
  `seqno` SMALLINT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `displayname` VARCHAR(45) NOT NULL,
  `description` VARCHAR(100) NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sessionstatustypcd`),
  UNIQUE INDEX `seqno_UNIQUE` (`seqno` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`session`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`session` ;

CREATE TABLE IF NOT EXISTS `spstest`.`session` (
  `sessionid` BIGINT NOT NULL AUTO_INCREMENT,
  `sessionstatustypcd` VARCHAR(5) NOT NULL,
  `sessionjoincd` VARCHAR(10) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `theme` VARCHAR(45) NULL,
  `datecreated` DATETIME NOT NULL,
  `location` VARCHAR(100) NULL,
  `dateopen` DATETIME NULL,
  `dateclosed` DATETIME NULL,
  `datedeleted` DATETIME NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sessionid`),
  INDEX `fk_session_sessionstatustyp1_idx` (`sessionstatustypcd` ASC),
  CONSTRAINT `fk_session_sessionstatustyp1`
    FOREIGN KEY (`sessionstatustypcd`)
    REFERENCES `spstest`.`sessionstatustyp` (`sessionstatustypcd`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`userroletyp`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`userroletyp` ;

CREATE TABLE IF NOT EXISTS `spstest`.`userroletyp` (
  `userroletypcd` VARCHAR(5) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `displayname` VARCHAR(45) NOT NULL,
  `description` VARCHAR(100) NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`userroletypcd`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`session_has_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`session_has_user` ;

CREATE TABLE IF NOT EXISTS `spstest`.`session_has_user` (
  `sessionid` BIGINT NOT NULL,
  `userid` INT NOT NULL,
  `userroletypcd` VARCHAR(5) NOT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sessionid`, `userid`),
  INDEX `fk_session_has_user_user1_idx` (`userid` ASC),
  INDEX `fk_session_has_user_session1_idx` (`sessionid` ASC),
  INDEX `fk_session_has_user_userroletyp1_idx` (`userroletypcd` ASC),
  CONSTRAINT `fk_session_has_user_session1`
    FOREIGN KEY (`sessionid`)
    REFERENCES `spstest`.`session` (`sessionid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_has_user_user1`
    FOREIGN KEY (`userid`)
    REFERENCES `spstest`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_has_user_userroletyp1`
    FOREIGN KEY (`userroletypcd`)
    REFERENCES `spstest`.`userroletyp` (`userroletypcd`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`ratingval`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`ratingval` ;

CREATE TABLE IF NOT EXISTS `spstest`.`ratingval` (
  `ratingval` SMALLINT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `displayname` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ratingval`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`beer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`beer` ;

CREATE TABLE IF NOT EXISTS `spstest`.`beer` (
  `beerid` VARCHAR(100) NOT NULL,
  `rawdata` VARCHAR(10000) NULL,
  `datecreated` DATETIME NOT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`beerid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`beersrctyp`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`beersrctyp` ;

CREATE TABLE IF NOT EXISTS `spstest`.`beersrctyp` (
  `beersrctypcd` VARCHAR(5) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `host` VARCHAR(100) NOT NULL,
  `port` INT NOT NULL,
  `urlpath` VARCHAR(200) NOT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`beersrctypcd`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`app`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`app` ;

CREATE TABLE IF NOT EXISTS `spstest`.`app` (
  `appid` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `datecreated` DATETIME NOT NULL,
  `active` CHAR NOT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`appid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`appsettings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`appsettings` ;

CREATE TABLE IF NOT EXISTS `spstest`.`appsettings` (
  `appsettingsid` INT NOT NULL AUTO_INCREMENT,
  `appid` INT NOT NULL,
  `appkey` VARCHAR(50) NOT NULL,
  `appval` VARCHAR(250) NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `appsettingscol` VARCHAR(45) NULL,
  INDEX `fk_appsettings_app1_idx` (`appid` ASC),
  PRIMARY KEY (`appsettingsid`),
  CONSTRAINT `fk_appsettings_app1`
    FOREIGN KEY (`appid`)
    REFERENCES `spstest`.`app` (`appid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`apptoken`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`apptoken` ;

CREATE TABLE IF NOT EXISTS `spstest`.`apptoken` (
  `appid` INT NOT NULL,
  `apptoken` VARCHAR(100) NOT NULL,
  `datecreated` DATETIME NOT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`appid`),
  UNIQUE INDEX `apptoken_UNIQUE` (`apptoken` ASC),
  CONSTRAINT `fk_apptoken_app1`
    FOREIGN KEY (`appid`)
    REFERENCES `spstest`.`app` (`appid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`ratingtyp`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`ratingtyp` ;

CREATE TABLE IF NOT EXISTS `spstest`.`ratingtyp` (
  `ratingtypcd` VARCHAR(5) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `displayname` VARCHAR(45) NOT NULL,
  `description` VARCHAR(100) NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ratingtypcd`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`beersessionstatustyp`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`beersessionstatustyp` ;

CREATE TABLE IF NOT EXISTS `spstest`.`beersessionstatustyp` (
  `beersessionstatustypcd` VARCHAR(5) NOT NULL,
  `seqno` SMALLINT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `displayname` VARCHAR(45) NOT NULL,
  `description` VARCHAR(100) NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`beersessionstatustypcd`),
  UNIQUE INDEX `seqno_UNIQUE` (`seqno` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`session_has_beer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`session_has_beer` ;

CREATE TABLE IF NOT EXISTS `spstest`.`session_has_beer` (
  `sessionbeerid` BIGINT NOT NULL AUTO_INCREMENT,
  `sessionid` BIGINT NOT NULL,
  `beerid` VARCHAR(100) NOT NULL,
  `beersessionstatustypcd` VARCHAR(5) NOT NULL,
  `seqno` SMALLINT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sessionbeerid`, `sessionid`, `beerid`),
  INDEX `fk_session_has_beer_beer1_idx` (`beerid` ASC),
  INDEX `fk_session_has_beer_session1_idx` (`sessionid` ASC),
  INDEX `fk_session_has_beer_beersessionstatustyp1_idx` (`beersessionstatustypcd` ASC),
  CONSTRAINT `fk_session_has_beer_session1`
    FOREIGN KEY (`sessionid`)
    REFERENCES `spstest`.`session` (`sessionid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_has_beer_beer1`
    FOREIGN KEY (`beerid`)
    REFERENCES `spstest`.`beer` (`beerid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_has_beer_beersessionstatustyp1`
    FOREIGN KEY (`beersessionstatustypcd`)
    REFERENCES `spstest`.`beersessionstatustyp` (`beersessionstatustypcd`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`beerrating`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`beerrating` ;

CREATE TABLE IF NOT EXISTS `spstest`.`beerrating` (
  `beerratingid` INT NOT NULL AUTO_INCREMENT,
  `sessionbeerid` BIGINT NOT NULL,
  `ratingtypcd` VARCHAR(5) NOT NULL,
  `ratingval` SMALLINT NOT NULL,
  `userid` INT NOT NULL,
  `comment` VARCHAR(500) NULL,
  `daterated` DATETIME NOT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`beerratingid`, `sessionbeerid`),
  INDEX `fk_beerrating_ratingtyp1_idx` (`ratingtypcd` ASC),
  INDEX `fk_beerrating_ratingval1_idx` (`ratingval` ASC),
  INDEX `fk_beerrating_user1_idx` (`userid` ASC),
  INDEX `fk_beerrating_session_has_beer1_idx` (`sessionbeerid` ASC),
  CONSTRAINT `fk_beerrating_ratingtyp1`
    FOREIGN KEY (`ratingtypcd`)
    REFERENCES `spstest`.`ratingtyp` (`ratingtypcd`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_beerrating_ratingval1`
    FOREIGN KEY (`ratingval`)
    REFERENCES `spstest`.`ratingval` (`ratingval`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_beerrating_user1`
    FOREIGN KEY (`userid`)
    REFERENCES `spstest`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_beerrating_session_has_beer1`
    FOREIGN KEY (`sessionbeerid`)
    REFERENCES `spstest`.`session_has_beer` (`sessionbeerid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`blacklistedword`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`blacklistedword` ;

CREATE TABLE IF NOT EXISTS `spstest`.`blacklistedword` (
  `word` VARCHAR(100) NOT NULL,
  `altword` VARCHAR(100) NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`word`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`avatar`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`avatar` ;

CREATE TABLE IF NOT EXISTS `spstest`.`avatar` (
  `avatarid` INT NOT NULL,
  PRIMARY KEY (`avatarid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`brewery`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`brewery` ;

CREATE TABLE IF NOT EXISTS `spstest`.`brewery` (
  `breweryid` VARCHAR(100) NOT NULL,
  `rawdata` VARCHAR(10000) NULL,
  `datecreated` DATETIME NOT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`breweryid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spstest`.`brewery_has_beer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spstest`.`brewery_has_beer` ;

CREATE TABLE IF NOT EXISTS `spstest`.`brewery_has_beer` (
  `breweryid` VARCHAR(100) NOT NULL,
  `beerid` VARCHAR(100) NOT NULL,
  `datelastmaint` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`breweryid`, `beerid`),
  INDEX `fk_brewery_has_beer_beer1_idx` (`beerid` ASC),
  INDEX `fk_brewery_has_beer_brewery1_idx` (`breweryid` ASC),
  CONSTRAINT `fk_brewery_has_beer_brewery1`
    FOREIGN KEY (`breweryid`)
    REFERENCES `spstest`.`brewery` (`breweryid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_brewery_has_beer_beer1`
    FOREIGN KEY (`beerid`)
    REFERENCES `spstest`.`beer` (`beerid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
