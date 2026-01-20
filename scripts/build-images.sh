#!/bin/bash
# Phase IV: Build Docker Images Script
# This script builds Docker images directly into Minikube's Docker daemon

set -e

# Configuration
CLUSTER_NAME="todo-chatbot"
BACKEND_IMAGE="todo-chatbot-backend"
FRONTEND_IMAGE="todo-chatbot-frontend"
TAG="latest"

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
echo -e "${BLUE}  Todo Chatbot - Build Images${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if minikube cluster is running
if ! minikube status -p "$CLUSTER_NAME" &> /dev/null; then
    echo -e "${RED}Error: Minikube cluster '$CLUSTER_NAME' is not running${NC}"
    echo "Please run: make setup"
    exit 1
fi

# Point Docker to Minikube's Docker daemon
echo -e "${GREEN}Configuring Docker to use Minikube's daemon...${NC}"
eval $(minikube docker-env -p "$CLUSTER_NAME")

# Build backend image
echo ""
echo -e "${GREEN}Building backend image: $BACKEND_IMAGE:$TAG${NC}"
echo -e "  Context: $PROJECT_ROOT/backend"
docker build \
    -t "$BACKEND_IMAGE:$TAG" \
    -f "$PROJECT_ROOT/backend/Dockerfile" \
    "$PROJECT_ROOT/backend"

# Build frontend image
echo ""
echo -e "${GREEN}Building frontend image: $FRONTEND_IMAGE:$TAG${NC}"
echo -e "  Context: $PROJECT_ROOT/frontend"
docker build \
    -t "$FRONTEND_IMAGE:$TAG" \
    -f "$PROJECT_ROOT/frontend/Dockerfile" \
    "$PROJECT_ROOT/frontend"

# List built images
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Build Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Built images in Minikube's Docker daemon:"
docker images | grep -E "($BACKEND_IMAGE|$FRONTEND_IMAGE)" | head -5

echo ""
echo -e "Next steps:"
echo -e "  1. Run ${BLUE}make deploy${NC} to deploy the application"
echo ""
