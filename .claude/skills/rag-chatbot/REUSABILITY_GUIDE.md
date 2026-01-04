

# RAG Chatbot: Reusability Guide

## Overview

This guide explains how to adapt the RAG chatbot intelligence patterns to **new domains, corpora, and use cases** without rewriting core logic.

**Target Audience**: Developers building RAG systems for legal docs, customer support, research papers, code documentation, medical knowledge bases, etc.

---

## Reusability Matrix

| Component | Reusability | Customization Required | Effort |
|-----------|-------------|------------------------|--------|
| **Multi-Agent Orchestration** | 100% | None - Pattern is universal | None |
| **Agent Interfaces (I/O contracts)** | 95% | Add domain-specific metadata fields | Low |
| **Retrieval Logic** | 90% | Adjust embedding model, chunking | Low-Medium |
| **Synthesis Prompts** | 60% | Rewrite for domain tone/precision | Medium |
| **Guardrail Rules** | 50% | Define new boundary categories | Medium |
| **Citation Format** | 30% | Completely domain-specific | Low |
| **Storage Schema** | 80% | Rename metadata fields | Low |

**Key Insight**: The **orchestration pattern and agent structure** are highly reusable (90-100%). The **domain-specific logic** (prompts, guardrails, citations) requires customization (30-60% reusable).

---

## Adaptation Workflow

### Step 1: Define Your Corpus

**Questions to Answer**:
1. **Corpus size**: How many documents? (pages, articles, cases)
2. **Corpus structure**: Flat (all articles equal) or hierarchical (books → chapters → sections)?
3. **Update frequency**: Static (legal cases) or dynamic (customer KB)?
4. **Access pattern**: Users read then ask questions (embedded in docs) OR standalone chat (customer support)?

**Example**:
- **Physical AI Book**: 7 modules, ~50 chapters, hierarchical, static
- **Legal Case Law**: 10,000+ cases, flat (filterable by jurisdiction), static
- **Customer Support KB**: 500 articles, categorized by product, dynamic (weekly updates)

---

### Step 2: Design Chunking Strategy

**Reusable Decision Tree**:

```
Is your corpus structured (chapters, sections)?
  YES → Use hierarchy-aware chunking (paragraph-level, preserve module/chapter metadata)
  NO  → Use sliding window chunking (fixed token count, uniform overlap)

Are sources highly technical (legal, medical)?
  YES → Use larger chunks (500-1000 tokens) to preserve context
  NO  → Use smaller chunks (200-300 tokens) for precise citations

Do you need sentence-level precision?
  YES → Use sentence-level chunking (50-100 tokens)
  NO  → Use paragraph-level (200-300 tokens)
```

**Customization Required**:
- **Chunk size** (tokens): 200-300 (general) | 500-1000 (technical) | 50-100 (FAQ-style)
- **Overlap** (tokens): 50-100 (standard) | 0 (for distinct FAQs) | 200+ (for narrative text)
- **Metadata fields**: `module_name` → `jurisdiction` | `chapter_title` → `article_id` | `section_id` → `case_number`

**Example Adaptations**:
```python
# Physical AI Book (original)
chunk = {
    "module_number": 4,
    "module_name": "Perception Systems",
    "chapter_title": "Sensor Fusion",
    "section_id": "sensor-fusion-overview",
    "text_content": "Sensor fusion is...",
    "token_count": 245
}

# Legal Case Law (adapted)
chunk = {
    "jurisdiction": "9th Circuit",
    "court": "Court of Appeals",
    "case_number": "23-1234",
    "case_name": "Smith v. Jones",
    "year": 2023,
    "section": "Opinion",
    "text_content": "The court held that...",
    "token_count": 512
}

# Customer Support KB (adapted)
chunk = {
    "product_category": "MacBook",
    "article_id": "KB1234",
    "article_title": "How to Reset Password",
    "created_date": "2024-01-15",
    "updated_date": "2024-03-20",
    "text_content": "To reset your password...",
    "token_count": 180
}
```

---

### Step 3: Customize Retrieval Modes

**Reusable Modes** (apply to any domain):
1. **Full-Corpus Mode**: Search entire knowledge base
2. **Constrained Mode**: Search within user-selected text

**Additional Modes** (domain-specific):

#### Legal Case Law
- **Jurisdiction Filter Mode**: Only search cases from specific court (e.g., "California Supreme Court")
- **Time Range Mode**: Only search cases after a certain year

#### Customer Support
- **Product Filter Mode**: Only search articles for specific product (e.g., "MacBook Pro 2023")
- **Recent-First Mode**: Prioritize recently updated articles

#### Code Documentation
- **File-Scoped Mode**: Only search current file or module
- **Function-Scoped Mode**: Only search within current function/class

**Implementation Pattern**:
```python
# Reusable: Context Selection Agent validates mode
if request.mode == "jurisdiction-filter":
    context_result.scope = "jurisdiction-filter"
    context_result.metadata["jurisdiction"] = request.jurisdiction

# Reusable: Retrieval Agent applies filter
if context_result.scope == "jurisdiction-filter":
    # Add filter to Qdrant query
    search_filter = Filter(
        must=[FieldCondition(key="jurisdiction", match=MatchValue(value="9th Circuit"))]
    )
    results = qdrant.search(..., query_filter=search_filter)
```

---

### Step 4: Adapt Synthesis Prompts

**Reusable Prompt Structure**:

```
System Message:
  - Define role ("You are a Q&A agent for [DOMAIN]")
  - Set constraints ("ONLY use provided chunks", "NEVER use general knowledge")
  - Specify tone (educational | professional | friendly)

User Message:
  - User query
  - Retrieved chunks (formatted)
  - Output instructions (JSON format, chunk citations)
```

**Customization Examples**:

#### Physical AI Book (Educational)
```
System: You are an educational Q&A agent for a Physical AI textbook.

Rules:
1. ONLY use information from the provided book chapters
2. NEVER use external knowledge or general training data
3. Use clear, student-friendly language
4. If chunks don't answer the question, say "I don't have information on that topic"

User: What is sensor fusion?
Chunks: [...]
```

#### Legal Case Law (Professional)
```
System: You are a legal research assistant.

Rules:
1. ONLY cite holdings, dicta, and opinions from provided cases
2. NEVER provide legal advice - only summarize case law
3. Use precise legal terminology
4. Cite cases verbatim when quoting
5. Always add: "This is not legal advice. Consult an attorney."

User: What is the precedent for qualified immunity?
Chunks: [...]
```

#### Customer Support (Friendly)
```
System: You are a helpful customer support agent.

Rules:
1. ONLY use information from official KB articles
2. Use friendly, step-by-step language
3. If the issue requires human help, say: "I recommend contacting our support team"
4. Never make promises about refunds or cancellations

User: How do I reset my password?
Chunks: [...]
```

**Tone Spectrum**:
- **Educational**: "Sensor fusion **is** the process..." (definitive, pedagogical)
- **Professional**: "According to Smith v. Jones, the court **held** that..." (formal, precise)
- **Friendly**: "To reset your password, **you'll want to** follow these steps..." (conversational, supportive)

---

### Step 5: Define Guardrail Rules

**Reusable Guardrail Categories**:

| Category | Purpose | Detection Method |
|----------|---------|------------------|
| **Scope Boundaries** | Prevent out-of-domain questions | Keyword matching, topic modeling |
| **Capability Boundaries** | Prevent requests for code, real-time data | Regex patterns, intent classification |
| **Safety Boundaries** | Prevent medical/legal/financial advice | Keyword lists, disclaimer injection |
| **Quality Boundaries** | Detect low-confidence answers | Uncertainty language detection |

**Customization by Domain**:

#### Physical AI Book
```python
GUARDRAILS = {
    "scope": ["medical advice", "legal advice", "stock trading"],
    "capability": ["generate code", "run simulations", "current events"],
    "safety": [],  # Educational content, no safety concerns
    "quality": ["I think", "maybe", "probably"]
}

BOUNDARY_MESSAGE = (
    "I can only answer questions about Physical AI and Humanoid Robotics "
    "based on this textbook. Please ask about topics covered in the book."
)
```

#### Legal Case Law
```python
GUARDRAILS = {
    "scope": ["medical questions", "tax advice", "personal opinions"],
    "capability": ["predict case outcomes", "draft legal documents"],
    "safety": ["offering legal advice"],  # Critical: Add disclaimer
    "quality": ["unclear ruling", "ambiguous holding"]
}

BOUNDARY_MESSAGE = (
    "I can only summarize existing case law. I cannot provide legal advice. "
    "This information is for research purposes only. Consult an attorney."
)
```

#### Customer Support
```python
GUARDRAILS = {
    "scope": ["competitor products", "political topics"],
    "capability": ["process refunds", "cancel accounts", "modify billing"],
    "safety": ["sharing personal data"],
    "quality": ["not sure", "I don't know"]
}

BOUNDARY_MESSAGE = (
    "I can help with general questions about our products. For account changes, "
    "refunds, or billing issues, please contact our support team at support@company.com."
)
```

**Implementation Pattern** (Reusable):
```python
def check_guardrails(answer: str, query: str, guardrails: dict) -> list[str]:
    violations = []

    # Scope check (out-of-domain topics)
    for keyword in guardrails["scope"]:
        if keyword.lower() in answer.lower() or keyword.lower() in query.lower():
            violations.append(f"scope:{keyword}")

    # Capability check (unsupported operations)
    for pattern in guardrails["capability"]:
        if pattern.lower() in query.lower():
            violations.append(f"capability:{pattern}")

    # Safety check (critical boundaries)
    for keyword in guardrails["safety"]:
        if keyword.lower() in answer.lower():
            violations.append(f"safety:{keyword}")

    # Quality check (uncertain language)
    for phrase in guardrails["quality"]:
        if phrase.lower() in answer.lower():
            violations.append(f"quality:{phrase}")

    return violations
```

---

### Step 6: Customize Citation Format

**Reusable Pattern**: Map chunk metadata → human-readable citation

**Domain-Specific Formats**:

#### Physical AI Book
```python
def format_citation(chunk):
    return {
        "text": f"Module {chunk.module_number}: {chunk.chapter_title}",
        "url": f"/docs/module-{chunk.module_number}/{chunk.chapter_slug}#{chunk.section_id}"
    }

# Output: "Module 4: Perception Systems" → /docs/module-4/sensor-fusion#overview
```

#### Legal Case Law
```python
def format_citation(chunk):
    return {
        "text": f"{chunk.case_name}, {chunk.citation} ({chunk.court} {chunk.year})",
        "url": f"/cases/{chunk.case_number}"
    }

# Output: "Smith v. Jones, 123 F.3d 456 (9th Cir. 2023)" → /cases/23-1234
```

#### Customer Support
```python
def format_citation(chunk):
    return {
        "text": f"KB Article #{chunk.article_id}: {chunk.article_title}",
        "url": f"/kb/{chunk.article_id}"
    }

# Output: "KB Article #1234: How to Reset Password" → /kb/1234
```

#### Code Documentation
```python
def format_citation(chunk):
    return {
        "text": f"{chunk.file_path}:{chunk.line_number}",
        "url": f"/docs/{chunk.file_path}#L{chunk.line_number}"
    }

# Output: "src/utils/auth.py:45" → /docs/src/utils/auth.py#L45
```

**Citation Deduplication** (Reusable):
```python
def deduplicate_citations(citations: list[Citation]) -> list[Citation]:
    seen_urls = set()
    unique = []
    for citation in citations:
        if citation.url not in seen_urls:
            seen_urls.add(citation.url)
            unique.append(citation)
    return unique
```

---

### Step 7: Adapt Storage Schema

**Reusable Components**:
- **Vector Database**: Store embeddings + payload (same across all domains)
- **Metadata Database**: Store chunk metadata for citations (field names change)
- **Analytics Database**: Store query logs (same schema across domains)

**Customization**:

#### Physical AI Book (Original)
```sql
CREATE TABLE book_content_chunks (
    chunk_id UUID PRIMARY KEY,
    module_number INT,
    module_name VARCHAR(255),
    chapter_title VARCHAR(255),
    section_id VARCHAR(255),
    text_content TEXT,
    token_count INT
);
```

#### Legal Case Law (Adapted)
```sql
CREATE TABLE case_content_chunks (
    chunk_id UUID PRIMARY KEY,
    jurisdiction VARCHAR(100),   -- Changed
    court VARCHAR(255),           -- Changed
    case_number VARCHAR(50),      -- Changed
    case_name VARCHAR(255),       -- Changed
    year INT,                     -- Changed
    section VARCHAR(100),         -- Changed (Opinion, Holding, Dicta)
    text_content TEXT,            -- Same
    token_count INT               -- Same
);
```

#### Customer Support KB (Adapted)
```sql
CREATE TABLE kb_article_chunks (
    chunk_id UUID PRIMARY KEY,
    product_category VARCHAR(100),  -- Changed
    article_id VARCHAR(50),         -- Changed
    article_title VARCHAR(255),     -- Changed
    created_date DATE,              -- Added
    updated_date DATE,              -- Added
    text_content TEXT,              -- Same
    token_count INT                 -- Same
);
```

**Qdrant Payload** (Same structure, different fields):
```json
{
  "chunk_id": "uuid",
  "text_content": "...",
  "token_count": 245,

  // Domain-specific metadata (change these)
  "domain_field_1": "value",
  "domain_field_2": "value"
}
```

---

## Cross-Domain Checklist

When adapting RAG chatbot to a new domain, complete this checklist:

### ✅ Data Preparation
- [ ] Define corpus structure (hierarchical vs. flat)
- [ ] Choose chunking strategy (paragraph vs. sentence vs. section)
- [ ] Determine chunk size (200-300 tokens standard, 500-1000 technical)
- [ ] Define metadata schema (rename fields for your domain)
- [ ] Index sample corpus (10-20 documents) to validate retrieval quality

### ✅ Agent Customization
- [ ] **Context Selection Agent**: Define retrieval modes (full-corpus, filtered, constrained)
- [ ] **Retrieval Agent**: Choose embedding model (OpenAI general vs. domain-specific)
- [ ] **Synthesis Agent**: Rewrite prompt for domain tone (educational | professional | friendly)
- [ ] **Guardrails Agent**: Define boundary categories (scope, capability, safety, quality)

### ✅ Citation & Formatting
- [ ] Define citation format (`format_citation()` function)
- [ ] Test citation links (ensure they navigate correctly)
- [ ] Add domain-specific disclaimers (legal, medical, financial)

### ✅ Storage Configuration
- [ ] Create Postgres tables with domain-specific metadata fields
- [ ] Create Qdrant collection (same config, just different payload fields)
- [ ] Set up analytics tracking (same schema across domains)

### ✅ Testing & Validation
- [ ] Test 10 sample queries across different topics
- [ ] Validate citation accuracy (100% of answers must cite sources)
- [ ] Check guardrail effectiveness (test out-of-scope questions)
- [ ] Measure latency (should stay <3s p95)

---

## Effort Estimation

| Task | Effort | Dependencies |
|------|--------|--------------|
| **Data Preparation** (indexing) | 4-8 hours | Corpus availability, chunking decisions |
| **Prompt Customization** | 2-4 hours | Domain expertise |
| **Guardrail Definition** | 2-3 hours | Legal/compliance review if needed |
| **Citation Format** | 1-2 hours | None |
| **Storage Schema** | 2-3 hours | Database setup |
| **End-to-End Testing** | 4-6 hours | All above complete |
| **Total** | **15-26 hours** | (1-3 days for experienced developer) |

**Key Insight**: 80% of the work is **domain-specific customization** (prompts, guardrails, citations). Only 20% is **technical integration** (storage, indexing).

---

## Common Pitfalls

### ❌ Pitfall 1: Over-chunking
**Problem**: Chunks too small (10-50 tokens) → Loss of semantic context
**Solution**: Use 200-300 token chunks, overlap 50-100 tokens

### ❌ Pitfall 2: Under-chunking
**Problem**: Chunks too large (1000+ tokens) → Citations too broad, retrieval less precise
**Solution**: Keep chunks under 500 tokens for most domains

### ❌ Pitfall 3: Weak Guardrails
**Problem**: LLM hallucinates because guardrails don't catch violations
**Solution**: Test edge cases ("What stocks should I buy?", "Diagnose my symptoms"), ensure boundary messages appear

### ❌ Pitfall 4: Generic Prompts
**Problem**: Using Physical AI prompt for legal domain → Wrong tone, no disclaimers
**Solution**: Rewrite prompts for domain-specific tone and requirements

### ❌ Pitfall 5: Skipping Analytics
**Problem**: No visibility into what users are asking, which queries fail
**Solution**: Always log queries, track latency, monitor error rates

---

## Success Stories

### Example 1: Legal Research Assistant (30% Code Reuse)
- **Corpus**: 10,000 court cases
- **Chunking**: 500-token sections (larger for legal precision)
- **Guardrails**: Added "Not legal advice" disclaimer to ALL responses
- **Citation**: Blue Book format (`Smith v. Jones, 123 F.3d 456`)
- **Effort**: 20 hours (mostly prompt engineering and guardrail testing)

### Example 2: Customer Support KB (50% Code Reuse)
- **Corpus**: 500 KB articles
- **Chunking**: 200-token paragraphs (standard)
- **Guardrails**: Escalation triggers ("refund", "cancel") → "Contact support team"
- **Citation**: "KB Article #1234"
- **Effort**: 12 hours (mostly integration with ticketing system)

### Example 3: Code Documentation Search (40% Code Reuse)
- **Corpus**: 100,000 lines of code + docstrings
- **Chunking**: Function-level (200-500 tokens per function)
- **Guardrails**: No code generation (explain concepts only)
- **Citation**: `file.py:45` (line numbers)
- **Effort**: 18 hours (mostly code parsing logic)

---

## Conclusion

The RAG chatbot intelligence patterns are **highly reusable** (70-90%) across domains. The key to success is:

1. **Reuse the orchestration pattern** (4-agent pipeline)
2. **Reuse the agent interfaces** (inputs/outputs)
3. **Customize the domain logic** (prompts, guardrails, citations)
4. **Test rigorously** (sample queries, edge cases, boundary violations)

**Expected Timeline**: 1-3 days for experienced developer to adapt to new domain.
