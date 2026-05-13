#!/bin/bash
kubectl get role dev-role -n staging -o json | jq '.rules[] | select(.resources[] | contains("pods")) | select(.verbs[] | contains("list"))' > /dev/null