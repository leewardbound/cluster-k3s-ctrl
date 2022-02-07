#!/usr/bin/env bash
PW=$(kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode)

echo $PW
echo $PW | copy
echo "http://localhost:7070/#/dashboard"

kubectl -n rook-ceph port-forward svc/rook-ceph-mgr-dashboard 7070:7000
