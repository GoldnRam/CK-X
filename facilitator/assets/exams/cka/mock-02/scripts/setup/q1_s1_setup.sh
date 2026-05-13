#!/bin/bash

kubectl create namespace frontend --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace backend --dry-run=client -o yaml | kubectl apply -f -
kubectl run web-ui -n frontend --image=nginx --port=3000
kubectl expose pod web-ui -n frontend --port=3000
