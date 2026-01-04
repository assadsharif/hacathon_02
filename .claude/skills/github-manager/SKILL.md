---
name: github-manager
description: Manage GitHub repositories, branches, pull requests, issues, and workflows using GitHub CLI. Use when creating repos, managing PRs, pushing code, handling branches, or automating GitHub operations. Triggers on requests involving repository setup, PR creation, branch management, or GitHub Actions.
---

# GitHub Manager

Comprehensive GitHub repository and workflow management using GitHub CLI (`gh`).

## Authentication Check

Always verify authentication before GitHub operations:
```bash
gh auth status
# Expected output:
# ✓ Logged in to github.com account <username>
# - Token scopes: 'repo', 'workflow', 'gist', 'read:org'
```

If not authenticated:
```bash
gh auth login
# Follow interactive prompts
```

## Repository Management

### Create New Repository

**Public repository:**
```bash
gh repo create <repo-name> --public --source=. --push
```

**Private repository:**
```bash
gh repo create <repo-name> --private --source=. --push
```

**With description and README:**
```bash
gh repo create <repo-name> --public --description "Project description" --add-readme
```

### Repository Information

```bash
# View repository details
gh repo view

# View specific repository
gh repo view owner/repo

# Open in browser
gh repo view --web
```

### Clone Repository

```bash
gh repo clone owner/repo

# Clone to specific directory
gh repo clone owner/repo target-directory
```

## Branch Management

### Create and Push Branch

```bash
# Create local branch
git checkout -b feature-branch

# Push and set upstream
git push -u origin feature-branch
```

### List Branches

```bash
# Local branches
git branch -vv

# Remote branches
git branch -r

# All branches with tracking info
gh repo view --json defaultBranchRef,branchProtectionRules
```

### Delete Branch

```bash
# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name

# Using gh CLI
gh api repos/:owner/:repo/git/refs/heads/branch-name -X DELETE
```

## Pull Request Workflow

### Create Pull Request

**Basic PR:**
```bash
gh pr create --title "Feature: Add new capability" --body "Description of changes"
```

**PR with template:**
```bash
gh pr create --title "Fix: Bug in authentication" --body "$(cat <<'EOF'
## Summary
- Fixed authentication token validation
- Added error handling for expired tokens

## Test Plan
- [ ] Unit tests pass
- [ ] Manual testing on staging
- [ ] No breaking changes

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Draft PR:**
```bash
gh pr create --draft --title "WIP: New feature" --body "Work in progress"
```

**PR to specific branch:**
```bash
gh pr create --base main --head feature-branch --title "Title" --body "Body"
```

### View Pull Requests

```bash
# List all PRs
gh pr list

# View specific PR
gh pr view 123

# View PR in browser
gh pr view 123 --web

# View PR diff
gh pr diff 123
```

### PR Operations

```bash
# Check out PR locally
gh pr checkout 123

# Review PR
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please fix X"
gh pr review 123 --comment --body "Looks good but minor suggestions"

# Merge PR
gh pr merge 123 --squash --delete-branch
gh pr merge 123 --merge
gh pr merge 123 --rebase

# Close PR without merging
gh pr close 123
```

### PR Status Checks

```bash
# View PR checks
gh pr checks 123

# Wait for checks to complete
gh pr checks 123 --watch
```

## Issue Management

### Create Issue

```bash
gh issue create --title "Bug: Application crashes on startup" --body "Description"
```

**With labels and assignees:**
```bash
gh issue create \
  --title "Feature request: Dark mode" \
  --body "Add dark mode support" \
  --label "enhancement,ui" \
  --assignee username
```

### View Issues

```bash
# List all issues
gh issue list

# Filter by state
gh issue list --state open
gh issue list --state closed

# Filter by label
gh issue list --label bug

# View specific issue
gh issue view 42
```

### Issue Operations

```bash
# Close issue
gh issue close 42

# Reopen issue
gh issue reopen 42

# Comment on issue
gh issue comment 42 --body "This is fixed in #43"
```

## Git Operations with GitHub

### Push Changes

```bash
# Push current branch
git push

# Push and set upstream
git push -u origin branch-name

# Force push (use with caution)
git push --force-with-lease

# Push all branches
git push --all
```

### Pull Changes

```bash
# Pull current branch
git pull

# Pull with rebase
git pull --rebase

# Pull specific branch
git pull origin main
```

### Sync Fork

```bash
# Add upstream remote
git remote add upstream https://github.com/original/repo.git

# Fetch upstream changes
git fetch upstream

# Merge upstream/main into local main
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

## GitHub Actions & Workflows

### View Workflow Runs

```bash
# List workflow runs
gh run list

# View specific run
gh run view 123456

# View run logs
gh run view 123456 --log
```

### Trigger Workflow

```bash
# Trigger workflow_dispatch event
gh workflow run workflow-name.yml

# With inputs
gh workflow run workflow-name.yml -f input1=value1 -f input2=value2
```

### Cancel Workflow Run

```bash
gh run cancel 123456
```

## Release Management

### Create Release

```bash
gh release create v1.0.0 --title "Release 1.0.0" --notes "Release notes here"

# With assets
gh release create v1.0.0 --title "v1.0.0" --notes "Notes" ./dist/*
```

### View Releases

```bash
# List releases
gh release list

# View specific release
gh release view v1.0.0
```

## GitHub Secrets

### Repository Secrets

```bash
# Set secret
gh secret set SECRET_NAME

# List secrets
gh secret list

# Delete secret
gh secret delete SECRET_NAME
```

## Common Patterns

### Complete Feature Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-capability

# 2. Make changes and commit
git add .
git commit -m "feat: add new capability"

# 3. Push to GitHub
git push -u origin feature/new-capability

# 4. Create PR
gh pr create --title "Feature: New capability" --body "Description"

# 5. After approval, merge
gh pr merge --squash --delete-branch
```

### Hotfix Workflow

```bash
# 1. Create hotfix branch from main
git checkout main
git pull
git checkout -b hotfix/critical-bug

# 2. Fix and commit
git add .
git commit -m "fix: critical bug in authentication"

# 3. Push and create PR
git push -u origin hotfix/critical-bug
gh pr create --title "Hotfix: Critical auth bug" --base main

# 4. Fast-track merge
gh pr merge --merge --delete-branch
```

### Repository Initialization for Existing Project

```bash
# 1. Initialize git if needed
git init
git add .
git commit -m "Initial commit"

# 2. Create GitHub repository
gh repo create project-name --public --source=. --push

# 3. Verify
gh repo view
```

## Collaboration Commands

### Add Collaborators

```bash
# Add collaborator (requires owner permissions)
gh api repos/:owner/:repo/collaborators/username -X PUT
```

### Repository Settings

```bash
# View repository settings
gh repo view --json name,description,visibility,defaultBranchRef

# Archive repository
gh repo archive owner/repo
```

## Troubleshooting

### Authentication Issues

```bash
# Check token scopes
gh auth status

# Refresh authentication
gh auth refresh -s repo,workflow

# Login with specific scopes
gh auth login --scopes repo,workflow,admin:org
```

### Remote Issues

```bash
# List remotes
git remote -v

# Add remote
git remote add origin https://github.com/owner/repo.git

# Change remote URL
git remote set-url origin https://github.com/owner/new-repo.git
```

### Permission Issues

**Error: Permission denied**
- Verify authentication: `gh auth status`
- Check repository access rights
- Ensure token has required scopes

## Best Practices

1. **Always verify auth before operations**: Run `gh auth status` first
2. **Use meaningful branch names**: `feature/`, `fix/`, `docs/`, `refactor/`
3. **Write descriptive PR titles**: Use conventional commits format
4. **Include test plans in PRs**: Document testing approach
5. **Delete branches after merge**: Keep repository clean
6. **Use draft PRs for WIP**: Signal work in progress
7. **Review before merging**: Always review changes
8. **Protect main branch**: Require PR reviews for main/master

## GitHub CLI Reference

Quick command reference:
- `gh repo` - Repository commands
- `gh pr` - Pull request commands
- `gh issue` - Issue commands
- `gh run` - Workflow run commands
- `gh release` - Release commands
- `gh secret` - Secrets management
- `gh auth` - Authentication commands
- `gh api` - Make authenticated GitHub API requests

For detailed help on any command:
```bash
gh <command> --help
```
