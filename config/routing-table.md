# Decision-Type Routing Table

## Default Activation by Decision Type

| Decision Type | Default Activation | Description |
|--------------|-------------------|-------------|
| **Strategic** | CEO, CFO, CTO, VP Sales | Acquisition, market strategy, competitive positioning, business model changes |
| **Operational** | CEO, COO, VP Delivery | Major process change, workflow restructuring, org restructure |
| **Financial** | CEO, CFO, COO | Funding round, major investment, cost reduction, budget reallocation |
| **Technical** | CEO, CTO, CISO | Platform migration, architecture change, technology adoption, infrastructure |
| **Personnel** | CEO, CAO, COO, VP Delivery | Layoff, major hiring, reorganization, culture change |
| **Compliance/Risk** | CEO, CISO, CAO, CFO | Regulatory change, breach response, audit, legal exposure |

The CEO can always override defaults by adding or removing C-suite members from the activation set. The CSO is activated at the CEO's discretion for any decision type that would benefit from evidence-based research (typically Strategic, Financial, and Compliance/Risk decisions).

## Full-Activation Threshold Conditions

After classifying the decision type and selecting default routing, the CEO assesses whether the issue has cross-cutting implications that warrant full activation. If **any** of these conditions apply, **all** C-suite members activate regardless of decision type:

### 1. Irreversibility

**Core question:** Can this decision be meaningfully reversed within 12 months at acceptable cost?

| Diagnostic Question | YES (triggers) | NO (does not trigger) |
|---------------------|----------------|----------------------|
| Does reversal require rebuilding destroyed capabilities (teams, infrastructure, relationships)? | Irreversible -- lost capabilities cannot be reconstituted quickly | Capabilities remain intact; change is operational, not structural |
| Does reversal require regulatory re-approval or re-licensing? | Irreversible -- regulatory timelines are outside company control | No regulatory gate; reversal is an internal decision |
| Would reversal cost more than 50% of the original decision's cost? | Effectively irreversible -- the sunk cost makes reversal economically irrational | Reversal is financially viable even if inconvenient |

**If ANY diagnostic question answers YES:** Threshold triggered -- full activation.

**Calibration Exemplars:**
- **YES (triggers):** "Divest our healthcare division" -- capabilities destroyed, client relationships severed, regulatory licenses surrendered. Cannot rebuild in under 3 years.
- **NO (does not trigger):** "Switch project management tools from Jira to Linear" -- data exportable, workflows adjustable, revert possible within weeks.
- **Borderline:** "Commit to 3-year cloud vendor contract with early termination fee" -- technically reversible but financially painful. Evaluate via cost-of-reversal diagnostic.

### 2. Headcount Impact

**Core question:** Does this decision affect more than 30% of current headcount through direct or cascading effects?

| Diagnostic Question | YES (triggers) | NO (does not trigger) |
|---------------------|----------------|----------------------|
| Does the decision directly eliminate, create, or reassign more than 30% of roles? | Direct headcount impact crosses the threshold | Headcount change is localized to a small portion of the organization |
| Do cascading effects on adjacent teams push the total affected headcount above 30%? | Indirect effects amplify impact beyond the immediate scope | Adjacent teams can absorb changes without significant disruption |
| Does the decision eliminate entire role categories rather than reducing headcount within existing categories? | Role elimination signals structural change affecting career paths and institutional knowledge | Roles persist; only staffing levels change |

**If ANY diagnostic question answers YES:** Threshold triggered -- full activation.

**Calibration Exemplars:**
- **YES (triggers):** "Reduce engineering from 100 to 40 through outsourcing" -- 60% direct headcount reduction, destroys institutional knowledge, cascading effects on product and QA teams.
- **NO (does not trigger):** "Hire 5 new sales reps" -- incremental addition under 5% of headcount, no structural change, no cascading effects.
- **Borderline:** "Merge two 50-person departments into one 70-person department" -- 30% net reduction with role elimination, but some staff redeployed. Evaluate via cascading-effects diagnostic.

### 3. Market Position Change

**Core question:** Does this decision alter how the company is positioned in its market or how it generates revenue?

| Diagnostic Question | YES (triggers) | NO (does not trigger) |
|---------------------|----------------|----------------------|
| Does the decision change which customer segments the company serves? | Repositioning to new segments alters competitive dynamics and go-to-market strategy | Existing segments continue to be served; changes are within current market |
| Does the decision change the revenue model (how the company charges or what it charges for)? | Revenue model change affects unit economics, pricing strategy, and financial projections | Revenue model unchanged; decision affects execution within current model |
| Does the decision shift the company's competitive positioning relative to key competitors? | Competitive repositioning triggers responses from competitors and reshapes market perception | Competitive position is maintained; decision is operational improvement |

**If ANY diagnostic question answers YES:** Threshold triggered -- full activation.

**Calibration Exemplars:**
- **YES (triggers):** "Pivot from B2B SaaS to B2C marketplace" -- changes customer segment, revenue model, and competitive positioning simultaneously.
- **NO (does not trigger):** "Launch a premium tier of existing product" -- same customer segment, same revenue model (subscription), incremental competitive differentiation.
- **Borderline:** "Acquire a competitor to consolidate market share" -- competitive positioning shifts but customer segment and revenue model may remain unchanged. Evaluate via competitive-positioning diagnostic.

### 4. Existential Financial Risk

**Core question:** Could this decision, if it fails, threaten the company's ability to continue operating?

| Diagnostic Question | YES (triggers) | NO (does not trigger) |
|---------------------|----------------|----------------------|
| Does the decision commit capital exceeding the company's runway threshold (e.g., more than 6 months of operating expenses)? | Failure could exhaust reserves before recovery is possible | Financial exposure is bounded and survivable even in worst case |
| Does the decision create a single-source dependency where failure of one external factor causes company failure? | Single point of failure with existential consequences | Risk is distributed; no single failure mode is existential |
| Does the decision significantly alter the company's debt-to-equity ratio or leverage position? | Increased leverage reduces margin for error and amplifies downside | Capital structure remains stable; financial flexibility preserved |

**If ANY diagnostic question answers YES:** Threshold triggered -- full activation.

**Calibration Exemplars:**
- **YES (triggers):** "Invest 80% of cash reserves in new product line" -- failure exhausts reserves with no fallback, creating existential liquidity risk.
- **NO (does not trigger):** "Increase marketing spend by 20%" -- bounded financial exposure, easily reversible, does not threaten operating continuity.
- **Borderline:** "Take on debt equal to annual revenue for expansion" -- leverage increases significantly, creating vulnerability to revenue shortfalls. Evaluate via debt-to-equity diagnostic.

### 5. Domain Uncertainty

**Core question:** Is the CEO unable to confidently identify which 2-3 domains are most relevant to this decision?

| Diagnostic Question | YES (triggers) | NO (does not trigger) |
|---------------------|----------------|----------------------|
| Has the company faced a substantially similar decision before with known domain relevance? | No precedent -- domain relevance must be discovered, not recalled | Precedent exists; domain routing follows established patterns |
| Does the decision span 4+ domains with no clear primary domain? | Ambiguous domain overlap makes selective routing unreliable | Clear primary domain with well-understood secondary effects |
| Is this a novel decision category that does not fit existing decision type classifications? | Novel category means default routing table may not apply | Decision fits an existing type; default routing is appropriate |

**If ANY diagnostic question answers YES:** Threshold triggered -- full activation.

**Calibration Exemplars:**
- **YES (triggers):** "Respond to an AI regulation that affects engineering, legal, sales, and product simultaneously" -- no precedent, spans 4+ domains, novel regulatory category with unclear primary domain.
- **NO (does not trigger):** "Negotiate a new office lease" -- clear precedent, primarily operational and financial, well-understood domain relevance.
- **Borderline:** "Launch operations in a new country" -- some precedent from existing markets, but regulatory, cultural, and operational unknowns may span more domains than expected. Evaluate via domain-overlap diagnostic.

The CEO states activation reasoning in the CEO Framing section of the Decision Record, including which threshold conditions (if any) triggered full activation. This makes routing a transparent, auditable analytical act.

## CSO Research Activation

The CSO is activated conditionally based on the CEO's assessment of whether the decision requires evidence investigation. Typical activation patterns:

| Decision Type | CSO Activation | Rationale |
|--------------|---------------|-----------|
| Strategic | Usually activated | Market data, competitor analysis, precedent research needed |
| Operational | Rarely activated | Internal processes rarely require external evidence |
| Financial | Sometimes activated | Market conditions, precedent transactions may be relevant |
| Technical | Sometimes activated | Technology landscape, vendor comparisons may be relevant |
| Personnel | Rarely activated | Internal HR decisions rarely require external research |
| Compliance/Risk | Usually activated | Regulatory landscape, legal precedent research needed |

When the CSO is activated, Phase 1.5 (Research Investigation) executes before domain analysis begins. The CSO's Research Dossier is broadcast to all activated C-suite members.
