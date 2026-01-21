#!/bin/bash
# [Task]: T002
# Setup Strimzi Kafka Operator on Minikube
# Reference: https://strimzi.io/quickstarts/

set -euo pipefail

NAMESPACE="${KAFKA_NAMESPACE:-kafka}"
STRIMZI_VERSION="${STRIMZI_VERSION:-latest}"

echo "=== Setting up Strimzi Kafka Operator ==="

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "ERROR: kubectl is not configured or cluster is not accessible."
    exit 1
fi

# Create Kafka namespace
echo "Creating namespace ${NAMESPACE}..."
kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

# Install Strimzi Operator
echo "Installing Strimzi Operator..."
kubectl create -f "https://strimzi.io/install/${STRIMZI_VERSION}?namespace=${NAMESPACE}" -n "${NAMESPACE}" || \
kubectl apply -f "https://strimzi.io/install/${STRIMZI_VERSION}?namespace=${NAMESPACE}" -n "${NAMESPACE}"

# Wait for operator to be ready
echo "Waiting for Strimzi operator to be ready..."
kubectl wait deployment/strimzi-cluster-operator \
    --for=condition=available \
    --timeout=300s \
    -n "${NAMESPACE}"

echo ""
echo "=== Strimzi Operator Installation Complete ==="
echo ""
kubectl get pods -n "${NAMESPACE}"
echo ""
echo "Strimzi Operator is ready! Now deploy Kafka cluster with:"
echo "  kubectl apply -f charts/strimzi-kafka/kafka-cluster.yaml -n ${NAMESPACE}"
