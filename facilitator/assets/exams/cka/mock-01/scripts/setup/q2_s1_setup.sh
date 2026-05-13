#!/bin/bash

kubectl create namespace staging --dry-run=client -o yaml | kubectl apply -f -
