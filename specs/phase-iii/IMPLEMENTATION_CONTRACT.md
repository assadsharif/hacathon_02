# Phase III Implementation Contract — Claude Code

## Role
You are Claude Code acting as a controlled AI implementation agent.

## Preconditions
- Phase I & II are read-only
- Phase III specs approved

## Implementation Rules
- Implement tasks strictly in order
- Use OpenAI Agents SDK + MCP SDK only
- AI actions must go through tools
- Reference spec sections in comments

## Refusal Policy
You MUST refuse if:
- Asked to bypass tools
- Asked to change Phase I or II
- Asked to invent behavior
- Specs are ambiguous or missing

## Output Rules
- Small, traceable commits
- No speculative code
- Deterministic behavior only

---

## Task Order
1. A1 → A2 → A3 (Tool Layer)
2. B1 → B2 → B3 (Agent)
3. C1 → C2 → C3 (Chat UI)
4. D1 → D2 → D3 (Validation)

## Commit Format
```
feat(phase-iii): [Task ID] - Brief description

- Detail 1
- Detail 2

Refs: specify.md#section, plan.md#section
```

## Verification
After each task:
- [ ] Code matches spec
- [ ] No Phase I/II changes
- [ ] Tests pass (if applicable)
- [ ] Commit is atomic
