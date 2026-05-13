#!/bin/bash

kubectl create deployment payment-service --image=nginx:1.24
kubectl set image deployment/payment-service nginx=nginx:1.25 --record
kubectl set image deployment/payment-service nginx=nginx:1.26 --record
