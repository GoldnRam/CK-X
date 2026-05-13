#!/bin/bash
kubectl get rolebinding dev-binding -n staging -o json | jq '.subjects[] | select(.name=="dev-user" and .kind=="User")' > /dev/null