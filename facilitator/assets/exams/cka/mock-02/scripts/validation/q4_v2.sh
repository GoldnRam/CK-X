#!/bin/bash
kubectl get daemonset monitoring-agent -o json | jq '.spec.template.spec.tolerations[] | select(.key=="node-role.kubernetes.io/control-plane" and .effect=="NoSchedule")' > /dev/null