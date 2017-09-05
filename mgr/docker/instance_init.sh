#!/bin/bash

function start_redis_server {
    redis-server &
}

function start_mysql {
    service mysql start
    sleep 1
}

function create_database {

    # TODO(sshank): Can't find .sql in repo. Hence following was added.
    cd /service/vfc/gvnfm/vnfmgr/mgr
    mysql -uroot -proot -e "CREATE USER 'gvnfm'@'localhost' IDENTIFIED BY 'gvnfm';"
    mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON * . * TO 'gvnfm'@'localhost';"
    mysql -uroot -proot -e "FLUSH PRIVILEGES;"
    mysql -ugvnfm -pgvnfm -e "CREATE DATABASE gvnfm;"
    python manage.py migrate

    # cd /service/vfc/gvnfm/vnfmgr/mgr/resources/bin
    # bash initDB.sh root $MYSQL_ROOT_PASSWORD 3306 127.0.0.1
    cd /service
}

start_redis_server
start_mysql
create_database