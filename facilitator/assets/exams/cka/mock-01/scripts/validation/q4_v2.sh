#!/bin/bash
kubectl get pvc db-pvc -n databases -o jsonpath='{.status.phase}' | grep -q 'Bound'