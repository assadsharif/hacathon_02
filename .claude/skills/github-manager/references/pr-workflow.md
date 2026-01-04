# Pull Request Workflow Patterns

## Standard Feature PR

```bash
# 1. Create feature branch
git checkout -b feature/user-authentication

# 2. Implement feature with commits
git add src/auth/
git commit -m "feat: add user authentication module"

git add tests/auth/
git commit -m "test: add authentication tests"

# 3. Push to GitHub
git push -u origin feature/user-authentication

# 4. Create PR with comprehensive description
gh pr create --title "Feature: User Authentication" --body "$(cat <<'EOF'
## Summary
Implements user authentication system with JWT tokens.

**Changes:**
- Add authentication middleware
- Implement login/logout endpoints
- Add JWT token validation
- Add user session management

## Test Plan
- [x] Unit tests for authentication module
- [x] Integration tests for login flow
- [x] Manual testing with different user roles
- [ ] Security review pending

## Breaking Changes
None

## Documentation
- Updated API documentation
- Added authentication guide to README

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"

# 5. Address review comments
git add .
git commit -m "fix: address PR review comments"
git push

# 6. Merge after approval
gh pr merge --squash --delete-branch
```

## Bug Fix PR

```bash
# 1. Create fix branch from main
git checkout main
git pull
git checkout -b fix/login-timeout

# 2. Fix bug
git add src/auth/session.ts
git commit -m "fix: resolve login timeout issue

- Increase session timeout to 30 minutes
- Add error handling for expired sessions
- Fixes #123"

# 3. Push and create PR
git push -u origin fix/login-timeout
gh pr create \
  --title "Fix: Login timeout issue" \
  --body "Resolves #123 - Users no longer experience premature timeouts"

# 4. Fast-track merge for critical fix
gh pr merge --merge --delete-branch
```

## Documentation PR

```bash
# Create docs branch
git checkout -b docs/api-guide

# Update documentation
git add docs/api-guide.md README.md
git commit -m "docs: add comprehensive API guide"

# Create PR
git push -u origin docs/api-guide
gh pr create \
  --title "Docs: Add API usage guide" \
  --body "Comprehensive guide for API integration" \
  --label documentation

# Merge
gh pr merge --squash --delete-branch
```

## Draft PR for Early Feedback

```bash
# Create experimental branch
git checkout -b experiment/new-architecture

# Initial implementation
git add src/
git commit -m "wip: prototype new architecture"

# Push and create draft PR
git push -u origin experiment/new-architecture
gh pr create --draft \
  --title "WIP: New service architecture" \
  --body "Early prototype for feedback. Not ready for review."

# Mark as ready when done
gh pr ready
```

## Multi-Commit PR with Clean History

```bash
# Feature branch with multiple logical commits
git checkout -b feature/payment-integration

# Commit 1: Core integration
git add src/payment/
git commit -m "feat: add payment provider integration"

# Commit 2: Error handling
git add src/payment/errors.ts
git commit -m "feat: add payment error handling"

# Commit 3: Tests
git add tests/payment/
git commit -m "test: add payment integration tests"

# Push all commits
git push -u origin feature/payment-integration

# Create PR that preserves commit history
gh pr create \
  --title "Feature: Payment provider integration" \
  --body "Multi-step implementation with clean commit history"

# Merge with merge commit (preserves history)
gh pr merge --merge --delete-branch
```

## Collaborative PR with Co-Authors

```bash
# Create branch
git checkout -b feature/collaborative-work

# Make commits with co-authors
git add .
git commit -m "feat: implement feature X

Co-authored-by: Alice <alice@example.com>
Co-authored-by: Bob <bob@example.com>"

# Push and create PR
git push -u origin feature/collaborative-work
gh pr create \
  --title "Feature: Collaborative implementation" \
  --body "Joint work by team members"
```

## PR Update Patterns

### Update PR with Latest Main

```bash
# Fetch latest main
git fetch origin main

# Rebase feature branch on main
git checkout feature/my-feature
git rebase origin/main

# Force push (use --force-with-lease for safety)
git push --force-with-lease
```

### Add Changes to Existing PR

```bash
# Make additional changes
git add .
git commit -m "feat: add requested functionality"

# Push to update PR
git push
```

### Squash Commits Before Merge

```bash
# Interactive rebase to squash commits
git rebase -i HEAD~3

# Mark commits as 'squash' in editor
# Force push updated history
git push --force-with-lease
```

## PR Review Workflow

### As Reviewer

```bash
# Check out PR locally
gh pr checkout 456

# Review changes
git log origin/main..HEAD
git diff origin/main

# Test locally
npm install
npm test

# Leave review
gh pr review 456 --approve --body "LGTM! Great implementation."

# Or request changes
gh pr review 456 --request-changes --body "Please address the following:
- Add error handling in line 42
- Update tests for edge case"
```

### As Author Responding to Review

```bash
# Address feedback
git add .
git commit -m "fix: address review feedback

- Add error handling
- Update tests for edge cases"

# Push updates
git push

# Comment on review
gh pr comment 456 --body "Updated per review comments. Ready for re-review."
```

## Common PR Merge Strategies

### Squash and Merge (Recommended for feature PRs)
```bash
gh pr merge 456 --squash --delete-branch
# Result: Single commit in main branch with all changes
```

### Merge Commit (Preserves history)
```bash
gh pr merge 456 --merge --delete-branch
# Result: All commits preserved, plus merge commit
```

### Rebase and Merge (Clean linear history)
```bash
gh pr merge 456 --rebase --delete-branch
# Result: Commits replayed on top of main, no merge commit
```

## PR Templates

Create `.github/pull_request_template.md`:
```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Test Plan
- [ ] Tests added/updated
- [ ] Manual testing completed
- [ ] No breaking changes

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] Ready for review
```
