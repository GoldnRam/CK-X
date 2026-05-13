#!/bin/bash
kubectl get deployment payment-service -o jsonpath='{.spec.template.spec.containers[0].image}' | grep -q 'nginx:1.25'