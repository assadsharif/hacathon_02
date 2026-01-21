#!/bin/bash
# [Task]: T059
# Phase V Deployment Validation Script
# Validates all Phase V components are running correctly

set -e

echo "============================================="
echo "Phase V Deployment Validation"
echo "============================================="
echo ""

# Configuration
NAMESPACE="${NAMESPACE:-todo-chatbot}"
KAFKA_NAMESPACE="kafka"
DAPR_NAMESPACE="dapr-system"
TIMEOUT=120

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    PASSED=$((PASSED + 1))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    FAILED=$((FAILED + 1))
}

check_warn() {
    echo -e "${YELLOW}!${NC} $1"
}

# =============================================
# 1. Dapr System Components
# =============================================
echo "1. Checking Dapr System Components..."

# Check Dapr pods
DAPR_PODS=$(kubectl get pods -n $DAPR_NAMESPACE --no-headers 2>/dev/null | grep -c "Running" || echo "0")
if [ "$DAPR_PODS" -ge 3 ]; then
    check_pass "Dapr system pods running ($DAPR_PODS pods)"
else
    check_fail "Dapr system pods not ready ($DAPR_PODS/3 running)"
fi

# Check dapr-operator
if kubectl get deployment dapr-operator -n $DAPR_NAMESPACE &>/dev/null; then
    check_pass "Dapr operator deployed"
else
    check_fail "Dapr operator not found"
fi

echo ""

# =============================================
# 2. Strimzi Kafka
# =============================================
echo "2. Checking Strimzi Kafka..."

# Check Strimzi operator
STRIMZI_OPERATOR=$(kubectl get pods -n $KAFKA_NAMESPACE -l name=strimzi-cluster-operator --no-headers 2>/dev/null | grep -c "Running" || echo "0")
if [ "$STRIMZI_OPERATOR" -ge 1 ]; then
    check_pass "Strimzi operator running"
else
    check_fail "Strimzi operator not running"
fi

# Check Kafka cluster
KAFKA_STATUS=$(kubectl get kafka todo-kafka -n $KAFKA_NAMESPACE -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' 2>/dev/null || echo "False")
if [ "$KAFKA_STATUS" == "True" ]; then
    check_pass "Kafka cluster ready"
else
    check_warn "Kafka cluster not fully ready (status: $KAFKA_STATUS)"
fi

# Check Kafka topic
TOPIC_STATUS=$(kubectl get kafkatopic task-events -n $KAFKA_NAMESPACE -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' 2>/dev/null || echo "False")
if [ "$TOPIC_STATUS" == "True" ]; then
    check_pass "task-events topic ready"
else
    check_warn "task-events topic not ready (status: $TOPIC_STATUS)"
fi

echo ""

# =============================================
# 3. Dapr Components
# =============================================
echo "3. Checking Dapr Components..."

# Check pubsub-kafka component
if kubectl get component pubsub-kafka -n $NAMESPACE &>/dev/null; then
    check_pass "Dapr pubsub-kafka component deployed"
else
    check_fail "Dapr pubsub-kafka component not found"
fi

# Check statestore-postgres component
if kubectl get component statestore-postgres -n $NAMESPACE &>/dev/null; then
    check_pass "Dapr statestore-postgres component deployed"
else
    check_fail "Dapr statestore-postgres component not found"
fi

# Check subscriptions
if kubectl get subscription task-events-backend -n $NAMESPACE &>/dev/null; then
    check_pass "Dapr subscriptions deployed"
else
    check_warn "Dapr subscriptions not found"
fi

echo ""

# =============================================
# 4. Phase V Microservices
# =============================================
echo "4. Checking Phase V Microservices..."

# Check audit-service
AUDIT_RUNNING=$(kubectl get pods -n $NAMESPACE -l app=audit-service --no-headers 2>/dev/null | grep -c "Running" || echo "0")
if [ "$AUDIT_RUNNING" -ge 1 ]; then
    check_pass "Audit service running"
else
    check_warn "Audit service not running"
fi

# Check reminder-service
REMINDER_RUNNING=$(kubectl get pods -n $NAMESPACE -l app=reminder-service --no-headers 2>/dev/null | grep -c "Running" || echo "0")
if [ "$REMINDER_RUNNING" -ge 1 ]; then
    check_pass "Reminder service running"
else
    check_warn "Reminder service not running"
fi

# Check recurring-service
RECURRING_RUNNING=$(kubectl get pods -n $NAMESPACE -l app=recurring-service --no-headers 2>/dev/null | grep -c "Running" || echo "0")
if [ "$RECURRING_RUNNING" -ge 1 ]; then
    check_pass "Recurring service running"
else
    check_warn "Recurring service not running"
fi

echo ""

# =============================================
# 5. Backend Dapr Sidecar
# =============================================
echo "5. Checking Backend Dapr Integration..."

# Check if backend has Dapr sidecar
BACKEND_POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
if [ -n "$BACKEND_POD" ]; then
    SIDECAR_COUNT=$(kubectl get pod $BACKEND_POD -n $NAMESPACE -o jsonpath='{.spec.containers[*].name}' 2>/dev/null | tr ' ' '\n' | grep -c "daprd" || echo "0")
    if [ "$SIDECAR_COUNT" -ge 1 ]; then
        check_pass "Backend has Dapr sidecar"
    else
        check_warn "Backend missing Dapr sidecar"
    fi
else
    check_fail "Backend pod not found"
fi

echo ""

# =============================================
# 6. Health Checks
# =============================================
echo "6. Running Health Checks..."

# Check audit service health (if running)
if [ "$AUDIT_RUNNING" -ge 1 ]; then
    AUDIT_POD=$(kubectl get pods -n $NAMESPACE -l app=audit-service -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    AUDIT_HEALTH=$(kubectl exec $AUDIT_POD -n $NAMESPACE -- curl -s http://localhost:8001/health 2>/dev/null | grep -c "healthy" || echo "0")
    if [ "$AUDIT_HEALTH" -ge 1 ]; then
        check_pass "Audit service health check passed"
    else
        check_warn "Audit service health check failed"
    fi
fi

echo ""

# =============================================
# Summary
# =============================================
echo "============================================="
echo "Validation Summary"
echo "============================================="
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}Phase V deployment validation PASSED${NC}"
    exit 0
else
    echo -e "${YELLOW}Phase V deployment has issues - review warnings above${NC}"
    exit 1
fi
