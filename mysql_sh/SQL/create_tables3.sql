CREATE TABLE test3 (
    id  varchar(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    unit int NOT NULL ,
    create_time int NOT NULL DEFAULT '1468339200',
    PRIMARY KEY (`id`,`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE(create_time)  
(  
    PARTITION p20160713 VALUES LESS THAN (1468339200)
);  
