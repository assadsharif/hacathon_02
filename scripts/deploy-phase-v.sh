#!/bin/bash
# [Task]: T005
# Phase V Full Deployment Orchestration Script
# Deploys: Dapr, Strimzi Kafka, Dapr Components, Todo Chatbot, Phase V Services

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "${SCRIPT_DIR}")"

# Configuration
MINIKUBE_PROFILE="${MINIKUBE_PROFILE:-todo-chatbot}"
KAFKA_NAMESPACE="${KAFKA_NAMESPACE:-kafka}"
DAPR_NAMESPACE="${DAPR_NAMESPACE:-dapr-system}"
APP_NAMESPACE="${APP_NAMESPACE:-default}"

echo "============================================"
echo "  Phase V Deployment - Event-Driven Todo"
echo "============================================"
echo ""
echo "Configuration:"
echo "  Minikube Profile: ${MINIKUBE_PROFILE}"
echo "  Kafka Namespace:  ${KAFKA_NAMESPACE}"
echo "  Dapr Namespace:   ${DAPR_NAMESPACE}"
echo "  App Namespace:    ${APP_NAMESPACE}"
echo ""

# Step 1: Verify Minikube is running
echo "=== Step 1: Verify Minikube ==="
if ! minikube status -p "${MINIKUBE_PROFILE}" &> /dev/null; then
    echo "Starting Minikube..."
    minikube start --memory=4096 --cpus=4 -p "${MINIKUBE_PROFILE}"
fi
echo "Minikube is running."
echo ""

# Step 2: Setup Dapr
echo "=== Step 2: Setup Dapr ==="
bash "${SCRIPT_DIR}/setup-dapr.sh"
echo ""

# Step 3: Setup Strimzi and Kafka
echo "=== Step 3: Setup Strimzi Kafka ==="
bash "${SCRIPT_DIR}/setup-strimzi.sh"

echo "Deploying Kafka cluster..."
kubectl apply -f "${PROJECT_ROOT}/charts/strimzi-kafka/kafka-cluster.yaml" -n "${KAFKA_NAMESPACE}"

echo "Waiting for Kafka cluster to be ready (this may take 2-3 minutes)..."
kubectl wait kafka/todo-kafka \
    --for=condition=Ready \
    --timeout=300s \
    -n "${KAFKA_NAMESPACE}" || {
    echo "WARNING: Kafka not ready yet, continuing..."
}

echo "Creating Kafka topics..."
kubectl apply -f "${PROJECT_ROOT}/charts/strimzi-kafka/kafka-topic.yaml" -n "${KAFKA_NAMESPACE}"
echo ""

# Step 4: Deploy Dapr Components
echo "=== Step 4: Deploy Dapr Components ==="
kubectl apply -f "${PROJECT_ROOT}/charts/dapr-components/" -n "${APP_NAMESPACE}"
echo ""

# Step 5: Build Docker Images
echo "=== Step 5: Build Docker Images ==="
eval $(minikube -p "${MINIKUBE_PROFILE}" docker-env)

echo "Building backend image..."
docker build -t todo-chatbot-backend:phase-v "${PROJECT_ROOT}/backend"

echo "Building frontend image..."
docker build -t todo-chatbot-frontend:phase-v "${PROJECT_ROOT}/frontend"

# Build Phase V services if they exist
if [ -d "${PROJECT_ROOT}/services/audit-service" ] && [ -f "${PROJECT_ROOT}/services/audit-service/Dockerfile" ]; then
    echo "Building audit-service image..."
    docker build -t audit-service:phase-v "${PROJECT_ROOT}/services/audit-service"
fi

if [ -d "${PROJECT_ROOT}/services/reminder-service" ] && [ -f "${PROJECT_ROOT}/services/reminder-service/Dockerfile" ]; then
    echo "Building reminder-service image..."
    docker build -t reminder-service:phase-v "${PROJECT_ROOT}/services/reminder-service"
fi

if [ -d "${PROJECT_ROOT}/services/recurring-service" ] && [ -f "${PROJECT_ROOT}/services/recurring-service/Dockerfile" ]; then
    echo "Building recurring-service image..."
    docker build -t recurring-service:phase-v "${PROJECT_ROOT}/services/recurring-service"
fi
echo ""

# Step 6: Deploy Applications with Helm
echo "=== Step 6: Deploy Applications ==="
helm upgrade --install todo-chatbot "${PROJECT_ROOT}/charts/todo-chatbot" \
    --namespace "${APP_NAMESPACE}" \
    --set backend.image.tag=phase-v \
    --set frontend.image.tag=phase-v \
    --set backend.dapr.enabled=true \
    --set frontend.dapr.enabled=true

# Deploy Phase V services if chart exists
if [ -f "${PROJECT_ROOT}/charts/phase-v-services/Chart.yaml" ]; then
    echo "Deploying Phase V services..."
    helm upgrade --install phase-v-services "${PROJECT_ROOT}/charts/phase-v-services" \
        --namespace "${APP_NAMESPACE}"
fi
echo ""

# Step 7: Wait for deployments
echo "=== Step 7: Wait for Deployments ==="
echo "Waiting for backend..."
kubectl wait deployment/todo-chatbot-backend \
    --for=condition=available \
    --timeout=120s \
    -n "${APP_NAMESPACE}" || echo "WARNING: Backend not ready"

echo "Waiting for frontend..."
kubectl wait deployment/todo-chatbot-frontend \
    --for=condition=available \
    --timeout=120s \
    -n "${APP_NAMESPACE}" || echo "WARNING: Frontend not ready"
echo ""

# Step 8: Display status
echo "=== Deployment Complete ==="
echo ""
echo "Pod Status:"
kubectl get pods -n "${APP_NAMESPACE}"
echo ""
echo "Services:"
kubectl get svc -n "${APP_NAMESPACE}"
echo ""
echo "Kafka Status:"
kubectl get kafka,kafkatopic -n "${KAFKA_NAMESPACE}"
echo ""
echo "Dapr Components:"
kubectl get components -n "${APP_NAMESPACE}"
echo ""
echo "============================================"
echo "  Deployment Summary"
echo "============================================"
echo ""
echo "To access the application:"
echo "  kubectl port-forward svc/todo-chatbot-frontend 3000:80 -n ${APP_NAMESPACE} &"
echo "  kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n ${APP_NAMESPACE} &"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "To validate Phase V features:"
echo "  bash scripts/validate-phase-v.sh"
