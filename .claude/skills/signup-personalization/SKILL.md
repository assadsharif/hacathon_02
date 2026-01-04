# Skill: Signup & Personalization Design Intelligence

**Version**: 1.0.0
**Type**: Design Pattern Library
**Domain**: User Authentication, Progressive Enhancement, Privacy-First Personalization

---

## Overview

This skill provides design intelligence for **privacy-first, progressive enhancement authentication** and **layered personalization** patterns. It guides the implementation of signup flows that balance:

- **Zero Friction**: Anonymous access without mandatory signup
- **Progressive Value**: Clear benefits at each tier upgrade
- **Privacy Compliance**: GDPR, CCPA, FERPA, COPPA out-of-the-box
- **Educational Ethics**: Gamification without dark patterns

**Core Philosophy**: **"Users own their data, not the platform."**

---

## When to Use This Skill

Use this skill when designing:

1. **Freemium SaaS Applications** (Tier 0 free → Tier 1 trial → Tier 2 paid)
2. **Educational Platforms** (anonymous learners → registered students → premium members)
3. **Documentation Sites** (public docs → personalized learning paths → analytics)
4. **Knowledge Bases** (public access → bookmarking → cross-device sync)
5. **Content Platforms** (readers → contributors → creators)

**Anti-Pattern**: Mandatory signup walls, aggressive popups, dark patterns ("9 people viewing this page!")

---

## Design Principles

### 1. Progressive Enhancement (4 Tiers)

Users start anonymous and upgrade only when they see clear value:

```
Tier 0 (Anonymous) → Tier 1 (Lightweight) → Tier 2 (Full) → Tier 3 (Premium)
```

**Tier 0: Anonymous** (Browser-Local Only)
- **Features**: Read content, search, browse
- **Storage**: localStorage (30-day retention)
- **Privacy**: Zero data collection, no cookies
- **Upgrade Trigger**: "Save your progress" after 10 actions

**Tier 1: Lightweight Signup** (Email Verification)
- **Features**: Conversation history, bookmarks, cross-device sync
- **Auth**: Email + password or magic link
- **Privacy**: Minimal data (email, name), explicit consent
- **Upgrade Trigger**: "Connect your account" for personalization

**Tier 2: Full Profile** (OAuth Integration)
- **Features**: Personalized recommendations, learning paths, progress tracking
- **Auth**: OAuth (Google, GitHub, Microsoft)
- **Privacy**: Profile data (avatar, GitHub username), explicit consent
- **Upgrade Trigger**: "Unlock analytics" for instructors

**Tier 3: Premium** (Paid Features)
- **Features**: Advanced analytics, API access, priority support
- **Auth**: Payment verification (Stripe, PayPal)
- **Privacy**: Billing data (encrypted), PCI DSS compliance

---

### 2. Privacy-First Data Management

**4-Tier Data Classification**:

| Tier | Data Type | Storage | Encryption | Consent Required? |
|------|-----------|---------|------------|-------------------|
| **Public** | Page views, search queries (anonymized) | Server logs | None | No |
| **Pseudonymous** | Session ID, browser fingerprint | localStorage | None | No |
| **Personal** | Email, name, OAuth profile | Database | AES-256 | Yes (explicit opt-in) |
| **Sensitive** | Progress, quiz scores, billing | Database | AES-256 + field-level | Yes (explicit opt-in) |

**Data Retention**:
- **Tier 0 (Anonymous)**: 30 days (browser-local, auto-deleted)
- **Tier 1+ (Authenticated)**: Until user requests deletion (GDPR Article 17)

---

### 3. Layered Personalization

**3 Personalization Layers** (progressive disclosure):

**Layer 1: Behavioral** (All Users, No PII)
- Recently viewed pages
- Search history (browser-local only)
- Scroll position (resume reading)

**Layer 2: Demographic** (Tier 1+, Explicit Consent)
- Learning goals (e.g., "I want to learn about humanoid robots")
- Experience level (beginner, intermediate, advanced)
- Preferred content format (video, text, interactive)

**Layer 3: Academic** (Tier 2+, Explicit Consent)
- Progress tracking (completed modules, quiz scores)
- Skill assessments (strengths, weaknesses)
- Personalized learning paths (adaptive content)

**Privacy Safeguard**: Each layer requires explicit consent ("Personalize my experience?")

---

### 4. Educational Gamification (Without Dark Patterns)

**✅ Ethical Gamification**:
- **Progress Indicators**: "3/7 modules complete" (informative, not manipulative)
- **Achievements**: "Completed first module!" (celebrate milestones)
- **Streaks**: "7-day learning streak" (encourage consistency)

**❌ Dark Patterns (NEVER USE)**:
- **False Urgency**: "9 people viewing this page!" (fake scarcity)
- **Guilt Trips**: "You haven't logged in for 3 days" (shame users)
- **Misleading Progress**: "You're 90% done!" (inflate completion to encourage signup)
- **Bait-and-Switch**: Free trial → paid without clear warning

---

## 4-Tier Progressive Enhancement

### Tier 0: Anonymous (Zero Friction)

**Goal**: Provide maximum value without any signup requirement

**Features**:
- ✅ Read all public content (documentation, blog posts)
- ✅ Search across all content
- ✅ Use chat widget (browser-local conversation history)
- ❌ No cross-device sync
- ❌ No server-side bookmarks

**Storage**: localStorage (30-day retention)
**Privacy**: Zero data collection, no tracking

**Upgrade Trigger**:
- After 10 chat messages: "Save your conversation? Sign up for free."
- After 5 bookmarked pages: "Sync your bookmarks across devices."

---

### Tier 1: Lightweight Signup (Email Verification)

**Goal**: Minimal friction signup for cross-device sync

**Features**:
- ✅ All Tier 0 features
- ✅ Cross-device conversation sync
- ✅ Server-side bookmarks
- ✅ Export conversation history (GDPR Article 20)
- ❌ No personalized recommendations

**Auth Methods**:
- Email + password (traditional signup)
- Magic link (passwordless, email-only)

**Data Collected**:
- Email address (required for verification)
- Display name (optional)

**Privacy**:
- Explicit consent: "We'll store your conversation history on our servers."
- Cookie consent banner (GDPR compliance)

**Upgrade Trigger**:
- After 20 messages: "Get personalized recommendations. Connect your GitHub/Google account."

---

### Tier 2: Full Profile (OAuth Integration)

**Goal**: Personalized learning experience with OAuth convenience

**Features**:
- ✅ All Tier 1 features
- ✅ Personalized recommendations (based on reading history)
- ✅ Learning paths (adaptive content)
- ✅ Progress tracking (completed modules, quiz scores)
- ❌ No advanced analytics

**Auth Methods**:
- OAuth (Google, GitHub, Microsoft)
- Social login (seamless signup, no password)

**Data Collected**:
- OAuth profile (name, avatar, email)
- Reading history (pages viewed, time spent)
- Progress data (completed modules, quiz scores)

**Privacy**:
- Explicit consent: "We'll personalize your learning path based on your progress."
- Data portability: Export all data (JSON/CSV)

**Upgrade Trigger**:
- For instructors: "See how your students are doing. Upgrade to Premium."

---

### Tier 3: Premium (Paid Features)

**Goal**: Advanced analytics and priority support for educators

**Features**:
- ✅ All Tier 2 features
- ✅ Advanced analytics (class progress, engagement metrics)
- ✅ API access (integrate with LMS)
- ✅ Priority support (24-hour response time)
- ✅ Custom branding (white-label option)

**Auth Methods**:
- Payment verification (Stripe, PayPal)
- Subscription management (monthly/annual billing)

**Data Collected**:
- Billing information (encrypted, PCI DSS compliant)
- Usage analytics (anonymized, aggregated)

**Privacy**:
- PCI DSS compliance for payment data
- Anonymized analytics (no individual student data shared)

---

## Compliance & Privacy

### GDPR (EU General Data Protection Regulation)

**Consent Management**:
- ✅ Explicit opt-in before Tier 1+ signup
- ✅ Clear privacy policy link
- ✅ "Do Not Track" mode (browser-local only, no server sync)

**User Rights**:
- ✅ Right to Access: Export conversation history (JSON/CSV)
- ✅ Right to Deletion: One-click account deletion (GDPR Article 17)
- ✅ Right to Portability: Download all user data

**Implementation**:
```json
{
  "gdpr_controls": {
    "consent_banner": true,
    "privacy_policy_link": "/privacy",
    "data_export_endpoint": "/api/v1/user/export",
    "data_deletion_endpoint": "/api/v1/user/delete",
    "retention_policy": "30_days_inactive_anonymous"
  }
}
```

---

### CCPA (California Consumer Privacy Act)

**"Do Not Sell My Data" Opt-Out**:
- ✅ Footer link: "Do Not Sell My Personal Information"
- ✅ Opt-out applies retroactively (existing data not sold)
- ✅ No account required to opt-out (global setting)

**Implementation**:
```json
{
  "ccpa_controls": {
    "do_not_sell_link": "/ccpa-opt-out",
    "opt_out_applies_retroactively": true,
    "third_party_sharing": false
  }
}
```

---

### FERPA (Family Educational Rights and Privacy Act)

**Student Privacy Protection**:
- ✅ No PII shared with third parties without parental consent (if <18)
- ✅ Educational records (progress, quiz scores) encrypted at rest
- ✅ Instructor access limited to authorized personnel

**Implementation**:
```json
{
  "ferpa_controls": {
    "age_gate": 13,
    "parental_consent_required_under": 18,
    "educational_records_encryption": "AES-256",
    "third_party_sharing": "parental_consent_only"
  }
}
```

---

### COPPA (Children's Online Privacy Protection Act)

**Age Gating (<13 years)**:
- ✅ Age verification before account creation
- ✅ Parental consent modal (email verification to parent)
- ✅ Limited data collection (no behavioral tracking for <13)

**Implementation**:
```json
{
  "coppa_controls": {
    "minimum_age": 13,
    "age_verification_method": "date_of_birth",
    "parental_consent_flow": "email_verification",
    "under_13_features_disabled": ["social_sharing", "public_profiles", "third_party_analytics"]
  }
}
```

---

## Integration Points

### Skills
- `.claude/skills/chatkit-widget/` (Session Continuity Pattern, Contextual Feature Discovery)
- `.claude/skills/rag-chatbot/` (Browser-Local Session Management Pattern)

### Agents
- None (design-time only, no runtime orchestration)

### MCP Servers
- `.claude/mcp/better-auth/` (OAuth integration, session management)

---

## Cross-Domain Applicability

| Domain | Use Cases | Applicability |
|--------|-----------|---------------|
| **Educational Platforms** | MOOCs, course platforms, LMS | ✅ Very High (FERPA, progressive learning paths) |
| **SaaS Applications** | Freemium products, productivity tools | ✅ Very High (Tier 0 free → paid conversion) |
| **Documentation Sites** | API docs, developer portals | ✅ High (anonymous readers → personalized paths) |
| **Knowledge Bases** | Internal wikis, help centers | ✅ High (public access → personalized search) |
| **E-Commerce** | Online stores, marketplaces | ✅ Medium (guest checkout → account creation) |

---

## Patterns

This skill includes **4 reusable design patterns** (see `patterns.md`):

1. **Progressive Enhancement Signup** (4-tier: Anonymous → Lightweight → Full → Premium)
2. **Layered Personalization** (3 layers: Behavioral → Demographic → Academic)
3. **Privacy-First Data Management** (4-tier data classification)
4. **Educational Gamification** (Ethical engagement without dark patterns)

**Total Lines**: ~1,300 (SKILL.md: 533, patterns.md: 783)

---

## References

- **GDPR Compliance**: https://gdpr.eu/
- **CCPA Compliance**: https://oag.ca.gov/privacy/ccpa
- **FERPA Guidelines**: https://www2.ed.gov/policy/gen/guid/fpco/ferpa/index.html
- **COPPA Compliance**: https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa
- **Ethical Design**: https://www.ethicaldesign.org/
- **Dark Patterns**: https://www.deceptive.design/

---

**Status**: Design-Complete ✅
**Lines**: 533
**Purpose**: Design-time intelligence for privacy-first authentication and personalization (Phase 7+ implementation reference)
