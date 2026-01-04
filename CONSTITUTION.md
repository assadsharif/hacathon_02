# Project Constitution: Todo App - Spec-Driven Development

## Purpose
Build a Todo Application strictly via Specifications following Spec-Driven Development (SDD) principles.

## Core Principles

### 1. Specification-First Development
- **Every feature must have a specification** before any code is written
- Specifications define:
  - User stories
  - Acceptance criteria
  - Technical requirements
  - Function signatures
  - Data structures
- No implementation without a finalized spec

### 2. Data Constraint: In-Memory Only
- **All data must be stored IN-MEMORY only**
- ❌ No database connections
- ❌ No file system persistence
- ❌ No external storage systems
- ✅ Python data structures (lists, dictionaries, objects)
- ✅ Data lives only during program execution

### 3. Quality Standards
Adhere to Clean Code principles:

#### Code Style
- Follow **PEP 8** style guide
- Use **type hints** for all function signatures
- Maintain **modular structure** with clear separation of concerns
- Keep functions small and focused (Single Responsibility Principle)

#### Code Organization
- Clear module boundaries
- Logical file structure
- Descriptive naming conventions
- Minimal coupling, high cohesion

#### Documentation
- Docstrings for all public functions and classes
- Clear comments for complex logic
- README files for major components

### 4. Development Workflow
Strict adherence to the SDD workflow:

1. **Spec**: Write feature specification in `/specs/phase1/features/`
2. **Plan**: Review and validate the specification
3. **Task Breakdown**: Identify implementation tasks
4. **Implementation**: Generate code that satisfies the spec
5. **Validation**: Verify acceptance criteria are met

### 5. No Manual Coding
- Code must be **generated from specifications**
- Human role: Define requirements, validate outputs
- AI role: Implement according to spec
- Violation of this principle = project failure

## Constraints & Boundaries

### Absolute Constraints
- ❌ No manual code written by the user
- ❌ No features outside the current phase/feature
- ❌ No persistence (no DB, no files)
- ❌ No frameworks or external dependencies (beyond standard library)
- ✅ Python console app only
- ✅ In-memory data structures only
- ✅ Every feature governed by a specification

### Technology Stack
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Development Methodology**: Spec-Driven Development
- **Code Generation**: AI-assisted from specifications

## Success Criteria
- All features implemented match their specifications exactly
- All acceptance criteria met
- Code follows PEP 8 and Clean Code principles
- No persistence layer exists
- All data operations work in-memory
- Application runs as a console interface

## Enforcement
Violation of any constraint or principle requires immediate correction before proceeding to the next step.
