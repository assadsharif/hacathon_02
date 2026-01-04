---
name: rag-chatbot
description: Retrieval-Augmented Generation (RAG) chatbot pattern for document-grounded Q&A. Use when building intelligent question-answering systems constrained to specific document corpora (books, wikis, technical docs). Triggers on requests involving semantic search, citation generation, content boundaries, or multi-agent orchestration for RAG systems.
---

# RAG Chatbot Intelligence

## Overview

This skill encapsulates the **conceptual patterns** for building RAG chatbots that answer user questions by retrieving relevant content from a document corpus and synthesizing answers using an LLM.

**Core Value Proposition**: Provide accurate, cited answers constrained to a specific knowledge base without hallucination or scope creep.

## Conceptual Architecture

### Multi-Agent Orchestration Pattern

RAG systems are best designed as **orchestrated multi-agent pipelines** where each agent has a single, well-defined responsibility:

```
User Query
    ↓
┌───────────────────────────────────────────┐
│  Agent 1: Context Selection               │
│  Determines retrieval scope               │
│  Outputs: Scope decision + validation     │
└──────────────┬────────────────────────────┘
               ↓
┌───────────────────────────────────────────┐
│  Agent 2: Retrieval                       │
│  Fetches relevant content                 │
│  Outputs: Ranked document chunks          │
└──────────────┬────────────────────────────┘
               ↓
┌───────────────────────────────────────────┐
│  Agent 3: Answer Synthesis                │
│  Generates natural language answer        │
│  Outputs: Answer text + chunk references  │
└──────────────┬────────────────────────────┘
               ↓
┌───────────────────────────────────────────┐
│  Agent 4: Citation & Guardrails           │
│  Enforces boundaries, adds citations      │
│  Outputs: Final answer with citations     │
└───────────────────────────────────────────┘
```

**Why This Pattern?**
- **Separation of Concerns**: Each agent focuses on one task
- **Independent Testing**: Each agent can be validated separately
- **Reusability**: Agents can be composed for different use cases
- **Failure Isolation**: Errors in one agent don't cascade

## Reusable Agent Roles

### 1. Context Selection Agent

**Responsibility**: Determine the scope of retrieval based on user intent and context.

**Conceptual Inputs**:
- User query (natural language question)
- Query mode (e.g., full-corpus vs. constrained-to-selection)
- Optional: User-highlighted text or section
- Optional: Current page/location context

**Conceptual Outputs**:
- Scope decision (full-corpus | constrained)
- Validation status (valid | warning | error)
- Context metadata for next agent

**Reusable Patterns**:
- **Dual-mode retrieval**: Support both broad searches and focused queries
- **Context validation**: Ensure selected text/scope is meaningful
- **Graceful degradation**: Fallback to broader scope if constrained scope is invalid

**Cross-Domain Applications**:
- Legal document Q&A: Full-corpus vs. specific-case-file retrieval
- Medical knowledge bases: All literature vs. patient-specific documents
- Code documentation: Entire codebase vs. current file/function

---

### 2. Retrieval Agent

**Responsibility**: Fetch semantically relevant content chunks from the corpus.

**Conceptual Inputs**:
- User query
- Retrieval scope (from Context Selection Agent)
- Top-k parameter (how many results)
- Relevance threshold

**Conceptual Outputs**:
- Ranked list of content chunks
- Relevance scores
- Retrieval metadata (latency, candidates evaluated)

**Reusable Patterns**:
- **Vector similarity search**: Embed query, find nearest neighbors in vector space
- **Hybrid retrieval**: Combine semantic (vector) + keyword (BM25) search
- **Constrained retrieval**: Use selected text directly as "chunk" (no search needed)
- **Deduplication**: Remove redundant chunks from same section/source

**Cross-Domain Applications**:
- Customer support: Retrieve relevant KB articles
- Research assistants: Find relevant papers/sections
- E-commerce: Product recommendation based on query embedding

**Technology-Agnostic Approach**:
- Vector database: Qdrant, Pinecone, Weaviate, or in-memory FAISS
- Embedding model: OpenAI, Sentence-BERT, or domain-specific encoders
- Storage: Separate metadata (Postgres, MongoDB) from vectors

---

### 3. Answer Synthesis Agent

**Responsibility**: Generate natural language answers using retrieved content and LLM.

**Conceptual Inputs**:
- User query
- Retrieved content chunks (ranked list)
- Query mode (for response framing)

**Conceptual Outputs**:
- Synthesized answer text
- Chunk IDs used (for citation mapping)
- Confidence score (high | medium | low)

**Reusable Patterns**:
- **Source-grounded synthesis**: LLM prompt includes retrieved chunks only
- **Hallucination prevention**: Explicit instruction to NOT use general knowledge
- **Confidence scoring**: Assess answer quality based on chunk relevance
- **Failure modes**: Return "no information" if chunks insufficient

**Prompt Engineering Patterns**:
```
System: You are a Q&A agent constrained to provided content ONLY.
Rules:
1. ONLY use information from the chunks below
2. NEVER use general knowledge
3. If chunks don't answer the question, say so explicitly
4. Reference which chunks you used

User Query: {query}
Retrieved Content:
{formatted_chunks}
```

**Cross-Domain Applications**:
- Any domain requiring source-grounded answers (legal, medical, technical)
- Multi-lingual Q&A (translate query, retrieve, synthesize in target language)
- Summarization with attribution (news articles, research papers)

---

### 4. Citation & Guardrails Agent

**Responsibility**: Add source citations and enforce content boundaries.

**Conceptual Inputs**:
- Synthesized answer text
- Chunk IDs used in answer
- Corpus metadata (module, chapter, section IDs)

**Conceptual Outputs**:
- Final answer with embedded citations
- Citation list (formatted as links/references)
- Validation flags (boundary violations, hallucination warnings)

**Reusable Patterns**:
- **Citation generation**: Map chunk IDs → human-readable source references
- **Boundary enforcement**: Detect out-of-scope content (medical advice, code generation, etc.)
- **Hallucination detection**: Flag uncertain language ("I think", "maybe", "probably")
- **Override on violation**: Replace answer with boundary message if guardrail triggered

**Guardrail Categories**:
1. **Scope boundaries**: Topic is outside corpus domain
2. **Capability boundaries**: Request for code, implementation details, real-time data
3. **Safety boundaries**: Medical/legal/financial advice
4. **Quality boundaries**: Answer lacks sources, is overly speculative

**Cross-Domain Applications**:
- Healthcare chatbots: Enforce "not medical advice" boundaries
- Legal assistants: Cite case law, statutes with precision
- Educational tools: Ensure answers stay within curriculum scope

---

## Data Model Patterns

### Content Chunking Strategy

**Paragraph-Level Chunking** (Recommended for most text corpora):
- Chunk size: 200-300 tokens (~800-1200 characters)
- Overlap: 50-100 tokens (preserve context across boundaries)
- Metadata: module_id, chapter_id, section_id, paragraph_index

**Why This Works**:
- Granular enough for precise citations
- Large enough for semantic coherence
- Overlap ensures continuity

**Alternative Strategies**:
- **Sentence-level**: Very precise, but may lose context (50-100 tokens)
- **Section-level**: Better context, but less precise citations (500-1000 tokens)
- **Sliding window**: Uniform token count with fixed overlap

### Metadata Schema

**Required Fields**:
- `chunk_id`: Unique identifier (UUID)
- `text_content`: The actual text chunk
- `source_reference`: How to cite this chunk (module, chapter, page, etc.)
- `embedding_vector`: Semantic representation (1536-dim for OpenAI embeddings)

**Optional but Valuable**:
- `token_count`: For chunk size validation
- `relevance_score`: From retrieval (for ranking)
- `created_at` / `updated_at`: For re-indexing workflows

---

## Retrieval Modes (Reusable Pattern)

### Mode 1: Full-Corpus Retrieval

**When to Use**: User asks a general question about any topic in the corpus.

**Flow**:
1. Embed user query using same model as corpus
2. Vector similarity search across all chunks
3. Return top-k chunks (typically 5-10)
4. Synthesize answer from retrieved chunks

**Example Queries**:
- "What is sensor fusion?" → Search entire robotics book
- "Explain inverse kinematics" → Search all chapters

---

### Mode 2: Constrained Retrieval (Selected-Text)

**When to Use**: User highlights text and asks a question about THAT SPECIFIC TEXT.

**Flow**:
1. User selects text on page
2. Treat selection as single "synthetic chunk" (no vector search)
3. Answer constrained to selected text ONLY
4. Useful for "explain this passage" or "simplify this concept"

**Example Queries**:
- User highlights paragraph about PID controllers, asks: "What does this mean in simple terms?"
- Answer must only reference the highlighted text

**Cross-Domain Use Cases**:
- Code review: Select function, ask "What does this do?"
- Legal contracts: Select clause, ask "What are my obligations here?"
- Research papers: Select methodology section, ask "How was this tested?"

---

## Storage Architecture (Technology-Agnostic)

### Three-Tier Storage Model

```
┌─────────────────────────────────────────┐
│  Tier 1: Vector Database                │
│  Purpose: Semantic search                │
│  Stores: embedding_vectors + payload     │
│  Examples: Qdrant, Pinecone, Weaviate   │
└─────────────────────────────────────────┘
         ↕ (chunk_id linkage)
┌─────────────────────────────────────────┐
│  Tier 2: Metadata Database               │
│  Purpose: Citation generation, analytics │
│  Stores: chunk metadata, query logs      │
│  Examples: Postgres, MongoDB, DynamoDB   │
└─────────────────────────────────────────┘
         ↕ (session_id linkage)
┌─────────────────────────────────────────┐
│  Tier 3: Session Storage (Optional)      │
│  Purpose: Conversation history           │
│  Stores: query-response pairs            │
│  Examples: Browser LocalStorage, Redis   │
└─────────────────────────────────────────┘
```

**Why Separate?**
- Vector DBs optimize for similarity search
- Relational DBs optimize for structured queries (analytics, citations)
- Session storage can be ephemeral (privacy-preserving)

---

## Reusability Checklist

When adapting this pattern to a new domain:

### ✅ What Stays the Same (Reusable)
- [ ] Multi-agent orchestration pattern
- [ ] Context selection → Retrieval → Synthesis → Guardrails flow
- [ ] Dual-mode retrieval (full-corpus vs. constrained)
- [ ] Citation generation from chunk IDs
- [ ] Guardrail categories (scope, capability, safety, quality)
- [ ] Three-tier storage architecture

### ⚙️ What Changes (Domain-Specific)
- [ ] **Chunking strategy**: Paragraph vs. sentence vs. section (depends on corpus structure)
- [ ] **Embedding model**: OpenAI vs. domain-specific (medical, legal, code embeddings)
- [ ] **Guardrail rules**: Medical boundaries vs. legal disclaimers vs. code safety
- [ ] **Citation format**: "Module 4: Perception" vs. "Smith v. Jones, 2023" vs. "README.md:45"
- [ ] **Prompt templates**: Educational tone vs. professional tone vs. technical precision

---

## Example Adaptations

### From Physical AI Book → Legal Case Law

**Changes Needed**:
1. **Chunking**: Paragraph-level → Case-section-level (opinions, holdings, dicta)
2. **Citations**: "Module 4" → "Smith v. Jones, 123 F.3d 456 (9th Cir. 2023)"
3. **Guardrails**: "No code generation" → "Not legal advice, consult attorney"
4. **Embedding Model**: General-purpose → Legal-BERT or domain-fine-tuned

**Reusable Components** (90% stays the same):
- Context Selection Agent (full-corpus vs. specific-case retrieval)
- Retrieval Agent (vector search with deduplication)
- Answer Synthesis Agent (source-grounded, hallucination prevention)
- Citation & Guardrails Agent (boundary enforcement, citation mapping)

---

### From Physical AI Book → Customer Support KB

**Changes Needed**:
1. **Chunking**: Paragraph-level → KB-article-level (each article is a chunk)
2. **Citations**: "Module 4: Chapter" → "KB Article #1234: How to Reset Password"
3. **Guardrails**: Educational boundaries → Customer tone, escalation triggers
4. **Query Mode**: Add "multi-turn conversation" mode for follow-ups

**Reusable Components** (95% stays the same):
- All 4 agents with minimal prompt adjustments
- Storage architecture (swap "module" for "category")
- Retrieval flow (semantic search across KB articles)

---

## Integration Patterns

### Pattern 1: Embedded in Documentation Site

**Use Case**: Physical AI Book (Docusaurus), technical wikis, product docs

**Architecture**:
- Backend: RAG API (FastAPI, Express, Flask)
- Frontend: React component embedded in docs site
- Session: Browser LocalStorage (privacy-preserving)

**Why This Works**:
- Users never leave documentation
- Context-aware (knows current page)
- Progressive enhancement (docs work without chatbot)

---

### Pattern 2: Standalone Chat Application

**Use Case**: Customer support, research assistants

**Architecture**:
- Backend: RAG API with persistent sessions (Redis, DynamoDB)
- Frontend: Dedicated chat UI (ChatGPT-like interface)
- Session: Server-side storage with authentication

**Why This Works**:
- Multi-device conversation history
- User authentication for personalization
- Full-featured chat UX

---

### Pattern 3: Slack/Discord Bot

**Use Case**: Internal knowledge bases, team wikis

**Architecture**:
- Backend: RAG API
- Frontend: Bot integration (Slack API, Discord.js)
- Session: Thread-based (Slack thread ID = session ID)

**Why This Works**:
- Zero deployment friction (users already in Slack/Discord)
- Threaded conversations natural fit for Q&A
- Team-wide knowledge sharing

---

## Performance Targets (Reusable Benchmarks)

### Latency Goals
- **Retrieval**: <500ms (p99) for vector search
- **Synthesis**: <2s (p95) for LLM response
- **Total pipeline**: <3s (p95) end-to-end

### Quality Metrics
- **Citation accuracy**: 100% (every answer must cite sources)
- **Boundary adherence**: >95% (low hallucination rate)
- **Retrieval relevance**: >80% (top-3 chunks should be relevant)

### Scalability
- **Concurrent users**: Design for 10-100 initially (free-tier constraints)
- **Corpus size**: Up to 1M chunks (~500-page book or 1000-article KB)
- **Query volume**: 1000-10,000 queries/day

---

## Best Practices

### 1. **Start with a Small Corpus**
- Index 10-20 documents first
- Validate retrieval quality before scaling
- Iterate on chunking strategy

### 2. **Monitor Hallucination Rate**
- Log all queries + answers
- Sample 5-10% for manual review
- Track "out-of-scope" detection accuracy

### 3. **Version Your Corpus**
- When docs update, create new vector collection (e.g., `corpus-v2`)
- Swap collection name in config (zero-downtime migration)
- Keep old version for rollback

### 4. **Use Guardrails Liberally**
- Better to refuse a question than hallucinate
- Provide clear boundary messages ("I can only answer X, not Y")
- Log boundary violations for guardrail refinement

### 5. **Optimize Costs**
- Use smaller embedding models where acceptable (text-embedding-3-small vs. large)
- Cache embeddings for frequently asked questions
- Implement rate limiting (prevent abuse)

---

## References

- **Agent Implementations**: See `rag-chatbot/src/agents/` for concrete examples
- **Orchestrator Pattern**: See `rag-chatbot/src/services/orchestrator.py`
- **Data Model**: See `specs/001-rag-chatbot/data-model.md`
- **API Contracts**: See `specs/001-rag-chatbot/contracts/openapi.yaml`

---

## When NOT to Use This Pattern

❌ **Don't use RAG when**:
- Corpus is tiny (<100 pages) → Simple keyword search may suffice
- Answers require real-time data → RAG is for static corpora
- No source attribution needed → Standard LLM fine-tuning may be better
- Highly structured data → SQL database + natural language-to-SQL may be better

✅ **DO use RAG when**:
- Corpus is large (100+ pages to millions of documents)
- Source citations are critical (legal, medical, academic)
- Content updates frequently (easier to re-index than retrain)
- Privacy/security requires on-premises deployment (no cloud LLM fine-tuning)
