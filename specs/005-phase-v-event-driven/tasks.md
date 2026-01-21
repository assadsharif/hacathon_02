# Tasks: Phase V Event-Driven Architecture

**Input**: Design documents from `/specs/005-phase-v-event-driven/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: No explicit test tasks requested in spec. Implementation includes validation.

**Organization**: Tasks grouped by functional requirement (FR-1 through FR-6 + Deployment).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: FR1=Advanced Tasks, FR2=Events, FR3=Reminders, FR4=Recurring, FR5=Audit, FR6=Sync, DR1=Deploy

## User Story Mapping

| FR | User Story | Priority | Description |
|----|------------|----------|-------------|
| FR-1 | US1 | P1 | Advanced Task Features (priority, due_date, tags, search/filter) |
| FR-2 | US2 | P1 | Event Publishing (Dapr Pub/Sub to Kafka) |
| FR-3 | US3 | P2 | Reminder Service (Dapr Jobs API) |
| FR-4 | US4 | P2 | Recurring Task Engine |
| FR-5 | US5 | P2 | Audit Log Service |
| FR-6 | US6 | P3 | Real-Time Sync (WebSocket) |
| DR-1 | US7 | P1 | Local Deployment (Minikube + Strimzi + Dapr) |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install Dapr and Strimzi on Minikube cluster

- [X] T001 Create scripts/setup-dapr.sh with Dapr Helm installation
- [X] T002 Create scripts/setup-strimzi.sh with Strimzi operator installation
- [X] T003 [P] Create charts/strimzi-kafka/kafka-cluster.yaml for single-node Kafka
- [X] T004 [P] Create charts/strimzi-kafka/kafka-topic.yaml for task-events topic
- [X] T005 Create scripts/deploy-phase-v.sh orchestration script

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database migrations and Dapr components that ALL services depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create backend/migrations/phase_v_migration.sql with schema changes from data-model.md
- [X] T007 [P] Create charts/dapr-components/pubsub-kafka.yaml from contracts/dapr-pubsub.yaml
- [X] T008 [P] Create charts/dapr-components/statestore-postgres.yaml from contracts/dapr-state.yaml
- [X] T009 [P] Create charts/dapr-components/subscriptions.yaml with all service subscriptions
- [X] T010 Update charts/todo-chatbot/templates/backend/deployment.yaml with Dapr annotations
- [X] T011 [P] Update charts/todo-chatbot/templates/frontend/deployment.yaml with Dapr annotations

**Checkpoint**: Dapr sidecars inject, Kafka running, database migrated

---

## Phase 3: User Story 1 - Advanced Task Features (Priority: P1) 🎯 MVP

**Goal**: Tasks support priority, due_date, reminder_at, recurrence, and tags

**Independent Test**: Create task via API with all new fields, verify stored correctly

### Implementation for User Story 1

- [X] T012 [P] [US1] Create backend/models/tag.py with Tag and TodoTag models
- [X] T013 [P] [US1] Extend backend/models/todo.py with priority, due_date, reminder_at, recurrence fields
- [X] T014 [US1] Create backend/services/tag_service.py for tag CRUD operations
- [X] T015 [US1] Update backend/services/todo_service.py with tag association logic
- [X] T016 [US1] Create backend/api/tags.py with /api/tags endpoints
- [X] T017 [US1] Update backend/api/todos.py with filtering, sorting, search parameters
- [X] T018 [US1] Create backend/schemas/tag.py with Pydantic request/response models
- [X] T019 [US1] Update backend/schemas/todo.py with new fields and recurrence schema
- [X] T020 [US1] Add validation rules for priority enum, due_date/reminder_at relationship

**Checkpoint**: Create/update tasks with all advanced features via API

---

## Phase 4: User Story 2 - Event Publishing (Priority: P1) 🎯 MVP

**Goal**: All task CRUD operations publish events to Kafka via Dapr

**Independent Test**: Create task, verify event appears in Kafka topic

### Implementation for User Story 2

- [X] T021 [P] [US2] Create backend/services/event_publisher.py with Dapr Pub/Sub client
- [X] T022 [P] [US2] Create backend/schemas/events.py with CloudEvents models from contracts/event-schema.json
- [X] T023 [US2] Update backend/services/todo_service.py to call event_publisher on create
- [X] T024 [US2] Update backend/services/todo_service.py to call event_publisher on update
- [X] T025 [US2] Update backend/services/todo_service.py to call event_publisher on complete
- [X] T026 [US2] Update backend/services/todo_service.py to call event_publisher on delete
- [X] T027 [US2] Add backend/api/events.py subscription endpoint for Dapr callbacks

**Checkpoint**: All CRUD operations emit events visible in Kafka

---

## Phase 5: User Story 5 - Audit Log Service (Priority: P2)

**Goal**: Immutable audit log consuming all task events

**Independent Test**: Create/update/delete tasks, verify all events in audit log

### Implementation for User Story 5

- [X] T028 [P] [US5] Create services/audit-service/requirements.txt with FastAPI, dapr dependencies
- [X] T029 [P] [US5] Create services/audit-service/Dockerfile
- [X] T030 [US5] Create services/audit-service/main.py with event handler endpoints
- [X] T031 [US5] Create services/audit-service/models.py with TaskEvent Dapr state model
- [X] T032 [US5] Create charts/phase-v-services/templates/audit/deployment.yaml with Dapr annotations
- [X] T033 [P] [US5] Create charts/phase-v-services/templates/audit/service.yaml
- [X] T034 [US5] Add GET /api/audit endpoint in backend for querying audit log via Dapr service invocation

**Checkpoint**: Query /api/audit returns all task events with timestamps

---

## Phase 6: User Story 3 - Reminder Service (Priority: P2)

**Goal**: Schedule reminders via Dapr Jobs API, notify at due time

**Independent Test**: Create task with due_date, verify reminder triggers

### Implementation for User Story 3

- [X] T035 [P] [US3] Create services/reminder-service/requirements.txt
- [X] T036 [P] [US3] Create services/reminder-service/Dockerfile
- [X] T037 [US3] Create services/reminder-service/main.py with task.created event handler
- [X] T038 [US3] Implement schedule_reminder() using Dapr Jobs API in reminder-service
- [X] T039 [US3] Implement cancel_reminder() for task.updated/deleted events
- [X] T040 [US3] Implement /job/{job-name} callback handler for triggered reminders
- [X] T041 [US3] Create charts/phase-v-services/templates/reminder/deployment.yaml
- [X] T042 [P] [US3] Create charts/phase-v-services/templates/reminder/service.yaml

**Checkpoint**: Create task with due_date, reminder fires at scheduled time

---

## Phase 7: User Story 4 - Recurring Task Engine (Priority: P2)

**Goal**: Completing recurring task auto-creates next occurrence

**Independent Test**: Complete recurring task, verify next instance created

### Implementation for User Story 4

- [X] T043 [P] [US4] Create services/recurring-service/requirements.txt
- [X] T044 [P] [US4] Create services/recurring-service/Dockerfile
- [X] T045 [US4] Create services/recurring-service/main.py with task.completed event handler
- [X] T046 [US4] Implement calculate_next_occurrence() for daily/weekly/monthly rules
- [X] T047 [US4] Implement create_next_task() via Dapr service invocation to backend
- [X] T048 [US4] Create charts/phase-v-services/templates/recurring/deployment.yaml
- [X] T049 [P] [US4] Create charts/phase-v-services/templates/recurring/service.yaml

**Checkpoint**: Complete recurring task, new task appears with next due_date

---

## Phase 8: User Story 6 - Real-Time Sync (Priority: P3)

**Goal**: Task changes propagate to all connected clients via WebSocket

**Independent Test**: Open two browser tabs, create task in one, see in other

### Implementation for User Story 6

- [X] T050 [US6] Create backend/api/websocket.py with /ws/tasks endpoint
- [X] T051 [US6] Create backend/services/connection_manager.py for WebSocket connections
- [X] T052 [US6] Update backend/api/events.py to broadcast events to WebSocket clients
- [X] T053 [US6] Create frontend/src/hooks/useTaskWebSocket.ts
- [X] T054 [US6] Update frontend/src/app/todos/page.tsx to subscribe to WebSocket
- [X] T055 [US6] Update frontend/src/app/chat/page.tsx to refresh on WebSocket events

**Checkpoint**: Real-time updates visible across multiple browser tabs

---

## Phase 9: User Story 7 - Local Deployment (Priority: P1)

**Goal**: Full Phase V deployment on Minikube with all services

**Independent Test**: Run make deploy-phase-v, access application, verify all features

### Implementation for User Story 7

- [X] T056 [US7] Create charts/phase-v-services/Chart.yaml
- [X] T057 [US7] Create charts/phase-v-services/values.yaml with default configurations
- [X] T058 [US7] Update Makefile with phase-v targets (setup-dapr, setup-strimzi, deploy-phase-v)
- [X] T059 [US7] Create scripts/validate-phase-v.sh with health checks for all services
- [X] T060 [US7] Build Docker images for all three new services in Minikube
- [ ] T061 [US7] End-to-end validation: create recurring task with reminder, complete it, verify audit

**Checkpoint**: Full Phase V deployed and functional on Minikube

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, cleanup, and hardening

- [ ] T062 [P] Update README.md with Phase V setup instructions
- [X] T063 [P] Create .env.example with new Phase V environment variables
- [X] T064 Add error handling for Dapr connection failures in event_publisher.py
- [X] T065 Add retry logic for Kafka connectivity issues
- [ ] T066 [P] Update frontend UI to display priority, due_date, tags on task cards
- [ ] T067 Run quickstart.md validation to verify setup guide accuracy

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ──────────────────────────────────────────────────────────────┐
                                                                               │
Phase 2 (Foundational) ◀──────────────────────────────────────────────────────┘
         │
         │ BLOCKS all user stories
         ▼
    ┌────┴────┬────────────┬────────────┬────────────┬────────────┐
    │         │            │            │            │            │
    ▼         ▼            ▼            ▼            ▼            ▼
Phase 3    Phase 4     Phase 5     Phase 6     Phase 7     Phase 9
  US1        US2         US5         US3         US4         US7
  (P1)       (P1)        (P2)        (P2)        (P2)        (P1)
    │         │            │            │            │            │
    └────┬────┴────────────┴────────────┴────────────┘            │
         │                                                         │
         ▼                                                         │
      Phase 8 (US6 - Real-Time Sync) ◀─────────────────────────────┘
         │     Depends on US2 (events flowing)
         ▼
      Phase 10 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|----------------------|
| US1 (Advanced Tasks) | Phase 2 | US2, US5, US7 |
| US2 (Event Publishing) | Phase 2 | US1, US5, US7 |
| US3 (Reminders) | US2 (events) | US4, US5 |
| US4 (Recurring) | US2 (events) | US3, US5 |
| US5 (Audit) | US2 (events) | US3, US4 |
| US6 (Real-Time) | US2 (events) | - |
| US7 (Deployment) | All services | - |

### Parallel Opportunities

**Phase 1 (can all run in parallel)**:
```bash
# All setup scripts
T001 setup-dapr.sh
T002 setup-strimzi.sh
T003 kafka-cluster.yaml
T004 kafka-topic.yaml
```

**Phase 2 (can all run in parallel)**:
```bash
# All Dapr components
T007 pubsub-kafka.yaml
T008 statestore-postgres.yaml
T009 subscriptions.yaml
T010 backend deployment.yaml
T011 frontend deployment.yaml
```

**User Stories 1, 2, 5 (can all run in parallel after Phase 2)**:
```bash
# Different services/files
US1: backend/models/tag.py, backend/services/tag_service.py
US2: backend/services/event_publisher.py
US5: services/audit-service/*
```

---

## Summary

| Phase | Tasks | Parallel | Description |
|-------|-------|----------|-------------|
| 1 - Setup | 5 | 3 | Dapr + Strimzi installation |
| 2 - Foundational | 6 | 4 | Migrations + Dapr components |
| 3 - US1 Advanced Tasks | 9 | 2 | Priority, due_date, tags, search |
| 4 - US2 Event Publishing | 7 | 2 | Dapr Pub/Sub to Kafka |
| 5 - US5 Audit Log | 7 | 3 | Event consumer service |
| 6 - US3 Reminders | 8 | 3 | Dapr Jobs API scheduler |
| 7 - US4 Recurring | 7 | 3 | Task recurrence engine |
| 8 - US6 Real-Time | 6 | 0 | WebSocket sync |
| 9 - US7 Deployment | 6 | 0 | Full deployment validation |
| 10 - Polish | 6 | 3 | Documentation + hardening |
| **TOTAL** | **67** | **23** | |

### MVP Scope (Recommended)

1. Phase 1: Setup
2. Phase 2: Foundational
3. Phase 3: US1 (Advanced Tasks)
4. Phase 4: US2 (Event Publishing)
5. Phase 9: US7 (Deployment)

**MVP = 33 tasks** - delivers advanced tasks with event publishing to Kafka

### Incremental Delivery

1. **MVP**: Setup + Foundational + US1 + US2 + US7 → Events flowing to Kafka
2. **+Audit**: US5 → Immutable event log
3. **+Reminders**: US3 → Scheduled notifications
4. **+Recurring**: US4 → Auto-regenerating tasks
5. **+Real-Time**: US6 → Multi-client sync
6. **+Polish**: Documentation and hardening
