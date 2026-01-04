---
name: docusaurus-book
description: Create and manage Docusaurus-based documentation books. Use when building structured educational content, technical books, or multi-module documentation sites. Triggers on requests involving Docusaurus setup, sidebar configuration, MDX content authoring, versioning, or GitHub Pages deployment.
---

# Docusaurus Book Authoring

## Quick Start

Initialize a new Docusaurus site:
```bash
npx create-docusaurus@latest my-book classic --typescript
```

## Project Structure

```
my-book/
├── docusaurus.config.ts    # Site configuration
├── sidebars.ts             # Navigation structure
├── docs/                   # Main content (modules/chapters)
│   ├── intro.md
│   └── module-1/
│       ├── _category_.json # Module metadata
│       ├── index.md        # Module overview
│       └── chapter-1.md
├── src/
│   └── pages/              # Custom pages (homepage)
└── static/                 # Images, assets
```

## Content Authoring

### Module Structure
Each module uses `_category_.json`:
```json
{
  "label": "Module 1: Introduction",
  "position": 1,
  "link": {"type": "doc", "id": "module-1/index"}
}
```

### Chapter Frontmatter
```markdown
---
sidebar_position: 1
title: Chapter Title
description: Brief description for SEO
---

# Chapter Title

## Learning Outcomes
- Outcome 1
- Outcome 2
```

### Sidebar Configuration
See [references/sidebar-patterns.md](references/sidebar-patterns.md) for advanced patterns.

## GitHub Pages Deployment

### GitHub Actions Workflow
See [references/deployment.md](references/deployment.md) for workflow configuration.

### Key Settings
- Set `baseUrl` to `/<repo-name>/` for project sites
- Enable GitHub Pages in repository settings → Pages → Source: GitHub Actions

## Versioning Strategy

For future phases, use Docusaurus versioning:
```bash
npm run docusaurus docs:version 1.0
```

This creates `versioned_docs/version-1.0/` preserving Phase 1 content while Phase 2+ evolves.

## Best Practices

1. **One concept per chapter** - Keep chapters focused
2. **Progressive complexity** - Order by difficulty within modules
3. **Cross-linking** - Use `[text](../module-2/chapter-1.md)` for related topics
4. **Consistent structure** - Every module has overview, learning outcomes, chapters
5. **Image organization** - Store in `static/img/<module-name>/`
