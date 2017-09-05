/******************drop old database and user***************************/
use mysql;
drop database IF  EXISTS gvnfm;
delete from user where User='gvnfm';
FLUSH PRIVILEGES;

/******************create new database and user***************************/
create database gvnfm CHARACTER SET utf8;

GRANT ALL PRIVILEGES ON gvnfm.* TO 'gvnfm'@'%' IDENTIFIED BY 'gvnfm' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON mysql.* TO 'gvnfm'@'%' IDENTIFIED BY 'gvnfm' WITH GRANT OPTION;

GRANT ALL PRIVILEGES ON gvnfm.* TO 'gvnfm'@'localhost' IDENTIFIED BY 'gvnfm' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON mysql.* TO 'gvnfm'@'localhost' IDENTIFIED BY 'gvnfm' WITH GRANT OPTION;
FLUSH PRIVILEGES;