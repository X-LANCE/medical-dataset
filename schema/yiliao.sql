/*
 Navicat Premium Data Transfer

 Source Server         : mysql_localhost
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : yiliao

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 05/08/2022 20:38:06
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for hz_info
-- ----------------------------
DROP TABLE IF EXISTS `hz_info`;
CREATE TABLE `hz_info`  (
  `KH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `KLX` int(11) NOT NULL,
  `YLJGDM` varchar(7) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `RYBH` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`KH`, `KLX`, `YLJGDM`) USING BTREE,
  INDEX `RYBH`(`RYBH`) USING BTREE,
  INDEX `YLJGDM`(`YLJGDM`) USING BTREE,
  INDEX `KH`(`KH`) USING BTREE,
  INDEX `KLX`(`KLX`) USING BTREE,
  CONSTRAINT `hz_info_ibfk_1` FOREIGN KEY (`RYBH`) REFERENCES `person_info` (`RYBH`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for jybgb
-- ----------------------------
DROP TABLE IF EXISTS `jybgb`;
CREATE TABLE `jybgb`  (
  `YLJGDM` varchar(7) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `BGDH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `BGRQ` date NULL DEFAULT NULL,
  `JYLX` int(11) NULL DEFAULT NULL,
  `JZLSH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `JZLX` int(11) NULL DEFAULT NULL,
  `KSBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `KSMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SQRGH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SQRXM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `BGRGH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `BGRXM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SHRGH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SHRXM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SHSJ` datetime NULL DEFAULT NULL,
  `SQKS` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SQKSMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JYKSBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JYKSMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `BGJGDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `BGJGMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SQRQ` date NULL DEFAULT NULL,
  `CJRQ` date NULL DEFAULT NULL,
  `JYRQ` date NULL DEFAULT NULL,
  `BGSJ` datetime NULL DEFAULT NULL,
  `BBDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `BBMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JYBBH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `BBZT` int(11) NULL DEFAULT NULL,
  `BBCJBW` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JSBBSJ` date NULL DEFAULT NULL,
  `JYXMMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JYXMDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JYSQJGMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JYJGMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JSBBRQSJ` datetime NULL DEFAULT NULL,
  `JYJSQM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JYJSGH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`YLJGDM`, `BGDH`) USING BTREE,
  INDEX `JZLSH`(`JZLSH`) USING BTREE,
  INDEX `YLJGDM`(`YLJGDM`) USING BTREE,
  INDEX `BGDH`(`BGDH`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for jyjgzbb
-- ----------------------------
DROP TABLE IF EXISTS `jyjgzbb`;
CREATE TABLE `jyjgzbb`  (
  `JYZBLSH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `YLJGDM` varchar(7) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `BGDH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `BGRQ` date NULL DEFAULT NULL,
  `JYRQ` date NULL DEFAULT NULL,
  `JCRGH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JCRXM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SHRGH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SHRXM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JCXMMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JCZBDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JCFF` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JCZBMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JCZBJGDX` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JCZBJGDL` decimal(11, 2) NULL DEFAULT NULL,
  `JCZBJGDW` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SBBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `YQBH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `YQMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `CKZFWDX` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `CKZFWXX` decimal(11, 2) NULL DEFAULT NULL,
  `CKZFWSX` decimal(11, 2) NULL DEFAULT NULL,
  `JLDW` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`JYZBLSH`, `YLJGDM`) USING BTREE,
  INDEX `YLJGDM`(`YLJGDM`) USING BTREE,
  INDEX `BGDH`(`BGDH`) USING BTREE,
  CONSTRAINT `jyjgzbb_ibfk_1` FOREIGN KEY (`YLJGDM`) REFERENCES `jybgb` (`YLJGDM`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `jyjgzbb_ibfk_2` FOREIGN KEY (`BGDH`) REFERENCES `jybgb` (`BGDH`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mzjzjlb
-- ----------------------------
DROP TABLE IF EXISTS `mzjzjlb`;
CREATE TABLE `mzjzjlb`  (
  `YLJGDM` varchar(7) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `JZLSH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `KH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `KLX` int(11) NULL DEFAULT NULL,
  `MJZH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `HZXM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `NLS` int(11) NULL DEFAULT NULL,
  `NLY` int(11) NULL DEFAULT NULL,
  `ZSEBZ` int(11) NULL DEFAULT NULL,
  `JZZTDM` int(11) NULL DEFAULT NULL,
  `JZZTMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JZJSSJ` datetime NULL DEFAULT NULL,
  `TXBZ` int(11) NULL DEFAULT NULL,
  `ZZBZ` int(11) NULL DEFAULT NULL,
  `WDBZ` int(11) NULL DEFAULT NULL,
  `JZKSBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JZKSMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JZKSRQ` date NULL DEFAULT NULL,
  `ZZYSGH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `QTJZYSGH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JZZDBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JZZDSM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `MZZYZDZZBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `MZZYZDZZMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `SG` decimal(11, 1) NULL DEFAULT NULL,
  `TZ` decimal(11, 1) NULL DEFAULT NULL,
  `TW` decimal(11, 1) NULL DEFAULT NULL,
  `SSY` int(11) NULL DEFAULT NULL,
  `SZY` int(11) NULL DEFAULT NULL,
  `XL` int(11) NULL DEFAULT NULL,
  `HXPLC` int(11) NULL DEFAULT NULL,
  `ML` int(11) NULL DEFAULT NULL,
  `JLSJ` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`YLJGDM`, `JZLSH`) USING BTREE,
  INDEX `KH`(`KH`) USING BTREE,
  INDEX `KLX`(`KLX`) USING BTREE,
  INDEX `YLJGDM`(`YLJGDM`) USING BTREE,
  INDEX `JZLSH`(`JZLSH`) USING BTREE,
  CONSTRAINT `mzjzjlb_ibfk_1` FOREIGN KEY (`YLJGDM`) REFERENCES `hz_info` (`YLJGDM`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mzjzjlb_ibfk_2` FOREIGN KEY (`KH`) REFERENCES `hz_info` (`KH`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mzjzjlb_ibfk_3` FOREIGN KEY (`KLX`) REFERENCES `hz_info` (`KLX`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for person_info
-- ----------------------------
DROP TABLE IF EXISTS `person_info`;
CREATE TABLE `person_info`  (
  `RYBH` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `XBDM` int(11) NULL DEFAULT NULL,
  `XBMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `XM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `CSRQ` date NULL DEFAULT NULL,
  `CSD` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `MZDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `MZMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `GJDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `GJMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JGDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JGMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `XLDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `XLMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `ZYLBDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `ZYMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`RYBH`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for zyjzjlb
-- ----------------------------
DROP TABLE IF EXISTS `zyjzjlb`;
CREATE TABLE `zyjzjlb`  (
  `YLJGDM` varchar(7) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `JZLSH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `MZJZLSH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `KH` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `KLX` int(11) NULL DEFAULT NULL,
  `HZXM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `WDBZ` int(11) NULL DEFAULT NULL,
  `RYDJSJ` datetime NULL DEFAULT NULL,
  `RYTJDM` int(11) NULL DEFAULT NULL,
  `RYTJMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JZKSDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `JZKSMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `RZBQDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `RZBQMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `RYCWH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `CYKSDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `CYKSMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `CYBQDM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `CYBQMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `CYCWH` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `ZYBMLX` int(11) NULL DEFAULT NULL,
  `ZYZDBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `ZYZDMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `ZYZYZDZZBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `ZYZYZDZZMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `MZBMLX` int(11) NULL DEFAULT NULL,
  `MZZDBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `MZZDMC` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `MZZYZDZZBM` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `RYSJ` datetime NULL DEFAULT NULL,
  `CYSJ` datetime NULL DEFAULT NULL,
  `CYZTDM` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`YLJGDM`, `JZLSH`) USING BTREE,
  INDEX `KH`(`KH`) USING BTREE,
  INDEX `KLX`(`KLX`) USING BTREE,
  INDEX `YLJGDM`(`YLJGDM`) USING BTREE,
  INDEX `JZLSH`(`JZLSH`) USING BTREE,
  CONSTRAINT `zyjzjlb_ibfk_1` FOREIGN KEY (`YLJGDM`) REFERENCES `hz_info` (`YLJGDM`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `zyjzjlb_ibfk_2` FOREIGN KEY (`KH`) REFERENCES `hz_info` (`KH`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `zyjzjlb_ibfk_3` FOREIGN KEY (`KLX`) REFERENCES `hz_info` (`KLX`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
