#!/usr/bin/env bash
cd $(dirname $0);
set -e
POD=$(kubectl get pod -n backups | grep toolbox-pod | awk '{print $1}')
echo $POD | grep -v "No resources"

CMD="kubectl cp -n backups ./tools $POD:/"
echo $CMD
$CMD
