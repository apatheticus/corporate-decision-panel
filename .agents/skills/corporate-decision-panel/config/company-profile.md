# Company Profile Configuration

## Overview

The skill supports company profile parameterization through **archetype presets** -- pre-configured profiles that set roster composition, default decision mode, escalation behavior, and industry-specific compliance frameworks. Users select an archetype during onboarding and can override individual settings afterward.

## Configuration Format

```yaml
company_profile:
  archetype: technology_saas  # technology_saas | professional_services | regulated_industry | manufacturing
  name: "Company Name"
  industry: "Industry Description"
  headcount: 350

  overrides:
    team_leads:
      facilities-office-manager: { active: false }
      product-ux-lead: { active: true, reports_to: cto }
    default_mode: analyst
    escalation_bias: normal  # conservative | normal | aggressive
```

## Archetype Presets

### Technology / SaaS (Default)

Default for mid-market IT/technology services companies, 200-500 employees.

| Setting | Value |
|---------|-------|
| **Roster Modifications** | Facilities/Office Manager inactive. Product/UX Lead active under CTO. |
| **Default Mode** | Analyst |
| **Compliance Focus** | SOC 2, GDPR |
| **Escalation Bias** | Normal |
| **Notes** | Pioneer-leaning for growth-stage companies. Technical decisions route through CTO + CISO by default. |

### Professional Services

For consulting, legal, accounting, and other professional services firms.

| Setting | Value |
|---------|-------|
| **Roster Modifications** | All roles active. VP Delivery weighted heavily in routing. |
| **Default Mode** | Architect |
| **Compliance Focus** | Client contract compliance, professional liability |
| **Escalation Bias** | Normal |
| **Notes** | Client-centric framing in COO and VP Sales domains. Resource Manager and Client Success Lead are primary analytical voices. |

### Regulated Industry

For healthcare, financial services, energy, and other regulated sectors.

| Setting | Value |
|---------|-------|
| **Roster Modifications** | All roles active. Compliance/GRC Lead has expanded scope. |
| **Default Mode** | Guardian |
| **Compliance Focus** | HIPAA, SOX, PCI-DSS (industry-specific, configured at setup) |
| **Escalation Bias** | Conservative |
| **Notes** | Industry-specific compliance frameworks auto-configured. CISO and CAO Legal are always activated for decisions touching regulated areas. |

### Manufacturing / Physical

For manufacturing, logistics, and physical product companies.

| Setting | Value |
|---------|-------|
| **Roster Modifications** | Facilities/Office Manager active. Supply chain emphasis in COO domain. |
| **Default Mode** | Analyst |
| **Compliance Focus** | Industry safety standards, environmental regulations |
| **Escalation Bias** | Normal |
| **Notes** | Vendor/Procurement Manager weighted heavily. COO domain is the default primary perspective for operational decisions. |

## Override Mechanism

After selecting an archetype, users override individual settings:

```yaml
overrides:
  team_leads:
    # Deactivate a role
    facilities-office-manager: { active: false }
    # Activate a conditional role
    facilities-office-manager: { active: true }
    # Reassign reporting
    product-ux-lead: { reports_to: coo }

  # Change default synthesis mode
  default_mode: guardian

  # Adjust escalation sensitivity
  # conservative = more likely to escalate to higher tiers
  # aggressive = less likely to escalate, keeps analysis lean
  escalation_bias: conservative

  # Add industry-specific compliance frameworks
  compliance_frameworks:
    - SOC2
    - GDPR
    - HIPAA
```

## Calibration Protocol

When the skill is first configured for a company, run an organizational stress test:

1. **Select a contentious test issue** -- an issue where reasonable people would disagree about the right approach. Example: "Should we acquire a competitor that would double our headcount but carries significant regulatory risk and requires taking on substantial debt?"

2. **Run full Tier 3 cascade** -- validates all agents produce coherent, domain-appropriate analysis for this company type.

3. **Run all five Decision Modes** -- domain analysis runs once, CEO synthesis runs five times.

4. **Verify 3-of-5 divergence** -- at least 3 of 5 modes must produce materially different outcomes. "Materially different" means either a different decision (approve vs. oppose vs. defer) or the same decision with substantially different conditions, guardrails, or accepted risks.

5. **Log calibration results:**

```yaml
calibration:
  stress_test_issue: "[issue description]"
  date: "[timestamp]"
  mode_results:
    guardian: "[decision summary]"
    pioneer: "[decision summary]"
    architect: "[decision summary]"
    analyst: "[decision summary]"
    sentinel: "[decision summary]"
  divergence_score: "[N] of 5 modes produced different decisions"
  calibration_status: pass  # or fail -- requiring prompt modifier revision
```

If calibration fails (fewer than 3 modes diverge on a deliberately contentious issue), the prompt modifiers need revision before the skill is considered calibrated.
