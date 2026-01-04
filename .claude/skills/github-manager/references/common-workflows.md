# Common GitHub Workflows

## Repository Setup Workflows

### Initialize New Project

```bash
# 1. Create local repository
git init
git add .
git commit -m "Initial commit"

# 2. Create GitHub repository and push
gh repo create my-project --public --source=. --push

# 3. Add description
gh repo edit --description "Project description"

# 4. Add topics/tags
gh repo edit --add-topic javascript,api,docker

# 5. Verify
gh repo view
```

### Fork and Contribute Workflow

```bash
# 1. Fork repository via GitHub CLI
gh repo fork owner/repo --clone

# 2. Add upstream remote (done automatically by fork command)
git remote -v

# 3. Create feature branch
git checkout -b feature/my-contribution

# 4. Make changes and commit
git add .
git commit -m "feat: add feature X"

# 5. Push to your fork
git push -u origin feature/my-contribution

# 6. Create PR to upstream
gh pr create --repo owner/repo \
  --title "Feature: My contribution" \
  --body "Description of contribution"
```

## Branch Management Workflows

### Feature Branch Workflow

```bash
# 1. Update main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/new-capability

# 3. Work and commit regularly
git add .
git commit -m "feat: implement X"

# 4. Keep feature branch updated with main
git fetch origin main
git rebase origin/main

# 5. Push feature branch
git push -u origin feature/new-capability

# 6. Create PR when ready
gh pr create --title "Feature: New capability"
```

### Gitflow-Style Workflow

```bash
# Main branches: main (production), develop (integration)

# 1. Start new feature from develop
git checkout develop
git pull
git checkout -b feature/user-profile

# 2. Develop feature
git add .
git commit -m "feat: add user profile page"

# 3. Create PR to develop
git push -u origin feature/user-profile
gh pr create --base develop --title "Feature: User profile"

# 4. Release preparation
git checkout develop
git pull
git checkout -b release/v1.2.0

# 5. Final testing and bug fixes on release branch
git commit -m "fix: minor release bugs"

# 6. Merge to main and tag
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# 7. Merge back to develop
git checkout develop
git merge release/v1.2.0
git push origin develop

# 8. Delete release branch
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

## Release Workflows

### Semantic Versioning Release

```bash
# 1. Update version in package.json
npm version patch  # or minor, or major
# This creates a git tag automatically

# 2. Push tag to GitHub
git push --tags

# 3. Create GitHub release
gh release create v1.2.3 \
  --title "Release v1.2.3" \
  --notes "$(cat <<'EOF'
## What's New
- Feature A
- Feature B

## Bug Fixes
- Fix issue X
- Fix issue Y

## Breaking Changes
None
EOF
)"

# 4. Upload release assets (if needed)
gh release upload v1.2.3 ./dist/*.zip
```

### Automated Release from CI

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: npm run build
      - name: Create Release
        run: |
          gh release create ${{ github.ref_name }} \
            --title "Release ${{ github.ref_name }}" \
            --generate-notes \
            ./dist/*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Collaboration Workflows

### Team Code Review Process

```bash
# Developer creates PR
gh pr create --title "Feature: X" --body "Description" --reviewer @reviewer1,@reviewer2

# Reviewer checks out PR
gh pr checkout 123
npm install
npm test

# Reviewer provides feedback
gh pr review 123 --comment --body "Please add tests for edge case Y"

# Developer addresses feedback
git add tests/
git commit -m "test: add edge case tests"
git push

# Reviewer approves
gh pr review 123 --approve

# Merge after 2 approvals
gh pr merge 123 --squash
```

### Pair Programming PR

```bash
# Start pairing session
git checkout -b feature/pair-programming

# Regular commits with co-authors
git commit -m "feat: implement feature

Co-authored-by: Partner <partner@example.com>"

# Create PR showing collaboration
gh pr create \
  --title "Feature: Pair programming result" \
  --body "Collaborative work session"
```

## Issue Management Workflows

### Bug Triage Workflow

```bash
# 1. User reports bug
gh issue create \
  --title "Bug: Login fails on Firefox" \
  --body "Steps to reproduce..." \
  --label bug

# 2. Triage: Add labels
gh issue edit 42 --add-label "priority:high,browser:firefox"

# 3. Assign to developer
gh issue edit 42 --add-assignee developer1

# 4. Developer creates fix branch
git checkout -b fix/firefox-login

# 5. Fix and reference issue in commit
git commit -m "fix: resolve Firefox login issue

Fixes #42"

# 6. PR automatically links to issue
gh pr create --title "Fix: Firefox login issue"

# 7. Merging PR auto-closes issue
gh pr merge --squash
```

### Feature Request Workflow

```bash
# 1. Create feature request
gh issue create \
  --title "Feature: Dark mode support" \
  --body "Add dark mode theme" \
  --label "enhancement"

# 2. Discuss and get approval
gh issue comment 99 --body "Approved for next sprint"

# 3. Convert to tracked work
gh issue edit 99 --add-label "status:in-progress"
gh issue edit 99 --add-assignee developer2

# 4. Implement
git checkout -b feature/dark-mode

# 5. Create PR linking to issue
gh pr create \
  --title "Feature: Dark mode" \
  --body "Implements #99"

# 6. Close issue when merged
gh pr merge --squash  # Auto-closes #99
```

## Maintenance Workflows

### Dependency Update Workflow

```bash
# 1. Create update branch
git checkout -b deps/update-dependencies

# 2. Update dependencies
npm update
npm audit fix

# 3. Test
npm test

# 4. Commit and create PR
git add package*.json
git commit -m "chore: update dependencies"
git push -u origin deps/update-dependencies

gh pr create \
  --title "Chore: Update dependencies" \
  --body "Security and feature updates" \
  --label dependencies
```

### Security Patch Workflow

```bash
# 1. Security issue identified
gh issue create \
  --title "Security: XSS vulnerability" \
  --label "security,priority:critical"

# 2. Create hotfix branch
git checkout main
git pull
git checkout -b security/xss-fix

# 3. Fix vulnerability
git commit -m "security: fix XSS vulnerability"

# 4. Create urgent PR
gh pr create \
  --title "Security: Fix XSS vulnerability" \
  --body "Critical security patch" \
  --label security

# 5. Fast-track review and merge
gh pr merge --merge --delete-branch

# 6. Create patch release
git tag -a v1.2.4 -m "Security patch"
git push --tags
gh release create v1.2.4 --title "Security Patch v1.2.4"
```

## Advanced Workflows

### Monorepo Multi-Package Release

```bash
# 1. Determine changed packages
git diff main --name-only | grep "packages/"

# 2. Version affected packages
npm version patch --workspace=packages/package-a
npm version patch --workspace=packages/package-b

# 3. Create PR for version bump
git add .
git commit -m "chore: bump package versions"
gh pr create --title "Chore: Version bump for release"

# 4. After merge, create release
gh release create v1.2.0 \
  --title "Release v1.2.0" \
  --notes "Multi-package release: package-a@1.2.0, package-b@1.3.0"
```

### Automated Changelog Generation

```bash
# Using GitHub CLI to generate release notes
gh release create v1.2.0 --generate-notes

# Or manual with conventional commits
git log v1.1.0..HEAD --oneline | grep "^feat:" > CHANGELOG.md
git log v1.1.0..HEAD --oneline | grep "^fix:" >> CHANGELOG.md
```

## GitHub Actions Integration

### Trigger Workflow on PR

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
      - name: Comment on PR
        run: |
          gh pr comment ${{ github.event.pull_request.number }} \
            --body "✅ Tests passed!"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Auto-label PRs

```yaml
# .github/workflows/label-pr.yml
name: Label PR

on:
  pull_request:
    types: [opened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Add labels
        run: |
          if [[ "${{ github.event.pull_request.title }}" == *"feat:"* ]]; then
            gh pr edit ${{ github.event.pull_request.number }} --add-label "feature"
          elif [[ "${{ github.event.pull_request.title }}" == *"fix:"* ]]; then
            gh pr edit ${{ github.event.pull_request.number }} --add-label "bugfix"
          fi
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
