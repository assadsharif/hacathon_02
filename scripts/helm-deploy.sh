#!/bin/bash
# Phase IV: Helm Deployment Script
# This script installs or upgrades the Todo Chatbot Helm release

set -e

# Configuration
CLUSTER_NAME="todo-chatbot"
RELEASE_NAME="todo-chatbot"
NAMESPACE="todo-chatbot"
CHART_PATH="charts/todo-chatbot"

# Secret values (should be overridden in production)
DB_PASSWORD="${DB_PASSWORD:-todopassword}"
JWT_SECRET="${JWT_SECRET:-your-super-secret-jwt-key-change-in-production}"
BETTER_AUTH_SECRET="${BETTER_AUTH_SECRET:-your-better-auth-secret-change-in-production}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Todo Chatbot - Helm Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if minikube cluster is running
if ! minikube status -p "$CLUSTER_NAME" &> /dev/null; then
    echo -e "${RED}Error: Minikube cluster '$CLUSTER_NAME' is not running${NC}"
    echo "Please run: make setup"
    exit 1
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo -e "${RED}Error: helm is not installed${NC}"
    echo "Please install helm: https://helm.sh/docs/intro/install/"
    exit 1
fi

# Set kubectl context
kubectl config use-context "$CLUSTER_NAME"

# Create namespace if not exists
echo -e "${GREEN}Ensuring namespace exists: $NAMESPACE${NC}"
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Check if release exists
if helm status "$RELEASE_NAME" -n "$NAMESPACE" &> /dev/null; then
    echo -e "${YELLOW}Upgrading existing release: $RELEASE_NAME${NC}"
    ACTION="upgrade"
else
    echo -e "${GREEN}Installing new release: $RELEASE_NAME${NC}"
    ACTION="install"
fi

# Deploy with Helm
echo ""
echo -e "${GREEN}Deploying to namespace: $NAMESPACE${NC}"

cd "$PROJECT_ROOT"

helm $ACTION "$RELEASE_NAME" "$CHART_PATH" \
    --namespace "$NAMESPACE" \
    --set database.credentials.password="$DB_PASSWORD" \
    --set secrets.jwtSecret="$JWT_SECRET" \
    --set secrets.betterAuthSecret="$BETTER_AUTH_SECRET" \
    --wait \
    --timeout 5m

# Get deployment status
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Release: ${BLUE}$RELEASE_NAME${NC}"
echo -e "Namespace: ${BLUE}$NAMESPACE${NC}"
echo ""

# Show pod status
echo -e "${GREEN}Pod Status:${NC}"
kubectl get pods -n "$NAMESPACE" -o wide

echo ""
echo -e "${GREEN}Service Status:${NC}"
kubectl get services -n "$NAMESPACE"

echo ""
echo -e "${GREEN}Ingress Status:${NC}"
kubectl get ingress -n "$NAMESPACE"

# Get minikube IP
MINIKUBE_IP=$(minikube ip -p "$CLUSTER_NAME")

echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  Access Instructions${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo -e "1. Add hosts entry (if not already done):"
echo -e "   ${BLUE}echo \"$MINIKUBE_IP todo-chatbot.local\" | sudo tee -a /etc/hosts${NC}"
echo ""
echo -e "2. Access the application:"
echo -e "   ${BLUE}http://todo-chatbot.local${NC}"
echo ""
echo -e "3. API Documentation:"
echo -e "   ${BLUE}http://todo-chatbot.local/docs${NC}"
echo ""
echo -e "4. Health Check:"
echo -e "   ${BLUE}curl http://todo-chatbot.local/health${NC}"
echo ""
