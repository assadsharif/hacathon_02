# Testing Skill

Comprehensive testing guidance for Docusaurus documentation sites.

## Quick Start

This skill provides procedures and best practices for:
- Build verification
- Performance audits (Lighthouse)
- Mobile responsiveness testing
- Accessibility validation
- Cross-browser compatibility
- Deployment validation

## When to Use

- Before deploying to production
- After major content updates
- During quality assurance
- Investigating performance issues
- Validating accessibility compliance

## Key Sections

1. **Build Verification** - Ensure builds complete without errors
2. **Performance Audits** - Lighthouse testing and Core Web Vitals
3. **Mobile Testing** - Responsive design validation (375px+)
4. **Accessibility** - Keyboard navigation, screen readers, ARIA
5. **Cross-Browser** - Testing across Chrome, Firefox, Safari
6. **Deployment** - GitHub Actions and production validation

## Success Criteria

- **Build**: No errors, all modules present
- **Performance**: ≥90 mobile, ≥95 desktop
- **Accessibility**: ≥95 score
- **Mobile**: No horizontal scroll at 375px
- **Deployment**: HTTPS enabled, site accessible

## Quick Commands

```bash
# Build verification
npm run build

# Lighthouse audit
lighthouse https://site.com/ --preset=mobile --view

# Check responsiveness
curl -s https://site.com/ | grep viewport

# Accessibility check
grep -r '<img ' build/ | grep -v 'alt='
```

## Related

- **Agent**: `.claude/agents/testing-validation/` - Autonomous test execution
- **Checklists**: `specs/Phase I/001-physical-ai-book/checklists/` - Project-specific tests
