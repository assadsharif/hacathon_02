# Phase V Quickstart Guide

**Date**: 2026-01-20 | **Branch**: `005-phase-v-event-driven`

## Prerequisites

- Minikube v1.32+ with Docker driver
- kubectl v1.28+
- Helm v3.14+
- 8GB RAM available (4GB for Minikube)
- Docker Desktop or Docker Engine

## Quick Setup (5 minutes)

```bash
# 1. Start Minikube with required resources
minikube start --memory=4096 --cpus=4 -p todo-chatbot

# 2. Install all Phase V infrastructure
make setup-phase-v

# 3. Deploy application
make deploy-phase-v

# 4. Access the application
make port-forward
# Open http://localhost:3000
```

---

## Detailed Setup

### Step 1: Minikube Cluster

```bash
# Start with sufficient resources
minikube start \
  --memory=4096 \
  --cpus=4 \
  --driver=docker \
  --profile=todo-chatbot

# Enable required addons
minikube addons enable ingress -p todo-chatbot
minikube addons enable storage-provisioner -p todo-chatbot
minikube addons enable metrics-server -p todo-chatbot
```

### Step 2: Install Dapr

```bash
# Add Dapr Helm repo
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Install Dapr runtime
helm upgrade --install dapr dapr/dapr \
  --namespace dapr-system \
  --create-namespace \
  --wait

# Verify Dapr is running
kubectl get pods -n dapr-system
```

Expected output:
```
NAME                                     READY   STATUS    RESTARTS   AGE
dapr-dashboard-xxx                       1/1     Running   0          1m
dapr-operator-xxx                        1/1     Running   0          1m
dapr-placement-server-xxx                1/1     Running   0          1m
dapr-scheduler-server-xxx                1/1     Running   0          1m
dapr-sentry-xxx                          1/1     Running   0          1m
dapr-sidecar-injector-xxx                1/1     Running   0          1m
```

### Step 3: Install Strimzi Kafka

```bash
# Create Kafka namespace
kubectl create namespace kafka

# Install Strimzi operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for operator to be ready
kubectl wait deployment/strimzi-cluster-operator \
  --for=condition=available \
  --timeout=300s \
  -n kafka

# Deploy Kafka cluster
kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.7.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
    storage:
      type: ephemeral
  zookeeper:
    replicas: 1
    storage:
      type: ephemeral
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF

# Wait for Kafka to be ready
kubectl wait kafka/todo-kafka \
  --for=condition=Ready \
  --timeout=300s \
  -n kafka
```

### Step 4: Create Kafka Topic

```bash
kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-events
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: 604800000
EOF
```

### Step 5: Deploy Dapr Components

```bash
# Apply Pub/Sub component
kubectl apply -f specs/005-phase-v-event-driven/contracts/dapr-pubsub.yaml

# Apply State Store component
kubectl apply -f specs/005-phase-v-event-driven/contracts/dapr-state.yaml

# Verify components
kubectl get components
```

### Step 6: Build and Deploy Application

```bash
# Point to Minikube's Docker daemon
eval $(minikube -p todo-chatbot docker-env)

# Build images
docker build -t todo-chatbot-backend:phase-v ./backend
docker build -t todo-chatbot-frontend:phase-v ./frontend
docker build -t reminder-service:phase-v ./services/reminder-service
docker build -t audit-service:phase-v ./services/audit-service
docker build -t recurring-service:phase-v ./services/recurring-service

# Deploy with Helm
helm upgrade --install todo-chatbot ./charts/todo-chatbot \
  --set backend.image.tag=phase-v \
  --set frontend.image.tag=phase-v \
  --set dapr.enabled=true

# Deploy Phase V services
helm upgrade --install phase-v-services ./charts/phase-v-services \
  --set reminderService.image.tag=phase-v \
  --set auditService.image.tag=phase-v \
  --set recurringService.image.tag=phase-v
```

---

## Verification

### Check All Pods

```bash
kubectl get pods -l app.kubernetes.io/part-of=todo-chatbot
```

Expected output:
```
NAME                                      READY   STATUS    RESTARTS   AGE
todo-chatbot-backend-xxx                  2/2     Running   0          2m
todo-chatbot-frontend-xxx                 2/2     Running   0          2m
todo-chatbot-postgresql-0                 1/1     Running   0          2m
reminder-service-xxx                      2/2     Running   0          1m
audit-service-xxx                         2/2     Running   0          1m
recurring-service-xxx                     2/2     Running   0          1m
```

Note: `2/2` means Dapr sidecar is injected successfully.

### Check Dapr Sidecars

```bash
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'
```

### Check Kafka Topics

```bash
kubectl -n kafka run kafka-topics --rm -it --restart=Never \
  --image=quay.io/strimzi/kafka:latest-kafka-3.7.0 -- \
  bin/kafka-topics.sh --list --bootstrap-server todo-kafka-kafka-bootstrap:9092
```

### Test Event Publishing

```bash
# Create a task via API
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_JWT>" \
  -d '{"title": "Test Phase V", "priority": "high"}'

# Check audit log
curl http://localhost:8000/api/audit?limit=5 \
  -H "Authorization: Bearer <YOUR_JWT>"
```

---

## Port Forwarding

```bash
# Frontend (http://localhost:3000)
kubectl port-forward svc/todo-chatbot-frontend 3000:80 &

# Backend (http://localhost:8000)
kubectl port-forward svc/todo-chatbot-backend 8000:8000 &

# Dapr Dashboard (http://localhost:9999)
dapr dashboard -k -p 9999 &

# Kafka (for debugging, localhost:9092)
kubectl port-forward svc/todo-kafka-kafka-bootstrap 9092:9092 -n kafka &
```

---

## Troubleshooting

### Dapr Sidecar Not Injecting

Check annotations on deployment:
```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "backend"
  dapr.io/app-port: "8000"
```

### Kafka Connection Issues

```bash
# Check Kafka pods
kubectl get pods -n kafka

# Check Kafka logs
kubectl logs -n kafka -l strimzi.io/name=todo-kafka-kafka
```

### Event Not Publishing

```bash
# Check backend logs for Dapr errors
kubectl logs -l app=todo-chatbot-backend -c daprd

# Check pub/sub component
kubectl describe component pubsub-kafka
```

### Out of Memory

```bash
# Increase Minikube memory
minikube stop -p todo-chatbot
minikube start --memory=6144 -p todo-chatbot
```

---

## Cleanup

```bash
# Delete application
helm uninstall todo-chatbot
helm uninstall phase-v-services

# Delete Kafka
kubectl delete kafka/todo-kafka -n kafka
kubectl delete -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Delete Dapr
helm uninstall dapr -n dapr-system

# Stop Minikube
minikube stop -p todo-chatbot

# Delete cluster (optional)
minikube delete -p todo-chatbot
```

---

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement backend event publishing (Group A)
3. Implement microservices (Group B)
4. Update Helm charts with Dapr annotations (Group C)
5. End-to-end testing (Group D)
