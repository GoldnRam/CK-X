#!/bin/bash
kubectl get pod app-frontend -n production -o jsonpath='{.status.phase}' | grep -q 'Running'