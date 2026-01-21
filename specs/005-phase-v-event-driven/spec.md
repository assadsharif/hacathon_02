# Phase V – Specification (WHAT)

## Scope
Upgrade the Todo Chatbot with **advanced task features**, **event-driven services**, and
**cloud-native deployment**.

---

## Functional Requirements

### FR-1: Advanced Task Features
- Tasks MUST support:
  - Recurring rules (daily, weekly, monthly)
  - Due dates
  - Scheduled reminders
  - Priorities
  - Tags
  - Search, filter, and sorting

### FR-2: Event Publishing
- Every task action MUST emit an event:
  - `task.created`
  - `task.updated`
  - `task.completed`
  - `task.deleted`
- Events MUST be published to Kafka via Dapr Pub/Sub.

### FR-3: Reminder System
- When a task has a due date:
  - A reminder event MUST be scheduled.
  - Notification MUST be sent at the exact time.
- Implementation MUST use Dapr Jobs API (no polling).

### FR-4: Recurring Task Engine
- Completing a recurring task MUST:
  - Publish a task event.
  - Trigger creation of the next occurrence asynchronously.

### FR-5: Audit Log
- All task events MUST be consumed by an audit service.
- Audit history MUST be immutable.

### FR-6: Real-Time Sync
- Task changes MUST propagate to all connected clients in near real-time.

---

## Deployment Requirements

### DR-1: Local Deployment
- Deploy on Minikube.
- Kafka MUST run locally via Strimzi Operator.
- Dapr MUST be enabled on all application pods.

### DR-2: Cloud Deployment
- Deploy to managed Kubernetes (AKS / GKE / OKE).
- Kafka MUST be managed (Redpanda Cloud or equivalent).
- CI/CD MUST deploy via GitHub Actions.

---

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| K8s Platform (Primary) | Minikube | Local-first development |
| Kafka Deployment | Strimzi Operator | Kubernetes-native, cloud-portable |
| Event Scope | Core CRUD | task.created, task.updated, task.completed, task.deleted |
| Service Mesh | Dapr | Pub/Sub, State, Jobs, Secrets, Service Invocation |

---

## Acceptance Criteria
- [ ] All advanced task features demonstrable via UI and API
- [ ] Kafka topics actively producing/consuming events
- [ ] Dapr sidecars visible on all application pods
- [ ] Audit log capturing all task events
- [ ] Reminder notifications triggered at scheduled times
- [ ] Recurring tasks auto-generate next occurrence
- [ ] Real-time sync working across multiple clients
- [ ] Cloud deployment reachable via public URL
