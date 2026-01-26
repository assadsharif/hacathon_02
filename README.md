# Todo Chatbot Application

A modern full-stack todo application with AI-powered chat, event-driven architecture, and multi-cloud deployment.

## Live Deployments

| Environment | Frontend | Backend API | Status |
|-------------|----------|-------------|--------|
| **Vercel (Production)** | https://frontend-sigma-seven-25.vercel.app | https://todo-api.20.81.84.247.nip.io | ✅ Active |
| **AKS (Azure)** | http://20.237.113.196:3000 | http://20.62.210.3:8000 | ✅ Active |
| **GKE (Google)** | *Configure after deployment* | *Configure after deployment* | 🔧 Ready |

### Try It Now
👉 **Live Demo**: https://frontend-sigma-seven-25.vercel.app
- Sign up for a free account
- Try the **AI Chat** interface at `/chat`
- Or use the traditional **Todos** interface at `/todos`

## Features

- User Authentication (Sign Up / Sign In)
- Create, Read, Update, Delete Todos
- **AI-Powered Chat** - Natural language todo management
- **Event-Driven Architecture** - Dapr pub/sub with Kafka
- **Multi-Cloud Deployment** - GKE and AKS
- **Observability** - Prometheus & Grafana dashboards
- Modern responsive UI

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend     │────▶│     Backend     │────▶│    PostgreSQL   │
│   (Next.js)     │     │   (FastAPI)     │     │     (Neon)      │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │     Dapr Pub/Sub        │
                    │   (Redpanda Cloud)      │
                    └────────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Audit Service  │    │Reminder Service │    │Recurring Service│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Auth**: Better Auth with JWT

### Backend
- **Framework**: FastAPI (Python 3.11)
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon Cloud)
- **Runtime**: Dapr sidecar for pub/sub

### Event-Driven Services
- **Audit Service**: Logs all task events
- **Reminder Service**: Handles task reminders
- **Recurring Service**: Manages recurring tasks

### Infrastructure
- **Container Registry**: GCR (Google), ACR (Azure)
- **Kubernetes**: GKE, AKS
- **Event Streaming**: Redpanda Cloud (Kafka-compatible)
- **Observability**: Prometheus + Grafana

## Project Structure

```
hacathon_02/
├── frontend/              # Next.js frontend
├── backend/               # FastAPI backend
├── services/              # Event-driven microservices
│   ├── audit-service/
│   ├── reminder-service/
│   └── recurring-service/
├── charts/                # Helm charts
│   ├── todo-chatbot/      # Main application
│   ├── phase-v-services/  # Microservices
│   ├── dapr-components/   # Dapr configuration
│   └── observability/     # Prometheus + Grafana
├── scripts/               # Deployment scripts
├── docs/                  # Documentation
└── .github/workflows/     # CI/CD pipelines
```

## Quick Start

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload

# Frontend
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

### Kubernetes Deployment (Local)

```bash
# Start Minikube
minikube start

# Install Dapr
dapr init -k

# Deploy application
helm upgrade --install todo-chatbot ./charts/todo-chatbot -n todo-chatbot --create-namespace
```

### Multi-Cloud Deployment

See [Phase VI Deployment Guide](docs/phase-vi-deployment.md) for complete instructions.

**Quick Deploy to AKS:**
```bash
./scripts/manual-deploy.sh aks latest
```

**Quick Deploy to GKE:**
```bash
./scripts/manual-deploy.sh gke latest
```

## AI Chat Interface

The application includes an AI-powered conversational interface for managing todos using natural language.

### Accessing the Chat

1. **Sign in** to your account
2. Navigate to **AI Chat** from the navigation bar, or visit `/chat` directly
3. Start chatting with the AI assistant to manage your todos

### Chat Capabilities

The AI assistant can help you with all todo operations:

#### Create Todos
```
You: "Add a task to buy milk"
AI: ✅ Created: 'Buy milk' (ID: 5, Status: active)

You: "Create a todo to call dentist with description schedule appointment"
AI: ✅ Created: 'Call dentist' with description 'schedule appointment' (ID: 6, Status: active)
```

#### List Todos
```
You: "What are my tasks?"
AI: 📋 You have 3 tasks:
    1. Buy milk (active)
    2. Call dentist (active)
    3. Review docs (completed)

You: "Show me only active todos"
AI: 📋 Active tasks:
    1. Buy milk (ID: 5)
    2. Call dentist (ID: 6)
```

#### Update Todos
```
You: "Mark task 5 as done"
AI: ✅ Updated: 'Buy milk' is now completed

You: "Update task 6 title to 'Call dentist tomorrow'"
AI: ✅ Updated: Task 6 title changed to 'Call dentist tomorrow'
```

#### Delete Todos
```
You: "Delete task 5"
AI: ✅ Deleted: 'Buy milk' has been removed

You: "Remove the dentist task"
AI: ✅ Deleted: 'Call dentist tomorrow' has been removed
```

### Smart Features

#### Clarification
The AI asks for clarification when your request is ambiguous:
```
You: "Delete it"
AI: 🤔 Which task would you like to delete? Please specify the task name or ID.
```

#### Refusal
The AI politely refuses unsupported operations:
```
You: "Schedule my tasks for next week"
AI: ℹ️ I can only create, list, update, and delete todos. Scheduling is not supported.
```

### Navigation

Switch between interfaces easily:
- **📝 Todos**: Traditional list view with full CRUD operations
- **💬 AI Chat**: Conversational interface for natural language task management

Both interfaces are synced in real-time and use the same backend API.

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/sign-up` | Register new user |
| POST | `/api/auth/sign-in` | Login user |
| GET | `/api/auth/me` | Get current user |

### Todos
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos/` | List all todos |
| POST | `/api/todos/` | Create todo |
| PUT | `/api/todos/{id}` | Update todo |
| DELETE | `/api/todos/{id}` | Delete todo |

### AI Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/` | Send message to AI |
| GET | `/api/chat/history` | Get chat history |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |

## CI/CD Pipeline

Automated deployments via GitHub Actions:

1. **Build** - Triggered on push to `main`
   - Builds Docker images
   - Pushes to GCR and ACR

2. **Deploy GKE** - After successful build
   - Deploys to Google Kubernetes Engine

3. **Deploy AKS** - After successful build
   - Deploys to Azure Kubernetes Service

### Manual Deployment
```bash
# Deploy to specific cloud
./scripts/manual-deploy.sh [gke|aks|both] [image-tag]

# Examples
./scripts/manual-deploy.sh aks latest
./scripts/manual-deploy.sh both v1.0.0
```

## Observability

### Access Dashboards

```bash
# Grafana (admin/admin123)
kubectl port-forward svc/prometheus-stack-grafana 3001:80 -n monitoring

# Prometheus
kubectl port-forward svc/prometheus-stack-kube-prom-prometheus 9090:9090 -n monitoring
```

### Custom Dashboards
- **Todo Chatbot Overview** - Application metrics
- **Dapr Pub/Sub** - Event streaming metrics

## Development Phases

| Phase | Description | Status |
|-------|-------------|--------|
| I | CLI Todo App | ✅ Complete |
| II | Web UI + Database | ✅ Complete |
| III | AI Chat Integration | ✅ Complete |
| IV | Kubernetes Deployment | ✅ Complete |
| V | Event-Driven Architecture | ✅ Complete |
| VI | Multi-Cloud Deployment | ✅ Complete |

## Environment Variables

### Backend
```env
DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET=your-secret-key
OPENAI_API_KEY=sk-...
DAPR_HTTP_PORT=3500
PUBSUB_NAME=pubsub-kafka
```

### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/name`)
5. Open Pull Request

## Documentation

- [Phase VI Deployment Guide](docs/phase-vi-deployment.md)
- [GitHub Secrets Setup](docs/github-secrets-setup.md)

## License

MIT License - see LICENSE file for details.

---

Built with Next.js, FastAPI, Dapr, and Kubernetes
