# Phase III Constitution — Hackathon II

## Purpose
Introduce an AI-powered conversational interface for the Todo system
WITHOUT altering Phase I (domain logic) or Phase II (web architecture).

## Authority Order
1. Phase I Specs (Domain Truth)
2. Phase II Specs (System Truth)
3. Phase III Constitution
4. Phase III Specify
5. Phase III Plan
6. Phase III Tasks
7. Phase III Implementation

## Core Principle
AI is an INTERFACE, not a decision-maker.

## Non-Negotiable Rules
- AI MUST NOT bypass backend APIs
- AI MUST NOT mutate database directly
- AI MUST NOT invent features or data
- AI MUST act through defined tools only
- All actions must be explainable and traceable

## Technology Lock
- OpenAI ChatKit (UI + orchestration)
- OpenAI Agents SDK
- Official MCP SDK
- Existing FastAPI backend (Phase II)
- Existing DB schema (Phase II)

## Forbidden Patterns
- AI writing SQL
- AI calling DB
- AI embedding business rules
- AI acting without tool invocation
- Prompt-based logic instead of specs

## Success Criteria
- User can manage todos via natural language
- AI maps intent → tool → backend → result
- Phase I & II remain unchanged and functional

## Compatibility Guarantees
- Phase I CLI app continues to work
- Phase II web app continues to work
- AI interface is additive, not replacement
- All existing tests must pass
