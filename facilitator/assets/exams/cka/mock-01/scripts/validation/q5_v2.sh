#!/bin/bash
kubectl get networkpolicy backend-policy -n shop -o yaml | grep -q 'tier: frontend'