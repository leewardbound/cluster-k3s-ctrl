#!/usr/bin/env bash
kubectl get secret $(kubectl get serviceaccount k10-k10 -o jsonpath="{.secrets[0].name}" --namespace kasten-io) --namespace kasten-io -ojsonpath="{.data.token}{'\n'}" | base64 --decode | copy
