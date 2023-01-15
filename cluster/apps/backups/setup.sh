#!/usr/bin/env bash
cd $(dirname $0);
set -e
POD=$(kubectl get pod -n backups | grep toolbox-pod | awk '{print $1}')
echo $POD | grep -v "No resources"

bash cp.sh

CMD="kubectl exec pod/$POD -- bash /tools/install.sh"
echo $CMD
$CMD
