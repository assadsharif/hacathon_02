---
name: testing
description: Comprehensive testing guidance for Docusaurus documentation sites. Use when validating builds, testing responsive design, running accessibility audits, or verifying deployment quality. Covers Lighthouse audits, mobile testing, keyboard navigation, and performance validation.
version: 1.0.0
author: Physical AI Book Project
---

# Testing Skill for Docusaurus Sites

## Overview

Systematic testing procedures for validating Docusaurus documentation sites across build verification, performance, accessibility, mobile responsiveness, and deployment quality.

**When to Use This Skill:**
- Validating local builds before deployment
- Testing deployed sites for performance and accessibility
- Verifying mobile responsiveness
- Running keyboard navigation and accessibility audits
- Pre-release quality assurance
- Post-deployment validation

---

## Testing Categories

### 1. Build Verification Testing
### 2. Performance & Lighthouse Audits
### 3. Mobile Responsiveness Testing
### 4. Accessibility & Keyboard Navigation
### 5. Cross-Browser Testing
### 6. Deployment Validation

---

## 1. Build Verification Testing

### Purpose
Ensure local builds complete without errors before deployment.

### Quick Reference

```bash
# Standard build test
cd <docusaurus-project>
npm run build

# Expected: "SUCCESS" message, no errors
# Output: build/ directory with static files
```

### Detailed Checklist

**Pre-Build Checks:**
- [ ] `package.json` dependencies up to date
- [ ] `docusaurus.config.ts` syntax valid
- [ ] All markdown files have valid frontmatter
- [ ] No broken internal links (or configured to warn only)

**Build Execution:**
```bash
# Clean build
rm -rf build/ .docusaurus/
npm run build

# Build with verbose output
npm run build -- --bundleAnalyzer
```

**Post-Build Verification:**
- [ ] Build completes without errors
- [ ] `build/` directory created
- [ ] All modules/pages present in build output
- [ ] `sitemap.xml` generated
- [ ] Search index created (in JS bundles)
- [ ] Static assets copied correctly

**Common Build Issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| MDX compilation error | Invalid JSX syntax in markdown | Escape `<` as `&lt;`, check JSX |
| Broken links error | Cross-reference path incorrect | Use relative paths or `onBrokenLinks: 'warn'` |
| Module not found | Missing dependency | Run `npm install` |
| Out of memory | Large site, insufficient heap | `NODE_OPTIONS=--max-old-space-size=4096 npm run build` |

### Build Size Analysis

```bash
# Analyze bundle size
npm run build -- --bundleAnalyzer

# Check build directory size
du -sh build/

# Expected: <50MB for documentation sites
```

---

## 2. Performance & Lighthouse Audits

### Purpose
Measure page load performance, Core Web Vitals, and overall site quality.

### Success Criteria (SC-003)

**Target Scores:**
- Performance: ≥90 (Mobile), ≥95 (Desktop)
- Accessibility: ≥95
- Best Practices: ≥90
- SEO: ≥90

**Core Web Vitals:**
- First Contentful Paint (FCP): <1.8s (Mobile), <0.9s (Desktop)
- Largest Contentful Paint (LCP): <2.5s (Mobile), <1.2s (Desktop)
- Total Blocking Time (TBT): <200ms
- Cumulative Layout Shift (CLS): <0.1

### Testing Methods

**Option 1: Chrome DevTools Lighthouse**

```
1. Open deployed site in Chrome
2. Open DevTools (F12)
3. Navigate to "Lighthouse" tab
4. Select categories: Performance, Accessibility, Best Practices, SEO
5. Device: Mobile (test mobile first)
6. Click "Analyze page load"
7. Wait 30-60 seconds for results
8. Screenshot and document scores
```

**Option 2: PageSpeed Insights (Web)**

```
1. Visit: https://pagespeed.web.dev/
2. Enter URL: https://your-site.github.io/project/
3. Click "Analyze"
4. Review Mobile and Desktop results
5. Download report PDF
```

**Option 3: Lighthouse CLI**

```bash
# Install Lighthouse globally
npm install -g lighthouse

# Run mobile audit
lighthouse https://your-site.github.io/project/ \
  --preset=mobile \
  --output html \
  --output-path ./lighthouse-mobile.html \
  --view

# Run desktop audit
lighthouse https://your-site.github.io/project/ \
  --preset=desktop \
  --output json \
  --output-path ./lighthouse-desktop.json

# Run specific categories
lighthouse https://your-site.github.io/project/ \
  --only-categories=performance,accessibility \
  --output html
```

### Interpreting Results

**Performance Optimizations for Docusaurus:**

| Issue | Docusaurus Solution |
|-------|---------------------|
| Large JavaScript bundles | Code splitting (automatic) |
| Slow initial load | Lazy loading, prefetching (built-in) |
| Unoptimized images | Use WebP, srcset attributes |
| Render-blocking resources | Preload critical resources in config |
| No CDN | GitHub Pages includes CDN automatically |

**Expected Lighthouse Scores for Static Docusaurus:**
- ✅ Performance: 95-100 (should easily pass)
- ✅ Accessibility: 95-100 (if proper semantic HTML used)
- ✅ Best Practices: 95-100 (Docusaurus follows standards)
- ✅ SEO: 95-100 (automatic sitemap, meta tags)

### Multi-Page Testing

Test representative pages from different sections:

```bash
# Homepage
lighthouse https://site.com/

# Module page
lighthouse https://site.com/module-1-intro/

# Deep chapter page
lighthouse https://site.com/module-4-perception/spatial-awareness

# Iterate through all modules (script)
for module in module-{1..7}*; do
  lighthouse "https://site.com/$module/" --output json --quiet
done
```

---

## 3. Mobile Responsiveness Testing

### Purpose
Ensure mobile users can read all content without horizontal scrolling, navigation works with touch.

### Success Criteria (SC-004)

**Requirements:**
- Site responsive at 375px viewport width minimum
- No horizontal scrolling on any page
- Sidebar collapse/expand works on mobile
- Touch interactions smooth and responsive
- Viewport meta tag present and correct

### Viewport Testing

**Chrome DevTools Method:**

```
1. Open site in Chrome
2. Open DevTools (F12)
3. Click "Toggle device toolbar" (Ctrl+Shift+M)
4. Select device or set custom dimensions
5. Test common viewports:
   - 375px × 667px (iPhone SE - smallest)
   - 390px × 844px (iPhone 12/13)
   - 393px × 851px (Pixel 5)
   - 768px × 1024px (iPad Mini)
```

**Manual Testing Checklist:**

**At 375px viewport:**
- [ ] No horizontal scrollbar on any page
- [ ] All text readable (not cut off)
- [ ] Images scale proportionally
- [ ] Tables responsive or horizontally scrollable within container
- [ ] Code blocks wrap or scroll within container
- [ ] Navigation menu accessible
- [ ] Footer displays correctly

**Hamburger Menu Testing (Mobile Navigation):**
- [ ] Hamburger icon (☰) visible in navbar
- [ ] Tapping hamburger opens sidebar overlay
- [ ] Sidebar covers 80-90% of screen width
- [ ] All modules/chapters accessible in sidebar
- [ ] Scrolling works within mobile sidebar
- [ ] Tap outside sidebar closes it
- [ ] Selecting chapter navigates and closes sidebar
- [ ] Animations smooth (no jank)

### Viewport Meta Tag Verification

```bash
# Check if viewport meta tag present
curl -s https://your-site.com/ | grep -i viewport

# Expected output:
# <meta name="viewport" content="width=device-width,initial-scale=1">
```

**Docusaurus Default:**
- ✅ Automatically includes responsive viewport meta
- ✅ No manual configuration needed
- ✅ Present in all generated HTML pages

### Responsive Design Breakpoints

**Docusaurus Breakpoints:**
- Desktop: >996px (full sidebar visible)
- Tablet: 768px - 996px (collapsible sidebar)
- Mobile: <768px (hamburger menu)
- Small mobile: ≥375px (minimum supported)

### Testing Responsive Elements

**Content Types to Verify:**

| Element | Expected Behavior |
|---------|-------------------|
| Long URLs | Wrap or break at appropriate points |
| Code blocks | Horizontal scroll within container |
| Wide tables | Scroll horizontally or stack on mobile |
| Images | Scale to container width (max-width: 100%) |
| Videos/iframes | Responsive sizing |
| Formulas | Wrap or scroll |

---

## 4. Accessibility & Keyboard Navigation

### Purpose
Ensure keyboard-only users and screen reader users can access all content.

### Success Criteria (SC-005)

**Requirements:**
- All interactive elements accessible via Tab key
- Focus indicators visible on all focusable elements
- Logical tab order
- Skip links present (optional but recommended)
- ARIA attributes correct
- Heading hierarchy proper (no skipped levels)

### Keyboard Navigation Testing

**Commands to Test:**

| Key | Expected Behavior |
|-----|-------------------|
| `Tab` | Move focus to next interactive element |
| `Shift+Tab` | Move focus to previous element |
| `Enter` | Activate focused link or button |
| `Space` | Scroll page down (on body), activate button |
| `/` | Focus search box (if search enabled) |
| `Esc` | Close mobile menu, modal, or search |

**Desktop Navigation Checklist:**
- [ ] Tab to navbar links
- [ ] Tab through all sidebar modules
- [ ] Tab through all chapter links
- [ ] Collapsed sections expand on Enter/Space
- [ ] Tab to main content links
- [ ] Tab to "Next page" navigation
- [ ] Tab to footer links
- [ ] Focus visible on all elements (outline/highlight)

**Mobile Navigation Checklist (375px viewport):**
- [ ] Tab to hamburger menu icon
- [ ] Enter opens sidebar overlay
- [ ] Tab cycles through sidebar items
- [ ] Enter selects chapter (closes sidebar)
- [ ] Esc closes sidebar
- [ ] Focus trapped in sidebar when open (doesn't jump to background)

### Focus Indicators

**Verify Focus Visible:**
```css
/* Check that custom CSS doesn't remove focus outlines */
/* BAD - never do this: */
*:focus { outline: none; }

/* GOOD - enhance default focus: */
*:focus { outline: 2px solid blue; }
```

**Test Focus Indicators:**
- [ ] All interactive elements show focus state
- [ ] Focus indicator not removed by CSS (`outline: none`)
- [ ] Focus indicator has sufficient contrast (3:1 minimum)
- [ ] Focus indicator visible on all backgrounds

### ARIA Attributes

**Verify Proper ARIA Usage:**
- [ ] Sidebar has `role="navigation"` or `<nav>` element
- [ ] Hamburger menu has `aria-label="Toggle navigation"`
- [ ] Collapsible sections have `aria-expanded="true/false"`
- [ ] Search has `role="search"` or `<search>` element
- [ ] Landmark regions properly labeled

### Heading Structure

**Check Heading Hierarchy:**

```bash
# Extract headings from page
curl -s https://your-site.com/ | grep -o '<h[1-6][^>]*>.*</h[1-6]>' | sed 's/<[^>]*>//g'
```

**Verify:**
- [ ] One H1 per page (page title)
- [ ] Logical heading hierarchy (H1 → H2 → H3)
- [ ] No skipped levels (e.g., H2 → H4)
- [ ] Headings describe content accurately

### Screen Reader Testing (Optional)

**Test with NVDA (Windows) or VoiceOver (Mac):**

1. Enable screen reader
2. Navigate page using arrow keys
3. Verify announcements:
   - [ ] Page title announced
   - [ ] Landmarks announced (navigation, main, etc.)
   - [ ] Links have descriptive text (not "click here")
   - [ ] Images have alt text (or marked decorative)
   - [ ] Form inputs have labels

### Color Contrast

**WCAG AA Requirements:**
- Normal text: 4.5:1 contrast ratio
- Large text (18pt+): 3:1 contrast ratio
- Interactive elements: 3:1 against background

**Testing Tools:**
- Chrome DevTools: Lighthouse accessibility audit
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Browser extension: axe DevTools

---

## 5. Cross-Browser Testing

### Purpose
Ensure consistent behavior across major browsers and platforms.

### Browsers to Test

**Tier 1 (Must Test):**
- Chrome (latest) - Desktop & Mobile
- Firefox (latest) - Desktop & Mobile
- Safari (latest) - Desktop & Mobile
- Edge (latest) - Desktop

**Tier 2 (Optional):**
- Samsung Internet (Mobile)
- Opera
- Brave

### Testing Checklist

**For Each Browser:**
- [ ] Homepage loads correctly
- [ ] Navigation works (sidebar, links)
- [ ] Search functions (if enabled)
- [ ] Mobile menu works (hamburger)
- [ ] Content displays correctly
- [ ] Images load
- [ ] Code blocks render properly
- [ ] Syntax highlighting works

### Browser DevTools Testing

**Chrome DevTools:**
```
F12 → Lighthouse tab → Run audits
F12 → Device toolbar (Ctrl+Shift+M) → Test responsive
```

**Firefox Developer Tools:**
```
F12 → Responsive Design Mode (Ctrl+Shift+M)
```

**Safari Web Inspector:**
```
Develop menu → Enter Responsive Design Mode
```

### Known Browser Differences

**Common Issues:**

| Issue | Browsers Affected | Solution |
|-------|-------------------|----------|
| Flexbox bugs | IE11 | Drop IE11 support (Docusaurus doesn't support) |
| CSS Grid differences | Safari <14 | Use fallbacks or require modern Safari |
| Font rendering | All | Accept minor differences as acceptable |
| Touch events | Mobile browsers | Test with actual devices when possible |

---

## 6. Deployment Validation

### Purpose
Verify site deployed correctly and is accessible at production URL.

### Pre-Deployment Checks

**Before Deploying:**
- [ ] Local build succeeds (`npm run build`)
- [ ] All tests passed locally
- [ ] No console errors in dev mode
- [ ] Git commit clean (no uncommitted changes)
- [ ] Branch up to date with remote

### GitHub Actions Workflow

**Verify Workflow Configuration:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: <docusaurus-directory>
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20.x'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: <docusaurus-directory>/build

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
    steps:
      - uses: actions/deploy-pages@v4
```

**Check Workflow Logs:**

```
1. Go to repository: Settings → Pages
2. Verify Source set to "GitHub Actions"
3. Go to Actions tab
4. Click latest workflow run
5. Verify all steps completed successfully (green checkmarks)
6. Check build logs for errors or warnings
```

### Post-Deployment Checks

**Verify Deployment:**

```bash
# Check if site is live
curl -I https://username.github.io/repository/

# Expected: HTTP/2 200

# Check homepage content
curl -s https://username.github.io/repository/ | grep -i "<title>"

# Expected: Your site title
```

**Manual Verification:**
- [ ] Site accessible at production URL
- [ ] Homepage loads correctly
- [ ] All 7 modules visible in sidebar
- [ ] Click through to sample chapters
- [ ] Search works (if enabled)
- [ ] Navigation works
- [ ] No 404 errors
- [ ] Images load
- [ ] Footer displays correctly

### DNS Propagation

**If using custom domain:**
- Wait 5-10 minutes for DNS propagation
- Check DNS resolution: `nslookup your-domain.com`
- Verify CNAME points to `username.github.io`

### HTTPS Verification

```bash
# Check SSL certificate
openssl s_client -connect username.github.io:443 -servername username.github.io

# Verify redirect HTTP → HTTPS
curl -I http://username.github.io/repository/

# Expected: 301 redirect to https://
```

### Deployment Checklist

**Complete Validation:**
- [ ] GitHub Actions workflow succeeded
- [ ] Site accessible at production URL
- [ ] HTTPS enabled and working
- [ ] No console errors (F12 → Console)
- [ ] All pages load correctly
- [ ] Navigation functional
- [ ] Mobile responsive
- [ ] Performance acceptable (Lighthouse)
- [ ] Accessibility verified

---

## Testing Workflow Summary

### Pre-Deployment Testing

```
1. Build Verification (Local)
   ├─ npm run build
   ├─ Verify no errors
   └─ Check build output

2. Local Testing
   ├─ npm run start (dev server)
   ├─ Manual navigation testing
   └─ Check for console errors

3. Commit & Push
   └─ Trigger CI/CD
```

### Post-Deployment Testing

```
1. Deployment Verification
   ├─ Check GitHub Actions logs
   ├─ Verify site accessible
   └─ No 404 errors

2. Performance Testing
   ├─ Lighthouse audit (Mobile & Desktop)
   └─ Core Web Vitals verification

3. Responsive Testing
   ├─ 375px viewport (iPhone SE)
   ├─ 768px viewport (Tablet)
   └─ 1920px viewport (Desktop)

4. Accessibility Testing
   ├─ Keyboard navigation
   ├─ Screen reader (optional)
   └─ Color contrast

5. Cross-Browser Testing
   ├─ Chrome
   ├─ Firefox
   └─ Safari (if available)
```

---

## Testing Tools Reference

### Essential Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| Chrome DevTools | Lighthouse, responsive testing, debugging | Built into Chrome |
| Lighthouse CLI | Automated audits | `npm install -g lighthouse` |
| axe DevTools | Accessibility testing | Browser extension |
| PageSpeed Insights | Performance analysis | Web-based (no install) |

### Optional Tools

| Tool | Purpose | Link |
|------|---------|------|
| WebAIM Contrast Checker | Color contrast verification | https://webaim.org/resources/contrastchecker/ |
| WAVE | Accessibility evaluation | https://wave.webaim.org/ |
| BrowserStack | Cross-browser testing | https://www.browserstack.com/ |
| Responsively App | Multi-viewport testing | https://responsively.app/ |

---

## Common Issues & Solutions

### Build Failures

**Issue**: MDX compilation error
```
Error: Unexpected character `<` before name
```
**Solution**: Escape angle brackets in markdown: `<` → `&lt;`, `>` → `&gt;`

**Issue**: Broken links error
```
Error: Broken link on source page /module-1/
```
**Solution**:
- Fix the link path
- Or set `onBrokenLinks: 'warn'` in docusaurus.config.ts

### Performance Issues

**Issue**: Low Lighthouse performance score (<80)
```
Largest Contentful Paint: 4.5s
```
**Solution**:
- Optimize images (use WebP, compress)
- Enable lazy loading
- Reduce JavaScript bundle size
- Use CDN (GitHub Pages includes this)

### Mobile Issues

**Issue**: Horizontal scrolling on mobile
```
Content width exceeds viewport
```
**Solution**:
- Check for fixed-width elements
- Ensure all content uses relative widths
- Test tables for responsiveness

### Accessibility Issues

**Issue**: Low accessibility score
```
Missing alt attributes on images
```
**Solution**:
- Add alt text to all images: `![Alt text](image.png)`
- Verify proper heading hierarchy
- Ensure sufficient color contrast

---

## Quick Testing Commands

```bash
# Full test suite (run from project root)

# 1. Build verification
npm run build

# 2. Check for broken links (manual inspection)
grep -r "](http" docs/ | grep -v "https://"

# 3. Lighthouse audit (after deployment)
lighthouse https://your-site.com/ --preset=mobile --view

# 4. Check responsive meta tag
curl -s https://your-site.com/ | grep viewport

# 5. Analyze bundle size
npm run build -- --bundleAnalyzer

# 6. Local preview
npm run serve
```

---

## Testing Checklist Template

```markdown
## Testing Report

**Date**: YYYY-MM-DD
**Site**: https://your-site.com/
**Tester**: [Name]

### Build Verification
- [ ] Local build succeeds
- [ ] No errors or warnings
- [ ] All modules present in build output

### Lighthouse Audit
- Performance (Mobile): __/100
- Performance (Desktop): __/100
- Accessibility: __/100
- Best Practices: __/100
- SEO: __/100

### Mobile Testing (375px)
- [ ] No horizontal scrolling
- [ ] Hamburger menu works
- [ ] All content accessible
- [ ] Touch interactions smooth

### Keyboard Navigation
- [ ] All elements accessible via Tab
- [ ] Focus indicators visible
- [ ] Logical tab order

### Cross-Browser
- [ ] Chrome: Working
- [ ] Firefox: Working
- [ ] Safari: Working

### Issues Found
- [List any issues discovered]

### Sign-Off
- [ ] All tests passed
- [ ] Ready for production
```

---

## Best Practices

**Testing Frequency:**
- ✅ Before every deployment (build verification)
- ✅ After major content updates (full test suite)
- ✅ Monthly (comprehensive audit)
- ✅ After Docusaurus upgrades (regression testing)

**Documentation:**
- Save Lighthouse reports (JSON/PDF)
- Screenshot test results
- Document issues and fixes
- Track performance over time

**Automation:**
- Use GitHub Actions for automated builds
- Set up Lighthouse CI for continuous testing
- Add pre-commit hooks for local validation

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-12-24
**Applies To**: Docusaurus 3.x, Static Documentation Sites
