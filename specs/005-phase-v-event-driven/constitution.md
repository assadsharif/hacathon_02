# Phase V – Constitution (WHY)

## Purpose
Phase V upgrades the Todo Chatbot into a **production-grade, cloud-native, event-driven system**
deployed on managed Kubernetes with **Dapr and Kafka**, while strictly following
Spec-Driven Development.

## Non-Negotiable Principles

### 1. Spec-Driven Development is mandatory
- No code without an approved Task ID.
- No tasks without Plan.
- No plan without Specify.
- Constitution overrides all files.

### 2. Event-Driven Architecture
- All task lifecycle events MUST be published via Kafka (through Dapr Pub/Sub).
- No synchronous coupling between services for reminders or recurring tasks.

### 3. Dapr First
- Applications MUST interact with infrastructure only through Dapr APIs:
  - Pub/Sub
  - State
  - Jobs API
  - Secrets
  - Service Invocation
- Direct Kafka or DB client usage is forbidden unless explicitly approved.

### 4. Cloud Portability
- Same Helm charts must deploy on:
  - Minikube (local)
  - Managed Kubernetes (AKS / GKE / OKE)
- No cloud-specific hardcoding.

### 5. Security by Default
- No secrets committed to Git.
- Secrets stored via Kubernetes Secrets or Dapr Secret Store.
- TLS and authentication delegated to platform defaults.

### 6. Observability
- Logging and monitoring MUST be enabled for all services.
- Failures must be diagnosable via Kubernetes-native tools.

### 7. No Vibe Coding
- Claude Code must STOP if any requirement is underspecified.
