#!/bin/bash
# Phase IV: Minikube Cluster Setup Script
# This script sets up a local Minikube cluster for the Todo Chatbot application

set -e

# Configuration
CLUSTER_NAME="todo-chatbot"
CPUS=4
MEMORY="4096"
DISK="20g"
DRIVER="docker"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Todo Chatbot - Minikube Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo -e "${RED}Error: minikube is not installed${NC}"
    echo "Please install minikube: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed${NC}"
    echo "Please install kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check if docker is installed (for docker driver)
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: docker is not installed${NC}"
    echo "Please install docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if cluster already exists
if minikube status -p "$CLUSTER_NAME" &> /dev/null; then
    echo -e "${YELLOW}Cluster '$CLUSTER_NAME' already exists${NC}"
    echo -e "${YELLOW}Starting existing cluster...${NC}"
    minikube start -p "$CLUSTER_NAME"
else
    echo -e "${GREEN}Creating new Minikube cluster: $CLUSTER_NAME${NC}"
    echo -e "  CPUs: $CPUS"
    echo -e "  Memory: $MEMORY MB"
    echo -e "  Disk: $DISK"
    echo -e "  Driver: $DRIVER"
    echo ""

    # Start minikube cluster
    minikube start \
        -p "$CLUSTER_NAME" \
        --cpus="$CPUS" \
        --memory="$MEMORY" \
        --disk-size="$DISK" \
        --driver="$DRIVER" \
        --kubernetes-version="v1.28.0"
fi

echo ""
echo -e "${GREEN}Enabling required addons...${NC}"

# Enable ingress addon for routing
echo -e "  - Enabling ingress..."
minikube addons enable ingress -p "$CLUSTER_NAME"

# Enable storage-provisioner for PVCs
echo -e "  - Enabling storage-provisioner..."
minikube addons enable storage-provisioner -p "$CLUSTER_NAME"

# Enable metrics-server for resource monitoring
echo -e "  - Enabling metrics-server..."
minikube addons enable metrics-server -p "$CLUSTER_NAME"

# Wait for ingress controller to be ready
echo ""
echo -e "${YELLOW}Waiting for ingress controller to be ready...${NC}"
kubectl wait --namespace ingress-nginx \
    --for=condition=ready pod \
    --selector=app.kubernetes.io/component=controller \
    --timeout=120s 2>/dev/null || echo -e "${YELLOW}Ingress controller starting (may take a moment)...${NC}"

# Create namespace for the application
echo ""
echo -e "${GREEN}Creating namespace: todo-chatbot${NC}"
kubectl create namespace todo-chatbot --dry-run=client -o yaml | kubectl apply -f -

# Set kubectl context
echo -e "${GREEN}Setting kubectl context to cluster: $CLUSTER_NAME${NC}"
kubectl config use-context "$CLUSTER_NAME"

# Get cluster info
MINIKUBE_IP=$(minikube ip -p "$CLUSTER_NAME")

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Minikube Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Cluster Name: ${BLUE}$CLUSTER_NAME${NC}"
echo -e "Minikube IP:  ${BLUE}$MINIKUBE_IP${NC}"
echo ""
echo -e "To add the hosts entry, run:"
echo -e "${YELLOW}echo \"$MINIKUBE_IP todo-chatbot.local\" | sudo tee -a /etc/hosts${NC}"
echo ""
echo -e "Next steps:"
echo -e "  1. Run ${BLUE}make build${NC} to build Docker images"
echo -e "  2. Run ${BLUE}make deploy${NC} to deploy the application"
echo ""
