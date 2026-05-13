#!/bin/bash
kubectl get configmap app-config -n production -o jsonpath="{.data['config\.yaml']}" | grep -q "database_host: postgres.production.svc.cluster.local"