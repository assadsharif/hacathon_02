# Phase IV: Kubernetes Deployment Makefile
# Todo Chatbot - Minikube + Helm Deployment

.PHONY: all setup build deploy validate clean logs status help

# Default target
all: setup build deploy validate

# Configuration
CLUSTER_NAME := todo-chatbot
NAMESPACE := todo-chatbot
RELEASE_NAME := todo-chatbot

#---------------------------------------
# Setup Commands
#---------------------------------------

## setup: Start Minikube cluster and enable required addons
setup:
	@echo "Setting up Minikube cluster..."
	@chmod +x scripts/minikube-setup.sh
	@./scripts/minikube-setup.sh

## setup-hosts: Add hosts entry for local access (requires sudo)
setup-hosts:
	@echo "Adding hosts entry..."
	@MINIKUBE_IP=$$(minikube ip -p $(CLUSTER_NAME)); \
	if grep -q "todo-chatbot.local" /etc/hosts; then \
		echo "Host entry already exists"; \
	else \
		echo "$$MINIKUBE_IP todo-chatbot.local" | sudo tee -a /etc/hosts; \
	fi

#---------------------------------------
# Build Commands
#---------------------------------------

## build: Build Docker images in Minikube's Docker daemon
build:
	@echo "Building Docker images..."
	@chmod +x scripts/build-images.sh
	@./scripts/build-images.sh

## build-backend: Build only the backend image
build-backend:
	@echo "Building backend image..."
	@eval $$(minikube docker-env -p $(CLUSTER_NAME)) && \
	docker build -t todo-chatbot-backend:latest -f backend/Dockerfile backend/

## build-frontend: Build only the frontend image
build-frontend:
	@echo "Building frontend image..."
	@eval $$(minikube docker-env -p $(CLUSTER_NAME)) && \
	docker build -t todo-chatbot-frontend:latest -f frontend/Dockerfile frontend/

#---------------------------------------
# Deploy Commands
#---------------------------------------

## deploy: Deploy application using Helm
deploy:
	@echo "Deploying with Helm..."
	@chmod +x scripts/helm-deploy.sh
	@./scripts/helm-deploy.sh

## upgrade: Upgrade existing Helm release
upgrade: deploy

## uninstall: Remove Helm release
uninstall:
	@echo "Uninstalling Helm release..."
	@helm uninstall $(RELEASE_NAME) -n $(NAMESPACE) || true

## redeploy: Uninstall and reinstall
redeploy: uninstall deploy

#---------------------------------------
# Validation Commands
#---------------------------------------

## validate: Run deployment validation checks
validate:
	@echo "Validating deployment..."
	@chmod +x scripts/validate-deployment.sh
	@./scripts/validate-deployment.sh

## health: Quick health check
health:
	@echo "Checking health endpoints..."
	@curl -s http://todo-chatbot.local/health | python3 -m json.tool 2>/dev/null || echo "Health check failed"

## test-api: Test API endpoints
test-api:
	@echo "Testing API endpoints..."
	@echo "1. Health check:"
	@curl -s http://todo-chatbot.local/health
	@echo ""
	@echo "2. Database health:"
	@curl -s http://todo-chatbot.local/health/db
	@echo ""

#---------------------------------------
# Status & Logs Commands
#---------------------------------------

## status: Show deployment status
status:
	@echo "=== Pods ==="
	@kubectl get pods -n $(NAMESPACE) -o wide
	@echo ""
	@echo "=== Services ==="
	@kubectl get services -n $(NAMESPACE)
	@echo ""
	@echo "=== Ingress ==="
	@kubectl get ingress -n $(NAMESPACE)
	@echo ""
	@echo "=== PVCs ==="
	@kubectl get pvc -n $(NAMESPACE)

## logs: Show all pod logs
logs:
	@echo "=== Backend Logs ==="
	@kubectl logs -l app.kubernetes.io/component=backend -n $(NAMESPACE) --tail=50 2>/dev/null || echo "No backend logs"
	@echo ""
	@echo "=== Frontend Logs ==="
	@kubectl logs -l app.kubernetes.io/component=frontend -n $(NAMESPACE) --tail=50 2>/dev/null || echo "No frontend logs"
	@echo ""
	@echo "=== Database Logs ==="
	@kubectl logs -l app.kubernetes.io/component=database -n $(NAMESPACE) --tail=50 2>/dev/null || echo "No database logs"

## logs-backend: Show backend logs
logs-backend:
	@kubectl logs -l app.kubernetes.io/component=backend -n $(NAMESPACE) -f

## logs-frontend: Show frontend logs
logs-frontend:
	@kubectl logs -l app.kubernetes.io/component=frontend -n $(NAMESPACE) -f

## logs-db: Show database logs
logs-db:
	@kubectl logs -l app.kubernetes.io/component=database -n $(NAMESPACE) -f

#---------------------------------------
# Debug Commands
#---------------------------------------

## shell-backend: Open shell in backend pod
shell-backend:
	@kubectl exec -it $$(kubectl get pods -n $(NAMESPACE) -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}') -n $(NAMESPACE) -- /bin/bash

## shell-frontend: Open shell in frontend pod
shell-frontend:
	@kubectl exec -it $$(kubectl get pods -n $(NAMESPACE) -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}') -n $(NAMESPACE) -- /bin/sh

## shell-db: Open psql in database pod
shell-db:
	@kubectl exec -it $$(kubectl get pods -n $(NAMESPACE) -l app.kubernetes.io/component=database -o jsonpath='{.items[0].metadata.name}') -n $(NAMESPACE) -- psql -U todouser -d tododb

## describe: Describe all resources
describe:
	@echo "=== Pods ==="
	@kubectl describe pods -n $(NAMESPACE)
	@echo ""
	@echo "=== Services ==="
	@kubectl describe services -n $(NAMESPACE)

## events: Show recent events
events:
	@kubectl get events -n $(NAMESPACE) --sort-by='.lastTimestamp'

#---------------------------------------
# Cleanup Commands
#---------------------------------------

## clean: Remove Helm release and namespace
clean:
	@echo "Cleaning up..."
	@helm uninstall $(RELEASE_NAME) -n $(NAMESPACE) 2>/dev/null || true
	@kubectl delete namespace $(NAMESPACE) 2>/dev/null || true

## clean-all: Stop and delete Minikube cluster
clean-all: clean
	@echo "Deleting Minikube cluster..."
	@minikube delete -p $(CLUSTER_NAME) 2>/dev/null || true

## restart: Restart all deployments
restart:
	@echo "Restarting deployments..."
	@kubectl rollout restart deployment -n $(NAMESPACE)

#---------------------------------------
# Dashboard & Monitoring
#---------------------------------------

## dashboard: Open Minikube dashboard
dashboard:
	@minikube dashboard -p $(CLUSTER_NAME)

## tunnel: Start Minikube tunnel (for LoadBalancer services)
tunnel:
	@minikube tunnel -p $(CLUSTER_NAME)

#---------------------------------------
# Help
#---------------------------------------

## help: Show this help message
help:
	@echo "Todo Chatbot - Kubernetes Deployment"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Quick Start:"
	@echo "  make setup      - Setup Minikube cluster"
	@echo "  make build      - Build Docker images"
	@echo "  make deploy     - Deploy with Helm"
	@echo "  make validate   - Validate deployment"
	@echo ""
	@echo "All targets:"
	@grep -E '^## ' Makefile | sed 's/## /  /' | column -t -s ':'
