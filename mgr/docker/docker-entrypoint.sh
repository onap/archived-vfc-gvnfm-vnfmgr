#!/bin/bash

if [ -z "$SERVICE_IP" ]; then
    export SERVICE_IP=`hostname -i`
fi
echo "SERVICE_IP=$SERVICE_IP"

# Configure service based on docker environment variables
python vfc/gvnfm/vnfmgr/mgr/mgr/pub/config/config.py
cat vfc/gvnfm/vnfmgr/mgr/mgr/pub/config/config.py

# microservice-specific one-time initialization
vfc/gvnfm/vnfmgr/mgr/docker/instance_init.sh

date > init.log

# Start the microservice
vfc/gvnfm/vnfmgr/mgr/docker/instance_run.sh