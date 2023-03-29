#!/usr/bin/bash
cd $(dirname $0)
set -e
RETRIES=20
FN=.dead-pods

for i in $(seq $RETRIES); do
    if [[ ! -f $FN || "" == $(cat $FN) ]] ; then
        echo "Getting pods to kill... (Attempt $i)"
        timeout 60 kubectl get po -A | grep -e "\(Unknown\|Evicted\)" | awk '{print $2 " -n " $1}' > .dead-pods
        sleep 3
    else
        break
    fi
done

echo "Found $(cat .dead-pods | wc -l) pods to kill..."

popline()(LC_CTYPE=C; l=`tail -n "${2:-1}" "$1"; echo t`; l=${l%t}; truncate -s "-${#l}" "$1"; printf %s "$l")


for line in $(cat $FN); do
    DELETE=$(popline $FN)
    timeout 10 kubectl delete pod $DELETE || (echo $DELETE >> $FN && sleep 3)
done
