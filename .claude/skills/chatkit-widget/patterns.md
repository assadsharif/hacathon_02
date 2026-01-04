# ChatKit Widget Design Patterns

**Document Type**: Reusable Design Patterns Catalog
**Phase**: 6 (Extension)
**Created**: 2025-12-26
**Status**: Design Artifacts

---

## Overview

This document catalogs **6 reusable design patterns** for implementing cross-platform chat widget integrations. These patterns are extracted from the ChatKit Widget Integration Skill and are applicable across documentation sites, educational platforms, enterprise knowledge bases, and SaaS tools.

Each pattern includes:
- **Problem Statement**: What challenge does this pattern solve?
- **Solution**: High-level design approach
- **Components**: Key architectural elements
- **Event Flow**: Sequence diagrams (design-level)
- **Cross-Domain Applicability**: How to adapt for different domains
- **Integration Points**: References to existing Phase 4-5 artifacts

---

## Pattern 1: Event-Driven Widget Architecture

### Problem Statement

**How do you design a chat widget that integrates with multiple backend services (RAG orchestration, authentication, analytics) without creating tight coupling?**

Traditional imperative architectures create brittle dependencies where the widget directly calls backend APIs. This makes it difficult to:
- Add new features (e.g., voice input) without modifying core widget code
- Replace backend services (e.g., switch from OpenAI to Anthropic)
- Test components in isolation
- Support real-time updates (e.g., agent streaming responses)

### Solution

**Event-driven architecture** where the widget and backend services communicate via standardized events. The widget acts as an **event bus**, emitting user actions and consuming agent responses.

**Core Principles**:
1. **Decoupling**: Widget doesn't know about backend implementation details
2. **Extensibility**: New features = new event types (no core changes)
3. **Testability**: Mock event producers/consumers for isolated testing
4. **Real-Time**: WebSocket or Server-Sent Events for streaming

### Components

#### Event Bus (Widget Core)

```typescript
// Design-level contract (not runtime code)
interface EventBus {
  emit(event: WidgetEvent): void;
  on(eventType: string, handler: EventHandler): void;
  off(eventType: string, handler: EventHandler): void;
}

type WidgetEvent =
  | UserMessageEvent
  | AgentResponseEvent
  | SystemMessageEvent
  | SignupFlowEvent
  | AuthenticationEvent
  | ErrorEvent;
```

#### Event Producers (User Interactions)

- **Text Input**: User types and submits question → `user_message` event
- **Mode Toggle**: User switches retrieval mode → `mode_changed` event
- **Signup Trigger**: User clicks "Save conversation" → `signup_initiated` event
- **Citation Click**: User clicks source link → `citation_clicked` event

#### Event Consumers (Backend Responses)

- **RAG Orchestration Agent**: Listens for `user_message`, emits `agent_response`
- **Better-Auth MCP**: Listens for `signup_initiated`, emits `authentication_completed`
- **Analytics Service**: Listens for all events, emits `analytics_tracked`

### Event Flow Diagram

```
User Action (Text Input)
    ↓
Widget emits: user_message
    ↓
RAG Orchestration Subagent consumes
    ↓
Agent processes (Context Selection → Retrieval → Synthesis → Guardrails)
    ↓
Agent emits: agent_response
    ↓
Widget consumes and renders
    ↓
User sees answer with citations
```

### Cross-Domain Applicability

| Domain | Adaptation | Event Types |
|--------|------------|-------------|
| **Documentation Sites** | API reference chatbot | `api_query`, `code_example_request` |
| **E-Commerce** | Product recommendations | `product_inquiry`, `recommendation_response` |
| **Customer Support** | Ticket automation | `ticket_created`, `agent_assigned`, `ticket_resolved` |
| **Healthcare** | Symptom checker | `symptom_input`, `diagnosis_suggestion`, `doctor_referral` |

### What Changes vs. What Stays the Same

**What Changes**:
- Event payload schemas (domain-specific data)
- Event types (new features = new events)
- Backend services (swap OpenAI for Anthropic)

**What Stays the Same**:
- Event bus architecture (emit/on/off pattern)
- Decoupling principles (loose coupling between widget and services)
- Testability approach (mock event producers/consumers)

### Integration Points

- **RAG Orchestration Subagent**: `.claude/agents/rag-orchestration/AGENT.md`
- **Better-Auth MCP Server**: `.claude/mcp/better-auth/README.md`
- **Dual-Mode Retrieval Pattern**: `.claude/skills/rag-chatbot/patterns.md#pattern-2`

---

## Pattern 2: Progressive Widget Loading

### Problem Statement

**How do you minimize initial bundle size for a chat widget while supporting rich features (voice input, image upload, analytics)?**

Chat widgets can become bloated with features, leading to:
- Slow initial page load (large JavaScript bundle)
- Unused features loaded upfront (most users only use text chat)
- Poor mobile performance (limited bandwidth, slower CPU)

### Solution

**Code-splitting and lazy loading** where the widget loads features **on-demand** based on user tier and interaction patterns.

**Core Principles**:
1. **Essential-First**: Load text chat UI immediately (core experience)
2. **On-Demand**: Load advanced features when triggered (voice button clicked)
3. **Tier-Based**: Premium features only load for paid users
4. **Prefetch**: Predict likely next features and prefetch in background

### Components

#### Load Tiers

**Tier 0 - Essential (Loaded Immediately)**:
- Widget shell (minimize/expand button)
- Text input and submit button
- Conversation history renderer
- Basic error handling

**Estimated Bundle Size**: 15 KB (gzipped)

---

**Tier 1 - Core Features (Loaded on First Interaction)**:
- RAG chatbot API client
- Citation link renderer
- Mode toggle (full-corpus vs. selected-text)
- Session management (LocalStorage)

**Estimated Bundle Size**: +25 KB (gzipped)

---

**Tier 2 - Enhanced Features (Loaded on Feature Access)**:
- Signup/authentication flows
- OAuth integration (Google, GitHub, Microsoft)
- Conversation export (JSON, CSV)
- Dark mode themes

**Estimated Bundle Size**: +35 KB (gzipped)

---

**Tier 3 - Premium Features (Loaded for Paid Users)**:
- Voice input (Web Speech API)
- Image upload (vision model integration)
- Code execution (Pyodide sandboxing)
- Real-time collaboration (WebSocket)

**Estimated Bundle Size**: +100 KB (gzipped)

### Loading Strategy

```typescript
// Design-level pseudocode (abstract operations, not runtime code)
class ChatKitWidget {
  async loadTier(tier: number) {
    switch(tier) {
      case 0:
        // Already loaded (essential features)
        break;
      case 1:
        await loadFeatureModule('rag-chatbot');
        await loadFeatureModule('citations');
        break;
      case 2:
        await loadFeatureModule('auth-flows');
        await loadFeatureModule('export');
        break;
      case 3:
        await loadFeatureModule('voice-input');
        await loadFeatureModule('image-upload');
        await loadFeatureModule('code-execution');
        break;
    }
  }
}
```

### Prefetching Strategy

```typescript
// Design-level prefetch triggers
const PREFETCH_TRIGGERS = {
  tier1: {
    event: 'widget_expanded',
    delay_ms: 2000,  // Wait 2s before prefetching
  },
  tier2: {
    event: 'third_message_sent',  // User engaged, likely to signup
    delay_ms: 0,
  },
  tier3: {
    user_tier: 'premium',
    event: 'conversation_started',
    delay_ms: 5000,
  },
};
```

### Cross-Domain Applicability

| Domain | Essential Features | Premium Features |
|--------|-------------------|------------------|
| **Documentation Sites** | Text search | Voice search, API playground |
| **E-Commerce** | Product search | Visual search (image upload), AR try-on |
| **Customer Support** | Text tickets | Video calls, screen sharing |
| **Healthcare** | Symptom checker | Image-based diagnosis, doctor consultation |

### What Changes vs. What Stays the Same

**What Changes**:
- Features per tier (domain-specific premium features)
- Bundle size estimates (depends on feature complexity)
- Prefetch triggers (based on user behavior analytics)

**What Stays the Same**:
- Lazy loading architecture (dynamic imports)
- Tier progression (free → basic → premium)
- Performance optimization goals (<100ms load time for Tier 0)

### Integration Points

- **Progressive Enhancement Signup Pattern**: `.claude/skills/signup-personalization/patterns.md#pattern-1`
- **Session Management Pattern**: `.claude/skills/rag-chatbot/patterns.md#pattern-5`

---

## Pattern 3: Session Continuity with Tier Upgrades

### Problem Statement

**How do you preserve user context (conversation history, bookmarks, preferences) when a user upgrades from anonymous (Tier 0) to authenticated (Tier 1+)?**

Losing context on signup creates a poor user experience:
- Conversation history disappears after signup
- Bookmarked content not carried over
- User must re-enter preferences (theme, language)

### Solution

**Session merge** where browser-local data (LocalStorage) is **uploaded to server** upon authentication, creating seamless continuity.

**Core Principles**:
1. **Transparent Migration**: User sees no interruption during tier upgrade
2. **Data Preservation**: All browser-local data transferred to server
3. **Conflict Resolution**: Handle edge cases (duplicate bookmarks, overlapping sessions)
4. **Privacy Compliance**: Explicit consent before uploading conversation history

### Components

#### Session Data Schema

**Browser-Local (Tier 0 - Anonymous)**:
```json
{
  "session_id": "anon-uuid-v4",
  "created_at": "2025-12-26T10:00:00.000Z",
  "tier": "anonymous",
  "data": {
    "conversation_history": [
      {"id": "msg-1", "role": "user", "content": "What is embodied intelligence?"},
      {"id": "msg-2", "role": "agent", "content": "Embodied intelligence refers to..."}
    ],
    "bookmarks": [
      {"content_id": "module-2-embodied/embodied-intelligence", "timestamp": "2025-12-26T10:15:00.000Z"}
    ],
    "preferences": {
      "theme": "dark",
      "language": "en"
    }
  }
}
```

**Server-Stored (Tier 1+ - Authenticated)**:
```json
{
  "user_id": "user-uuid",
  "session_id": "auth-session-uuid",
  "tier": "lightweight",
  "data": {
    "conversation_history": [...],  // Merged from browser-local
    "bookmarks": [...],              // Merged from browser-local
    "preferences": {...},            // Merged from browser-local
    "learning_path": "beginner",     // New fields (Tier 1+ only)
    "progress": {"completed_modules": 2}
  }
}
```

### Session Merge Flow

```
Step 1: User clicks "Save conversation" (Tier 0 → Tier 1 upgrade)
    ↓
Step 2: Widget shows signup modal (email or OAuth)
    ↓
Step 3: User completes authentication
    ↓
Step 4: Widget emits `authentication_completed` event
    ↓
Step 5: Widget reads browser-local session data (LocalStorage)
    ↓
Step 6: Widget uploads session data to server (/api/v1/session/merge)
    ↓
Step 7: Server merges browser-local → server-side session
    ↓
Step 8: Server returns merged session data + JWT token
    ↓
Step 9: Widget updates UI (no page refresh, seamless transition)
    ↓
Step 10: Browser-local session cleared (data now on server)
```

### Conflict Resolution

**Scenario**: User has two browser-local sessions (different devices) and signs up

**Resolution Strategy**:
- **Conversation History**: Merge both sessions, sort by timestamp
- **Bookmarks**: Deduplicate by `content_id`, keep earliest timestamp
- **Preferences**: Server-side session wins (most recent)

```typescript
// Design-level merge logic
function mergeBookmarks(localBookmarks, serverBookmarks) {
  const combined = [...localBookmarks, ...serverBookmarks];
  const deduplicated = deduplicateByContentId(combined);
  return sortByTimestamp(deduplicated);
}
```

### Privacy Consent

**GDPR Requirement**: Explicit consent before uploading conversation history

**Implementation**:
```json
{
  "consent_modal": {
    "title": "Save Your Conversation?",
    "message": "We'll securely store your conversation history on our servers so you can access it from any device. You can delete it anytime.",
    "actions": [
      {"label": "Yes, Save My Conversation", "event": "consent_granted"},
      {"label": "No, Keep It Local Only", "event": "consent_denied"}
    ]
  }
}
```

### Cross-Domain Applicability

| Domain | Session Data | Merge Strategy |
|--------|--------------|----------------|
| **Documentation Sites** | Search history, bookmarked pages | Keep all searches, deduplicate bookmarks |
| **E-Commerce** | Cart items, wish list | Merge cart (sum quantities), deduplicate wish list |
| **Learning Platforms** | Progress, quiz scores | Merge progress (max value per module), average quiz scores |
| **Productivity Tools** | Drafts, templates | Merge drafts (all), deduplicate templates by ID |

### What Changes vs. What Stays the Same

**What Changes**:
- Session data schema (domain-specific fields)
- Conflict resolution logic (cart merge vs. conversation merge)
- Consent messaging (GDPR vs. CCPA vs. FERPA)

**What Stays the Same**:
- Session merge architecture (browser-local → server upload)
- Transparent migration (no page refresh)
- Privacy-first approach (explicit consent)

### Integration Points

- **Progressive Enhancement Signup Pattern**: `.claude/skills/signup-personalization/patterns.md#pattern-1`
- **Browser-Local Session Management Pattern**: `.claude/skills/rag-chatbot/patterns.md#pattern-5`
- **Better-Auth MCP Server**: `.claude/mcp/better-auth/README.md`

---

## Pattern 4: Citation-Aware Message Rendering

### Problem Statement

**How do you render chatbot responses with inline citations that link back to source material while maintaining readability and accessibility?**

Plain text responses with URLs at the end are:
- Hard to read (interrupts flow)
- Difficult to attribute (which sentence came from which source?)
- Not accessible (screen readers can't distinguish citations from content)

### Solution

**Inline citation rendering** where citations are embedded as **superscript numbers** (academic style) or **hover-able footnotes** (web style), linking to stable section IDs.

**Core Principles**:
1. **Attribution Clarity**: Every claim clearly attributed to source
2. **Non-Intrusive**: Citations don't interrupt reading flow
3. **Accessible**: ARIA labels for screen readers
4. **Stable Links**: Citations use stable section IDs (not fragile URLs)

### Components

#### Citation Metadata

```typescript
interface Citation {
  id: string;                    // citation-1, citation-2, ...
  module_id: string;             // Stable module ID (e.g., "module-4-perception")
  chapter_id: string;            // Stable chapter ID (e.g., "sensor-fusion")
  section_id: string;            // Stable section ID (e.g., "multimodal-integration")
  url: string;                   // Resolved URL path (dynamic)
  excerpt: string;               // Text snippet (50-100 chars)
  position: number;              // Character offset in response text
}
```

#### Rendering Styles

**Style 1: Academic Superscript**
```
Embodied intelligence refers to intelligence that arises from the interaction
between an agent and its environment.[1] This contrasts with disembodied
approaches like traditional symbolic AI.[2]

[1] Module 2: Embodied Intelligence
[2] Module 1: Introduction to Physical AI
```

**Style 2: Hover-able Footnotes**
```
Embodied intelligence refers to intelligence that arises from the interaction
between an agent and its environment.¹

[Hover over ¹ shows tooltip:]
"Module 2: Embodied Intelligence - Definition
Click to view source →"
```

**Style 3: Inline Links (Web-Native)**
```
Embodied intelligence refers to intelligence that arises from the interaction
between an agent and its environment (see: Embodied Intelligence).
```

### Rendering Algorithm

```typescript
// Design-level pseudocode
function renderMessageWithCitations(message: string, citations: Citation[]) {
  let output = message;

  // Sort citations by position (descending) to avoid offset issues
  const sorted = sortByPositionDesc(citations);

  for (const citation of sorted) {
    const citationMark = `<sup><a href="${citation.url}" aria-label="Citation ${citation.id}">[${citation.id}]</a></sup>`;
    output = insertAtPosition(output, citation.position, citationMark);
  }

  return output + renderCitationFootnotes(citations);
}

function renderCitationFootnotes(citations: Citation[]) {
  return citations.map(c =>
    `[${c.id}] <a href="${c.url}">${c.module_id} - ${c.chapter_id}</a>`
  ).join('\n');
}
```

### Accessibility

**ARIA Labels**:
```html
<sup>
  <a href="/docs/module-2/embodied-intelligence"
     aria-label="Citation 1: Embodied Intelligence chapter">
    [1]
  </a>
</sup>
```

**Screen Reader Flow**:
```
"Embodied intelligence refers to intelligence that arises from the interaction
between an agent and its environment. Citation 1, Embodied Intelligence chapter.
This contrasts with disembodied approaches like traditional symbolic AI.
Citation 2, Introduction to Physical AI chapter."
```

### Cross-Domain Applicability

| Domain | Citation Style | Source Attribution |
|--------|----------------|-------------------|
| **Academic Journals** | Superscript numbers | APA, MLA, Chicago style |
| **Legal Documents** | Bluebook citations | Case law, statutes (Smith v. Jones, 123 F.3d 456) |
| **Medical Docs** | Vancouver numbering | PubMed references (PMID:12345678) |
| **Technical Docs** | Inline links | API endpoint docs, code examples |

### What Changes vs. What Stays the Same

**What Changes**:
- Citation rendering style (academic vs. legal vs. medical)
- Source metadata (APA author-date vs. Bluebook case law)
- URL resolution (stable IDs → API docs vs. case law databases)

**What Stays the Same**:
- Citation metadata structure (id, source, excerpt, position)
- Accessibility requirements (ARIA labels, screen reader support)
- Stable-ID principle (restructuring-resilient links)

### Integration Points

- **Stable-ID Citation Pattern**: `.claude/skills/rag-chatbot/patterns.md#pattern-3`
- **RAG Orchestration Subagent**: `.claude/agents/rag-orchestration/AGENT.md`

---

## Pattern 5: Graceful Degradation for Network Failures

### Problem Statement

**How do you design a chat widget that remains functional even when backend services (RAG API, authentication server) are unavailable?**

Network failures are inevitable:
- User on slow/unreliable connection (mobile, rural areas)
- Backend API downtime (deployments, outages)
- Rate limiting (user exceeded quota)

Without graceful degradation:
- Widget becomes completely unusable (blank screen, spinning loader)
- User loses conversation history (no offline persistence)
- No fallback options (can't browse docs manually)

### Solution

**Multi-tier fallback strategy** with **offline-first architecture** where the widget provides degraded but functional service during outages.

**Core Principles**:
1. **Fail Gracefully**: Show useful error messages, not technical jargon
2. **Offline Persistence**: LocalStorage as fallback for server failures
3. **Progressive Enhancement**: Basic features work offline (text display, bookmarks)
4. **Retry Logic**: Exponential backoff for transient failures

### Components

#### Fallback Tiers

**Tier 1: Full Functionality (Backend Available)**
- Real-time RAG chatbot responses
- OAuth authentication
- Server-side session sync
- Analytics tracking

**Tier 2: Degraded Service (Backend Slow)**
- Cached responses for common questions
- Session-based auth (no OAuth)
- Browser-local session only
- No analytics

**Tier 3: Offline Mode (Backend Unavailable)**
- Static FAQ responses (pre-loaded)
- No authentication (anonymous only)
- Browser-local session persistence
- Manual doc browsing (link to topics)

**Tier 4: Critical Failure (Widget Broken)**
- Fallback to plain "Contact Support" link
- No widget rendering
- Minimal UI (text-only)

### Error Detection & Fallback Logic

```typescript
// Design-level error handling
async function sendMessageWithFallback(message: string) {
  try {
    // Tier 1: Try full RAG API
    const response = await ragAPI.query(message, {timeout: 5000});
    return response;
  } catch (error) {
    if (error.type === 'timeout' || error.type === 'network') {
      // Tier 2: Try cached responses
      const cached = getCachedResponse(message);
      if (cached) return cached;

      // Tier 3: Fallback to static FAQ
      const faq = getStaticFAQ(message);
      if (faq) return faq;

      // Tier 4: Manual fallback
      return {
        type: 'fallback',
        content: "I'm having trouble connecting. Try browsing topics manually:",
        actions: [
          {label: "View All Topics", url: "/docs"},
          {label: "Retry", event: "retry_query"}
        ]
      };
    }

    throw error;  // Unrecoverable error
  }
}
```

### Retry Strategy

**Exponential Backoff**:
```
Attempt 1: 0s delay
Attempt 2: 1s delay
Attempt 3: 2s delay
Attempt 4: 4s delay
Attempt 5: 8s delay (max 3 retries)
```

**Circuit Breaker**:
```typescript
// Design-level circuit breaker
class CircuitBreaker {
  state: 'closed' | 'open' | 'half-open';
  failureCount: number;
  failureThreshold: number = 5;
  resetTimeout: number = 60000;  // 1 minute

  async execute(operation) {
    if (this.state === 'open') {
      throw new Error('Circuit breaker open - service unavailable');
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
}
```

### Offline Caching Strategy

**Cached Responses (Top 100 Questions)**:
```json
{
  "cached_qa": [
    {
      "question": "What is embodied intelligence?",
      "answer": "Embodied intelligence refers to...",
      "citations": [{"module_id": "module-2-embodied", "chapter_id": "definition"}],
      "cached_at": "2025-12-26T00:00:00.000Z",
      "ttl_hours": 168
    }
  ]
}
```

**Static FAQ (Pre-Loaded)**:
```json
{
  "faq": [
    {
      "category": "Getting Started",
      "questions": [
        {
          "q": "How do I ask questions?",
          "a": "Type your question and press Enter. The chatbot searches the entire book."
        },
        {
          "q": "Can I search specific sections?",
          "a": "Yes! Highlight any text, then ask a follow-up question."
        }
      ]
    }
  ]
}
```

### Cross-Domain Applicability

| Domain | Tier 1 (Full) | Tier 3 (Offline) |
|--------|---------------|------------------|
| **Documentation Sites** | Real-time code search | Static API reference |
| **E-Commerce** | Live product recommendations | Cached top products |
| **Banking** | Real-time balance | Last synced balance (read-only) |
| **Healthcare** | Live symptom checker | Pre-loaded common symptoms FAQ |

### What Changes vs. What Stays the Same

**What Changes**:
- Cached data (domain-specific top questions)
- Fallback UX (e-commerce shows cached products, docs show static FAQ)
- Retry thresholds (banking: 10 retries, docs: 3 retries)

**What Stays the Same**:
- Multi-tier fallback architecture (Tier 1-4 degradation)
- Exponential backoff retry logic
- Circuit breaker pattern (prevent cascading failures)

### Integration Points

- **Browser-Local Session Management Pattern**: `.claude/skills/rag-chatbot/patterns.md#pattern-5`
- **Error Handling Middleware**: `rag-chatbot/src/api/middleware/error_handling.py`

---

## Pattern 6: Contextual Feature Discovery

### Problem Statement

**How do you guide users to discover advanced widget features (voice input, image upload, bookmarks) without overwhelming them with onboarding tutorials?**

Traditional approaches fail:
- Long onboarding tutorials (users skip)
- Feature overload (too many buttons upfront)
- Hidden features (users never discover)

### Solution

**Progressive feature discovery** where advanced features are revealed **contextually** based on user behavior and tier progression.

**Core Principles**:
1. **Just-In-Time**: Show feature prompts when relevant (not upfront)
2. **Value-First**: Explain benefit before showing feature
3. **Non-Intrusive**: Subtle hints, not modal overlays
4. **Dismissible**: User can hide hints permanently

### Components

#### Discovery Triggers

**Trigger 1: Repeated Questions (Voice Input)**
```
Condition: User asks 5+ questions in one session
Trigger: Show voice input hint
Message: "💡 Tip: Try voice input for faster questions (click microphone icon)"
Timing: After 5th question submitted
Dismissible: Yes
```

**Trigger 2: Long Text Selection (Selected-Text Mode)**
```
Condition: User selects >200 characters of text
Trigger: Show selected-text mode hint
Message: "💡 You've selected text! Ask a follow-up question to focus on this passage."
Timing: 2 seconds after text selection
Dismissible: Yes
```

**Trigger 3: Third Conversation (Bookmarks)**
```
Condition: User returns for 3rd session
Trigger: Show bookmark hint
Message: "💡 Bookmark answers to find them later! Click the bookmark icon on any message."
Timing: After 3rd session starts
Dismissible: Yes
```

**Trigger 4: Failed Search (Tier Upgrade)**
```
Condition: Chatbot returns "No results found" or low-confidence answer
Trigger: Show signup prompt (Tier 1 gets better results)
Message: "Sign up for free to unlock personalized search and save your conversations."
Timing: Immediately after failed search
Dismissible: No (but can click "Not now")
```

#### Discovery UI Patterns

**Pattern 1: Inline Tooltips (Subtle)**
```html
<button aria-label="Voice input">
  <MicrophoneIcon />
  <span class="tooltip">Try voice input! (Beta)</span>
</button>
```

**Pattern 2: Pulsing Badge (Attention-Grabbing)**
```html
<button class="feature-new">
  <ImageIcon />
  <span class="badge pulse">NEW</span>
</button>
```

**Pattern 3: Toast Notifications (Non-Intrusive)**
```json
{
  "toast": {
    "type": "feature_hint",
    "icon": "💡",
    "message": "Bookmark this answer for later review!",
    "action": {
      "label": "Try It",
      "event": "bookmark_current_message"
    },
    "duration_ms": 5000,
    "position": "bottom-right"
  }
}
```

#### Feature Onboarding Checklist

```json
{
  "onboarding_checklist": {
    "ask_first_question": {
      "completed": true,
      "hint_shown": false
    },
    "try_selected_text_mode": {
      "completed": false,
      "hint_shown": true,
      "hint_dismissed": false
    },
    "bookmark_answer": {
      "completed": false,
      "hint_shown": false
    },
    "try_voice_input": {
      "completed": false,
      "hint_shown": false,
      "tier_required": "lightweight"
    }
  }
}
```

### Cross-Domain Applicability

| Domain | Contextual Features | Discovery Triggers |
|--------|---------------------|-------------------|
| **E-Commerce** | Visual search (image upload) | After 3 failed text searches |
| **Learning Platforms** | Spaced repetition reminders | After completing 1 module |
| **Productivity Tools** | Keyboard shortcuts | After 10 mouse clicks on same action |
| **Healthcare** | Symptom tracker integration | After 3 symptom-related questions |

### What Changes vs. What Stays the Same

**What Changes**:
- Discovery triggers (domain-specific behaviors)
- Feature hints (e-commerce: "Try visual search", docs: "Try voice input")
- Tier requirements (free vs. paid feature thresholds)

**What Stays the Same**:
- Progressive disclosure architecture (features revealed over time)
- Non-intrusive UI (toasts, tooltips, not modals)
- Dismissible hints (user control)

### Integration Points

- **Progressive Enhancement Signup Pattern**: `.claude/skills/signup-personalization/patterns.md#pattern-1`
- **Layered Personalization Pattern**: `.claude/skills/signup-personalization/patterns.md#pattern-2`

---

## Cross-Pattern Integration Matrix

| Pattern | Integrates With | Shared Components |
|---------|----------------|-------------------|
| **Event-Driven Architecture** | All patterns | Event bus, standardized event schemas |
| **Progressive Loading** | Session Continuity, Feature Discovery | Tier progression, lazy loading |
| **Session Continuity** | Event-Driven, Graceful Degradation | LocalStorage, session merge logic |
| **Citation Rendering** | Event-Driven (citation_clicked events) | Stable-ID resolution, accessibility |
| **Graceful Degradation** | Session Continuity (offline persistence) | Circuit breaker, retry logic |
| **Feature Discovery** | Progressive Loading (tier-based hints) | Onboarding checklist, toast notifications |

---

## Pattern Selection Guide

### When to Use Each Pattern

**Event-Driven Architecture** → Always (foundational pattern)
- Decouples widget from backend services
- Enables real-time features (streaming responses)
- Simplifies testing and maintenance

**Progressive Loading** → Large widgets (>50 KB initial bundle)
- Improves initial load time (mobile, slow networks)
- Reduces unused code (most users don't use voice input)

**Session Continuity** → Progressive signup flows
- Preserves user context during tier upgrades
- Reduces friction (no data loss on authentication)

**Citation Rendering** → Knowledge-intensive domains
- Academic documentation (research papers, textbooks)
- Legal Q&A (case law, statutes)
- Medical chatbots (PubMed references)

**Graceful Degradation** → Mission-critical applications
- Banking (show last synced balance if API down)
- Healthcare (cached symptom checker)
- E-commerce (cached product catalog)

**Feature Discovery** → Feature-rich widgets (5+ advanced features)
- Guides users to discover value incrementally
- Reduces onboarding friction (no long tutorials)

---

## References

### Internal Documentation

- **ChatKit Widget Skill**: `.claude/skills/chatkit-widget/SKILL.md`
- **RAG Chatbot Patterns**: `.claude/skills/rag-chatbot/patterns.md`
- **Signup-Personalization Patterns**: `.claude/skills/signup-personalization/patterns.md`
- **RAG Orchestration Subagent**: `.claude/agents/rag-orchestration/AGENT.md`
- **Better-Auth MCP Server**: `.claude/mcp/better-auth/README.md`

### External Resources

- **Event-Driven Architecture**: https://martinfowler.com/articles/201701-event-driven.html
- **Code Splitting (Webpack)**: https://webpack.js.org/guides/code-splitting/
- **LocalStorage Best Practices**: https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage
- **Circuit Breaker Pattern**: https://martinfowler.com/bliki/CircuitBreaker.html
- **Progressive Enhancement**: https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-26 | Initial 6 design patterns for ChatKit widget integration |

---

**Created**: 2025-12-26
**Maintained By**: Academic Spec-Driven Development Project
**License**: Documentation Only (No Code)
