import json
import os

base_dir = r"d:\Code\CK-X\facilitator\assets\exams\cka\mock-02"
setup_dir = os.path.join(base_dir, "scripts", "setup")
val_dir = os.path.join(base_dir, "scripts", "validation")

os.makedirs(setup_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

questions = []

def add_question(q_id, namespace, hostname, text, concepts, setups, verifications):
    q = {
        "id": str(q_id),
        "namespace": namespace,
        "machineHostname": hostname,
        "question": text,
        "concepts": concepts,
        "verification": []
    }
    
    for i, s_script in enumerate(setups):
        path = os.path.join(setup_dir, f"q{q_id}_s{i+1}_setup.sh")
        with open(path, "w", newline='\n') as f:
            f.write("#!/bin/bash\n" + s_script)
            
    for i, (desc, v_script, weight) in enumerate(verifications):
        v_id = str(i+1)
        v_file = f"q{q_id}_v{v_id}.sh"
        q["verification"].append({
            "id": v_id,
            "description": desc,
            "verificationScriptFile": v_file,
            "expectedOutput": "0",
            "weightage": weight
        })
        path = os.path.join(val_dir, v_file)
        with open(path, "w", newline='\n') as f:
            f.write("#!/bin/bash\n" + v_script)
            
    questions.append(q)

# Q1
add_question(1, "backend", "controlplane", 
"""An application in namespace `backend` needs to call a service in namespace `frontend` via DNS. The service name is `web-ui` and it exposes port 3000.

The application's configuration needs the full DNS name to connect. What is the correct DNS name within the cluster that the backend application should use?

Write the exact DNS name to a file `/tmp/exam/q1_dns_name.txt`.

Also, verify that pod-to-pod DNS resolution works using nslookup or dig from a test pod.
""", 
["dns", "services", "troubleshooting"],
[
"""
kubectl create namespace frontend --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace backend --dry-run=client -o yaml | kubectl apply -f -
kubectl run web-ui -n frontend --image=nginx --port=3000
kubectl expose pod web-ui -n frontend --port=3000
"""
],
[
    ("Correct DNS name in file", "grep -q 'web-ui.frontend.svc.cluster.local' /tmp/exam/q1_dns_name.txt", 5)
])

# Q2
add_question(2, "default", "controlplane",
"""A deployment `payment-service` has been updated with a new image version that introduced a bug. Users are reporting errors. You need to:
1. Check the deployment's rollout history
2. Identify which revision had the issue
3. Rollback to the previous stable version
4. Verify the rollback completed successfully
""",
["deployments", "rollout", "rollback"],
[
"""
kubectl create deployment payment-service --image=nginx:1.24
kubectl set image deployment/payment-service nginx=nginx:1.25 --record
kubectl set image deployment/payment-service nginx=nginx:1.26 --record
"""
],
[
    ("Deployment rolled back to 1.25", "kubectl get deployment payment-service -o jsonpath='{.spec.template.spec.containers[0].image}' | grep -q 'nginx:1.25'", 5)
])

# Q3
add_question(3, "default", "controlplane",
"""A pod needs access to database credentials:
- Username: `dbuser`
- Password: `secret123`
- Database: `appdb`

Create a Secret named `db-creds` and mount it in a deployment named `app-deploy` as environment variables (not as files).

Verify that the pod can access these environment variables without exposing them in pod logs.
""",
["secrets", "pods", "envvars"],
[
"""
kubectl create deployment app-deploy --image=nginx
"""
],
[
    ("Secret exists", "kubectl get secret db-creds", 2),
    ("Deployment mounts secret as env vars", "kubectl get deployment app-deploy -o json | jq '.spec.template.spec.containers[0].envFrom[] | select(.secretRef.name==\"db-creds\")' > /dev/null", 3)
])

# Q4
add_question(4, "default", "controlplane",
"""A monitoring agent needs to run on every node in the cluster, including control plane nodes. Currently, some nodes are missing the agent due to taints.

Create or update a DaemonSet named `monitoring-agent` to:
1. Run the `datadog/agent:latest` image on all nodes
2. Tolerate the taint `node-role.kubernetes.io/control-plane:NoSchedule`
3. Verify the agent is running on all nodes
""",
["daemonsets", "tolerations", "taints"],
[
"""
# Nothing to pre-create
"""
],
[
    ("DaemonSet exists", "kubectl get daemonset monitoring-agent", 2),
    ("DaemonSet has correct toleration", "kubectl get daemonset monitoring-agent -o json | jq '.spec.template.spec.tolerations[] | select(.key==\"node-role.kubernetes.io/control-plane\" and .effect==\"NoSchedule\")' > /dev/null", 3)
])

# Q5
add_question(5, "default", "controlplane",
"""The API server appears to be responding slowly. You need to:
1. Check the API server logs for errors or warnings
2. Verify the API server is listening on port 6443

Write the command you would use to check the API server logs to a file `/tmp/exam/q5_command.txt`.
""",
["troubleshooting", "apiserver"],
[
"""
# Nothing to pre-create
"""
],
[
    ("Correct command in file", "grep -qE 'kubectl logs -n kube-system .*kube-apiserver.*' /tmp/exam/q5_command.txt || grep -q 'journalctl -u kubelet' /tmp/exam/q5_command.txt", 5)
])

# Dump assessment
with open(os.path.join(base_dir, "assessment.json"), "w") as f:
    json.dump({"questions": questions}, f, indent=2)

print("Generated scripts and assessment.json for Mock Exam 02")
