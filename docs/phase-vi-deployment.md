# Phase VI: Multi-Cloud Deployment Guide

## Overview

This guide covers deploying the Todo Chatbot application to multiple cloud providers:
- **Google Kubernetes Engine (GKE)** - Google Cloud Platform
- **Azure Kubernetes Service (AKS)** - Microsoft Azure

Both deployments use:
- **Redpanda Cloud** - Managed Kafka-compatible event streaming
- **Neon** - Serverless PostgreSQL database
- **Dapr** - Distributed application runtime for pub/sub

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Redpanda Cloud                              │
│                   (Kafka-compatible)                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               │               ▼
┌─────────────────┐       │       ┌─────────────────┐
│      GKE        │       │       │      AKS        │
│  (us-central1)  │       │       │    (eastus)     │
├─────────────────┤       │       ├─────────────────┤
│ - Frontend (2)  │       │       │ - Frontend (2)  │
│ - Backend (2)   │       │       │ - Backend (2)   │
│ - Audit (1)     │       │       │ - Audit (1)     │
│ - Reminder (1)  │       │       │ - Reminder (1)  │
│ - Recurring (1) │       │       │ - Recurring (1) │
│ - Dapr Sidecars │       │       │ - Dapr Sidecars │
└────────┬────────┘       │       └────────┬────────┘
         │                │                │
         └────────────────┼────────────────┘
                          │
                          ▼
                ┌─────────────────┐
                │   Neon Cloud    │
                │  (PostgreSQL)   │
                └─────────────────┘
```

## Prerequisites

### Required Accounts
- Google Cloud Platform account with billing enabled
- Microsoft Azure account with billing enabled
- Redpanda Cloud account
- Neon account (serverless PostgreSQL)
- GitHub account (for CI/CD)

### Required CLI Tools
```bash
# Google Cloud SDK
curl https://sdk.cloud.google.com | bash
gcloud init

# Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az login

# Kubernetes CLI
# Already included with gcloud/az

# Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Dapr CLI
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
```

## Step 1: Redpanda Cloud Setup

1. **Create Cluster**
   - Go to [Redpanda Cloud Console](https://cloud.redpanda.com)
   - Create a Serverless cluster
   - Note the broker URL (format: `<cluster-id>.<region>.redpanda.cloud:9092`)

2. **Create Topic**
   ```
   Topic name: task-events
   Partitions: 3
   Retention: 7 days
   ```

3. **Create SASL Credentials**
   - Navigate to Security → Users
   - Create a new user with SCRAM-SHA-256
   - Save username and password

4. **Test Connection**
   ```bash
   rpk cluster info --brokers <broker-url> \
     --sasl-mechanism SCRAM-SHA-256 \
     --user <username> --password <password> --tls-enabled
   ```

## Step 2: GKE Deployment

### 2.1 Create GKE Cluster

```bash
# Set project
export PROJECT_ID=<your-project-id>
gcloud config set project $PROJECT_ID

# Enable APIs
gcloud services enable container.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Create cluster
gcloud container clusters create todo-chatbot \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type e2-medium \
  --enable-ip-alias

# Get credentials
gcloud container clusters get-credentials todo-chatbot --zone us-central1-a
```

### 2.2 Build and Push Images to GCR

```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Build and push images
docker build -t gcr.io/$PROJECT_ID/todo-chatbot-backend:latest ./backend
docker build -t gcr.io/$PROJECT_ID/todo-chatbot-frontend:latest ./frontend
docker build -t gcr.io/$PROJECT_ID/audit-service:latest ./services/audit-service
docker build -t gcr.io/$PROJECT_ID/reminder-service:latest ./services/reminder-service
docker build -t gcr.io/$PROJECT_ID/recurring-service:latest ./services/recurring-service

docker push gcr.io/$PROJECT_ID/todo-chatbot-backend:latest
docker push gcr.io/$PROJECT_ID/todo-chatbot-frontend:latest
docker push gcr.io/$PROJECT_ID/audit-service:latest
docker push gcr.io/$PROJECT_ID/reminder-service:latest
docker push gcr.io/$PROJECT_ID/recurring-service:latest
```

### 2.3 Install Dapr on GKE

```bash
dapr init -k --runtime-version 1.15.0
dapr status -k
```

### 2.4 Create Kubernetes Secrets

```bash
kubectl create namespace todo-chatbot

# Application secrets
kubectl create secret generic todo-chatbot-secrets \
  --namespace todo-chatbot \
  --from-literal=DATABASE_URL=<neon-connection-string> \
  --from-literal=JWT_SECRET=<jwt-secret> \
  --from-literal=OPENAI_API_KEY=<openai-key>

# Redpanda secrets
kubectl create secret generic redpanda-secrets \
  --namespace todo-chatbot \
  --from-literal=username=<redpanda-user> \
  --from-literal=password=<redpanda-password>

# Database secrets for Dapr state store
kubectl create secret generic db-secrets \
  --namespace todo-chatbot \
  --from-literal=connectionString=<neon-connection-string>
```

### 2.5 Deploy with Helm

```bash
# Deploy Dapr components
helm upgrade --install dapr-components ./charts/dapr-components \
  -n todo-chatbot \
  -f ./charts/dapr-components/values-cloud.yaml \
  --set pubsub.brokers=<redpanda-broker-url>

# Deploy main application
helm upgrade --install todo-chatbot ./charts/todo-chatbot \
  -n todo-chatbot \
  -f ./charts/todo-chatbot/values-gke.yaml \
  --set backend.image.repository=gcr.io/$PROJECT_ID/todo-chatbot-backend \
  --set frontend.image.repository=gcr.io/$PROJECT_ID/todo-chatbot-frontend

# Deploy Phase V services
helm upgrade --install phase-v-services ./charts/phase-v-services \
  -n todo-chatbot \
  -f ./charts/phase-v-services/values-gke.yaml \
  --set auditService.image.repository=gcr.io/$PROJECT_ID/audit-service \
  --set reminderService.image.repository=gcr.io/$PROJECT_ID/reminder-service \
  --set recurringService.image.repository=gcr.io/$PROJECT_ID/recurring-service
```

### 2.6 Verify GKE Deployment

```bash
# Check pods
kubectl get pods -n todo-chatbot

# Get external IPs
kubectl get svc -n todo-chatbot

# Test health
curl http://<backend-ip>:8000/health
```

## Step 3: AKS Deployment

### 3.1 Create AKS Cluster

```bash
# Set variables
export RESOURCE_GROUP=todo-chatbot-rg
export CLUSTER_NAME=todo-chatbot
export ACR_NAME=todochatbotacr$(date +%s)

# Create resource group
az group create --name $RESOURCE_GROUP --location eastus

# Create ACR
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

# Create AKS cluster
az aks create \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --attach-acr $ACR_NAME \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME
```

### 3.2 Build and Push Images to ACR

```bash
# Login to ACR
az acr login --name $ACR_NAME

# Build and push images
docker build -t $ACR_NAME.azurecr.io/todo-chatbot-backend:latest ./backend
docker build -t $ACR_NAME.azurecr.io/todo-chatbot-frontend:latest ./frontend
docker build -t $ACR_NAME.azurecr.io/audit-service:latest ./services/audit-service
docker build -t $ACR_NAME.azurecr.io/reminder-service:latest ./services/reminder-service
docker build -t $ACR_NAME.azurecr.io/recurring-service:latest ./services/recurring-service

docker push $ACR_NAME.azurecr.io/todo-chatbot-backend:latest
docker push $ACR_NAME.azurecr.io/todo-chatbot-frontend:latest
docker push $ACR_NAME.azurecr.io/audit-service:latest
docker push $ACR_NAME.azurecr.io/reminder-service:latest
docker push $ACR_NAME.azurecr.io/recurring-service:latest
```

### 3.3 Install Dapr on AKS

```bash
dapr init -k --runtime-version 1.15.0
dapr status -k
```

### 3.4 Create Kubernetes Secrets

```bash
kubectl create namespace todo-chatbot

# Same secrets as GKE (see section 2.4)
```

### 3.5 Deploy with Helm

```bash
# Deploy Dapr components
helm upgrade --install dapr-components ./charts/dapr-components \
  -n todo-chatbot \
  -f ./charts/dapr-components/values-cloud.yaml \
  --set pubsub.brokers=<redpanda-broker-url>

# Deploy main application
helm upgrade --install todo-chatbot ./charts/todo-chatbot \
  -n todo-chatbot \
  -f ./charts/todo-chatbot/values-aks.yaml \
  --set backend.image.repository=$ACR_NAME.azurecr.io/todo-chatbot-backend \
  --set frontend.image.repository=$ACR_NAME.azurecr.io/todo-chatbot-frontend

# Deploy Phase V services
helm upgrade --install phase-v-services ./charts/phase-v-services \
  -n todo-chatbot \
  -f ./charts/phase-v-services/values-aks.yaml \
  --set auditService.image.repository=$ACR_NAME.azurecr.io/audit-service \
  --set reminderService.image.repository=$ACR_NAME.azurecr.io/reminder-service \
  --set recurringService.image.repository=$ACR_NAME.azurecr.io/recurring-service
```

### 3.6 Verify AKS Deployment

```bash
# Check pods
kubectl get pods -n todo-chatbot

# Get external IPs
kubectl get svc -n todo-chatbot

# Test health
curl http://<backend-ip>:8000/health
```

## Step 4: Observability Stack

### Deploy to Both Clusters

```bash
# Add Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create monitoring namespace
kubectl create namespace monitoring

# Install kube-prometheus-stack
helm upgrade --install prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --set grafana.adminPassword=admin123 \
  --set grafana.service.type=LoadBalancer

# Apply custom dashboards
kubectl apply -f ./charts/observability/dashboards/
```

### Access Grafana

```bash
# Port forward
kubectl port-forward svc/prometheus-stack-grafana 3001:80 -n monitoring

# Open http://localhost:3001
# Username: admin
# Password: admin123
```

## Step 5: CI/CD Pipeline

### Configure GitHub Secrets

Navigate to your repository Settings → Secrets and variables → Actions, and add:

| Secret | Description |
|--------|-------------|
| `GCP_PROJECT_ID` | GCP project ID |
| `GCP_SA_KEY` | Service account JSON key |
| `AZURE_CREDENTIALS` | Azure service principal JSON |
| `ACR_NAME` | Azure Container Registry name |
| `ACR_USERNAME` | ACR admin username |
| `ACR_PASSWORD` | ACR admin password |
| `DATABASE_URL` | Neon PostgreSQL URL |
| `JWT_SECRET` | JWT signing secret |
| `OPENAI_API_KEY` | OpenAI API key |
| `REDPANDA_BROKERS` | Redpanda broker URL |
| `REDPANDA_USERNAME` | Redpanda SASL username |
| `REDPANDA_PASSWORD` | Redpanda SASL password |

### Workflow Triggers

- **Build**: Triggers on push to `main` (paths: `backend/**`, `frontend/**`, `services/**`)
- **Deploy GKE**: Triggers after successful build
- **Deploy AKS**: Triggers after successful build

### Manual Deployment

```bash
# Emergency manual deployment
./scripts/manual-deploy.sh gke latest
./scripts/manual-deploy.sh aks latest
./scripts/manual-deploy.sh both v1.0.0
```

## Step 6: Validation

### Run E2E Tests

```bash
./scripts/e2e-cloud-test.sh gke
./scripts/e2e-cloud-test.sh aks
```

### Health Checks

```bash
# GKE
curl http://<gke-backend-ip>:8000/health
curl http://<gke-frontend-ip>:3000

# AKS
curl http://<aks-backend-ip>:8000/health
curl http://<aks-frontend-ip>:3000
```

### Verify Event Flow

1. Create a todo via the UI
2. Check audit service logs for event receipt
3. Verify in Grafana Dapr Pub/Sub dashboard

## Troubleshooting

### Common Issues

**Pods not starting:**
```bash
kubectl describe pod <pod-name> -n todo-chatbot
kubectl logs <pod-name> -n todo-chatbot
```

**Dapr sidecar not injecting:**
```bash
# Check Dapr status
dapr status -k

# Verify namespace has Dapr enabled
kubectl get namespace todo-chatbot -o yaml | grep dapr
```

**LoadBalancer IP pending:**
```bash
# Check events
kubectl get events -n todo-chatbot --sort-by='.lastTimestamp'
```

**Redpanda connection issues:**
```bash
# Check Dapr component status
kubectl get components -n todo-chatbot
kubectl describe component pubsub-kafka -n todo-chatbot
```

### Useful Commands

```bash
# View all resources
kubectl get all -n todo-chatbot

# Check Dapr logs
kubectl logs <pod-name> -c daprd -n todo-chatbot

# Restart deployment
kubectl rollout restart deployment <name> -n todo-chatbot

# Scale deployment
kubectl scale deployment <name> --replicas=3 -n todo-chatbot
```

## Cost Management

### GKE Free Tier
- 1 zonal cluster free
- e2-medium nodes: ~$25/month each
- Estimated: ~$50-75/month for 2 nodes

### AKS Free Tier
- Control plane free
- Standard_B2s nodes: ~$30/month each
- Estimated: ~$60-90/month for 2 nodes

### Tips
- Use preemptible/spot VMs for non-production
- Scale down when not in use
- Set up budget alerts

## Security Considerations

- All secrets stored in Kubernetes Secrets
- TLS enabled for Redpanda Cloud connection
- SASL authentication for Kafka
- No secrets in Git repository
- Use managed identities where possible
