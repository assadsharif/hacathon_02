# GitHub Pages Deployment

## Table of Contents
1. [GitHub Actions Workflow](#github-actions)
2. [Configuration Settings](#configuration)
3. [Custom Domain Setup](#custom-domain)

## GitHub Actions Workflow {#github-actions}

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build website
        run: npm run build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## Configuration Settings {#configuration}

In `docusaurus.config.ts`:

```typescript
const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  url: 'https://<username>.github.io',
  baseUrl: '/<repo-name>/',
  organizationName: '<username>',
  projectName: '<repo-name>',
  trailingSlash: false,

  // For GitHub Pages deployment
  deploymentBranch: 'gh-pages',
};
```

## Repository Settings

1. Go to repository Settings → Pages
2. Source: GitHub Actions
3. Wait for first deployment to complete

## Custom Domain Setup {#custom-domain}

1. Add `CNAME` file to `static/` folder with domain name
2. Configure DNS:
   - A record: `185.199.108.153` (and .109, .110, .111)
   - Or CNAME: `<username>.github.io`
3. Update `url` in config to custom domain

## Troubleshooting

- **404 errors**: Check `baseUrl` matches repository name
- **Assets missing**: Ensure `static/` contents are committed
- **Build fails**: Run `npm run build` locally first
