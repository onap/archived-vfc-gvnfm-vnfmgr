#!/bin/bash

function start_redis_server {
    redis-server &
}

function start_mysql {
    service mysql start
    sleep 1
}

function create_database {
    cd /service/vfc/gvnfm/vnfmgr/mgr/docker
    mysql -uroot -proot < createdb.sql
    mysql -uroot -proot < createobj.sql
    cd /service
}

start_redis_server
start_mysql
create_database