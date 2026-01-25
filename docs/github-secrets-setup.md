# GitHub Secrets Setup Guide

## Phase VI: CI/CD Pipeline Configuration

This guide explains how to configure GitHub Secrets required for the CI/CD pipelines.

## Required Secrets

### Google Cloud (GKE) Secrets

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `GCP_PROJECT_ID` | Your GCP project ID | `gcloud config get-value project` |
| `GCP_SA_KEY` | Service account JSON key (base64) | See instructions below |

**Creating GCP Service Account Key:**

```bash
# Create service account
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions"

# Grant required roles
PROJECT_ID=$(gcloud config get-value project)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/container.developer"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com

# Copy the contents of key.json as GCP_SA_KEY secret
cat key.json

# Clean up
rm key.json
```

### Azure (AKS) Secrets

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `AZURE_CREDENTIALS` | Service principal JSON | See instructions below |
| `ACR_NAME` | Azure Container Registry name | `todochatbotacr48370` |
| `ACR_USERNAME` | ACR admin username | See instructions below |
| `ACR_PASSWORD` | ACR admin password | See instructions below |

**Creating Azure Service Principal:**

```bash
# Create service principal with contributor role
az ad sp create-for-rbac \
  --name "github-actions" \
  --role contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv) \
  --sdk-auth

# Copy the JSON output as AZURE_CREDENTIALS secret
```

**Getting ACR Credentials:**

```bash
# Get ACR admin credentials
az acr credential show --name todochatbotacr48370

# ACR_USERNAME: todochatbotacr48370
# ACR_PASSWORD: (copy the password value)
```

### Application Secrets

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `DATABASE_URL` | Neon PostgreSQL connection string | From Neon dashboard |
| `JWT_SECRET` | JWT signing secret | Generate: `openssl rand -base64 32` |
| `BETTER_AUTH_SECRET` | Better Auth secret | Generate: `openssl rand -base64 32` |
| `OPENAI_API_KEY` | OpenAI API key | From OpenAI dashboard |

### Redpanda Cloud Secrets

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `REDPANDA_BROKERS` | Redpanda Cloud broker URL | From Redpanda Cloud console |
| `REDPANDA_USERNAME` | SASL username | From Redpanda Cloud security settings |
| `REDPANDA_PASSWORD` | SASL password | From Redpanda Cloud security settings |

## Adding Secrets to GitHub

1. Go to your repository: https://github.com/assadsharif/hacathon_02
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Add each secret with the name and value from above

## Quick Setup Script

Run this script to display your current values (run locally):

```bash
#!/bin/bash
echo "=== GCP Secrets ==="
echo "GCP_PROJECT_ID: $(gcloud config get-value project 2>/dev/null)"
echo ""
echo "=== Azure Secrets ==="
echo "ACR_NAME: todochatbotacr48370"
az acr credential show --name todochatbotacr48370 --query "[username, passwords[0].value]" -o tsv 2>/dev/null
echo ""
echo "=== Redpanda Secrets ==="
echo "Check your Redpanda Cloud console for broker URL and credentials"
```

## Verification

After adding all secrets, trigger the build workflow:

```bash
gh workflow run "Build and Push Images" --repo assadsharif/hacathon_02
gh run list --repo assadsharif/hacathon_02 --workflow "Build and Push Images" --limit 1
```

## Secret Summary Checklist

- [ ] `GCP_PROJECT_ID`
- [ ] `GCP_SA_KEY`
- [ ] `AZURE_CREDENTIALS`
- [ ] `ACR_NAME`
- [ ] `ACR_USERNAME`
- [ ] `ACR_PASSWORD`
- [ ] `DATABASE_URL`
- [ ] `JWT_SECRET`
- [ ] `BETTER_AUTH_SECRET`
- [ ] `OPENAI_API_KEY`
- [ ] `REDPANDA_BROKERS`
- [ ] `REDPANDA_USERNAME`
- [ ] `REDPANDA_PASSWORD`
