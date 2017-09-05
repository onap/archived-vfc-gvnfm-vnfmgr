#!/bin/bash

cd /service/vfc/gvnfm/vnfmgr/mgr
chmod +x run.sh
./run.sh

while [ ! -f logs/runtime_vnfmgr.log ]; do
    sleep 1
done
tail -F logs/runtime_vnfmgr.log