/* --------- user：spider1 ------ */
/* --------- db：parser_component ------ */
/*创建一个表，IP_availability，用于存储生成的假UA（用户代理）*/

USE parser_component;
DROP TABLE IF EXISTS `IP_availability`;
CREATE TABLE IF NOT EXISTS `IP_availability`(
    `id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`ip_address` VARCHAR(21) NOT NULL COMMENT 'ip的地址+端口号，最长可达21位，作为主键可确保数据库中的ip地址不会重复',
	`is_http` TINYINT DEFAULT NULL COMMENT '是否为HTTP协议，是为1，否为0',
	`is_https` TINYINT DEFAULT NULL COMMENT '是否为HTTPS协议，是为1，否为0',
	`update_time` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	PRIMARY KEY ( `id` ),
	UNIQUE KEY `uniqueIPAndPort` (`ip_address` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '记录可用的IP';


/* --------- user：spider1 ------ */
/* --------- db：parser_component ------ */
/*创建一个表，fake_user_agent，用于存储生成的假UA（用户代理）*/

USE parser_component;
CREATE TABLE IF NOT EXISTS `fake_user_agent`(
	`id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`ua` VARCHAR(1000) NOT NULL COMMENT '用户代理',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '生成的假UA（用户代理）';