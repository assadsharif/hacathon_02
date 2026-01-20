#!/bin/bash
# Phase IV: Deployment Validation Script
# This script validates the Todo Chatbot deployment

set -e

# Configuration
CLUSTER_NAME="todo-chatbot"
NAMESPACE="todo-chatbot"
HOST="todo-chatbot.local"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Todo Chatbot - Deployment Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Helper functions
check_pass() {
    echo -e "  ${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "  ${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "  ${YELLOW}!${NC} $1"
    ((WARNINGS++))
}

# Check if minikube cluster is running
echo -e "${BLUE}[1/7] Checking Minikube Cluster${NC}"
if minikube status -p "$CLUSTER_NAME" &> /dev/null; then
    check_pass "Minikube cluster '$CLUSTER_NAME' is running"
else
    check_fail "Minikube cluster '$CLUSTER_NAME' is not running"
    echo -e "${RED}Please run: make setup${NC}"
    exit 1
fi

# Set kubectl context
kubectl config use-context "$CLUSTER_NAME" &> /dev/null

# Check namespace exists
echo ""
echo -e "${BLUE}[2/7] Checking Namespace${NC}"
if kubectl get namespace "$NAMESPACE" &> /dev/null; then
    check_pass "Namespace '$NAMESPACE' exists"
else
    check_fail "Namespace '$NAMESPACE' does not exist"
fi

# Check pods status
echo ""
echo -e "${BLUE}[3/7] Checking Pod Status${NC}"

# Database pod
DB_PODS=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/component=database -o jsonpath='{.items[*].status.phase}' 2>/dev/null)
if [[ "$DB_PODS" == *"Running"* ]]; then
    check_pass "Database pod is running"
else
    check_fail "Database pod is not running (status: $DB_PODS)"
fi

# Backend pod
BACKEND_PODS=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/component=backend -o jsonpath='{.items[*].status.phase}' 2>/dev/null)
if [[ "$BACKEND_PODS" == *"Running"* ]]; then
    check_pass "Backend pod is running"
else
    check_fail "Backend pod is not running (status: $BACKEND_PODS)"
fi

# Frontend pod
FRONTEND_PODS=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/component=frontend -o jsonpath='{.items[*].status.phase}' 2>/dev/null)
if [[ "$FRONTEND_PODS" == *"Running"* ]]; then
    check_pass "Frontend pod is running"
else
    check_fail "Frontend pod is not running (status: $FRONTEND_PODS)"
fi

# Check services
echo ""
echo -e "${BLUE}[4/7] Checking Services${NC}"

if kubectl get service -n "$NAMESPACE" -l app.kubernetes.io/component=database &> /dev/null; then
    check_pass "Database service exists"
else
    check_fail "Database service not found"
fi

if kubectl get service -n "$NAMESPACE" -l app.kubernetes.io/component=backend &> /dev/null; then
    check_pass "Backend service exists"
else
    check_fail "Backend service not found"
fi

if kubectl get service -n "$NAMESPACE" -l app.kubernetes.io/component=frontend &> /dev/null; then
    check_pass "Frontend service exists"
else
    check_fail "Frontend service not found"
fi

# Check ingress
echo ""
echo -e "${BLUE}[5/7] Checking Ingress${NC}"

if kubectl get ingress -n "$NAMESPACE" &> /dev/null; then
    INGRESS_HOST=$(kubectl get ingress -n "$NAMESPACE" -o jsonpath='{.items[0].spec.rules[0].host}' 2>/dev/null)
    if [[ "$INGRESS_HOST" == "$HOST" ]]; then
        check_pass "Ingress configured for host: $HOST"
    else
        check_warn "Ingress host mismatch: expected $HOST, got $INGRESS_HOST"
    fi
else
    check_fail "Ingress not found"
fi

# Check PVC for database
echo ""
echo -e "${BLUE}[6/7] Checking Persistent Volume Claims${NC}"

PVC_STATUS=$(kubectl get pvc -n "$NAMESPACE" -o jsonpath='{.items[0].status.phase}' 2>/dev/null)
if [[ "$PVC_STATUS" == "Bound" ]]; then
    check_pass "Database PVC is bound"
else
    check_warn "Database PVC status: $PVC_STATUS"
fi

# Health checks
echo ""
echo -e "${BLUE}[7/7] Running Health Checks${NC}"

MINIKUBE_IP=$(minikube ip -p "$CLUSTER_NAME" 2>/dev/null)

# Check if host is resolvable
if grep -q "$HOST" /etc/hosts 2>/dev/null; then
    check_pass "Host entry exists in /etc/hosts"

    # Try backend health check
    if curl -s --connect-timeout 5 "http://$HOST/health" | grep -q "healthy" 2>/dev/null; then
        check_pass "Backend health check passed"
    else
        check_warn "Backend health check failed (may need time to start)"
    fi

    # Try frontend
    if curl -s --connect-timeout 5 "http://$HOST/" | grep -q "html" 2>/dev/null; then
        check_pass "Frontend is responding"
    else
        check_warn "Frontend not responding (may need time to start)"
    fi
else
    check_warn "Host entry not found in /etc/hosts"
    echo -e "     Run: ${YELLOW}echo \"$MINIKUBE_IP $HOST\" | sudo tee -a /etc/hosts${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Validation Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "  ${GREEN}Passed:${NC}   $PASSED"
echo -e "  ${RED}Failed:${NC}   $FAILED"
echo -e "  ${YELLOW}Warnings:${NC} $WARNINGS"
echo ""

if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}All critical checks passed!${NC}"
    echo ""
    echo -e "Access the application at: ${BLUE}http://$HOST${NC}"
    exit 0
else
    echo -e "${RED}Some checks failed. Please review the issues above.${NC}"
    exit 1
fi
