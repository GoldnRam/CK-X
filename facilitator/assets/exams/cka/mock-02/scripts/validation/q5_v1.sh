#!/bin/bash
grep -qE 'kubectl logs -n kube-system .*kube-apiserver.*' /tmp/exam/q5_command.txt || grep -q 'journalctl -u kubelet' /tmp/exam/q5_command.txt