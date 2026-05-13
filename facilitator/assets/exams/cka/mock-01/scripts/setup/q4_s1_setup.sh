#!/bin/bash

kubectl create namespace databases --dry-run=client -o yaml | kubectl apply -f -
