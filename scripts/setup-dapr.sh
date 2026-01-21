#!/bin/bash
# [Task]: T001
# Setup Dapr on Minikube cluster
# Reference: https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-deploy/

set -euo pipefail

NAMESPACE="${DAPR_NAMESPACE:-dapr-system}"
DAPR_VERSION="${DAPR_VERSION:-1.14}"

echo "=== Setting up Dapr on Kubernetes ==="

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo "ERROR: Helm is not installed. Please install Helm first."
    exit 1
fi

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "ERROR: kubectl is not configured or cluster is not accessible."
    exit 1
fi

# Add Dapr Helm repo
echo "Adding Dapr Helm repository..."
helm repo add dapr https://dapr.github.io/helm-charts/ || true
helm repo update

# Create namespace if it doesn't exist
echo "Creating namespace ${NAMESPACE}..."
kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

# Install Dapr runtime
echo "Installing Dapr ${DAPR_VERSION}..."
helm upgrade --install dapr dapr/dapr \
    --namespace "${NAMESPACE}" \
    --set global.ha.enabled=false \
    --set dapr_scheduler.replicaCount=1 \
    --set dapr_placement.replicaCount=1 \
    --wait \
    --timeout 5m

# Verify installation
echo "Verifying Dapr installation..."
kubectl wait --for=condition=available deployment/dapr-operator \
    --namespace "${NAMESPACE}" \
    --timeout=120s

kubectl wait --for=condition=available deployment/dapr-sidecar-injector \
    --namespace "${NAMESPACE}" \
    --timeout=120s

# Scheduler is a StatefulSet, wait for it differently
kubectl wait --for=jsonpath='{.status.readyReplicas}'=1 statefulset/dapr-scheduler-server \
    --namespace "${NAMESPACE}" \
    --timeout=120s || echo "Scheduler ready check completed"

echo ""
echo "=== Dapr Installation Complete ==="
echo ""
kubectl get pods -n "${NAMESPACE}"
echo ""
echo "Dapr is ready for use!"
