# Implementation Plan: Phase V Event-Driven Architecture

**Branch**: `005-phase-v-event-driven` | **Date**: 2026-01-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-phase-v-event-driven/spec.md`

## Summary

Upgrade the Todo Chatbot into a production-grade, cloud-native, event-driven system deployed on Kubernetes with Dapr and Kafka. All task lifecycle events (created, updated, completed, deleted) will be published via Dapr Pub/Sub to Kafka topics. New services include a Reminder Service (Dapr Jobs API), Recurring Task Engine, and Audit Log Service. Advanced task features (due dates, priorities, tags, recurring rules) will be added to the data model.

## Technical Context

**Language/Version**: Python 3.11 (Backend), Node 20 (Frontend)
**Primary Dependencies**: FastAPI, Dapr SDK, Strimzi Kafka Operator
**Storage**: PostgreSQL (existing) + Dapr State Store for service state
**Testing**: pytest, Dapr test containers
**Target Platform**: Kubernetes (Minikube local, managed K8s cloud)
**Project Type**: Web (backend/frontend) + microservices (reminder, audit, recurring)
**Performance Goals**: Event delivery <500ms p95, real-time sync <1s
**Constraints**: Dapr-only infrastructure access (no direct Kafka/DB clients in new services)
**Scale/Scope**: Single cluster, 3 new microservices, 4 event types

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| 1. Spec-Driven Development | ✅ PASS | Using /sp.plan workflow |
| 2. Event-Driven Architecture | ✅ PASS | All task events via Dapr Pub/Sub to Kafka |
| 3. Dapr First | ✅ PASS | Pub/Sub, State, Jobs API, Service Invocation |
| 4. Cloud Portability | ✅ PASS | Helm charts for Minikube and managed K8s |
| 5. Security by Default | ✅ PASS | Secrets via K8s Secrets/Dapr Secret Store |
| 6. Observability | ✅ PASS | Kubernetes-native logging/monitoring |
| 7. No Vibe Coding | ✅ PASS | Full spec provided before implementation |

**Phase V Constitution Compliance**: All 7 non-negotiable principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/005-phase-v-event-driven/
├── constitution.md      # Phase V principles (WHY)
├── spec.md              # Phase V requirements (WHAT)
├── plan.md              # This file (HOW)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (event schemas, API specs)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   └── task.py          # Extended with due_date, priority, tags, recurrence
│   ├── services/
│   │   ├── task_service.py  # Modified to publish events
│   │   └── event_publisher.py  # Dapr Pub/Sub client
│   └── api/
│       └── tasks.py         # Existing endpoints (enhanced)
└── tests/
    └── test_events.py       # Event publishing tests

services/
├── reminder-service/        # NEW: Dapr Jobs API scheduler
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── audit-service/           # NEW: Event consumer, immutable log
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── recurring-service/       # NEW: Recurring task generator
    ├── Dockerfile
    ├── main.py
    └── requirements.txt

charts/
├── todo-chatbot/            # Existing (enhanced with Dapr annotations)
├── strimzi-kafka/           # NEW: Kafka cluster via Strimzi
├── dapr-components/         # NEW: Pub/Sub, State, Jobs configs
└── phase-v-services/        # NEW: Reminder, Audit, Recurring deployments

scripts/
├── setup-strimzi.sh         # Install Strimzi operator
├── setup-dapr.sh            # Install Dapr runtime
└── deploy-phase-v.sh        # Full Phase V deployment
```

**Structure Decision**: Microservices architecture with 3 new services (reminder, audit, recurring) deployed alongside existing backend/frontend. All services communicate via Dapr Pub/Sub (Kafka).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 3 new microservices | Event-driven decoupling required by constitution | Monolithic event handlers would violate "no synchronous coupling" principle |
| Strimzi Operator | Kubernetes-native Kafka per spec | External Kafka harder to deploy locally |
| Dapr Jobs API | No-polling reminder system required | Cron/polling explicitly forbidden by spec |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Kubernetes Cluster                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐ │
│  │  Frontend   │    │   Backend   │    │   Dapr Sidecar (daprd)  │ │
│  │  (Next.js)  │───▶│  (FastAPI)  │◀──▶│  - Pub/Sub             │ │
│  └─────────────┘    └──────┬──────┘    │  - State               │ │
│                            │           │  - Service Invocation  │ │
│                            ▼           └───────────┬─────────────┘ │
│                    ┌───────────────┐               │               │
│                    │  PostgreSQL   │               │               │
│                    └───────────────┘               │               │
│                                                    │               │
│  ┌─────────────────────────────────────────────────┼───────────────┤
│  │                    Kafka (Strimzi)              │               │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐  │               │
│  │  │task.created│ │task.updated│ │task.deleted│  │               │
│  │  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘  │               │
│  └────────┼──────────────┼──────────────┼─────────┘               │
│           │              │              │                          │
│           ▼              ▼              ▼                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │   Reminder  │  │    Audit    │  │  Recurring  │                │
│  │   Service   │  │   Service   │  │   Service   │                │
│  │ (Jobs API)  │  │ (Consumer)  │  │ (Consumer)  │                │
│  └─────────────┘  └─────────────┘  └─────────────┘                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Decisions

1. **Event Topics**: Single Kafka topic `task-events` with event type in payload (simpler than 4 separate topics)
2. **Dapr Pub/Sub**: Use `pubsub.kafka` component bound to Strimzi cluster
3. **State Management**: Audit log uses Dapr State Store (PostgreSQL-backed) for immutability
4. **Jobs API**: Reminder service schedules one-time jobs via Dapr Jobs API
5. **Real-Time Sync**: WebSocket connection from frontend subscribes to Dapr pub/sub via backend

## Dependencies

| Component | Version | Source |
|-----------|---------|--------|
| Dapr | 1.14+ | `helm install dapr dapr/dapr` |
| Strimzi | 0.43+ | `kubectl apply -f strimzi-cluster-operator` |
| Kafka | 3.7+ | Via Strimzi |
| daprd sidecar | 1.14+ | Auto-injected via annotations |

## Risk Analysis

| Risk | Mitigation |
|------|------------|
| Strimzi complexity | Use minimal single-node Kafka config for local |
| Dapr learning curve | Follow official quickstarts, test in isolation |
| Event ordering | Use partition key (user_id) for ordering guarantees |

## Next Steps

1. **Phase 0**: Create `research.md` with Dapr/Strimzi best practices
2. **Phase 1**: Create `data-model.md` with extended Task schema
3. **Phase 1**: Create `contracts/` with event schemas
4. **Phase 2**: Generate `tasks.md` via `/sp.tasks`
