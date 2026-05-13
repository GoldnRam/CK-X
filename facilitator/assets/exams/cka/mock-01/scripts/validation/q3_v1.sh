#!/bin/bash
kubectl get node worker-1 -o jsonpath='{.spec.unschedulable}' | grep -q 'true'