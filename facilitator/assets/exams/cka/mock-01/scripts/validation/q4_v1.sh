#!/bin/bash
kubectl get pv db-pv -o json | jq '.spec | select(.capacity.storage=="5Gi" and .accessModes[0]=="ReadWriteMany" and .storageClassName=="fast-ssd")' > /dev/null