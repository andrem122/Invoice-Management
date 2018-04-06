-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (3,'2'),(1,'Customers'),(4,'Customers Staff'),(2,'Workers');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `permission_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) DEFAULT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `codename` varchar(100) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,1,'add_current_worker','Can add current_ worker'),(2,1,'change_current_worker','Can change current_ worker'),(3,1,'delete_current_worker','Can delete current_ worker'),(4,2,'add_job','Can add job'),(5,2,'change_job','Can change job'),(6,2,'delete_job','Can delete job'),(7,3,'add_request_payment','Can add request_ payment'),(8,3,'change_request_payment','Can change request_ payment'),(9,3,'delete_request_payment','Can delete request_ payment'),(10,4,'add_house','Can add house'),(11,4,'change_house','Can change house'),(12,4,'delete_house','Can delete house'),(13,5,'add_logentry','Can add log entry'),(14,5,'change_logentry','Can change log entry'),(15,5,'delete_logentry','Can delete log entry'),(16,6,'add_group','Can add group'),(17,6,'change_group','Can change group'),(18,6,'delete_group','Can delete group'),(19,7,'add_permission','Can add permission'),(20,7,'change_permission','Can change permission'),(21,7,'delete_permission','Can delete permission'),(22,8,'add_user','Can add user'),(23,8,'change_user','Can change user'),(24,8,'delete_user','Can delete user'),(25,9,'add_contenttype','Can add content type'),(26,9,'change_contenttype','Can change content type'),(27,9,'delete_contenttype','Can delete content type'),(28,10,'add_session','Can add session'),(29,10,'change_session','Can change session'),(30,10,'delete_session','Can delete session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` text,
  `username` varchar(150) DEFAULT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `is_staff` text,
  `is_active` text,
  `date_joined` datetime DEFAULT NULL,
  `last_name` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$100000$aVC5r6Nt6rW3$7EWevM00/+oezCLdOXSETKX5LykUxPiqjbl8ZmbB0hs=','2018-04-04 00:00:00','1','genuwine12','','andre.mashraghi@gmail.com','1','1','2018-02-27 00:00:00',''),(2,'pbkdf2_sha256$100000$MoYOmwO0HtGL$7rOmmGpgFBSaiBql/TRKeWNnWCbShSposfvjmOqQv18=','2018-04-05 00:00:00','0','am3141','','am3141@live.com','0','1','2018-02-27 00:00:00',''),(6,'pbkdf2_sha256$100000$Vd3J8r9MEef4$3A3NosHm0k2+VM+DZlewkCeGErQtiZ0aZVBJNXayx6M=','2018-03-22 00:00:00','0','samjack','','negar@jazayrigroup.net','0','1','2018-02-27 00:00:00',''),(7,'pbkdf2_sha256$100000$raJgn2kzbWzJ$8VaSrjOX98rcPhuj4zc4l4Jb3mUR01OXn8NPGgkqqTo=','2018-03-07 00:00:00','0','Barttileinstallation','','bartjp80@invoicehome.com','0','1','2018-03-07 00:00:00',''),(8,'pbkdf2_sha256$100000$1lUOpo4oIMUJ$Xum6QPGiqx3AszWyLCdVkjsHMp5LVt3Svb9xPOPxryA=','2018-03-13 00:00:00','0','Clarospaintinginc','','josesito503.jv@gmail.com','0','1','2018-03-13 00:00:00',''),(9,'pbkdf2_sha256$100000$s5Nz8yX9TpPg$bY6w/PnApZkf4/9fPDzcQeaW5rFK+3lTwud19lSWh6E=','2018-03-14 00:00:00','0','ElectricalandLightingDesignLLC','','electricalandlightingdesign@gmail.com','0','1','2018-03-14 00:00:00',''),(10,'pbkdf2_sha256$100000$peWsjrRAredd$1liblAZaqhlsaVaf/kM0y6QbgQFK5ZnngZloiztqL5M=','2018-03-15 00:00:00','0','electricalandlightingdesignllc','','electricalandlightingdesign@gmail.com','0','1','2018-03-14 00:00:00',''),(11,'pbkdf2_sha256$100000$ZTGnU80WpDQV$eY8g8ESLt/vD7lATlj2/zXGXmCW36Um8hdjMp70Q7t0=','2018-04-05 00:00:00','0','Bluehomecarellc','','bluehomecarellc@gmail.com','0','1','2018-03-14 00:00:00',''),(12,'pbkdf2_sha256$100000$RLoaXM5ovoJH$D13YWeYFB/uGzMrBP+KGGUKjD6SPXeKS5pIMnN9/vuM=','2018-03-27 00:00:00','0','JamesLawton','','JAMESBLAWTON2@gmail.com','0','1','2018-03-15 00:00:00',''),(14,'pbkdf2_sha256$100000$UAH9jSnonzGH$lw7r2YeiNauIDf0qxMMJAipTG3C9g8b3t4sbWiNHqy8=','2018-04-04 00:00:00','0','allcompany','','amarchdesin1@gmail.com','0','1','2018-03-15 00:00:00',''),(15,'pbkdf2_sha256$100000$cVDlaTAORYoG$0iiibBGdNgh8rkdnWQBbYAsvMJlOOQ/lIjSJ8le2sNY=','2018-03-15 00:00:00','0','coasttocoastgaragedoor','','Service@c2cgaragedoors.com','0','1','2018-03-15 00:00:00',''),(16,'pbkdf2_sha256$100000$j7zYgneNoKbq$M5ZN4AFIHUDPEmam1JOypi5zRox5+VbuBg7tFAe7RvM=','2018-03-21 00:00:00','0','kingairconditioning','','Kingsair24@gmail.com','0','1','2018-03-21 00:00:00',''),(17,'pbkdf2_sha256$100000$Z4anBRipKXix$NsVd2pgk2WYsYATgLBPyHZ3bEoDZMYAc3R0NQ/TVEoc=','2018-03-26 00:00:00','0','GedeonProfessionalLandscape','','gedeontreetrimming@gmail.com','0','1','2018-03-21 00:00:00',''),(18,'pbkdf2_sha256$100000$EiTQnEhYPUaG$l6qJBNlBzaa4Ga86TLd+4DvuLTB7P6cQh5ePQMR2Hg4=','2018-03-29 00:00:00','0','Kingsair24@gmail.com','','Kingsair24@gmail.com','0','1','2018-03-28 00:00:00',''),(19,'pbkdf2_sha256$100000$OzxGr9JINLL6$7CaxmWWLXqBlWXiBXBC63FuU1bZy2OKZ3mJzSuWVCnI=','2018-03-29 00:00:00','0','Diamondacllc','','firefighterdiamond77@hotmail.com','0','1','2018-03-29 00:00:00',''),(20,'pbkdf2_sha256$100000$KesTGQfPBeRx$2e0nd3tfpbgsp8jA+/mIfK03o624MTXK4xBFzNZrAG0=','2018-03-30 00:00:00','0','DiamondACLLC','','firefighterdiamond77@hotmail.com','0','1','2018-03-29 00:00:00',''),(21,'pbkdf2_sha256$100000$s6tD497hbZfj$EPpRxSRYOTmYGra3Ye0fEfA8m7RV8ujJrns+CabTqXM=','2018-04-04 00:00:00','0','bigbossusa','','bigbossusa@hotmail.com','0','1','2018-04-04 00:00:00','');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,2,1),(8,6,3),(9,6,4),(10,7,2),(11,7,3),(12,8,2),(13,8,3),(14,9,2),(15,9,3),(16,10,2),(17,10,3),(18,11,2),(19,11,3),(20,12,2),(21,12,3),(24,14,2),(25,14,3),(26,15,2),(27,15,3),(28,16,2),(29,16,3),(30,17,2),(31,17,3),(32,18,2),(33,18,3),(34,19,2),(35,19,3),(36,20,2),(37,20,3),(38,21,2),(39,21,3);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `permission_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) DEFAULT NULL,
  `object_id` text,
  `object_repr` varchar(200) DEFAULT NULL,
  `action_flag` text,
  `change_message` text,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'1','Carlos_Painting_Inc-22852 Marbella Cir','2','[{\"changed\": {\"fields\": [\"balance_amount\"]}}]',2,1,'2018-02-27 00:00:00'),(2,'1','Carlos_Painting_Inc-22852 Marbella Cir','2','[{\"changed\": {\"fields\": [\"start_amount\"]}}]',2,1,'2018-02-27 00:00:00'),(3,'4','Carlos_Painting_Inc-3916 NW Deer Oak','3','',1,1,'2018-02-27 00:00:00'),(4,'2','Carlos_Painting_Inc-3916 NW Deer Oak','3','',2,1,'2018-02-27 00:00:00'),(5,'1','Carlos_Painting_Inc-22852 Marbella Cir','3','',2,1,'2018-02-27 00:00:00'),(6,'1','22852 Marbella Cir','2','[{\"changed\": {\"fields\": [\"payment_history\", \"completed_jobs\"]}}]',4,1,'2018-02-27 00:00:00'),(7,'3','Carlos_Painting_Inc','3','',8,1,'2018-02-27 00:00:00'),(8,'4','staff','3','',8,1,'2018-02-27 00:00:00'),(9,'7','Worker3-117 Waterview Way','3','',1,1,'2018-03-07 00:00:00'),(10,'3','Worker3-117 Waterview Way','3','',2,1,'2018-03-07 00:00:00'),(11,'4','Barttileinstallation-11852 61st St N','3','',2,1,'2018-03-14 00:00:00'),(12,'8','Barttileinstallation-11852 61st St N','3','',1,1,'2018-03-14 00:00:00'),(13,'12','16785 Temple Blvd','2','[{\"changed\": {\"fields\": [\"proposed_jobs\"]}}]',4,1,'2018-03-15 00:00:00'),(14,'12','16785 Temple Blvd','2','[{\"changed\": {\"fields\": [\"proposed_jobs\"]}}]',4,1,'2018-03-15 00:00:00'),(15,'11','Worker3-16785 Temple Blvd','3','',2,1,'2018-03-15 00:00:00'),(16,'10','Plana-16785 Temple Blvd','3','',2,1,'2018-03-15 00:00:00'),(17,'8','Plana-16785 Temple Blvd','3','',2,1,'2018-03-15 00:00:00'),(18,'13','Plana','3','',8,1,'2018-03-15 00:00:00'),(19,'5','Worker3','3','',8,1,'2018-03-15 00:00:00'),(20,'14','kingairconditioning-4680 NE Sandpebble Trace','3','',2,1,'2018-03-22 00:00:00'),(21,'7','Clarospaintinginc-250-True','1','[{\"added\": {}}]',3,1,'2018-03-22 00:00:00'),(22,'7','Clarospaintinginc-250.00-True','3','',3,1,'2018-03-22 00:00:00'),(23,'5','Clarospaintinginc-10562 Wheelhouse Circle','2','[{\"changed\": {\"fields\": [\"total_paid\"]}}]',2,1,'2018-03-22 00:00:00'),(24,'5','Clarospaintinginc-10562 Wheelhouse Circle','2','[{\"changed\": {\"fields\": [\"balance_amount\"]}}]',2,1,'2018-03-22 00:00:00'),(25,'8','10562 Wheelhouse Circle','2','[]',4,1,'2018-03-22 00:00:00'),(26,'11','Clarospaintinginc-10562 Wheelhouse Circle','3','',1,1,'2018-03-22 00:00:00'),(27,'12','coasttocoastgaragedoor-5033 Solar Point Drive','2','[{\"changed\": {\"fields\": [\"total_paid\", \"balance_amount\"]}}]',2,1,'2018-03-22 00:00:00'),(28,'15','coasttocoastgaragedoor-5033 Solar Point Drive','3','',1,1,'2018-03-22 00:00:00'),(29,'8','GedeonProfessionalLandscape-1260-False','1','[{\"added\": {}}]',3,1,'2018-03-22 00:00:00'),(30,'9','kingairconditioning-1390-False','1','[{\"added\": {}}]',3,1,'2018-03-22 00:00:00'),(31,'10','GedeonProfessionalLandscape-110-False','1','[{\"added\": {}}]',3,1,'2018-03-22 00:00:00'),(32,'11','GedeonProfessionalLandscape-120-False','1','[{\"added\": {}}]',3,1,'2018-03-22 00:00:00'),(33,'12','allcompany-225-False','1','[{\"added\": {}}]',3,1,'2018-03-22 00:00:00'),(34,'15','JamesLawton-395-False','1','[{\"added\": {}}]',3,1,'2018-03-29 00:00:00'),(35,'16','GedeonProfessionalLandscape-70-False','1','[{\"added\": {}}]',3,1,'2018-03-29 00:00:00'),(36,'17','JamesLawton-200-False','1','[{\"added\": {}}]',3,1,'2018-03-29 00:00:00'),(37,'18','JamesLawton-175-False','1','[{\"added\": {}}]',3,1,'2018-03-29 00:00:00'),(38,'19','GedeonProfessionalLandscape-400-False','1','[{\"added\": {}}]',3,1,'2018-03-29 00:00:00'),(39,'13','allcompany-0.00-True','3','',3,1,'2018-03-29 00:00:00'),(40,'28','GedeonProfessionalLandscape-13377 Doubletree Circle','3','',1,1,'2018-03-29 00:00:00');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) DEFAULT NULL,
  `app_label` varchar(100) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (5,'admin','logentry'),(6,'auth','group'),(7,'auth','permission'),(8,'auth','user'),(9,'contenttypes','contenttype'),(1,'jobs','current_worker'),(4,'jobs','house'),(2,'jobs','job'),(3,'jobs','request_payment'),(10,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) DEFAULT NULL,
  `app` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `applied` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-02-27 00:00:00'),(2,'auth','0001_initial','2018-02-27 00:00:00'),(3,'admin','0001_initial','2018-02-27 00:00:00'),(4,'admin','0002_logentry_remove_auto_add','2018-02-27 00:00:00'),(5,'contenttypes','0002_remove_content_type_name','2018-02-27 00:00:00'),(6,'auth','0002_alter_permission_name_max_length','2018-02-27 00:00:00'),(7,'auth','0003_alter_user_email_max_length','2018-02-27 00:00:00'),(8,'auth','0004_alter_user_username_opts','2018-02-27 00:00:00'),(9,'auth','0005_alter_user_last_login_null','2018-02-27 00:00:00'),(10,'auth','0006_require_contenttypes_0002','2018-02-27 00:00:00'),(11,'auth','0007_alter_validators_add_error_messages','2018-02-27 00:00:00'),(12,'auth','0008_alter_user_username_max_length','2018-02-27 00:00:00'),(13,'auth','0009_alter_user_last_name_max_length','2018-02-27 00:00:00'),(14,'jobs','0001_initial','2018-02-27 00:00:00'),(15,'jobs','0002_auto_20180219_2022','2018-02-27 00:00:00'),(16,'sessions','0001_initial','2018-02-27 00:00:00');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) DEFAULT NULL,
  `session_data` text,
  `expire_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('ucggujlq5c1rdoqom0n6qboad88j1a6m','YWMxNDMyN2YwNTQ2ZDk3OGIyNmM1Y2YwY2U1OGNiYjU0MzQzOWQ5Yjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzQxMzliOTY1YTY4MzI1ODU5MzUzYTNhMjg1MjY2NzAzODhjY2Y0NSIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2018-03-13 00:00:00'),('wikor60y4rmd6joyoxq5wfmwi4oihojv','YWMxNDMyN2YwNTQ2ZDk3OGIyNmM1Y2YwY2U1OGNiYjU0MzQzOWQ5Yjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzQxMzliOTY1YTY4MzI1ODU5MzUzYTNhMjg1MjY2NzAzODhjY2Y0NSIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2018-03-13 00:00:00'),('jp39zpodc32bt06lvfagjd3i7q81d2se','N2NkNzAwMGNmMjJlNjdkNmQ4OWI3OGYzODkwMzNkYWNmZjkxYWQyNjp7Il9hdXRoX3VzZXJfaGFzaCI6IjQwMzc4MDIxZGRkYWViYTc3MjU4OGY1Y2Y2ZDE0MDZlOTNkM2ZlMTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2In0=','2018-03-13 00:00:00'),('3dw33yhlqbz908wpnsuk261q1kkjfqoz','N2NkNzAwMGNmMjJlNjdkNmQ4OWI3OGYzODkwMzNkYWNmZjkxYWQyNjp7Il9hdXRoX3VzZXJfaGFzaCI6IjQwMzc4MDIxZGRkYWViYTc3MjU4OGY1Y2Y2ZDE0MDZlOTNkM2ZlMTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2In0=','2018-03-13 00:00:00'),('o50srslgfgikt8uxv668nslb2qbpng5e','OTVlODlkNGZhYjBlNTBhZmU4Y2NkOWNiYWIzYjkyZDNiYWVmZWY0OTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc0MTM5Yjk2NWE2ODMyNTg1OTM1M2EzYTI4NTI2NjcwMzg4Y2NmNDUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2018-03-13 00:00:00'),('9r5tqk72zeoka88h0syf2a3oconuvie6','OTFhMDJlNWU1OGM3YTE3ZGQ3MmNhOTZjNzkwYjI0NThhOGFkODljYzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjUiLCJfYXV0aF91c2VyX2hhc2giOiI0MDk3NDEzYzM0NWQ1YzAwMGFiZmI2MTIwYTM2NTY5Mzc0Y2EzMzdkIn0=','2018-03-15 00:00:00'),('0yl0owou15icvcr839xdrmnt5jw2fp23','MzU2MDg5YzU1MzA2MTNhNDBmMDgzMTBmNmM0ZDIyZjhiNjhmNTVkZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmNhZmE5MjdiMjc0M2YwNzUxZmNiNTZmMDZiMjg3ZTAzZjgyZTk3In0=','2018-03-21 00:00:00'),('lnuj3k5zlgi12ovzlamrdtc5n2o347ij','MzU2MDg5YzU1MzA2MTNhNDBmMDgzMTBmNmM0ZDIyZjhiNjhmNTVkZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5MmNhZmE5MjdiMjc0M2YwNzUxZmNiNTZmMDZiMjg3ZTAzZjgyZTk3In0=','2018-03-21 00:00:00'),('n0flx6oi19xpdgufzxx3pb4svyt7xo5e','ZDQ0MGM5MTk0YWEzNTM1MmJiYTU2YjBkNmY4YmRiMDkzZmM5NzMzNzp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NzUwNDc2N2Y4OTZjMmM4ZWQ5OGIyMTllMTZlOTZlMWMyZjQ3YTY0In0=','2018-03-21 00:00:00'),('unhjrmg5yq5he4tgxf7zs6xkcgy92w0a','NGNjNTBhZmJmYzExOWZlZmVjMjEyMTE2OWE4NmZhOWE0ZGE1Nzk5Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTJjYWZhOTI3YjI3NDNmMDc1MWZjYjU2ZjA2YjI4N2UwM2Y4MmU5NyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-03-22 00:00:00'),('qipffqgmjnsb1p29pc7pgdexllbdvno3','YWZlZDNlOGJmMGQzMGZjYjFhMzU3NTE1ZDk1MjVkNWM3M2M2OGU5Zjp7Il9hdXRoX3VzZXJfaGFzaCI6IjkyY2FmYTkyN2IyNzQzZjA3NTFmY2I1NmYwNmIyODdlMDNmODJlOTciLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-03-26 00:00:00'),('ehn9z0106zsu0ufrgpi0m538cfkekie5','NjUyNzU3YmM2MzI1MWE3NjU1YTliNDM3M2JjODdiOWRjMWNkMjYwMjp7Il9hdXRoX3VzZXJfaGFzaCI6ImUxZjlmMzAxZGY5MDgxMjlmYzgwNmJiN2FlZGEzMjhjYzIxYWU5ZjIiLCJfYXV0aF91c2VyX2lkIjoiOCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-03-27 00:00:00'),('hytxq7dntp1j6alykzntee6cbdk4irnk','MWYxNGMzNDIwNmJjMjJlZDMxOGQ5ZGJmYTI1ODhkNWM2MTc3MGM0MTp7Il9hdXRoX3VzZXJfaGFzaCI6IjZhOGRmZDA5ZDBhNDAwNzc5ODhiYmMzZGEyMDk3YjEzZGNmN2NkM2MiLCJfYXV0aF91c2VyX2lkIjoiOSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-03-28 00:00:00'),('npn7basmjnyku8hog7pkckl6bft97iqe','ZjdlZDM4ZmI1ZWE4NWJkM2E2N2RiNGQzOGViZGRhY2U1YTg3YTg0Zjp7Il9hdXRoX3VzZXJfaGFzaCI6IjVlNWFjZjExZWEzNjUzNjBkYmNhNzBlYTExYzNlODIyNWM1OTJiMDIiLCJfYXV0aF91c2VyX2lkIjoiMTAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-29 00:00:00'),('ehh8yj0x5rp018ob8gmn0rnaohhdc2t1','ZGFhMTcyNTJmNTRkYWRmOGE1NmFhYWFjZTVlYzhmYzM3MmI1NDYyYzp7Il9hdXRoX3VzZXJfaWQiOiIxMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNjQ2ZTRhNzkzZjJlZTQ3OGIxNDQ5ZGI2YTgyYTE1OTExYzIxMDEwMiJ9','2018-04-19 00:00:00'),('7963xvz55rtzbd4wau83uaq2de9k4xnu','NGVkMWViODA2Yzk1YTViOGJjY2M0ZDFiYTdhN2I1ZmYxZjdhOTUxMjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc0MTM5Yjk2NWE2ODMyNTg1OTM1M2EzYTI4NTI2NjcwMzg4Y2NmNDUiLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-03-28 00:00:00'),('1sfz6vdifelu3e73n3a5baiddz3vc0b6','YWZlZDNlOGJmMGQzMGZjYjFhMzU3NTE1ZDk1MjVkNWM3M2M2OGU5Zjp7Il9hdXRoX3VzZXJfaGFzaCI6IjkyY2FmYTkyN2IyNzQzZjA3NTFmY2I1NmYwNmIyODdlMDNmODJlOTciLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-03-28 00:00:00'),('m95508m55m24claj4qkeezyr37pifwln','YWMxOWQxYzQzYzkzZjUwOTY4YmY0ZTQ5MDUxOWFhMzBiNzNhZThlZjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NDEzOWI5NjVhNjgzMjU4NTkzNTNhM2EyODUyNjY3MDM4OGNjZjQ1In0=','2018-03-31 00:00:00'),('udfz4mo6oafg8710r75mljl9l8x2q600','MmU0MTY2OWM2OTZiMDlmMTE0YmZjMDhlMTM4YmRkMWZkM2U5MjU5Zjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiI5MmNhZmE5MjdiMjc0M2YwNzUxZmNiNTZmMDZiMjg3ZTAzZjgyZTk3In0=','2018-03-28 00:00:00'),('kuygm3f85z934idelcocislpfyj31sqp','OWZjYjg3YzA0NDA5OGYwYWRhYjU3Yjc5ZmI3NTkyODk3NjZjNzUwNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI3NDEzOWI5NjVhNjgzMjU4NTkzNTNhM2EyODUyNjY3MDM4OGNjZjQ1In0=','2018-03-28 00:00:00'),('9yu8c1v7r2z2qpq9t5panjc5yk7xojug','M2UxYTJlZWQ3NTcyODM5Mjg1NmU0OTA5YjBmMzM5MTliMTkzN2JkZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEyIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTg4ZTEwZDUwMTg4ZDFhOTE5NmJjMWRiYTliODk0Yjg0NzViMWU1ZiJ9','2018-03-29 00:00:00'),('ef113vcc0ir7y2buav6wnpek3te1d1yx','N2NkNzAwMGNmMjJlNjdkNmQ4OWI3OGYzODkwMzNkYWNmZjkxYWQyNjp7Il9hdXRoX3VzZXJfaGFzaCI6IjQwMzc4MDIxZGRkYWViYTc3MjU4OGY1Y2Y2ZDE0MDZlOTNkM2ZlMTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2In0=','2018-04-05 00:00:00'),('pwst1j7osxr9jo9lf4pe7dsfenuen7o2','NzdiYzUyODFiZTQwOTNiNDI5YzgxNzdmNTRhNWRlOThhOTA0YmE2NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjE0IiwiX2F1dGhfdXNlcl9oYXNoIjoiMTVmZTAxOGRjYjI4ZDZjZmNlZDFmMmEyM2FiNmUyM2RmZTZkODFkZSJ9','2018-03-29 00:00:00'),('qzub74kyxybgqrgae6sa6g02p00ztb1k','YWMxNDMyN2YwNTQ2ZDk3OGIyNmM1Y2YwY2U1OGNiYjU0MzQzOWQ5Yjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzQxMzliOTY1YTY4MzI1ODU5MzUzYTNhMjg1MjY2NzAzODhjY2Y0NSIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2018-04-05 00:00:00'),('6mrcqe88pxs9m0j676v7s93csud385q6','YzFiOTRhMWQwNGM4NmYyODlhOWZhZmRmZDYwYjQ2ZDQ0MmZjNGYxNzp7Il9hdXRoX3VzZXJfaWQiOiIxNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTZjNzQyM2JlZTE4ZGMwMjk5ZDFjMzAzYTU5MWJmYTNiOWE0YTcyYSJ9','2018-03-29 00:00:00'),('6alwcez95g7osfmtf24vuocojoqmvymf','MTY1ZTQxYTJmZjMxMmUyNWI0Mjk5MjNhYzAyNmFmYzRiNDM5ZDMyNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNGNmNzZhM2FmMGNhZTRiYjVkMmRjZmFhMmMxZjhkNjAwZThlNjI3ZSIsIl9hdXRoX3VzZXJfaWQiOiIxNiJ9','2018-04-04 00:00:00'),('7j6kjohp9hvyipwnlabbxmh23ms9vpa1','OTVlODlkNGZhYjBlNTBhZmU4Y2NkOWNiYWIzYjkyZDNiYWVmZWY0OTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc0MTM5Yjk2NWE2ODMyNTg1OTM1M2EzYTI4NTI2NjcwMzg4Y2NmNDUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2018-04-05 00:00:00'),('f2iirmj8700zwo0vaicqm8jkirpw1ws2','OTVlODlkNGZhYjBlNTBhZmU4Y2NkOWNiYWIzYjkyZDNiYWVmZWY0OTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc0MTM5Yjk2NWE2ODMyNTg1OTM1M2EzYTI4NTI2NjcwMzg4Y2NmNDUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2018-04-09 00:00:00'),('dk1y5so3k2o7ne5b5fcakyah3hhkg50g','OWZjYjg3YzA0NDA5OGYwYWRhYjU3Yjc5ZmI3NTkyODk3NjZjNzUwNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI3NDEzOWI5NjVhNjgzMjU4NTkzNTNhM2EyODUyNjY3MDM4OGNjZjQ1In0=','2018-04-09 00:00:00'),('dluxgwcwx2dboon0k91xvp0s5z7go1rl','OTVlODlkNGZhYjBlNTBhZmU4Y2NkOWNiYWIzYjkyZDNiYWVmZWY0OTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc0MTM5Yjk2NWE2ODMyNTg1OTM1M2EzYTI4NTI2NjcwMzg4Y2NmNDUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2018-04-09 00:00:00'),('k7ul6i11mv7qx6496mo7s0tjhalwyyfn','MjU0Njc0OTk1ODU5MTcwOThhZWViNDg2YThhM2JiOTlhNmRlY2JjYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImE4OGUxMGQ1MDE4OGQxYTkxOTZiYzFkYmE5Yjg5NGI4NDc1YjFlNWYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxMiJ9','2018-04-10 00:00:00'),('jsfiudhazcymow7rs5u7fduur6g9cvxm','OTVlODlkNGZhYjBlNTBhZmU4Y2NkOWNiYWIzYjkyZDNiYWVmZWY0OTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc0MTM5Yjk2NWE2ODMyNTg1OTM1M2EzYTI4NTI2NjcwMzg4Y2NmNDUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2018-04-10 00:00:00'),('qc9q1tofty14637oim9kq83xdbg2rqfs','YzMzZDYxODdjYTJmMGM0Mzk2NTI3ODg4NTRhOTM3MjA0MTVkNGIwMDp7Il9hdXRoX3VzZXJfaGFzaCI6IjQwOTZkODFkNjJkZDEzOTNhZTFiOGYwMjk0ZjYwNmYxZjFjMjlhNDAiLCJfYXV0aF91c2VyX2lkIjoiMTgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-04-11 00:00:00'),('aqzgfd8k9v6iqcm8cbiddjfxdoqdjeyy','NjcxMDg5NTI3NDE5YTQ5YzMwZGQ4NTQ3OThiOThkMmZjOWQ5Y2YzMDp7Il9hdXRoX3VzZXJfaGFzaCI6IjE1ZmUwMThkY2IyOGQ2Y2ZjZWQxZjJhMjNhYjZlMjNkZmU2ZDgxZGUiLCJfYXV0aF91c2VyX2lkIjoiMTQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-04-12 00:00:00'),('k3z3c2qxcbunyagy4gqlkw03cps6r945','YWMxOWQxYzQzYzkzZjUwOTY4YmY0ZTQ5MDUxOWFhMzBiNzNhZThlZjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NDEzOWI5NjVhNjgzMjU4NTkzNTNhM2EyODUyNjY3MDM4OGNjZjQ1In0=','2018-04-19 00:00:00'),('vrpucb6oftmzia5ks6fcyiovdy972rud','OWZjYjg3YzA0NDA5OGYwYWRhYjU3Yjc5ZmI3NTkyODk3NjZjNzUwNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI3NDEzOWI5NjVhNjgzMjU4NTkzNTNhM2EyODUyNjY3MDM4OGNjZjQ1In0=','2018-04-12 00:00:00'),('h4g5xamn1lu6cu98p64x3gsf10amh01c','OTNkMTUyODJhMWQwN2Q3OTVjOGUyNzE4MzA0ODMyMmM3Mjc1NzA2ODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjE4IiwiX2F1dGhfdXNlcl9oYXNoIjoiNDA5NmQ4MWQ2MmRkMTM5M2FlMWI4ZjAyOTRmNjA2ZjFmMWMyOWE0MCJ9','2018-04-12 00:00:00'),('d9mwm4p5l4m3oyvw7vmowelhrljjtzma','OTNkMTUyODJhMWQwN2Q3OTVjOGUyNzE4MzA0ODMyMmM3Mjc1NzA2ODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjE4IiwiX2F1dGhfdXNlcl9oYXNoIjoiNDA5NmQ4MWQ2MmRkMTM5M2FlMWI4ZjAyOTRmNjA2ZjFmMWMyOWE0MCJ9','2018-04-12 00:00:00'),('vccl8uuvtp0ptccknhbfzys7tbcmrnma','OWZjYjg3YzA0NDA5OGYwYWRhYjU3Yjc5ZmI3NTkyODk3NjZjNzUwNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI3NDEzOWI5NjVhNjgzMjU4NTkzNTNhM2EyODUyNjY3MDM4OGNjZjQ1In0=','2018-04-13 00:00:00'),('h3m0kgj71erd496pk195xy7tcn9w6psx','OWZjYjg3YzA0NDA5OGYwYWRhYjU3Yjc5ZmI3NTkyODk3NjZjNzUwNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI3NDEzOWI5NjVhNjgzMjU4NTkzNTNhM2EyODUyNjY3MDM4OGNjZjQ1In0=','2018-04-15 00:00:00'),('67wfxouekyh7d5y4jz9ivzr9kcc07cmx','OTE3MDVjMjkxMGZhYzdkYzk2ZDlmMDA1ZmM3ZmRlMzQ1MTQxZGE1Zjp7Il9hdXRoX3VzZXJfaWQiOiIyMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzQ5MTIxYzZiMDQ3NmFmNGYwYjVjZGNhNmEwZTJmNGVmM2IwODRhOCJ9','2018-04-18 00:00:00'),('x4g3yzi86kzggs2mhmvjdw09o9ubii55','YWMxOWQxYzQzYzkzZjUwOTY4YmY0ZTQ5MDUxOWFhMzBiNzNhZThlZjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NDEzOWI5NjVhNjgzMjU4NTkzNTNhM2EyODUyNjY3MDM4OGNjZjQ1In0=','2018-04-18 00:00:00'),('op1qcrbr9b2mjlqnpu4lfr98k7umyhdc','YWMxOWQxYzQzYzkzZjUwOTY4YmY0ZTQ5MDUxOWFhMzBiNzNhZThlZjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NDEzOWI5NjVhNjgzMjU4NTkzNTNhM2EyODUyNjY3MDM4OGNjZjQ1In0=','2018-04-18 00:00:00');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs_current_worker`
--

DROP TABLE IF EXISTS `jobs_current_worker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs_current_worker` (
  `id` int(11) DEFAULT NULL,
  `current` text,
  `company_id` int(11) DEFAULT NULL,
  `house_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs_current_worker`
--

LOCK TABLES `jobs_current_worker` WRITE;
/*!40000 ALTER TABLE `jobs_current_worker` DISABLE KEYS */;
INSERT INTO `jobs_current_worker` VALUES (12,'1',10,27),(31,'1',18,13);
/*!40000 ALTER TABLE `jobs_current_worker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs_house`
--

DROP TABLE IF EXISTS `jobs_house`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs_house` (
  `id` int(11) DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `proposed_jobs` text,
  `pending_payments` text,
  `payment_history` text,
  `completed_jobs` text,
  `customer_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs_house`
--

LOCK TABLES `jobs_house` WRITE;
/*!40000 ALTER TABLE `jobs_house` DISABLE KEYS */;
INSERT INTO `jobs_house` VALUES (1,'22852 Marbella Cir','0','0','0','0',2),(2,'3916 NW Deer Oak','1','0','1','1',2),(3,'17323 Boca Club','0','0','0','0',2),(4,'5033 Solar Point Drive','0','0','0','1',2),(5,'10861 Southeast Arielle Terrace','0','0','0','0',2),(6,'7360 Via Luria','0','0','0','0',2),(7,'157 Gregory Place','0','0','0','0',2),(8,'10562 Wheelhouse Circle','1','0','1','1',2),(9,'13377 Doubletree Circle','1','0','0','1',2),(10,'522 S Palmway','0','0','0','0',2),(11,'175 Citrus Aveune','1','0','1','1',2),(12,'16785 Temple Blvd','0','0','0','1',2),(13,'1133 Benoist Farms Road','0','0','0','0',2),(14,'4680 NE Sandpebble Trace','1','0','0','1',2),(15,'6915 Aliso Avenue','1','0','1','1',2),(16,'9070 Strandhill Way','0','0','0','0',2),(17,'12880 72nd Ct N','0','0','0','0',2),(18,'10303 Boca Springs Drive','0','0','0','0',2),(19,'4745 Sherwood Forest Drive','1','0','0','0',2),(20,'1432 Cold Springs Ct','1','0','1','1',2),(21,'441 W 35th Street','0','0','0','0',2),(22,'6924 Camille Street','0','0','0','0',2),(23,'10475 Galleria Street','0','0','0','1',2),(24,'11852 61st St N','0','0','0','1',2),(25,'6334 Ungerer Street','0','0','0','0',2),(26,'117 Waterview Way','0','0','0','1',2),(27,'414 Griswold Dr','1','0','1','1',2),(28,'3015 Rockville Ln','0','0','0','1',2);
/*!40000 ALTER TABLE `jobs_house` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs_job`
--

DROP TABLE IF EXISTS `jobs_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs_job` (
  `id` int(11) DEFAULT NULL,
  `start_amount` decimal(10,0) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `total_paid` decimal(10,0) DEFAULT NULL,
  `approved` text,
  `document_link` varchar(100) DEFAULT NULL,
  `balance_amount` decimal(10,0) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `house_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs_job`
--

LOCK TABLES `jobs_job` WRITE;
/*!40000 ALTER TABLE `jobs_job` DISABLE KEYS */;
INSERT INTO `jobs_job` VALUES (5,250,'2018-03-13 00:00:00',250,'1','uploads/10562 Wheelhouse Circle/20180305_171703.jpg',0,8,8),(6,5200,'2018-03-14 00:00:00',2800,'1','uploads/414 Griswold Dr/414_GRISWOLD.pdf',2400,10,27),(7,900,'2018-03-14 00:00:00',900,'1','uploads/10475 Galleria Street/10475_galleria.pdf',0,11,23),(9,1800,'2018-03-15 00:00:00',1800,'1','uploads/16785 Temple Blvd/invoice_house_loxahachee_Jazayri_Const_2_D3N5UXq.doc',0,14,12),(12,1500,'2018-03-15 00:00:00',1500,'1','uploads/5033 Solar Point Drive/Inv_2818_from_Coast_To_Coast_Garage_Door_13572_2.pdf',0,15,4),(13,1390,'2018-03-21 00:00:00',1390,'1','uploads/4680 NE Sandpebble Trace/4680_4680_NE_Sandpebble_Tr_2_T_14_SE_Goodman.pdf',0,16,14),(15,990,'2018-03-21 00:00:00',990,'1','uploads/6915 Aliso Avenue/6915_aliso.pdf',0,11,15),(16,1260,'2018-03-21 00:00:00',1260,'1','uploads/16785 Temple Blvd/invoice53.pdf',0,17,12),(17,110,'2018-03-21 00:00:00',110,'1','uploads/1432 Cold Springs Ct/invoice56.pdf',0,17,20),(18,120,'2018-03-21 00:00:00',120,'1','uploads/11852 61st St N/invoice57.pdf',0,17,24),(19,225,'2018-03-22 00:00:00',225,'1','uploads/3015 Rockville Ln/Samjack_Blackston_LLC20180321_08593803_1288.pdf',0,14,28),(20,400,'2018-03-23 00:00:00',400,'1','uploads/13377 Doubletree Circle/invoice59.pdf',0,17,9),(21,70,'2018-03-26 00:00:00',70,'1','uploads/117 Waterview Way/invoice60.pdf',0,17,26),(22,120,'2018-03-26 00:00:00',0,'0','uploads/13377 Doubletree Circle/invoice61.pdf',120,17,9),(23,200,'2018-03-27 00:00:00',200,'1','uploads/3916 NW Deer Oak/Maintenance_3916_Deer_Oak.pdf',0,12,2),(24,175,'2018-03-27 00:00:00',175,'1','uploads/5033 Solar Point Drive/1522122777806_5033_solar_point.pdf',0,12,4),(25,395,'2018-03-27 00:00:00',395,'1','uploads/5033 Solar Point Drive/Lawn_Maint._3_7_18.pdf',0,12,4),(26,289,'2018-03-28 00:00:00',0,'0','uploads/1133 Benoist Farms Road/1627_1133_Benoist_Farms_103_srvc.pdf',289,18,13),(27,225,'2018-03-29 00:00:00',225,'1','uploads/3015 Rockville Ln/Samjack_Blackston_LLC2.pdf',0,14,28),(28,1770,'2018-03-29 00:00:00',1770,'1','uploads/6915 Aliso Avenue/invoice_1019.pdf',0,11,15),(29,89,'2018-03-29 00:00:00',0,'1','uploads/1133 Benoist Farms Road/1627_1133_Benoist_Farms_103_srvc_22jWvwr.pdf',89,18,13),(30,2498,'2018-03-30 00:00:00',2498,'1','uploads/414 Griswold Dr/414_Griwold.pdf',0,20,27),(31,275,'2018-04-04 00:00:00',275,'1','uploads/1432 Cold Springs Ct/Invoice_-_1432_Cold_Springs_-_Wellington__-__Leak_Detection.pdf',0,21,20),(32,85,'2018-04-04 00:00:00',0,'0','uploads/1432 Cold Springs Ct/Invoice_-_1432_Cold_Springs_-_Wellington__-__pump_leak_union.pdf',85,21,20),(33,85,'2018-04-04 00:00:00',85,'1','uploads/3916 NW Deer Oak/Invoice_-_Monthly_Service_-_3916_Nw_Deer_Oak_-_Jensen_Beach__-__lBTxbG4.pdf',0,21,2),(34,85,'2018-04-04 00:00:00',0,'0','uploads/13377 Doubletree Circle/Invoice_-_Monthly_Service_-_13377_Double_tree_-_Wellingt_4GMGwts.pdf',85,21,9),(35,85,'2018-04-04 00:00:00',85,'1','uploads/175 Citrus Aveune/Invoice_-_Monthly_Service_-_175_Citrus_Ave_-_Boynton_Beach__-__XOeBhaL.pdf',0,21,11),(36,85,'2018-04-04 00:00:00',85,'1','uploads/10562 Wheelhouse Circle/Invoice_-Monthly_Service_-_10562_Whellhouse_-_Boca_Raton_GiUfVA9.pdf',0,21,8),(37,85,'2018-04-04 00:00:00',0,'0','uploads/4745 Sherwood Forest Drive/Invoice_-_Monthly_Service_-_4745_Sherwood_-_Delrey_Be_4ExfwbW.pdf',85,21,19),(38,85,'2018-04-04 00:00:00',85,'1','uploads/1432 Cold Springs Ct/Invoice_-_Monthly_Service_-_1432_Cold_Springs_-_Wellington__su4oTxI.pdf',0,21,20),(39,3195,'2018-04-05 00:00:00',0,'0','uploads/6915 Aliso Avenue/invoice_1022.pdf',3195,11,15),(40,1425,'2018-04-05 00:00:00',0,'0','uploads/6915 Aliso Avenue/invoice_1023.pdf',1425,11,15);
/*!40000 ALTER TABLE `jobs_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs_request_payment`
--

DROP TABLE IF EXISTS `jobs_request_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs_request_payment` (
  `id` int(11) DEFAULT NULL,
  `submit_date` datetime DEFAULT NULL,
  `approved_date` datetime DEFAULT NULL,
  `amount` decimal(10,0) DEFAULT NULL,
  `approved` text,
  `document_link` varchar(100) DEFAULT NULL,
  `house_id` int(11) DEFAULT NULL,
  `job_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs_request_payment`
--

LOCK TABLES `jobs_request_payment` WRITE;
/*!40000 ALTER TABLE `jobs_request_payment` DISABLE KEYS */;
INSERT INTO `jobs_request_payment` VALUES (3,'2018-03-14 00:00:00','2018-03-14 00:00:00',900,'1','',23,7),(4,'2018-03-15 00:00:00','2018-03-15 00:00:00',2800,'1','',27,6),(5,'2018-03-15 00:00:00','2018-03-15 00:00:00',1800,'1','',12,9),(6,'2018-03-22 00:00:00','2018-03-22 00:00:00',990,'1','',15,15),(8,'2018-03-22 00:00:00','2018-03-22 00:00:00',1260,'1','admin_uploads/GedeonProfessionalLandscape-16785 Temple Blvd/Andre_Mashraghi-Resume_FAU.pdf',12,16),(9,'2018-03-22 00:00:00','2018-03-22 00:00:00',1390,'1','admin_uploads/kingairconditioning-4680 NE Sandpebble Trace/Andre_Mashraghi-Resume_FAU.pdf',14,13),(10,'2018-03-22 00:00:00','2018-03-22 00:00:00',110,'1','admin_uploads/GedeonProfessionalLandscape-1432 Cold Springs Ct/Andre_Mashraghi-Resume_FAU.pdf',20,17),(11,'2018-03-22 00:00:00','2018-03-22 00:00:00',120,'1','admin_uploads/GedeonProfessionalLandscape-11852 61st St N/Andre_Mashraghi-Resume_FAU.pdf',24,18),(12,'2018-03-22 00:00:00','2018-03-22 00:00:00',225,'1','admin_uploads/allcompany-3015 Rockville Ln/Andre_Mashraghi-Resume_FAU.pdf',28,19),(14,'2018-03-29 00:00:00','2018-03-29 00:00:00',225,'1','',28,27),(15,'2018-03-29 00:00:00','2018-03-29 00:00:00',395,'1','admin_uploads/JamesLawton-5033 Solar Point Drive/3015_cancellation.pdf',4,25),(16,'2018-03-29 00:00:00','2018-03-29 00:00:00',70,'1','admin_uploads/GedeonProfessionalLandscape-117 Waterview Way/3015_cancellation.pdf',26,21),(17,'2018-03-29 00:00:00','2018-03-29 00:00:00',200,'1','admin_uploads/JamesLawton-3916 NW Deer Oak/3015_cancellation.pdf',2,23),(18,'2018-03-29 00:00:00','2018-03-29 00:00:00',175,'1','admin_uploads/JamesLawton-5033 Solar Point Drive/3015_cancellation_5xdHWJl.pdf',4,24),(19,'2018-03-29 00:00:00','2018-03-29 00:00:00',400,'1','admin_uploads/GedeonProfessionalLandscape-13377 Doubletree Circle/3015_cancellation.pdf',9,20),(20,'2018-03-29 00:00:00','2018-03-29 00:00:00',1770,'1','',15,28),(21,'2018-04-03 00:00:00','2018-04-03 00:00:00',2498,'1','',27,30),(22,'2018-04-05 00:00:00','2018-04-05 00:00:00',85,'1','',2,33),(23,'2018-04-05 00:00:00','2018-04-05 00:00:00',85,'1','',8,36),(24,'2018-04-05 00:00:00','2018-04-05 00:00:00',85,'1','',11,35),(25,'2018-04-05 00:00:00','2018-04-05 00:00:00',85,'1','',20,38),(26,'2018-04-05 00:00:00','2018-04-05 00:00:00',275,'1','',20,31);
/*!40000 ALTER TABLE `jobs_request_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sqlite_sequence`
--

DROP TABLE IF EXISTS `sqlite_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sqlite_sequence` (
  `name` blob,
  `seq` blob
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sqlite_sequence`
--

LOCK TABLES `sqlite_sequence` WRITE;
/*!40000 ALTER TABLE `sqlite_sequence` DISABLE KEYS */;
INSERT INTO `sqlite_sequence` VALUES ('django_migrations','16'),('django_admin_log','40'),('django_content_type','10'),('auth_permission','30'),('auth_user','21'),('jobs_current_worker','31'),('jobs_house','28'),('auth_group','4'),('auth_user_groups','39'),('jobs_job','40'),('jobs_request_payment','26');
/*!40000 ALTER TABLE `sqlite_sequence` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-28 17:07:01
