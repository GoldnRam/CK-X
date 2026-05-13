#!/bin/bash

kubectl create namespace shop --dry-run=client -o yaml | kubectl apply -f -
kubectl run frontend --image=nginx -n shop --labels=tier=frontend
kubectl run backend --image=nginx -n shop --labels=tier=backend
