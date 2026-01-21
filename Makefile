# Phase IV & V: Kubernetes Deployment Makefile
# Todo Chatbot - Minikube + Helm + Dapr + Strimzi Deployment
# [Task]: T058 - Added Phase V targets

.PHONY: all setup build deploy validate clean logs status help
.PHONY: setup-dapr setup-strimzi deploy-phase-v validate-phase-v build-phase-v

# Default target
all: setup build deploy validate

# Phase V full deployment
all-phase-v: setup setup-dapr setup-strimzi build build-phase-v deploy deploy-phase-v validate-phase-v

# Configuration
CLUSTER_NAME := todo-chatbot
NAMESPACE := todo-chatbot
RELEASE_NAME := todo-chatbot
PHASE_V_RELEASE := phase-v-services

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

#---------------------------------------
# Phase V: Event-Driven Architecture
# [Task]: T058 - Phase V Makefile targets
#---------------------------------------

## setup-dapr: Install Dapr on Minikube cluster
setup-dapr:
	@echo "Setting up Dapr..."
	@chmod +x scripts/setup-dapr.sh
	@./scripts/setup-dapr.sh

## setup-strimzi: Install Strimzi Kafka operator
setup-strimzi:
	@echo "Setting up Strimzi Kafka..."
	@chmod +x scripts/setup-strimzi.sh
	@./scripts/setup-strimzi.sh

## build-phase-v: Build Phase V microservice images
build-phase-v:
	@echo "Building Phase V service images..."
	@eval $$(minikube docker-env -p $(CLUSTER_NAME)) && \
	docker build -t audit-service:phase-v -f services/audit-service/Dockerfile services/audit-service/ && \
	docker build -t reminder-service:phase-v -f services/reminder-service/Dockerfile services/reminder-service/ && \
	docker build -t recurring-service:phase-v -f services/recurring-service/Dockerfile services/recurring-service/

## deploy-phase-v: Deploy Phase V services and components
deploy-phase-v:
	@echo "Deploying Phase V infrastructure..."
	@chmod +x scripts/deploy-phase-v.sh
	@./scripts/deploy-phase-v.sh

## validate-phase-v: Validate Phase V deployment
validate-phase-v:
	@echo "Validating Phase V deployment..."
	@chmod +x scripts/validate-phase-v.sh
	@./scripts/validate-phase-v.sh

## logs-audit: Show audit service logs
logs-audit:
	@kubectl logs -l app=audit-service -n $(NAMESPACE) -f

## logs-reminder: Show reminder service logs
logs-reminder:
	@kubectl logs -l app=reminder-service -n $(NAMESPACE) -f

## logs-recurring: Show recurring service logs
logs-recurring:
	@kubectl logs -l app=recurring-service -n $(NAMESPACE) -f

## logs-kafka: Show Kafka logs
logs-kafka:
	@kubectl logs -l strimzi.io/name=todo-kafka-kafka -n kafka -f --tail=50

## status-phase-v: Show Phase V deployment status
status-phase-v:
	@echo "=== Dapr Status ==="
	@kubectl get pods -n dapr-system
	@echo ""
	@echo "=== Kafka Status ==="
	@kubectl get kafka -n kafka
	@kubectl get kafkatopic -n kafka
	@echo ""
	@echo "=== Phase V Services ==="
	@kubectl get pods -n $(NAMESPACE) -l 'app in (audit-service,reminder-service,recurring-service)'
	@echo ""
	@echo "=== Dapr Components ==="
	@kubectl get components -n $(NAMESPACE)

## uninstall-phase-v: Remove Phase V services
uninstall-phase-v:
	@echo "Uninstalling Phase V services..."
	@helm uninstall $(PHASE_V_RELEASE) -n $(NAMESPACE) 2>/dev/null || true
	@kubectl delete -f charts/dapr-components/ -n $(NAMESPACE) 2>/dev/null || true
	@kubectl delete -f charts/strimzi-kafka/ -n kafka 2>/dev/null || true

#---------------------------------------
# Help
#---------------------------------------

## help: Show this help message
help:
	@echo "Todo Chatbot - Kubernetes Deployment"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Quick Start (Phase IV):"
	@echo "  make setup      - Setup Minikube cluster"
	@echo "  make build      - Build Docker images"
	@echo "  make deploy     - Deploy with Helm"
	@echo "  make validate   - Validate deployment"
	@echo ""
	@echo "Phase V (Event-Driven):"
	@echo "  make setup-dapr    - Install Dapr"
	@echo "  make setup-strimzi - Install Strimzi Kafka"
	@echo "  make build-phase-v - Build microservice images"
	@echo "  make deploy-phase-v - Deploy Phase V services"
	@echo "  make all-phase-v   - Full Phase V deployment"
	@echo ""
	@echo "All targets:"
	@grep -E '^## ' Makefile | sed 's/## /  /' | column -t -s ':'
