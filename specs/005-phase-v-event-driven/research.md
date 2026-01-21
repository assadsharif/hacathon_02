# Phase V Research: Event-Driven Architecture

**Date**: 2026-01-20 | **Branch**: `005-phase-v-event-driven`

## Research Tasks

1. Dapr Pub/Sub with Kafka best practices
2. Strimzi Kafka setup on Minikube
3. Dapr Jobs API for reminder scheduling
4. Event schema design patterns
5. Real-time sync implementation

---

## 1. Dapr Pub/Sub with Kafka

### Decision
Use Dapr Pub/Sub component (`pubsub.kafka`) with Strimzi-managed Kafka cluster.

### Rationale
- **Portability**: Dapr's component model decouples the pub/sub API from the underlying broker. Swapping Kafka for another broker requires only a YAML change, no code changes.
- **Built-in resiliency**: Kafka has its own retry behaviors; Dapr resiliency augments (not replaces) these.
- **Schema flexibility**: Can use JSON payloads directly or integrate Schema Registry for Avro.

### Key Findings

#### Consumer Group Behavior
When subscribing to multiple topics, Dapr creates a single consumer group distributed across all topics. For optimal partitioning:
- **Solution**: Configure separate Pub/Sub components with different consumer group IDs if strict partitioning is needed.
- **Our approach**: Single consumer group is acceptable since each service subscribes to a single topic.

#### Message Format
- Payload is automatically serialized/deserialized as JSON within Dapr.
- Date/Datetime fields must be Epoch Unix timestamps (not ISO8601).
- Schema subjects are derived from topic names: `{topic-name}-value`.

#### Subscription Types
1. **Declarative** (YAML) - Hot reload supported via `HotReload` feature gate.
2. **Programmatic** (SDK) - Subscribe in application code.
3. **Streaming** - For high-throughput scenarios.

**Recommendation**: Use declarative subscriptions for predictability.

#### Message TTL
- Kafka uses topic-level `retention.ms` for TTL.
- Dapr adds per-message TTL capability on top of topic retention.

### Component Configuration

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub-kafka
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "my-cluster-kafka-bootstrap.kafka:9092"
    - name: consumerGroup
      value: "todo-chatbot"
    - name: authType
      value: "none"  # Use "sasl" for production
```

### Sources
- [Apache Kafka | Dapr Docs](https://docs.dapr.io/reference/components-reference/supported-pubsub/setup-apache-kafka/)
- [Publish and Subscribe Overview | Dapr Docs](https://docs.dapr.io/developing-applications/building-blocks/pubsub/pubsub-overview/)
- [Pub/Sub Quickstart | Dapr Docs](https://docs.dapr.io/getting-started/quickstarts/pubsub-quickstart/)

---

## 2. Strimzi Kafka Setup on Minikube

### Decision
Deploy Kafka using Strimzi Operator on Minikube with minimal single-node configuration.

### Rationale
- **Kubernetes-native**: Uses CRDs (Custom Resource Definitions) for Kafka resources.
- **Cloud-portable**: Same configuration works on managed Kubernetes (AKS/GKE/OKE).
- **Simplified operations**: Operator handles broker management, topic creation, user management.

### Setup Steps

1. **Start Minikube with sufficient resources**:
   ```bash
   minikube start --memory=4096 --cpus=4 -p todo-chatbot
   ```

2. **Create Kafka namespace**:
   ```bash
   kubectl create namespace kafka
   ```

3. **Install Strimzi Operator**:
   ```bash
   kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
   ```

4. **Deploy Kafka Cluster**:
   ```yaml
   apiVersion: kafka.strimzi.io/v1beta2
   kind: Kafka
   metadata:
     name: todo-kafka
     namespace: kafka
   spec:
     kafka:
       version: 3.7.0
       replicas: 1
       listeners:
         - name: plain
           port: 9092
           type: internal
           tls: false
       config:
         offsets.topic.replication.factor: 1
         transaction.state.log.replication.factor: 1
         transaction.state.log.min.isr: 1
         default.replication.factor: 1
         min.insync.replicas: 1
       storage:
         type: ephemeral
     zookeeper:
       replicas: 1
       storage:
         type: ephemeral
     entityOperator:
       topicOperator: {}
       userOperator: {}
   ```

5. **Wait for cluster ready**:
   ```bash
   kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=300s -n kafka
   ```

### Cleanup
```bash
kubectl -n kafka delete $(kubectl get strimzi -o name -n kafka)
```

### Sources
- [Strimzi Quickstarts](https://strimzi.io/quickstarts/)
- [Setting Up Kafka on Minikube Using Strimzi](https://saedhasan.medium.com/setting-up-kafka-on-minikube-k8s-using-strimzi-5cac7870d943)
- [Strimzi GitHub](https://github.com/strimzi/strimzi-kafka-operator)

---

## 3. Dapr Jobs API for Reminders

### Decision
Use Dapr Jobs API for scheduling task reminders (no polling).

### Rationale
- **Spec requirement**: FR-3 explicitly requires "no polling" for reminders.
- **Native integration**: Dapr Scheduler service is automatically started with `dapr init`.
- **At-least-once delivery**: Jobs API guarantees job execution with durability bias.

### Key Findings

#### Job Types
- **One-time job**: Schedule for a specific `dueTime`.
- **Recurring job**: Schedule with `cron` expression or `interval`.

#### How It Works
1. Application schedules job via Dapr sidecar (HTTP/gRPC).
2. Sidecar attaches namespace and appID, sends to Scheduler service.
3. At trigger time, Scheduler sends job back to sidecar.
4. Sidecar calls application's `/job/{job-name}` endpoint (HTTP) or `OnJobEvent` (gRPC).

#### SDK Support
- **Go SDK**: Full support (recommended for production).
- **.NET SDK**: Full support with `DaprPreviewClient`.
- **Python SDK**: Use HTTP API directly.

#### API Endpoints

**Schedule a job**:
```
POST http://localhost:<daprPort>/v1.0-alpha1/jobs/<job-name>
Content-Type: application/json

{
  "dueTime": "2026-01-20T15:00:00Z",
  "data": {
    "taskId": "task-123",
    "userId": "user-456"
  }
}
```

**Handle triggered job (app implements)**:
```
POST http://localhost:<appPort>/job/<job-name>
```

#### Storage Considerations
- Default storage: 1Gi (insufficient for production).
- Recommended: 16Gi or more for production deployments.
- Scheduler also handles actor reminders and workflow timers.

### Reminder Service Design

```python
# reminder_service.py
from fastapi import FastAPI
from dapr.clients import DaprClient

app = FastAPI()

def schedule_reminder(task_id: str, user_id: str, due_time: str):
    """Schedule a reminder job via Dapr Jobs API."""
    with DaprClient() as client:
        client.invoke_method(
            app_id="dapr",
            method_name=f"v1.0-alpha1/jobs/reminder-{task_id}",
            http_verb="POST",
            data={
                "dueTime": due_time,
                "data": {"taskId": task_id, "userId": user_id}
            }
        )

@app.post("/job/reminder-{task_id}")
async def handle_reminder(task_id: str, data: dict):
    """Called by Dapr when reminder triggers."""
    # Send notification to user
    pass
```

### Sources
- [Jobs Overview | Dapr Docs](https://docs.dapr.io/developing-applications/building-blocks/jobs/jobs-overview/)
- [Jobs API Reference | Dapr Docs](https://docs.dapr.io/reference/api/jobs_api/)
- [Jobs Quickstart | Dapr Docs](https://docs.dapr.io/getting-started/quickstarts/jobs-quickstart/)
- [Introducing Dapr Jobs API | Diagrid Blog](https://www.diagrid.io/blog/introducing-the-new-dapr-jobs-api-and-scheduler-service)

---

## 4. Event Schema Design

### Decision
Use CloudEvents envelope with JSON payload, single topic with event type routing.

### Rationale
- CloudEvents is the CNCF standard for event data.
- Dapr Pub/Sub automatically wraps messages in CloudEvents format.
- Single topic simplifies operations; event type in payload enables filtering.

### Event Schema

```json
{
  "specversion": "1.0",
  "type": "task.created",
  "source": "/todo-chatbot/backend",
  "id": "evt-123-abc",
  "time": "2026-01-20T12:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "taskId": "task-789",
    "userId": "user-456",
    "title": "Buy groceries",
    "completed": false,
    "priority": "high",
    "dueDate": 1737367200,
    "tags": ["shopping", "personal"],
    "recurrence": {
      "rule": "daily",
      "interval": 1
    },
    "createdAt": 1737280800,
    "updatedAt": 1737280800
  }
}
```

### Event Types

| Event Type | Trigger | Consumers |
|------------|---------|-----------|
| `task.created` | New task created | Audit, Reminder (if due_date) |
| `task.updated` | Task modified | Audit, Reminder (reschedule if due_date changed) |
| `task.completed` | Task marked done | Audit, Recurring (if recurring task) |
| `task.deleted` | Task removed | Audit, Reminder (cancel job) |

### Topic Configuration

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-events
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: 604800000  # 7 days
```

---

## 5. Real-Time Sync Implementation

### Decision
Use WebSocket connection from frontend, backend subscribes to Dapr pub/sub and broadcasts.

### Rationale
- Phase V spec requires "near real-time" sync across connected clients.
- WebSocket provides bidirectional, low-latency communication.
- Backend acts as bridge between Kafka events and WebSocket clients.

### Architecture

```
Frontend ──WebSocket──▶ Backend ◀──Dapr Pub/Sub──▶ Kafka
```

### Implementation Approach

1. **Backend WebSocket endpoint** (`/ws/tasks`):
   - Authenticate via JWT in connection params.
   - Maintain active connections per user.
   - Broadcast task events to user's connections.

2. **Backend Dapr subscription**:
   - Subscribe to `task-events` topic.
   - Filter events by user_id.
   - Push to appropriate WebSocket connections.

3. **Frontend WebSocket client**:
   - Connect on app load.
   - Reconnect on disconnect.
   - Update local state on event receipt.

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Server-Sent Events (SSE) | Simple, HTTP-based | Unidirectional only | Rejected |
| Polling | Simple implementation | Not real-time, wasteful | Rejected |
| Direct Kafka consumer in frontend | True real-time | Security risk, complexity | Rejected |
| **WebSocket via backend** | Bidirectional, secure, standard | Additional connection management | **Selected** |

---

## Summary of Decisions

| Research Area | Decision | Rationale |
|---------------|----------|-----------|
| Pub/Sub | Dapr `pubsub.kafka` component | Portability, built-in resiliency |
| Kafka | Strimzi Operator on Minikube | Kubernetes-native, cloud-portable |
| Reminders | Dapr Jobs API | No polling required, at-least-once delivery |
| Event Format | CloudEvents envelope, JSON payload | CNCF standard, Dapr-native |
| Topic Strategy | Single `task-events` topic | Simpler operations, type-based routing |
| Real-Time | WebSocket via backend | Secure, bidirectional, standard |

---

## Open Questions (Resolved)

| Question | Resolution |
|----------|------------|
| How to handle consumer group partitioning? | Single consumer group acceptable for our scale |
| How to format date fields in events? | Epoch Unix timestamps (Dapr requirement) |
| Jobs API SDK support for Python? | Use HTTP API directly, SDK in preview |
| Production storage for Scheduler? | 16Gi recommended (not critical for local dev) |
