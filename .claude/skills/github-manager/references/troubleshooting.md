# GitHub Troubleshooting Guide

## Authentication Issues

### Problem: "gh: command not found"

**Solution:**
```bash
# Install GitHub CLI
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# macOS
brew install gh

# Windows
winget install GitHub.cli
```

### Problem: "Authentication required"

**Check status:**
```bash
gh auth status
```

**Solution:**
```bash
# Login
gh auth login

# Or refresh with specific scopes
gh auth refresh -s repo,workflow,admin:org
```

### Problem: "Insufficient permissions" or "403 Forbidden"

**Check token scopes:**
```bash
gh auth status
# Look for: Token scopes: 'repo', 'workflow', ...
```

**Solution:**
```bash
# Refresh with required scopes
gh auth refresh -s repo,workflow,admin:org,write:packages

# Or re-login
gh auth logout
gh auth login
```

### Problem: Token expired

**Solution:**
```bash
# Refresh authentication
gh auth refresh

# If that fails, re-login
gh auth logout
gh auth login
```

## Repository Issues

### Problem: "Repository not found"

**Check repository exists:**
```bash
gh repo view owner/repo
```

**Solution:**
```bash
# Verify repository name and owner
# Check if repository is private (requires authentication)
# Ensure you have access to the repository

# Clone with correct URL
gh repo clone owner/repo
```

### Problem: "Remote origin already exists"

**Solution:**
```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/owner/repo.git

# Or update existing remote
git remote set-url origin https://github.com/owner/repo.git
```

### Problem: "No such remote 'origin'"

**Solution:**
```bash
# Add origin remote
git remote add origin https://github.com/owner/repo.git

# Verify
git remote -v
```

## Push/Pull Issues

### Problem: "Updates were rejected because the tip of your current branch is behind"

**Solution 1: Pull and merge (safe)**
```bash
git pull --rebase origin main
# Resolve any conflicts
git push
```

**Solution 2: Force push (use with caution)**
```bash
# Only if you're certain no one else is working on the branch
git push --force-with-lease
```

### Problem: "src refspec main does not match any"

**Cause:** Branch doesn't exist or no commits made

**Solution:**
```bash
# Ensure you have commits
git log

# If no commits, make initial commit
git add .
git commit -m "Initial commit"

# Push
git push -u origin main
```

### Problem: "fatal: refusing to merge unrelated histories"

**Solution:**
```bash
# Allow unrelated histories (use carefully)
git pull origin main --allow-unrelated-histories

# Or start fresh
git remote remove origin
git remote add origin <url>
git fetch origin
git reset --hard origin/main
```

## Branch Issues

### Problem: "Branch already exists"

**Solution:**
```bash
# Use existing branch
git checkout existing-branch

# Or delete and recreate
git branch -D existing-branch
git checkout -b existing-branch

# Delete remote branch
git push origin --delete existing-branch
```

### Problem: "Cannot delete branch - not fully merged"

**Solution:**
```bash
# Force delete local branch
git branch -D branch-name

# Verify it's safe to delete
git branch --contains branch-name

# Delete remote branch
git push origin --delete branch-name
```

### Problem: "Your branch is ahead of 'origin/main' by X commits"

**Solution:**
```bash
# Push commits
git push

# Or reset to origin (lose local commits)
git reset --hard origin/main
```

## Pull Request Issues

### Problem: "No commits between main and feature-branch"

**Cause:** Branches are identical

**Solution:**
```bash
# Make changes on feature branch
git checkout feature-branch
# ... make changes ...
git add .
git commit -m "Add changes"
git push
```

### Problem: "PR has conflicts"

**Solution:**
```bash
# Update feature branch with main
git checkout feature-branch
git fetch origin main
git merge origin/main

# Resolve conflicts in files
# Then commit
git add .
git commit -m "Resolve merge conflicts"
git push
```

### Problem: "Cannot merge - check failures"

**View failed checks:**
```bash
gh pr checks <pr-number>
```

**Solution:**
```bash
# Fix issues causing check failures
# Commit and push fixes
git add .
git commit -m "Fix check failures"
git push

# Checks will re-run automatically
```

### Problem: "PR merge button disabled"

**Common causes:**
- Required reviews not completed
- Failing status checks
- Merge conflicts
- Branch protection rules

**Check PR status:**
```bash
gh pr view <pr-number>
gh pr checks <pr-number>
```

## Git Configuration Issues

### Problem: "Please tell me who you are"

**Solution:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Problem: Wrong author in commits

**Solution:**
```bash
# Set correct user for repository
git config user.name "Correct Name"
git config user.email "correct@email.com"

# Amend last commit author
git commit --amend --author="Correct Name <correct@email.com>" --no-edit

# For multiple commits, use rebase
git rebase -i HEAD~5
# Mark commits as 'edit', then for each:
git commit --amend --author="Correct Name <correct@email.com>" --no-edit
git rebase --continue
```

## GitHub Actions Issues

### Problem: Workflow not triggering

**Check workflow file:**
```bash
# View workflow file
cat .github/workflows/workflow-name.yml

# Validate YAML syntax
yamllint .github/workflows/workflow-name.yml
```

**Common issues:**
- Wrong trigger events
- Incorrect branch names in `on.push.branches`
- Syntax errors in YAML
- Workflow file not in `.github/workflows/`

### Problem: "Resource not accessible by integration"

**Cause:** GitHub token lacks permissions

**Solution in workflow:**
```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write
```

### Problem: Workflow secrets not available

**Set repository secrets:**
```bash
# Using gh CLI
gh secret set SECRET_NAME
```

**Or via GitHub web:**
Settings → Secrets and variables → Actions → New repository secret

## Large File Issues

### Problem: "remote: error: File too large"

**GitHub file size limits:**
- Soft limit: 50 MB (warning)
- Hard limit: 100 MB (rejection)

**Solution:**
```bash
# Remove large file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/large/file" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner (easier)
# https://rtyley.github.io/bfg-repo-cleaner/

# Use Git LFS for large files
git lfs install
git lfs track "*.psd"
git add .gitattributes
git add file.psd
git commit -m "Add large file with LFS"
```

## Miscellaneous Issues

### Problem: ".gitignore not working"

**Cause:** Files already tracked

**Solution:**
```bash
# Remove files from git tracking
git rm -r --cached .

# Re-add all files (respecting .gitignore)
git add .
git commit -m "Fix .gitignore"
```

### Problem: Accidentally committed secrets

**Immediate action:**
```bash
# DO NOT just remove from latest commit
# Secrets remain in git history!

# 1. Invalidate the exposed secret immediately
# 2. Remove from all history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secrets.env" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push
git push --force --all

# 4. Notify security team
```

**Prevention:**
```bash
# Use .gitignore
echo ".env" >> .gitignore
echo "secrets.yml" >> .gitignore

# Use git-secrets tool
git secrets --install
git secrets --register-aws
```

### Problem: "detached HEAD state"

**Solution:**
```bash
# Create branch from current state
git checkout -b new-branch-name

# Or return to a branch
git checkout main
```

### Problem: Lost commits after reset

**Solution:**
```bash
# View reflog (all commit history)
git reflog

# Find your lost commit
# Checkout or create branch from it
git checkout <commit-hash>
git checkout -b recovered-branch
```

## Performance Issues

### Problem: Slow clone/fetch

**Solution:**
```bash
# Shallow clone (faster)
git clone --depth 1 https://github.com/owner/repo.git

# Or for existing repo
git fetch --depth 1
```

### Problem: Large repository size

**Check size:**
```bash
du -sh .git
git count-objects -vH
```

**Solution:**
```bash
# Clean up
git gc --aggressive --prune=now

# Remove old branches
git remote prune origin

# Use shallow clone for new clones
git clone --depth 1 --single-branch
```

## Getting Help

### Check GitHub Status
Visit: https://www.githubstatus.com/

### GitHub CLI Help
```bash
# General help
gh --help

# Command-specific help
gh pr --help
gh repo --help

# View manual pages
man gh
man git
```

### Useful Diagnostic Commands
```bash
# Check git version
git --version

# Check gh CLI version
gh --version

# View git configuration
git config --list

# View authentication status
gh auth status

# View remotes
git remote -v

# View all branches
git branch -a

# View recent commits
git log --oneline -10
```
