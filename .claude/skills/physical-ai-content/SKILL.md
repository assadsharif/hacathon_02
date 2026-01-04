---
name: physical-ai-content
description: Domain expertise for Physical AI and Humanoid Robotics content authoring. Use when writing educational content about embodied intelligence, humanoid robots, perception-action loops, or robot learning. Provides terminology, conceptual frameworks, and content structure guidance for robotics education.
---

# Physical AI Content Authoring

## Core Concepts

### Physical AI Definition
Physical AI = AI systems that:
1. Perceive the physical world through sensors
2. Act upon it through actuators
3. Learn from physical interaction
4. Exhibit embodied intelligence

### Key Distinctions
| Traditional AI | Physical AI |
|---------------|-------------|
| Disembodied | Embodied |
| Static data | Dynamic sensing |
| Software-only | Hardware integration |
| Simulated environments | Real-world physics |

## Content Structure Guidelines

### Module Introduction Pattern
```markdown
# Module N: [Title]

## Overview
[2-3 paragraphs explaining the module's place in the curriculum]

## Learning Outcomes
By the end of this module, you will be able to:
- [Outcome 1 - use action verbs: explain, identify, compare]
- [Outcome 2]
- [Outcome 3]

## Prerequisites
- [Required prior knowledge]
- [Recommended modules to complete first]

## Chapters
1. [Chapter title] - [brief description]
2. [Chapter title] - [brief description]
```

### Chapter Pattern
```markdown
# Chapter Title

## Key Concepts
[Bullet list of concepts covered]

## [Main Content Sections]

## Summary
[Key takeaways]

## Further Reading
[Academic references, papers, resources]
```

## Terminology Reference

See [references/terminology.md](references/terminology.md) for Physical AI vocabulary.

## Module Topics Reference

See [references/module-topics.md](references/module-topics.md) for detailed topic breakdowns per module.

---

## Phase 2: Interactive Learning System Architecture

**Scope**: Conceptual design specifications for intelligent assistance capabilities.
**Constraints**: Documentation and architectural specification only. No implementation.

### RAG System Specification

**Purpose**: Retrieval-augmented generation for contextual assistance within documentation.

**System Boundaries**:
- Query understanding and intent classification
- Retrieval strategy selection based on query characteristics
- Context assembly from retrieved sources
- Response generation grounded in documentation content
- Citation and source attribution mechanisms

**Quality Requirements**:
- Factual accuracy (responses must align with source documentation)
- Citation transparency (every claim traceable to source)
- Relevance ranking (most pertinent information prioritized)
- Context coherence (retrieved chunks must form logical context)
- Latency constraints (retrieval and generation within acceptable bounds)

**Retrieval Strategies**:

**Document-Level Retrieval**:
- Semantic similarity across entire documents
- Module-level granularity for broad queries
- Chapter-level granularity for specific topics
- Cross-reference resolution between modules

**Selection-Level Retrieval**:
- Paragraph-level semantic chunks
- Heading-aware segmentation boundaries
- Key concept extraction and indexing
- Definition and terminology isolation

**Hybrid Retrieval**:
- Keyword matching for technical terms
- Semantic similarity for conceptual queries
- Metadata filtering (module, chapter, topic tags)
- Recency and update timestamp weighting

### Agent Architecture Specification

**Framework Consideration**: OpenAI Agents / ChatKit architectural patterns.

**Agent Capabilities**:
- Conversational state management across multi-turn interactions
- Tool invocation for retrieval operations
- Response formatting and structuring
- Context window management and truncation strategies
- Error recovery and clarification requests

**Agent Boundaries**:
- Read-only access to documentation corpus
- No modification of underlying content
- No external API calls beyond configured retrieval
- No persistent user data storage beyond session context

**Conversation Flow**:
- Query reception and intent classification
- Retrieval strategy selection
- Context assembly from vector and metadata sources
- Response generation with citation
- Follow-up question handling
- Disambiguation and clarification protocols

### Vector Database Design

**Technology Consideration**: Qdrant conceptual model.

**Index Structure**:
- Embedding dimensionality aligned with chosen model
- Collection organization by content type (module, chapter, paragraph)
- Payload schema for metadata attachment
- HNSW graph construction parameters for recall/latency tradeoff

**Metadata Schema**:
- Document identifiers (module, chapter, section)
- Content type classification (definition, example, summary)
- Hierarchy information (parent-child relationships)
- Update timestamps for freshness tracking
- Cross-reference links to related content

**Query Mechanisms**:
- Vector similarity search with configurable k
- Metadata filtering for scoped retrieval
- Score threshold enforcement for quality control
- Hybrid search combining vector and keyword signals

**Operational Requirements**:
- Index update strategy on content changes
- Backup and recovery procedures
- Performance monitoring and query latency tracking

### Relational Metadata Storage

**Technology Consideration**: Neon Postgres conceptual schema.

**Metadata Entities**:
- Content hierarchy (modules, chapters, sections)
- Cross-reference graph (bidirectional links)
- Learning path sequences and prerequisites
- User interaction logs (queries, retrievals, feedback)
- System performance metrics (latency, retrieval quality)

**Relational Constraints**:
- Referential integrity between content entities
- Cascade deletion rules for content removal
- Unique constraints on document identifiers
- Temporal validity for versioned content

**Query Patterns**:
- Hierarchical traversal for context assembly
- Graph queries for related content discovery
- Temporal queries for version history
- Aggregation for analytics and insights

**Schema Evolution**:
- Migration strategy for schema changes
- Backward compatibility requirements
- Versioning and rollback procedures

### API Boundary Design

**Technology Consideration**: FastAPI interface patterns.

**Endpoint Categories**:
- Query submission and response retrieval
- Feedback collection for response quality
- System health and status monitoring
- Administrative operations (index refresh, metrics)

**Request Specifications**:
- Query payload structure (text, filters, context)
- Authentication and authorization requirements
- Rate limiting and quota enforcement
- Request validation and error responses

**Response Specifications**:
- Response payload structure (answer, citations, confidence)
- Error taxonomy and status codes
- Pagination for large result sets
- Streaming for incremental response delivery

**Interface Contracts**:
- Versioning strategy for API evolution
- Deprecation policy and migration paths
- Schema documentation and validation
- Client SDK considerations

**Non-Functional Requirements**:
- Response time targets (p50, p95, p99)
- Throughput capacity and scaling boundaries
- Error rate thresholds
- Availability and uptime commitments

### Docusaurus Integration Specification

**Embedding Strategy**:
- Chat widget placement and visibility controls
- Responsive design for mobile and desktop viewports
- Accessibility compliance (WCAG AA)
- Theming consistency with documentation style

**User Experience Flow**:
- Widget activation and deactivation
- Query input and response display
- Citation navigation to source content
- Conversation history management
- Feedback mechanism for response quality

**Performance Considerations**:
- Lazy loading to minimize page load impact
- Asynchronous communication to prevent blocking
- Client-side caching for repeated queries
- Progressive enhancement for feature availability

**Privacy and Security**:
- Query data handling and retention policies
- No personally identifiable information collection
- Compliance with data protection regulations
- Opt-out mechanisms for users

---

## Phase 2 Constraints and Boundaries

**Explicitly Forbidden in Skill Usage**:
- Writing implementation code for endpoints, database schemas, or agents
- Generating pseudo-code or code templates
- Creating SQL queries or database migration scripts
- Writing production prompts for chatbot responses
- Implementing vector indexing or embedding generation code
- Building frontend components or UI code

**Permitted in Skill Usage**:
- Architectural diagrams and system boundary definitions
- Interface specifications and contract definitions
- Quality requirements and acceptance criteria
- Trade-off analysis between design alternatives
- Conceptual models and data flow descriptions
- Non-functional requirements and operational constraints

**Phase 2 Delivery Artifacts**:
- System architecture specifications
- API interface definitions (OpenAPI/Swagger schemas)
- Data model conceptual schemas (ERD, vector payload structures)
- Quality attribute scenarios and acceptance criteria
- Deployment topology and component diagrams
- Operational runbooks and monitoring requirements

**SDD Compliance**:
All Phase 2 specifications must be:
- Declarative (describing what, not how)
- Testable (clear acceptance criteria)
- Technology-agnostic where possible (specify patterns, not products)
- Separated from implementation (design before code)
- Documented in spec.md, plan.md, tasks.md artifacts per SDD methodology
