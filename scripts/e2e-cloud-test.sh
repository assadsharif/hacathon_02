#!/bin/bash
# [Task]: T061
# Phase VI: End-to-End Cloud Test Script
# Tests the deployed application on GKE or AKS
#
# Usage:
#   ./scripts/e2e-cloud-test.sh [gke|aks]
#
# Examples:
#   ./scripts/e2e-cloud-test.sh aks
#   ./scripts/e2e-cloud-test.sh gke

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Configuration
NAMESPACE="todo-chatbot"
TEST_USER_EMAIL="e2e-test-$(date +%s)@example.com"
TEST_USER_PASSWORD="TestPassword123!"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((TESTS_PASSED++))
    ((TESTS_TOTAL++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((TESTS_FAILED++))
    ((TESTS_TOTAL++))
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_usage() {
    echo "Usage: $0 [gke|aks]"
    echo ""
    echo "Arguments:"
    echo "  target     Target cloud: gke or aks"
    echo ""
    echo "Examples:"
    echo "  $0 aks"
    echo "  $0 gke"
}

get_service_ip() {
    local service_name=$1
    kubectl get svc "$service_name" -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo ""
}

switch_context() {
    local target=$1

    if [[ "$target" == "gke" ]]; then
        log_info "Switching to GKE context..."
        gcloud container clusters get-credentials todo-chatbot --zone us-central1-a 2>/dev/null || {
            log_warning "Could not switch to GKE context"
            return 1
        }
    elif [[ "$target" == "aks" ]]; then
        log_info "Switching to AKS context..."
        az aks get-credentials --resource-group todo-chatbot-rg --name todo-chatbot --overwrite-existing 2>/dev/null || {
            log_warning "Could not switch to AKS context"
            return 1
        }
    fi

    log_success "Switched to $target context"
}

# Test functions
test_cluster_connectivity() {
    log_info "Testing cluster connectivity..."

    if kubectl cluster-info &>/dev/null; then
        log_success "Cluster is accessible"
    else
        log_fail "Cannot connect to cluster"
        return 1
    fi
}

test_pods_running() {
    log_info "Checking pod status..."

    local running_pods
    running_pods=$(kubectl get pods -n "$NAMESPACE" --no-headers 2>/dev/null | grep -c "Running" || echo "0")

    if [[ "$running_pods" -ge 5 ]]; then
        log_success "All pods are running ($running_pods pods)"
    else
        log_fail "Expected at least 5 running pods, found $running_pods"
        kubectl get pods -n "$NAMESPACE"
    fi
}

test_dapr_sidecars() {
    log_info "Checking Dapr sidecars..."

    local pods_with_sidecars
    pods_with_sidecars=$(kubectl get pods -n "$NAMESPACE" --no-headers 2>/dev/null | awk '{print $2}' | grep -c "2/2" || echo "0")

    if [[ "$pods_with_sidecars" -ge 4 ]]; then
        log_success "Dapr sidecars injected ($pods_with_sidecars pods with 2/2 containers)"
    else
        log_fail "Expected at least 4 pods with Dapr sidecars, found $pods_with_sidecars"
    fi
}

test_backend_health() {
    local backend_ip=$1

    log_info "Testing backend health endpoint..."

    if [[ -z "$backend_ip" ]]; then
        log_fail "Backend IP not available"
        return 1
    fi

    local response
    response=$(curl -s --connect-timeout 10 "http://$backend_ip:8000/health" 2>/dev/null || echo "")

    if echo "$response" | grep -q "healthy"; then
        log_success "Backend health check passed"
    else
        log_fail "Backend health check failed"
        echo "Response: $response"
    fi
}

test_frontend_accessible() {
    local frontend_ip=$1

    log_info "Testing frontend accessibility..."

    if [[ -z "$frontend_ip" ]]; then
        log_fail "Frontend IP not available"
        return 1
    fi

    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 "http://$frontend_ip:3000/" 2>/dev/null || echo "000")

    if [[ "$http_code" == "200" ]]; then
        log_success "Frontend is accessible (HTTP $http_code)"
    else
        log_fail "Frontend returned HTTP $http_code"
    fi
}

test_api_docs() {
    local backend_ip=$1

    log_info "Testing API documentation endpoint..."

    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 "http://$backend_ip:8000/docs" 2>/dev/null || echo "000")

    if [[ "$http_code" == "200" ]]; then
        log_success "API docs accessible (HTTP $http_code)"
    else
        log_fail "API docs returned HTTP $http_code"
    fi
}

test_user_signup() {
    local backend_ip=$1

    log_info "Testing user signup..."

    local response
    response=$(curl -s --connect-timeout 10 -X POST "http://$backend_ip:8000/api/auth/sign-up" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$TEST_USER_EMAIL\", \"password\": \"$TEST_USER_PASSWORD\", \"name\": \"E2E Test User\"}" 2>/dev/null || echo "")

    if echo "$response" | grep -qE "(token|id|email)"; then
        log_success "User signup successful"
        echo "$response" > /tmp/e2e_signup_response.json
    else
        # User might already exist, try signin
        log_warning "Signup failed, trying signin (user may already exist)"
        test_user_signin "$backend_ip"
        return $?
    fi
}

test_user_signin() {
    local backend_ip=$1

    log_info "Testing user signin..."

    local response
    response=$(curl -s --connect-timeout 10 -X POST "http://$backend_ip:8000/api/auth/sign-in" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$TEST_USER_EMAIL\", \"password\": \"$TEST_USER_PASSWORD\"}" 2>/dev/null || echo "")

    if echo "$response" | grep -qE "(token|access_token)"; then
        log_success "User signin successful"
        # Extract token for subsequent requests
        AUTH_TOKEN=$(echo "$response" | grep -oP '"(access_)?token"\s*:\s*"\K[^"]+' | head -1)
        export AUTH_TOKEN
    else
        log_fail "User signin failed"
        echo "Response: $response"
    fi
}

test_create_todo() {
    local backend_ip=$1

    log_info "Testing todo creation..."

    if [[ -z "${AUTH_TOKEN:-}" ]]; then
        log_warning "No auth token available, skipping todo creation test"
        return
    fi

    local response
    response=$(curl -s --connect-timeout 10 -X POST "http://$backend_ip:8000/api/todos/" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        -d "{\"title\": \"E2E Test Todo $(date +%s)\", \"description\": \"Created by e2e-cloud-test.sh\"}" 2>/dev/null || echo "")

    if echo "$response" | grep -qE "(id|title)"; then
        log_success "Todo creation successful"
        TODO_ID=$(echo "$response" | grep -oP '"id"\s*:\s*\K[0-9]+' | head -1)
        export TODO_ID
    else
        log_fail "Todo creation failed"
        echo "Response: $response"
    fi
}

test_list_todos() {
    local backend_ip=$1

    log_info "Testing todo listing..."

    if [[ -z "${AUTH_TOKEN:-}" ]]; then
        log_warning "No auth token available, skipping todo listing test"
        return
    fi

    local response
    response=$(curl -s --connect-timeout 10 -X GET "http://$backend_ip:8000/api/todos/" \
        -H "Authorization: Bearer $AUTH_TOKEN" 2>/dev/null || echo "")

    if echo "$response" | grep -qE "(\[|\{)"; then
        log_success "Todo listing successful"
    else
        log_fail "Todo listing failed"
        echo "Response: $response"
    fi
}

test_dapr_components() {
    log_info "Checking Dapr components..."

    local components
    components=$(kubectl get components -n "$NAMESPACE" --no-headers 2>/dev/null | wc -l || echo "0")

    if [[ "$components" -ge 1 ]]; then
        log_success "Dapr components configured ($components components)"
        kubectl get components -n "$NAMESPACE" --no-headers 2>/dev/null | while read -r line; do
            echo "  - $line"
        done
    else
        log_fail "No Dapr components found"
    fi
}

test_services_have_endpoints() {
    log_info "Checking service endpoints..."

    local services_with_endpoints=0
    local services=("todo-chatbot-backend" "todo-chatbot-frontend")

    for svc in "${services[@]}"; do
        local ip
        ip=$(get_service_ip "$svc")
        if [[ -n "$ip" ]]; then
            ((services_with_endpoints++))
            log_info "  $svc: $ip"
        else
            log_warning "  $svc: No external IP"
        fi
    done

    if [[ "$services_with_endpoints" -ge 2 ]]; then
        log_success "All main services have external IPs"
    else
        log_fail "Some services missing external IPs"
    fi
}

test_monitoring_stack() {
    log_info "Checking monitoring stack..."

    local monitoring_pods
    monitoring_pods=$(kubectl get pods -n monitoring --no-headers 2>/dev/null | grep -c "Running" || echo "0")

    if [[ "$monitoring_pods" -ge 3 ]]; then
        log_success "Monitoring stack running ($monitoring_pods pods)"
    else
        log_warning "Monitoring stack may not be fully deployed ($monitoring_pods pods)"
    fi
}

print_summary() {
    echo ""
    echo "========================================"
    echo "  E2E Test Summary"
    echo "========================================"
    echo ""
    echo -e "  Total Tests:  $TESTS_TOTAL"
    echo -e "  ${GREEN}Passed:${NC}       $TESTS_PASSED"
    echo -e "  ${RED}Failed:${NC}       $TESTS_FAILED"
    echo ""

    if [[ "$TESTS_FAILED" -eq 0 ]]; then
        echo -e "  ${GREEN}All tests passed!${NC}"
        return 0
    else
        echo -e "  ${RED}Some tests failed.${NC}"
        return 1
    fi
}

# Main script
main() {
    local target="${1:-}"

    if [[ -z "$target" ]] || [[ "$target" == "-h" ]] || [[ "$target" == "--help" ]]; then
        print_usage
        exit 0
    fi

    if [[ "$target" != "gke" ]] && [[ "$target" != "aks" ]]; then
        echo "Error: Invalid target '$target'. Use 'gke' or 'aks'."
        exit 1
    fi

    echo "========================================"
    echo "  E2E Cloud Test - $target"
    echo "  Phase VI: Multi-Cloud Deployment"
    echo "========================================"
    echo ""

    # Switch to correct context
    switch_context "$target" || {
        echo "Failed to switch context. Exiting."
        exit 1
    }

    echo ""
    echo "--- Infrastructure Tests ---"
    test_cluster_connectivity
    test_pods_running
    test_dapr_sidecars
    test_dapr_components
    test_services_have_endpoints
    test_monitoring_stack

    echo ""
    echo "--- Application Tests ---"

    # Get service IPs
    BACKEND_IP=$(get_service_ip "todo-chatbot-backend")
    FRONTEND_IP=$(get_service_ip "todo-chatbot-frontend")

    log_info "Backend IP: ${BACKEND_IP:-Not available}"
    log_info "Frontend IP: ${FRONTEND_IP:-Not available}"
    echo ""

    if [[ -n "$BACKEND_IP" ]]; then
        test_backend_health "$BACKEND_IP"
        test_api_docs "$BACKEND_IP"
        test_user_signup "$BACKEND_IP"
        test_create_todo "$BACKEND_IP"
        test_list_todos "$BACKEND_IP"
    else
        log_fail "Backend IP not available, skipping API tests"
    fi

    if [[ -n "$FRONTEND_IP" ]]; then
        test_frontend_accessible "$FRONTEND_IP"
    else
        log_fail "Frontend IP not available, skipping frontend tests"
    fi

    print_summary
}

main "$@"
