#!/bin/bash
kubectl get deployment app-deploy -o json | jq '.spec.template.spec.containers[0].envFrom[] | select(.secretRef.name=="db-creds")' > /dev/null