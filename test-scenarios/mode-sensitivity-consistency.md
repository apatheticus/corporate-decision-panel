# Mode Sensitivity Consistency Scenarios

**Requirement:** TEST-04
**Validates:** Mode sensitivity ratings produce consistent results across similar decision types
**Specification References:**
- `templates/comparative-decision-record.md` (Quantitative Sensitivity Criteria, Divergence Classification Guide)
- `config/decision-modes.md` (five mode definitions with weighting tables)

---

## Purpose

This scenario validates that the quantitative sensitivity criteria from comparative-decision-record.md produce stable, predictable ratings based on decision structural characteristics, not on the specific domain or wording of the issue. If two decisions share the same structural profile (decision type, threshold triggers, advocate/skeptic tension level), they should produce the same sensitivity level -- demonstrating that the criteria are specification-driven, not arbitrary.

## Methodology

Two pairs of scenarios are defined:
- **Pair 1:** Expected HIGH sensitivity (irreversible strategic decisions with strong advocate/skeptic tension)
- **Pair 2:** Expected LOW sensitivity (clear, mandatory decisions with unambiguous evidence)

Each pair shares structural characteristics but differs in business domain. The structural similarity is what drives sensitivity level; the domain difference proves the criteria generalize.

---

## Pair 1: Expected HIGH Sensitivity

### Structural Profile

| Attribute | Value |
|-----------|-------|
| Decision Type | Strategic |
| Thresholds Triggered | Irreversibility, Existential Financial Risk |
| Advocate/Skeptic Tension | HIGH (CTO/VP Sales see growth opportunity vs CFO/CISO see existential risk) |
| Expected Sensitivity | HIGH |

**Expected Rationale:** Decision direction will diverge because risk appetite is the deciding factor. Guardian and Sentinel will oppose or defer; Pioneer will approve aggressively. 3+ distinct decisions expected. Multiple determinative perspectives expected (CFO for risk-averse modes, CTO/VP Sales for growth modes). Contradictory conditions expected (Guardian's conditions designed to prevent action vs Pioneer's designed to accelerate it).

### Scenario A: "Divest our healthcare division to fund AI expansion"

**Issue:** The company's healthcare consulting division generates 35% of revenue but is growing at 5% annually. The AI services division generates 15% of revenue but growing at 40% annually. A private equity firm has offered $30M for the healthcare division. Proceeds would fund aggressive AI expansion.

**Invocation:** `/cdp:deliberate all-modes: Should we divest our healthcare consulting division for $30M to fund AI services expansion?`

| Attribute | Value |
|-----------|-------|
| Decision Type | Strategic |
| Thresholds | Irreversibility (divestiture cannot be undone), Existential Financial Risk ($30M deal affecting 35% of revenue base) |

**Expected Dimension Analysis (per Quantitative Sensitivity Criteria):**

- **Decision Direction: DIVERGE** -- Guardian/Sentinel oppose (giving up proven revenue for speculative growth), Pioneer approves (competitive window in AI), Analyst conditionally approves (growth data supports but revenue concentration risk), Architect seeks phased approach. 4+ distinct decision values.
- **Determinative Perspective: DIVERGE** -- Risk-averse modes cite CFO (revenue loss), growth modes cite CTO (AI capability), systemic modes cite CAO (organizational upheaval). 4+ distinct roles.
- **Condition Overlap: DIVERGE** -- Guardian's conditions prevent divestiture (require replacement revenue first), Pioneer's conditions accelerate it (lock in PE offer before it expires). Contradictory conditions.
- **Rating: HIGH**

### Scenario B: "Acquire competitor in adjacent market using 60% of cash reserves"

**Issue:** A direct competitor in the company's secondary market (cloud infrastructure) is available for acquisition at $25M, representing 60% of the company's cash reserves. The competitor has strong technology and 50 enterprise customers but is unprofitable.

**Invocation:** `/cdp:deliberate all-modes: Should we acquire CloudInfra Corp for $25M, using 60% of our cash reserves?`

| Attribute | Value |
|-----------|-------|
| Decision Type | Strategic |
| Thresholds | Irreversibility (acquisition cannot be undone), Existential Financial Risk (60% of cash reserves), Market Position Change (alters competitive positioning in cloud infrastructure) |

**Expected Dimension Analysis (per Quantitative Sensitivity Criteria):**

- **Decision Direction: DIVERGE** -- Guardian opposes (existential capital risk for unprofitable target), Pioneer approves (50 enterprise customers and technology), Sentinel defers (needs investigation of unprofitability root causes), Analyst conditionally approves, Architect seeks conditions for organizational integration. 4+ distinct decision values.
- **Determinative Perspective: DIVERGE** -- CFO for capital risk modes, CTO for technology acquisition modes, VP Sales for market expansion modes, COO for integration feasibility modes. 4+ distinct roles.
- **Condition Overlap: DIVERGE** -- Guardian requires the target to reach profitability before close (contradicts Pioneer's urgency), Sentinel requires 6-month investigation period (contradicts competitive pressure). Contradictory conditions.
- **Rating: HIGH**

### Consistency Assertion for Pair 1

Both scenarios share: Strategic decision type, irreversibility threshold, existential financial risk, high advocate/skeptic tension between growth-oriented and risk-averse perspectives. Both should produce HIGH sensitivity because the decision outcome fundamentally depends on the organization's risk appetite -- a factor that differs by mode definition.

**If these scenarios produce different sensitivity levels**, it indicates the criteria are sensitive to domain content rather than structural characteristics, which would be a flaw in the specification. The specific dimension producing the inconsistency would identify which classification rule needs refinement.

---

## Pair 2: Expected LOW Sensitivity

### Structural Profile

| Attribute | Value |
|-----------|-------|
| Decision Type | Compliance/Risk (Scenario A) / Operational (Scenario B) |
| Thresholds Triggered | None (the action itself is not the risk; inaction is) |
| Advocate/Skeptic Tension | LOW (all perspectives converge because the action is essentially mandatory) |
| Expected Sensitivity | LOW |

**Expected Rationale:** All modes converge on the same decision because the evidence is unambiguous and the cost of inaction exceeds the cost of action regardless of risk posture. 1 decision direction expected. 1-2 determinative perspectives expected. Substantively identical conditions expected.

### Scenario A: "Patch critical zero-day vulnerability in production authentication system"

**Issue:** Security researchers have published a proof-of-concept exploit for a zero-day vulnerability in the authentication library used in production. Active exploitation has been observed in the wild. The patch is available and has been tested in staging.

**Invocation:** `/cdp:deliberate all-modes: Should we deploy the emergency patch for CVE-2026-XXXXX in our production authentication system?`

| Attribute | Value |
|-----------|-------|
| Decision Type | Compliance/Risk |
| Thresholds | None triggered (patching is the low-risk action; NOT patching is the existential risk) |

**Expected Dimension Analysis (per Quantitative Sensitivity Criteria):**

- **Decision Direction: CONVERGE** -- All 5 modes produce "Approve" (immediate deployment). The vulnerability is actively exploited; delay increases risk in every synthesis posture. 1 distinct decision value.
- **Determinative Perspective: CONVERGE** -- CISO cited in all or nearly all modes (unambiguous security authority for an active exploit). 1 distinct role.
- **Condition Overlap: CONVERGE** -- All modes require post-deployment monitoring, incident response readiness, and customer notification if data was potentially exposed. Substantively the same conditions.
- **Rating: LOW**

### Scenario B: "Respond to regulatory order requiring data localization within 30 days"

**Issue:** The data protection authority has issued a binding order requiring all customer data for EU customers to be stored in EU data centers within 30 days. Non-compliance penalties are 4% of global annual revenue. The company currently stores all data in US-East.

**Invocation:** `/cdp:deliberate all-modes: Should we execute an emergency data migration to comply with the EU data localization order within 30 days?`

| Attribute | Value |
|-----------|-------|
| Decision Type | Operational (compliance-driven) |
| Thresholds | None triggered (compliance is mandatory; the question is execution approach, not whether to comply) |

**Expected Dimension Analysis (per Quantitative Sensitivity Criteria):**

- **Decision Direction: CONVERGE** -- All 5 modes produce "Approve" (compliance is mandatory). 4% revenue penalty makes non-compliance irrational in every synthesis posture. 1 distinct decision value.
- **Determinative Perspective: CONVERGE** -- CISO/CAO (Legal) cited across modes (regulatory compliance authority is unambiguous). 1-2 distinct roles.
- **Condition Overlap: CONVERGE** -- All modes require migration plan with rollback capability, customer notification, and legal sign-off. The mandatory nature of compliance eliminates meaningful condition variance. Substantively the same conditions.
- **Rating: LOW**

### Consistency Assertion for Pair 2

Both scenarios share: mandatory action driven by clear external forcing function, no meaningful threshold triggers (inaction is the risk, not action), low advocate/skeptic tension because no mode's risk posture argues against compliance/security. Both should produce LOW sensitivity because the evidence speaks for itself -- synthesis posture does not change the outcome.

**If these scenarios produce different sensitivity levels**, it indicates the criteria incorrectly discriminate based on domain (security vs regulatory) rather than structural characteristics. The specific dimension producing the inconsistency would identify which classification rule needs refinement.

---

## Overall Validation Statement

If Pair 1 both produce HIGH and Pair 2 both produce LOW, the criteria demonstrate:

1. **Discrimination** -- The criteria correctly distinguish between decisions where mode matters a lot (HIGH) and decisions where mode barely matters (LOW)
2. **Consistency** -- Structurally similar decisions produce the same rating regardless of business domain
3. **Specification-driven** -- The ratings follow from the quantitative criteria (dimension counts and classifications), not from subjective assessment

If any pair produces inconsistent ratings, the inconsistency points to a specific dimension's classification rule that needs refinement, enabling targeted specification improvement.
