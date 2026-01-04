# RAG Chatbot Design Patterns

**Extracted From**: `specs/001-rag-chatbot/` (Phase 2 RAG Chatbot Design)
**Version**: 1.0.0 | **Created**: 2025-12-26

---

## Overview

This document catalogs **five reusable design patterns** extracted from the Physical AI & Humanoid Robotics RAG chatbot architectural design. Each pattern addresses a specific design challenge in building retrieval-augmented generation (RAG) systems and can be applied independently across different domains.

**Pattern Catalog**:
1. Multi-Agent RAG Orchestration Pattern
2. Dual-Mode Retrieval Pattern
3. Stable-ID Citation Pattern
4. Guardrails Layer Pattern
5. Browser-Local Session Management Pattern

---

## Pattern 1: Multi-Agent RAG Orchestration

### Problem Statement

How do you design a RAG system that is **modular, testable, and maintainable** while coordinating multiple complex operations (context selection, retrieval, synthesis, validation) in a single query-response flow?

### Context

Traditional monolithic RAG systems combine all logic into a single function or service, leading to:
- **Testing Difficulty**: Cannot test retrieval independently from synthesis
- **Maintenance Burden**: Changes to citation logic require touching synthesis code
- **Reusability Limitations**: Cannot reuse retrieval logic in non-RAG contexts
- **Failure Opacity**: When pipeline fails, unclear which component caused the error

### Solution

Decompose the RAG pipeline into **four distinct agent roles**, each with a single responsibility, coordinated by an orchestrator:

**Agent Pipeline**:
```
[1] Context Selection → [2] Retrieval → [3] Answer Synthesis → [4] Citation & Guardrails
```

**Agent Responsibilities**:

| Agent Role | Responsibility | Inputs | Outputs |
|------------|----------------|--------|---------|
| **Context Selection** | Determine retrieval scope | Query, mode, optional context | Scope decision (full-corpus or constrained) |
| **Retrieval** | Fetch relevant content | Query, scope, top-k | Ranked list of chunks + metadata |
| **Answer Synthesis** | Generate natural language response | Query, chunks | Answer text + chunk IDs used |
| **Citation & Guardrails** | Add citations, enforce boundaries | Answer, chunk IDs, metadata | Final response with citations + validation flags |

**Orchestration Flow**:
1. Orchestrator receives user query
2. Calls Agent 1 (Context Selection) → receives scope decision
3. Calls Agent 2 (Retrieval) with scope → receives chunks
4. Calls Agent 3 (Synthesis) with chunks → receives answer
5. Calls Agent 4 (Guardrails) with answer → receives final response
6. Returns final response to user

**Key Design Principles**:
- **Sequential Execution**: Each agent depends on the previous agent's output (no parallelization within pipeline)
- **Stateless Agents**: All state passed via inputs/outputs (no shared global state)
- **Single Responsibility**: Each agent has exactly one job (no overlap)
- **Failure Isolation**: Error in Agent 2 doesn't crash Agent 3 (orchestrator handles errors)

### Consequences

**Benefits**:
- ✅ **Independent Testing**: Each agent can be unit tested in isolation
- ✅ **Reusability**: Retrieval Agent can be reused in non-RAG contexts (semantic search)
- ✅ **Clear Failure Attribution**: Orchestrator logs which agent failed and why
- ✅ **Parallel Development**: Different developers can work on different agents simultaneously
- ✅ **Easy Extension**: Add new agents (e.g., Re-Ranking Agent) without modifying existing agents

**Tradeoffs**:
- ⚠️ **Latency Overhead**: Sequential execution adds orchestration overhead (vs. single function)
- ⚠️ **Complexity**: More components to deploy and monitor
- ⚠️ **Interface Contracts**: Requires strict input/output contracts between agents

### When to Use

- Building RAG systems for production (not prototypes)
- System requires high testability and maintainability
- Multiple developers working on the project
- Need to support multiple retrieval modes or synthesis strategies

### When NOT to Use

- Prototyping or proof-of-concept (overhead not justified)
- Single-query, throw-away script
- System so simple it fits in <100 lines of code

### Example Adaptations

**Legal Document Q&A**:
- Agent 1: Add jurisdiction filter (constrain retrieval to specific court jurisdiction)
- Agent 2: Retrieval ranks by recency (newer cases weighted higher)
- Agent 3: Synthesis uses formal legal language template
- Agent 4: Citations formatted as Bluebook style + "Not legal advice" disclaimer

**Customer Support KB**:
- Agent 1: Add product filter (constrain to user's product)
- Agent 2: Retrieval includes article popularity score (frequently accessed KB articles ranked higher)
- Agent 3: Synthesis uses friendly, step-by-step tone
- Agent 4: Guardrails detect escalation keywords ("refund", "cancel") → route to human agent

---

## Pattern 2: Dual-Mode Retrieval

### Problem Statement

How do you balance **broad exploration** (searching entire corpus) with **focused clarification** (answering about specific selected text) in a single user interface without confusing users?

### Context

Users have two distinct information needs:
1. **Exploratory Queries**: "What is sensor fusion?" → Search all available content
2. **Clarification Queries**: "What does THIS paragraph mean?" → Answer only about selected text

Mixing these modes in a single interface creates confusion:
- User highlights text but asks unrelated question → Should system use selection or ignore it?
- User asks broad question while text is selected → Should system clear selection or constrain search?

### Solution

Implement **two explicit retrieval modes** with clear UI differentiation and validation logic:

**Mode 1: Full-Corpus Retrieval**
- **Trigger**: User submits query WITHOUT text selection OR explicitly selects "Search All" mode
- **Scope**: Entire indexed knowledge base
- **Retrieval Strategy**: Vector similarity search across all chunks
- **Response Framing**: "Based on the [corpus name]..."

**Mode 2: Constrained Retrieval (Selected-Text)**
- **Trigger**: User highlights text AND submits query (selection context active)
- **Scope**: Selected text ONLY (treated as single chunk)
- **Retrieval Strategy**: No vector search (passthrough selected text to synthesis)
- **Response Framing**: "Based on your selected text..."

**Validation Logic**:

| Scenario | Mode | Selection State | Action |
|----------|------|-----------------|--------|
| User asks query without selection | Full-Corpus | None | Proceed with full-corpus retrieval |
| User selects text + asks query | Constrained | Valid (>50 chars, <5 min old) | Use selected text as single chunk |
| User selects text + navigates to new page + asks query | Auto-fallback | Stale (page changed) | Clear selection, fallback to full-corpus with notification |
| User selects <50 characters + asks query | Auto-fallback | Invalid (too short) | Warn user, fallback to full-corpus |

**UI Indicators**:
- **Mode Toggle**: Visual indicator showing "Full Book" vs "Selected Text" mode
- **Selection Highlight**: Selected text remains visually highlighted while mode active
- **Response Badge**: Response shows mode used ("Searched full book" vs "Answered from selected text")

### Consequences

**Benefits**:
- ✅ **User Clarity**: Users always know which mode they're in
- ✅ **Precision Control**: Constrained mode prevents over-answering (pulling in irrelevant chapters)
- ✅ **Performance**: Constrained mode skips vector search (faster response)
- ✅ **Context Preservation**: Selected text remains available for follow-up questions

**Tradeoffs**:
- ⚠️ **UI Complexity**: Requires mode toggle and selection state management
- ⚠️ **Validation Overhead**: Must track selection staleness, page navigation
- ⚠️ **Edge Cases**: Ambiguous scenarios (selection exists but unrelated to query) need handling

### When to Use

- Documentation Q&A systems (technical docs, books, wikis)
- Code review assistants (explain selected function vs. entire codebase)
- Legal contract review (specific clause vs. entire contract)
- Educational assistants (selected paragraph vs. entire textbook chapter)

### When NOT to Use

- Pure conversational AI (no document grounding)
- Systems where ALL queries are broad (no need for constrained mode)
- Mobile-first interfaces where text selection is difficult

### Design Decisions

**Selection Staleness Threshold**:
- **Choice**: Clear selection after 5 minutes OR page navigation
- **Rationale**: Balance between preserving context and preventing stale data
- **Alternative**: Let user manually clear selection (more control, more cognitive load)

**Minimum Selection Length**:
- **Choice**: Require ≥50 characters
- **Rationale**: Shorter selections lack semantic context for meaningful answers
- **Alternative**: No minimum (allow single-word definitions)

**Fallback Behavior**:
- **Choice**: Auto-fallback to full-corpus with user notification
- **Rationale**: Better to over-answer than reject query
- **Alternative**: Reject invalid constrained queries (forces user to re-select)

---

## Pattern 3: Stable-ID Citation

### Problem Statement

How do you ensure **citation links remain valid** when document structure changes (chapters reorganized, sections renamed, URLs refactored)?

### Context

Traditional URL-based citations break when content moves:
- **Problem**: Citation points to `/docs/module-4/sensor-fusion`
- **Change**: Module 4 reorganized, content now at `/docs/perception/sensors/fusion`
- **Result**: Citation link returns 404 error

This is especially problematic for:
- Educational content (frequent updates, reorganization)
- Living documentation (continuous improvement cycles)
- Multi-version systems (v1 vs. v2 structure differences)

### Solution

Use **stable section identifiers** independent of URL structure, with dynamic URL construction:

**Metadata Schema**:
```
BookContentChunk:
  chunk_id: UUID (internal reference)
  text_content: string
  source_metadata:
    module_id: string (stable, e.g., "perception-systems")
    chapter_id: string (stable, e.g., "sensor-fusion")
    section_id: string (stable, e.g., "multimodal-integration")
  url_path: string (dynamic, constructed at runtime)
```

**Citation Generation Process**:

1. **At Indexing Time**:
   - Extract stable IDs from document frontmatter (YAML metadata)
   - Store: `module_id`, `chapter_id`, `section_id` (stable identifiers)
   - **Do NOT store** hardcoded URLs (URLs can change)

2. **At Query Time** (Citation Agent):
   - Retrieve chunk metadata by `chunk_id`
   - Resolve stable IDs to current URL structure
   - Construct URL dynamically: `/docs/{module_id}/{chapter_id}#{section_id}`
   - Format citation: `[Module Name: Chapter Title](constructed_URL)`

3. **At Content Restructure**:
   - URLs change: `/docs/module-4/sensor-fusion` → `/docs/perception/sensors/fusion`
   - Stable IDs unchanged: `module_id=perception-systems`, `section_id=multimodal-integration`
   - **Citations automatically work** (URL reconstructed from stable IDs)

**Stable ID Strategy (Docusaurus Example)**:

```markdown
---
id: sensor-fusion  # Stable section ID
title: Sensor Fusion and Multi-Modal Integration
sidebar_position: 3
---

## Overview {#overview}  # Stable heading anchor

Content here...

## Applications {#applications}  # Stable heading anchor
```

- **Section ID**: From frontmatter `id` field (never changes even if file renamed)
- **Heading Anchor**: From manual anchor tag `{#anchor-name}` (not auto-generated from heading text)

### Consequences

**Benefits**:
- ✅ **Restructuring-Resilient**: Citations survive content reorganization
- ✅ **Multi-Version Support**: v1 and v2 of docs can coexist with different URLs but same stable IDs
- ✅ **URL Refactoring**: Frontend can change URL patterns without breaking citations

**Tradeoffs**:
- ⚠️ **Metadata Discipline**: Requires authors to maintain stable IDs (not auto-generated)
- ⚠️ **Indexing Overhead**: Must store stable IDs separately from URLs
- ⚠️ **Fallback Complexity**: When stable ID missing, need graceful degradation (link to chapter root)

### When to Use

- Documentation that evolves frequently (technical docs, product docs)
- Multi-version documentation (v1.x, v2.x with different structures)
- Content management systems with reorganization workflows
- Any system where citation longevity is critical (academic, legal, medical)

### When NOT to Use

- Static, frozen corpora (content never changes)
- Short-lived content (daily news articles, temporary announcements)
- Systems where 404 errors are acceptable (low-stakes content)

### Implementation Variants

**Variant 1: Frontmatter-Based Stable IDs** (Recommended)
- Stable IDs stored in document frontmatter
- Authors manually assign IDs
- Works with Docusaurus, VitePress, Jekyll, Hugo

**Variant 2: Database-Backed Stable IDs**
- Stable IDs stored in separate database table
- CMS auto-generates IDs on first publish
- Works with headless CMS (Contentful, Strapi)

**Variant 3: Content Hash Stable IDs**
- Stable ID = hash of normalized content (first 100 characters)
- Auto-generated, no manual assignment needed
- Breaks if content text changes (less stable)

---

## Pattern 4: Guardrails Layer

### Problem Statement

How do you **enforce content boundaries** and **prevent hallucination** in RAG systems while maintaining user-friendly responses?

### Context

RAG systems face several failure modes:
1. **Out-of-Scope Queries**: User asks about topics not in knowledge base
2. **Capability Confusion**: User requests actions beyond system capabilities (code generation, real-time data)
3. **Hallucination Risk**: Language model invents answers not grounded in retrieved content
4. **Low-Quality Responses**: Answer is vague, speculative, or lacks citations

Without guardrails, system responds to all queries, leading to:
- Loss of user trust (hallucinated answers)
- Scope creep (answering unrelated questions)
- Safety risks (medical/legal/financial advice without disclaimers)

### Solution

Add a **post-synthesis validation layer** (Guardrails Agent) that checks synthesized answers against rules before delivering to user:

**Guardrail Categories**:

| Category | Detects | Action on Violation | Example |
|----------|---------|---------------------|---------|
| **Content Boundary** | Out-of-scope topics | Override answer | Query: "What is quantum computing?" → Response: "I can only answer based on the Physical AI book" |
| **Capability Boundary** | Disallowed capabilities | Override answer | Query: "Write me code for PID control" → Response: "I can explain concepts but cannot write code" |
| **Confidence Boundary** | Uncertain language | Flag with warning | Answer contains "I think" → Append: "Note: This answer may be speculative" |
| **Citation Coverage** | Missing source attribution | Reject answer | Answer has no chunk references → Response: "I couldn't find relevant information" |

**Validation Process**:

1. **Input**: Synthesized answer from Answer Synthesis Agent
2. **Check 1 - Content Boundary**:
   - Scan answer for mentions of topics NOT in corpus metadata
   - Use domain-specific keyword lists (example: for robotics book, flag "blockchain", "cryptocurrency")
   - If detected → **OVERRIDE** answer with boundary message

3. **Check 2 - Capability Boundary**:
   - Scan query for action verbs ("write", "implement", "build", "create", "generate")
   - Scan query for disallowed request types (code, real-time data, predictions)
   - If detected → **OVERRIDE** answer with capability message

4. **Check 3 - Confidence Boundary**:
   - Scan answer for hedge words ("I think", "maybe", "possibly", "probably", "unclear")
   - If detected → **APPEND WARNING** to answer (preserve answer, flag uncertainty)

5. **Check 4 - Citation Coverage**:
   - Verify chunk_ids_used list is non-empty
   - Verify all chunks resolve to valid metadata
   - If empty or invalid → **OVERRIDE** answer with "no information" message

6. **Output**: Final response with citations + validation flags

**Boundary Message Templates**:

- **Out-of-Scope**: "I can only answer questions based on the [corpus name]. This topic isn't covered in the available material."
- **Code Generation**: "I can explain concepts from the book but cannot write code or provide implementation details."
- **Real-Time Data**: "I only have information from the [corpus name] as of [date]. I cannot provide real-time or current information."
- **No Information**: "I don't have enough information in the book to answer that question. Try rephrasing or asking about a different topic."

### Consequences

**Benefits**:
- ✅ **Hallucination Prevention**: Empty chunk list → "no information" (never invents answers)
- ✅ **User Trust**: Clear boundaries → users know system limitations
- ✅ **Scope Enforcement**: Out-of-scope detection → prevents scope creep
- ✅ **Safety Compliance**: Medical/legal guardrails → reduces liability risk

**Tradeoffs**:
- ⚠️ **False Positives**: Overly strict guardrails may reject valid questions
- ⚠️ **Maintenance Burden**: Keyword lists need updating as corpus evolves
- ⚠️ **User Frustration**: Too many boundary messages may frustrate users

### When to Use

- Production RAG systems (not prototypes)
- High-stakes domains (medical, legal, financial)
- Systems with strict scope requirements
- Multi-user systems (prevent abuse)

### When NOT to Use

- Internal tools with trusted users only
- Exploratory prototypes (guardrails add friction)
- Systems where hallucination risk is acceptable

### Design Decisions

**Guardrail Strictness**:
- **Strict Mode**: Any violation → Override answer (safer, may frustrate users)
- **Permissive Mode**: Soft violations → Append warning, preserve answer (better UX, some risk)
- **Hybrid Mode**: Hard violations → Override, soft violations → Warn

**Detection Strategy**:
- **Keyword-Based**: Fast, simple, but brittle (misses synonyms)
- **Embedding-Based**: Detect semantic similarity to out-of-scope topics (slower, more robust)
- **LLM-Based**: Use secondary LLM call to classify query intent (expensive, most accurate)

---

## Pattern 5: Browser-Local Session Management

### Problem Statement

How do you provide **conversation history persistence** without requiring user authentication, server-side storage, or compromising user privacy?

### Context

Users expect conversation continuity:
- Scroll through previous questions and answers
- Return to chatbot after navigating away
- Resume conversation after brief interruption

Traditional solutions have tradeoffs:
- **Server-side storage**: Requires authentication, raises privacy concerns, costs money
- **No persistence**: Poor UX, users lose context
- **Cookies**: Limited storage (4KB), privacy regulations (GDPR)

For documentation chatbots and educational tools, authentication is often **not desired**:
- Friction in UX (signup required)
- Privacy concerns (tracking student questions)
- Infrastructure complexity (user management)

### Solution

Use **browser LocalStorage** for client-side session persistence with automatic pruning:

**Session Architecture**:

```
Browser LocalStorage:
  chatbot_session_id: UUID (generated on first visit)
  conversation_history: Array<QueryResponse>
    - query_text
    - answer_text
    - citations
    - timestamp
    - mode
  last_updated: ISO 8601 datetime
```

**Session Lifecycle**:

1. **First Visit**:
   - Check LocalStorage for `chatbot_session_id`
   - If not found → Generate new UUID → Store in LocalStorage
   - Initialize empty `conversation_history` array

2. **Query Submission**:
   - Send query to backend with `session_id` from LocalStorage
   - Receive response
   - Append `{query, answer, citations, timestamp}` to `conversation_history`
   - Update `last_updated` timestamp
   - Save to LocalStorage

3. **Page Navigation**:
   - User navigates to different doc page
   - Session persists (LocalStorage survives navigation)
   - **But**: Clear ephemeral context (selected text, page-specific state)

4. **Return Visit (Same Day)**:
   - Load `conversation_history` from LocalStorage
   - Display previous questions and answers
   - Continue conversation with same `session_id`

5. **Automatic Pruning** (on load):
   - Remove queries older than 7 days
   - Keep only last 20 queries (FIFO)
   - Whichever limit reached first

**Privacy Design**:
- **No server-side storage**: Backend receives `session_id` but does NOT store conversation history
- **No cross-device sync**: History tied to single browser (privacy-preserving)
- **No tracking**: `session_id` is random UUID, not linked to user identity
- **User control**: Clear history button in UI → Wipe LocalStorage

### Consequences

**Benefits**:
- ✅ **Zero Authentication**: No signup, no user management
- ✅ **Privacy-Preserving**: No server-side conversation logs
- ✅ **Zero Cost**: No database storage for sessions
- ✅ **Instant Load**: History loaded from LocalStorage (no network call)
- ✅ **GDPR Compliant**: Data stored locally, user controls deletion

**Tradeoffs**:
- ⚠️ **No Cross-Device Sync**: History lost if user switches browser/device
- ⚠️ **Storage Limits**: LocalStorage ~5-10MB (limit ~200-500 queries)
- ⚠️ **Clearing Risk**: User clearing browser data loses history
- ⚠️ **No Analytics**: Cannot analyze conversation patterns (privacy tradeoff)

### When to Use

- Documentation chatbots (Docusaurus, VitePress, GitBook)
- Educational tools (student privacy critical)
- Demo/prototype applications (no user management overhead)
- Privacy-first applications (GDPR, CCPA compliance)

### When NOT to Use

- Enterprise applications (multi-device sync required)
- Customer support (need server-side conversation logs for agent review)
- Systems requiring conversation analytics (A/B testing, quality monitoring)

### Design Decisions

**Pruning Strategy**:
- **Time-Based**: Keep last 7 days (balances context preservation with storage)
- **Count-Based**: Keep last 20 queries (prevents storage overflow)
- **Hybrid**: Apply both limits (whichever reached first)

**Session ID Scope**:
- **Per-Browser**: Session tied to browser (localStorage key = global)
- **Per-Corpus**: Session tied to specific doc site (localStorage key includes corpus_id)
- **Per-Page**: Session tied to current page (localStorage key includes page_url)

**Fallback Behavior (Storage Disabled)**:
- **Graceful Degradation**: Chatbot works but warns "History won't persist"
- **Hard Failure**: Chatbot refuses to work (not recommended)

---

## Cross-Pattern Relationships

These five patterns work together in RAG chatbot systems:

**Pattern Dependencies**:
```
Multi-Agent Orchestration (Pattern 1)
  ├─→ Uses: Dual-Mode Retrieval (Pattern 2) in Retrieval Agent
  ├─→ Uses: Stable-ID Citation (Pattern 3) in Citation & Guardrails Agent
  └─→ Uses: Guardrails Layer (Pattern 4) in Citation & Guardrails Agent

Browser-Local Session (Pattern 5)
  └─→ Provides: session_id to Multi-Agent Orchestration (Pattern 1)
```

**Common Combinations**:

- **Documentation Chatbot**: Pattern 1 + 2 + 3 + 5 (skip Pattern 4 if low-stakes)
- **Legal Q&A**: Pattern 1 + 3 + 4 (skip Pattern 2 if no text selection, skip Pattern 5 if authentication required)
- **Customer Support**: Pattern 1 + 4 (skip Pattern 2/3 if KB articles are whole chunks, skip Pattern 5 if server sessions needed)

---

## Pattern Application Matrix

| Domain | P1: Multi-Agent | P2: Dual-Mode | P3: Stable-ID | P4: Guardrails | P5: Browser Session |
|--------|----------------|---------------|---------------|----------------|-------------------|
| **Technical Docs** | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Optional | ✅ Yes |
| **Legal Q&A** | ✅ Yes | ⚠️ Optional | ✅ Yes | ✅ Yes | ❌ No (auth required) |
| **Medical KB** | ✅ Yes | ⚠️ Optional | ✅ Yes | ✅ Yes (critical) | ❌ No (HIPAA, auth required) |
| **Customer Support** | ✅ Yes | ❌ No | ⚠️ Optional | ✅ Yes | ❌ No (analytics required) |
| **Educational Content** | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Optional | ✅ Yes (privacy) |
| **Internal Wiki** | ✅ Yes | ⚠️ Optional | ⚠️ Optional | ❌ No | ⚠️ Optional |

**Legend**:
- ✅ **Recommended**: Pattern strongly applies to this domain
- ⚠️ **Optional**: Pattern adds value but not critical
- ❌ **Not Recommended**: Pattern doesn't fit domain constraints

---

## References

- **Source Design**: `specs/001-rag-chatbot/plan.md`
- **Agent Definitions**: `.claude/agents/rag-orchestration/AGENT.md`
- **Skill Overview**: `.claude/skills/rag-chatbot/SKILL.md`
- **Created**: 2025-12-26
- **Version**: 1.0.0
- **License**: Academic Use Only
