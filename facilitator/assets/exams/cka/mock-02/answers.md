# Mock Exam 02 Solutions

## Question 1: Service Discovery and DNS

```bash
mkdir -p /tmp/exam
echo "web-ui.frontend.svc.cluster.local" > /tmp/exam/q1_dns_name.txt
```

## Question 2: Deployment Rolling Update and Rollback

```bash
kubectl rollout history deployment/payment-service
kubectl rollout undo deployment/payment-service --to-revision=2
```

## Question 3: Secrets and Environment Variables

```bash
kubectl create secret generic db-creds \
  --from-literal=username=dbuser \
  --from-literal=password=secret123 \
  --from-literal=database=appdb

kubectl set env --from=secret/db-creds deployment/app-deploy
```

## Question 4: DaemonSet Configuration

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: monitoring-agent
spec:
  selector:
    matchLabels:
      app: monitoring-agent
  template:
    metadata:
      labels:
        app: monitoring-agent
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule
      containers:
      - name: agent
        image: datadog/agent:latest
```

## Question 5: Cluster API Server Debugging

```bash
mkdir -p /tmp/exam
echo "kubectl logs -n kube-system -l component=kube-apiserver" > /tmp/exam/q5_command.txt
```
