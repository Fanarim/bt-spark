-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';



-- -----------------------------------------------------
-- Schema tweet_wishes
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tweet_wishes` DEFAULT CHARACTER SET latin1 ;
USE `tweet_wishes` ;


-- -----------------------------------------------------
-- Table `tweet_wishes`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tweet_wishes`.`users` ;

CREATE TABLE IF NOT EXISTS `tweet_wishes`.`users` (
  `id` BIGINT NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `profile_picture_url` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tweet_wishes`.`tweet_wishes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tweet_wishes`.`tweet_wishes` ;

CREATE TABLE IF NOT EXISTS `tweet_wishes`.`tweet_wishes` (
  `id` BIGINT NOT NULL,
  `author` BIGINT NOT NULL,
  `tweet_text` TEXT NULL DEFAULT NULL,
  `created_at` DATETIME NULL,
  `is_retweet` TINYINT(1) NULL DEFAULT NULL,
  `retweet_tweet_id` BIGINT NULL,
  `sentiment` DOUBLE NULL,
  -- TODO uncomment after constraints are met
  -- INDEX `fk_tweet_wishes_users_idx` (`author` ASC),
  -- INDEX `fk_tweet_wishes_tweet_wishes1_idx` (`retweet_tweet_id` ASC),
  PRIMARY KEY (`id`)
  -- TODO uncomment after constraints are met
  -- CONSTRAINT `fk_author`
  --   FOREIGN KEY (`author`)
  --   REFERENCES `tweet_wishes`.`users` (`id`)
  --   ON DELETE NO ACTION
  --   ON UPDATE NO ACTION,
  -- CONSTRAINT `fk_retweet_of_tweet`
  --   FOREIGN KEY (`retweet_tweet_id`)
  --   REFERENCES `tweet_wishes`.`tweet_wishes` (`id`)
  --   ON DELETE NO ACTION
  --   ON UPDATE NO ACTION
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `tweet_wishes`.`tweet_mentions_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tweet_wishes`.`tweet_mentions_user` ;

CREATE TABLE IF NOT EXISTS `tweet_wishes`.`tweet_mentions_user` (
  `tweet_id` BIGINT NOT NULL,
  `user_id` VARCHAR(255) NOT NULL
  -- TODO uncomment after constraints are met
  -- INDEX `fk_tweet_mentions_user_users1_idx` (`username` ASC),
  -- CONSTRAINT `fk_tweet_mentioning_user`
  --   FOREIGN KEY (`tweet_id`)
  --   REFERENCES `tweet_wishes`.`tweet_wishes` (`id`)
  --   ON DELETE NO ACTION
  --   ON UPDATE NO ACTION,
  -- CONSTRAINT `fk_user_mentioned`
  --   FOREIGN KEY (`user_id`)
  --   REFERENCES `tweet_wishes`.`users` (`id`)
  --   ON DELETE NO ACTION
  --   ON UPDATE NO ACTION
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tweet_wishes`.`hashtags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tweet_wishes`.`hashtags` ;

CREATE TABLE IF NOT EXISTS `tweet_wishes`.`hashtags` (
  `hashtag` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`hashtag`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tweet_wishes`.`tweet_contains_hashtag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tweet_wishes`.`tweet_contains_hashtag` ;

CREATE TABLE IF NOT EXISTS `tweet_wishes`.`tweet_contains_hashtag` (
  `tweet_id` BIGINT NOT NULL,
  `hashtag` VARCHAR(255) NOT NULL
  -- TODO uncomment after constraints are met
  -- INDEX `fk_hashtag_idx` (`hashtag` ASC),
  -- CONSTRAINT `fk_tweet_containining_hash`
  --   FOREIGN KEY (`tweet_id`)
  --   REFERENCES `tweet_wishes`.`tweet_wishes` (`id`)
  --   ON DELETE NO ACTION
  --   ON UPDATE NO ACTION,
  -- CONSTRAINT `fk_hashtag_contained`
  --   FOREIGN KEY (`hashtag`)
  --   REFERENCES `tweet_wishes`.`hashtags` (`hastag`)
  --   ON DELETE NO ACTION
  --   ON UPDATE NO ACTION
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tweet_wishes`.`stats_general_3s`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tweet_wishes`.`stats_general_3s` ;

CREATE TABLE IF NOT EXISTS `tweet_wishes`.`stats_general_3s` (
  `datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tweets_total` BIGINT NULL DEFAULT NULL,
  `tweets_english` BIGINT NULL DEFAULT NULL,
  `wishes_total` BIGINT NULL DEFAULT NULL,
  `sentiment_average` SMALLINT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `tweet_wishes`.`stats_general_10m`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tweet_wishes`.`stats_general_10m` ;

CREATE TABLE IF NOT EXISTS `tweet_wishes`.`stats_general_10m` (
  `datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tweets_total` BIGINT NULL DEFAULT NULL,
  `tweets_english` BIGINT NULL DEFAULT NULL,
  `wishes_total` BIGINT NULL DEFAULT NULL,
  `sentiment_average` SMALLINT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `tweet_wishes`.`stats_general_1d`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tweet_wishes`.`stats_general_1d` ;

CREATE TABLE IF NOT EXISTS `tweet_wishes`.`stats_general_1d` (
  `datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tweets_total` BIGINT NULL DEFAULT NULL,
  `tweets_english` BIGINT NULL DEFAULT NULL,
  `wishes_total` BIGINT NULL DEFAULT NULL,
  `sentiment_average` SMALLINT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;



-- -----------------------------------------------------
-- Events for database 'tweet_wishes'
-- -----------------------------------------------------
/*!50106 SET @save_time_zone= @@TIME_ZONE */ ;
/*!50106 DROP EVENT IF EXISTS `stats_general_10m_clean` */;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8 */ ;;
/*!50003 SET character_set_results = utf8 */ ;;
/*!50003 SET collation_connection  = utf8_general_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'UTC' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`user_rw`@`%`*/ /*!50106 EVENT `stats_general_10m_clean` ON SCHEDULE EVERY 1 DAY STARTS '2016-01-01 00:00:00' ON COMPLETION NOT PRESERVE ENABLE COMMENT 'Clean old data from stats_general_10m' DO delete from stats_general_10m where datetime < timestamp(utc_timestamp() - interval 3 day) */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
/*!50106 DROP EVENT IF EXISTS `stats_general_10m_to_1d` */;;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8 */ ;;
/*!50003 SET character_set_results = utf8 */ ;;
/*!50003 SET collation_connection  = utf8_general_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'UTC' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`user_rw`@`%`*/ /*!50106 EVENT `stats_general_10m_to_1d` ON SCHEDULE EVERY 1 DAY STARTS '2016-01-01 00:02:00' ON COMPLETION NOT PRESERVE ENABLE COMMENT 'Aggregate general stats 10m -> 1d' DO begin insert into stats_general_1d (tweets_total, tweets_english, wishes_total, sentiment_average) select SUM(tweets_total), SUM(tweets_english), SUM(wishes_total), AVG(sentiment_average) from stats_general_10m where datetime > timestamp(utc_timestamp() - interval 1 day); end */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
/*!50106 DROP EVENT IF EXISTS `stats_general_3s_clean` */;;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8 */ ;;
/*!50003 SET character_set_results = utf8 */ ;;
/*!50003 SET collation_connection  = utf8_general_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'UTC' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`user_rw`@`%`*/ /*!50106 EVENT `stats_general_3s_clean` ON SCHEDULE EVERY 10 MINUTE STARTS '2016-01-01 00:00:00' ON COMPLETION NOT PRESERVE ENABLE COMMENT 'Clean old data from stats_general_3s' DO delete from stats_general_3s where datetime < timestamp(utc_timestamp() - interval 1 hour) */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
/*!50106 DROP EVENT IF EXISTS `stats_general_3s_to_10m` */;;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8 */ ;;
/*!50003 SET character_set_results = utf8 */ ;;
/*!50003 SET collation_connection  = utf8_general_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'UTC' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`user_rw`@`%`*/ /*!50106 EVENT `stats_general_3s_to_10m` ON SCHEDULE EVERY 10 MINUTE STARTS '2016-01-01 00:01:00' ON COMPLETION NOT PRESERVE ENABLE COMMENT 'Aggregate general stats 3s -> 10m' DO begin insert into stats_general_10m (tweets_total, tweets_english, wishes_total, sentiment_average) select SUM(tweets_total), SUM(tweets_english), SUM(wishes_total), AVG(sentiment_average) from stats_general_3s where datetime > timestamp(utc_timestamp() - interval 10 minute); end */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
DELIMITER ;
/*!50106 SET TIME_ZONE= @save_time_zone */ ;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
