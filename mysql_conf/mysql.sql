BEGIN;
USE `nzbdtdb`;
CREATE TABLE spider (
    id int(4) not null primary key auto_increment,
    title varchar(255) NOT NULL UNIQUE,
    text varchar(5000) ,
    article_time varchar(64) ,
    spider_time varchar(64) ,
    image_1 varchar(256) ,
    image_2 varchar(256) ,
    image_3 varchar(256) ,
    source varchar(32)
)
;
COMMIT;