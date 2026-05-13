#!/bin/bash

kubectl create namespace production --dry-run=client -o yaml | kubectl apply -f -
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: app-frontend
  namespace: production
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "if [ ! -f /etc/app/config.yaml ]; then exit 1; else sleep 3600; fi"]
EOF
