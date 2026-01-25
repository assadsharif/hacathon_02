#!/bin/bash
# [Task]: T046
# Phase VI: Manual Deployment Script
# Emergency deployment script for manual deployments when CI/CD is unavailable
#
# Usage:
#   ./scripts/manual-deploy.sh [gke|aks|both] [image-tag]
#
# Examples:
#   ./scripts/manual-deploy.sh gke latest
#   ./scripts/manual-deploy.sh aks v1.0.0
#   ./scripts/manual-deploy.sh both $(git rev-parse --short HEAD)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
GKE_CLUSTER="todo-chatbot"
GKE_ZONE="us-central1-a"
GKE_PROJECT="${GCP_PROJECT_ID:-}"

AKS_CLUSTER="todo-chatbot"
AKS_RESOURCE_GROUP="todo-chatbot-rg"
ACR_NAME="${ACR_NAME:-todochatbotacr48370}"

NAMESPACE="todo-chatbot"
CHART_DIR="./charts"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_usage() {
    echo "Usage: $0 [gke|aks|both] [image-tag]"
    echo ""
    echo "Arguments:"
    echo "  target     Target cloud: gke, aks, or both"
    echo "  image-tag  Docker image tag (default: latest)"
    echo ""
    echo "Environment Variables:"
    echo "  GCP_PROJECT_ID  GCP project ID (required for GKE)"
    echo "  ACR_NAME        Azure Container Registry name (default: todochatbotacr48370)"
    echo ""
    echo "Examples:"
    echo "  $0 gke latest"
    echo "  $0 aks v1.0.0"
    echo "  $0 both \$(git rev-parse --short HEAD)"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check for required tools
    local missing_tools=()

    command -v kubectl >/dev/null 2>&1 || missing_tools+=("kubectl")
    command -v helm >/dev/null 2>&1 || missing_tools+=("helm")

    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi

    # Check for Helm charts
    if [[ ! -d "$CHART_DIR/todo-chatbot" ]]; then
        log_error "Helm chart not found at $CHART_DIR/todo-chatbot"
        exit 1
    fi

    log_success "Prerequisites check passed"
}

switch_to_gke() {
    log_info "Switching to GKE context..."

    if [[ -z "$GKE_PROJECT" ]]; then
        log_error "GCP_PROJECT_ID environment variable not set"
        exit 1
    fi

    command -v gcloud >/dev/null 2>&1 || {
        log_error "gcloud CLI not installed"
        exit 1
    }

    gcloud container clusters get-credentials "$GKE_CLUSTER" \
        --zone "$GKE_ZONE" \
        --project "$GKE_PROJECT"

    log_success "Switched to GKE context"
}

switch_to_aks() {
    log_info "Switching to AKS context..."

    command -v az >/dev/null 2>&1 || {
        log_error "Azure CLI not installed"
        exit 1
    }

    az aks get-credentials \
        --resource-group "$AKS_RESOURCE_GROUP" \
        --name "$AKS_CLUSTER" \
        --overwrite-existing

    log_success "Switched to AKS context"
}

deploy_to_gke() {
    local image_tag="$1"

    log_info "Deploying to GKE with tag: $image_tag"

    switch_to_gke

    # Ensure namespace exists
    kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

    # Deploy Dapr components
    log_info "Deploying Dapr components..."
    helm upgrade --install dapr-components "$CHART_DIR/dapr-components" \
        --namespace "$NAMESPACE" \
        -f "$CHART_DIR/dapr-components/values-cloud.yaml" \
        --set pubsub.brokers="${REDPANDA_BROKERS:-}" \
        --wait --timeout 5m || log_warning "Dapr components deployment had issues"

    # Deploy todo-chatbot
    log_info "Deploying todo-chatbot..."
    helm upgrade --install todo-chatbot "$CHART_DIR/todo-chatbot" \
        --namespace "$NAMESPACE" \
        -f "$CHART_DIR/todo-chatbot/values-gke.yaml" \
        --set backend.image.repository="gcr.io/$GKE_PROJECT/todo-chatbot-backend" \
        --set backend.image.tag="$image_tag" \
        --set frontend.image.repository="gcr.io/$GKE_PROJECT/todo-chatbot-frontend" \
        --set frontend.image.tag="$image_tag" \
        --wait --timeout 5m

    # Deploy phase-v-services
    log_info "Deploying phase-v-services..."
    helm upgrade --install phase-v-services "$CHART_DIR/phase-v-services" \
        --namespace "$NAMESPACE" \
        -f "$CHART_DIR/phase-v-services/values-gke.yaml" \
        --set auditService.image.repository="gcr.io/$GKE_PROJECT/audit-service" \
        --set auditService.image.tag="$image_tag" \
        --set reminderService.image.repository="gcr.io/$GKE_PROJECT/reminder-service" \
        --set reminderService.image.tag="$image_tag" \
        --set recurringService.image.repository="gcr.io/$GKE_PROJECT/recurring-service" \
        --set recurringService.image.tag="$image_tag" \
        --wait --timeout 5m || log_warning "Phase-v-services deployment had issues"

    log_success "GKE deployment completed"

    # Show status
    echo ""
    log_info "GKE Deployment Status:"
    kubectl get pods -n "$NAMESPACE"
    echo ""
    kubectl get svc -n "$NAMESPACE" | grep -E "LoadBalancer|NAME"
}

deploy_to_aks() {
    local image_tag="$1"

    log_info "Deploying to AKS with tag: $image_tag"

    switch_to_aks

    # Ensure namespace exists
    kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

    # Deploy Dapr components
    log_info "Deploying Dapr components..."
    helm upgrade --install dapr-components "$CHART_DIR/dapr-components" \
        --namespace "$NAMESPACE" \
        -f "$CHART_DIR/dapr-components/values-cloud.yaml" \
        --set pubsub.brokers="${REDPANDA_BROKERS:-}" \
        --wait --timeout 5m || log_warning "Dapr components deployment had issues"

    # Deploy todo-chatbot
    log_info "Deploying todo-chatbot..."
    helm upgrade --install todo-chatbot "$CHART_DIR/todo-chatbot" \
        --namespace "$NAMESPACE" \
        -f "$CHART_DIR/todo-chatbot/values-aks.yaml" \
        --set backend.image.repository="$ACR_NAME.azurecr.io/todo-chatbot-backend" \
        --set backend.image.tag="$image_tag" \
        --set frontend.image.repository="$ACR_NAME.azurecr.io/todo-chatbot-frontend" \
        --set frontend.image.tag="$image_tag" \
        --wait --timeout 5m

    # Deploy phase-v-services
    log_info "Deploying phase-v-services..."
    helm upgrade --install phase-v-services "$CHART_DIR/phase-v-services" \
        --namespace "$NAMESPACE" \
        -f "$CHART_DIR/phase-v-services/values-aks.yaml" \
        --set auditService.image.repository="$ACR_NAME.azurecr.io/audit-service" \
        --set auditService.image.tag="$image_tag" \
        --set reminderService.image.repository="$ACR_NAME.azurecr.io/reminder-service" \
        --set reminderService.image.tag="$image_tag" \
        --set recurringService.image.repository="$ACR_NAME.azurecr.io/recurring-service" \
        --set recurringService.image.tag="$image_tag" \
        --wait --timeout 5m || log_warning "Phase-v-services deployment had issues"

    log_success "AKS deployment completed"

    # Show status
    echo ""
    log_info "AKS Deployment Status:"
    kubectl get pods -n "$NAMESPACE"
    echo ""
    kubectl get svc -n "$NAMESPACE" | grep -E "LoadBalancer|NAME"
}

health_check() {
    local target="$1"

    log_info "Running health checks for $target..."

    # Get backend service IP
    local backend_ip
    backend_ip=$(kubectl get svc todo-chatbot-backend -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")

    if [[ -n "$backend_ip" ]]; then
        log_info "Testing backend health at $backend_ip:8000..."
        if curl -sf "http://$backend_ip:8000/health" >/dev/null 2>&1; then
            log_success "Backend health check passed"
        else
            log_warning "Backend health check failed"
        fi
    else
        log_warning "Backend LoadBalancer IP not yet assigned"
    fi
}

# Main script
main() {
    local target="${1:-}"
    local image_tag="${2:-latest}"

    if [[ -z "$target" ]] || [[ "$target" == "-h" ]] || [[ "$target" == "--help" ]]; then
        print_usage
        exit 0
    fi

    echo "======================================"
    echo "  Manual Deployment Script"
    echo "  Phase VI: Multi-Cloud Deployment"
    echo "======================================"
    echo ""

    check_prerequisites

    case "$target" in
        gke)
            deploy_to_gke "$image_tag"
            health_check "gke"
            ;;
        aks)
            deploy_to_aks "$image_tag"
            health_check "aks"
            ;;
        both)
            deploy_to_gke "$image_tag"
            health_check "gke"
            echo ""
            echo "--------------------------------------"
            echo ""
            deploy_to_aks "$image_tag"
            health_check "aks"
            ;;
        *)
            log_error "Invalid target: $target"
            print_usage
            exit 1
            ;;
    esac

    echo ""
    echo "======================================"
    log_success "Deployment complete!"
    echo "======================================"
}

main "$@"
