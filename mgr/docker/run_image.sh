#!/bin/bash

function run_lcm {
    docker run -it --name vfc-gvnfm-vnfmgr -p 3306:3306 -p 8403:8403 -e MSB_ADDR=127.0.0.1 nexus3.onap.org:10003/onap/vfc/gvnfm/vnfmgr
}

run_lcm