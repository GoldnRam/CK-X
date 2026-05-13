#!/bin/bash
kubectl auth can-i list pods -n staging --as dev-user | grep -q 'yes'