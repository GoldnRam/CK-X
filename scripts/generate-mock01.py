import json
import os

base_dir = r"d:\Code\CK-X\facilitator\assets\exams\cka\mock-01"
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
add_question(1, "production", "controlplane", 
"""A pod named `app-frontend` in namespace `production` is stuck in `CrashLoopBackOff`. The pod's container is looking for a configuration file at `/etc/app/config.yaml`, but this file doesn't exist in the image.

You need to:
1. Create a ConfigMap named `app-config` with the file content: `database_host: postgres.production.svc.cluster.local`
2. Mount this ConfigMap as a file at `/etc/app/config.yaml` in the pod
3. Verify the pod starts successfully

The pod manifest already exists; you only need to update it.
""", 
["pods", "configmaps", "troubleshooting"],
[
"""
kubectl create namespace production --dry-run=client -o yaml | kubectl apply -f -
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: app-frontend
  namespace: production
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "if [ ! -f /etc/app/config.yaml ]; then exit 1; else sleep 3600; fi"]
EOF
"""
],
[
    ("ConfigMap exists", "kubectl get configmap app-config -n production", 2),
    ("ConfigMap has correct content", 'kubectl get configmap app-config -n production -o jsonpath="{.data[\'config\\.yaml\']}" | grep -q "database_host: postgres.production.svc.cluster.local"', 2),
    ("Pod is running", "kubectl get pod app-frontend -n production -o jsonpath='{.status.phase}' | grep -q 'Running'", 3)
])

# Q2
add_question(2, "staging", "controlplane",
"""A developer needs to be able to list Deployments and Pods in the `staging` namespace, but not in other namespaces. Currently, they cannot perform these actions.

Create:
1. A Role that allows listing Pods and Deployments in `staging` named `dev-role`
2. A RoleBinding that grants this Role to the user `dev-user` named `dev-binding`

Verify the permissions work using `kubectl auth can-i`.
""",
["rbac", "security"],
[
"""
kubectl create namespace staging --dry-run=client -o yaml | kubectl apply -f -
"""
],
[
    ("Role exists with correct permissions", "kubectl get role dev-role -n staging -o json | jq '.rules[] | select(.resources[] | contains(\"pods\")) | select(.verbs[] | contains(\"list\"))' > /dev/null", 3),
    ("RoleBinding exists and binds user", "kubectl get rolebinding dev-binding -n staging -o json | jq '.subjects[] | select(.name==\"dev-user\" and .kind==\"User\")' > /dev/null", 2),
    ("User can list pods in staging", "kubectl auth can-i list pods -n staging --as dev-user | grep -q 'yes'", 2)
])

# Q3
add_question(3, "default", "controlplane",
"""Node `worker-1` needs maintenance and will be offline for 1 hour.

1. Prepare the node for maintenance without losing pod data
2. Verify the node is ready for maintenance
""",
["nodes", "maintenance"],
[
"""
kubectl uncordon worker-1 || true
"""
],
[
    ("Node worker-1 is unschedulable", "kubectl get node worker-1 -o jsonpath='{.spec.unschedulable}' | grep -q 'true'", 5)
])

# Q4
add_question(4, "databases", "controlplane",
"""An application needs persistent storage that:
1. Size: 5Gi
2. Access mode: can be used by multiple pods simultaneously (ReadWriteMany)
3. Storage class: `fast-ssd`
4. Name of PVC: `db-pvc`

Create the PV named `db-pv` (hostPath `/data`) and the PVC `db-pvc` in the `databases` namespace.
""",
["storage", "pv", "pvc"],
[
"""
kubectl create namespace databases --dry-run=client -o yaml | kubectl apply -f -
"""
],
[
    ("PV exists with correct specs", "kubectl get pv db-pv -o json | jq '.spec | select(.capacity.storage==\"5Gi\" and .accessModes[0]==\"ReadWriteMany\" and .storageClassName==\"fast-ssd\")' > /dev/null", 3),
    ("PVC exists and is bound", "kubectl get pvc db-pvc -n databases -o jsonpath='{.status.phase}' | grep -q 'Bound'", 3)
])

# Q5
add_question(5, "shop", "controlplane",
"""Currently, all pods in namespace `shop` can communicate with each other. You need to implement network isolation using a NetworkPolicy named `backend-policy`:
1. Backend pods (label: `tier=backend`) can receive traffic from frontend pods (label: `tier=frontend`) on port 3000 only.
""",
["networking", "networkpolicy"],
[
"""
kubectl create namespace shop --dry-run=client -o yaml | kubectl apply -f -
kubectl run frontend --image=nginx -n shop --labels=tier=frontend
kubectl run backend --image=nginx -n shop --labels=tier=backend
"""
],
[
    ("NetworkPolicy exists", "kubectl get networkpolicy backend-policy -n shop", 2),
    ("Policy allows traffic from frontend on port 3000", "kubectl get networkpolicy backend-policy -n shop -o yaml | grep -q 'tier: frontend'", 3)
])

# Dump assessment
with open(os.path.join(base_dir, "assessment.json"), "w") as f:
    json.dump({"questions": questions}, f, indent=2)

print("Generated scripts and assessment.json")
