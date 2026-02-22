# Idea Report: The Engagement Model

**Direction explored by:** Free Thinker + Grounder
**Report number:** 2
**Related threads:** Interaction tiers, CEO decision modes, scenario forking, user invocation patterns

---

## The Idea

The Team of Teams skill needs an **engagement model** — a coherent design for how users interact with the system across different types of decisions. Rather than a single mode of operation (the full five-phase cascade), the skill offers a two-dimensional control surface: **depth** (how many agents engage and how thoroughly) and **width** (how many decision perspectives the CEO synthesizes from).

**Depth is controlled through three interaction tiers:**
- **Tier 1: The Hallway Question** — Direct consult with a single C-suite agent. Fast, conversational, domain-specific. No CEO involvement, no formal routing. Output: Advisory Note (3-5 sentences).
- **Tier 2: The Working Session** — CEO routes to 2-4 relevant C-suite members. Each does domain analysis with team lead perspectives. CEO produces a lightweight synthesis. Output: Panel Assessment (abbreviated Decision Record, ~1 page).
- **Tier 3: The Board Meeting** — Full five-phase cascade from Report #1. All relevant C-suite members activated, full team lead analysis, full CEO deliberation. Output: Complete Decision Record.

**Width is controlled through four CEO Decision Modes:**
- **Guardian Mode** (risk-averse) — Weights skeptic roles more heavily. Favors protecting what exists over pursuing what's possible. High threshold for accepting risk.
- **Pioneer Mode** (growth-oriented) — Weights advocate roles more heavily. Treats skeptic concerns as engineering problems to solve. Favors capturing opportunities.
- **Architect Mode** (consensus-building) — Weights the fault lines themselves. Seeks the position that satisfies the most domain concerns. Favors organizational alignment.
- **Analyst Mode** (data-driven) — Weights confidence levels regardless of role disposition. High-confidence findings carry more weight. Flags low-confidence areas for further research.

The default experience is simple: one tier, one mode, one decision. Power users can unlock multi-mode comparison, where the same domain analysis produces different CEO syntheses side by side, revealing how risk appetite shapes the outcome.

## The Key Insight

The difference between a quarterly novelty and a daily tool is whether the skill matches the user's engagement level to the decision's weight. Most organizational questions don't need a full board meeting — they need a hallway conversation or a focused working session. By offering three tiers, the skill becomes a permanent member of the user's workflow, not an event they invoke for major decisions.

## How We Got Here

The Free Thinker's "second wave" proposed five directions beyond the core architecture. Interaction tiers (Direction E) was identified by both the Free Thinker and Grounder as the idea that determines adoption — "the one that determines whether anyone actually uses this regularly." The CEO Personalities thread (originally planted during Report #1 development) was recognized by the Grounder as a special case of a broader concept — Decision Modes that parameterize the CEO's synthesis without changing the underlying domain analysis. The Grounder proposed unifying depth (tiers) and width (modes) into a single engagement model.

## The Grounder's Take

- **Does this connect to what was asked for?** Yes — the concept seed asks for a skill that "makes decisions and answers questions on issues." The engagement model is how users present those issues and receive those answers. Without it, the spec describes an engine with no steering wheel.
- **Would the audience care?** This is the idea the builder agent needs second, right after the core architecture. You can't build a usable skill without defining how users invoke it and what they get back at each level of engagement.
- **Is this one of the good ones?** Yes. The tiers solve the adoption problem. The decision modes solve the "whose judgment?" problem. Together they make the skill feel like having an executive team on retainer rather than a bureaucratic decision machine.

## The Free Thinker's Vision

The most ambitious version: every issue the user brings is automatically triaged to the right tier by the CEO, the user can escalate or de-escalate with a word, and for the biggest decisions, a multi-mode comparison shows the decision space — "here's what a Guardian CEO decides, here's what a Pioneer CEO decides, here's the Architect's compromise, and here's what the Analyst says you need to know before choosing." The user sees their own decision-making style reflected back to them and can choose consciously.

## Architecture Details

### Invocation Patterns
The skill supports four invocation commands:
- **`/consult [role]: [question]`** — Tier 1. Direct consult with a named C-suite role.
- **`/panel [roles]: [issue]`** — Tier 2. User-selected panel of C-suite roles.
- **`/deliberate: [issue]`** — Tier 3. Full cascade with CEO routing.
- **`/evaluate: [issue]`** — Unclassified. CEO triages and recommends a tier. User can override.

Optional flags:
- `--mode [guardian|pioneer|architect|analyst]` — Override default decision mode.
- `--compare-modes` — Run Tier 2/3 analysis through all four modes and produce comparative output.

### Tier Selection Logic
When the CEO triages an unclassified issue:
1. Assess scope (single-domain vs. multi-domain vs. cross-cutting)
2. Assess impact (low/medium/high/critical)
3. Assess reversibility (easily reversed vs. difficult to reverse vs. irreversible)
4. Recommend tier with one-sentence justification visible to user
5. User can accept, escalate, or de-escalate

### Output Formats by Tier

**Tier 1 — Advisory Note:**
- Domain recommendation (1-2 sentences)
- Key consideration (1 sentence)
- Suggested follow-up if warranted (which other roles might want to weigh in)
- Total length: 3-5 sentences

**Tier 2 — Panel Assessment:**
- Executive Summary (3-5 sentences)
- Domain analyses from activated roles only (1 paragraph each)
- Top 2-3 fault lines
- Recommendation with conditions
- Total length: ~1 page

**Tier 3 — Full Decision Record:**
- Complete format as specified in Report #1
- Total length: 3-5 pages

### Decision Mode Implementation
- Decision Modes are implemented as **CEO synthesis prompt modifiers** — injected text that changes how the CEO weighs domain recommendations
- The underlying domain analysis is identical across modes
- Multi-mode comparison runs the CEO synthesis phase multiple times with different modifiers, producing a **Decision Space Map** that shows how each mode shapes the outcome
- Default mode: Analyst (most neutral). Configurable in company profile.

## Open Threads

- **Company Profile integration:** Decision Mode default and tier escalation thresholds could be configurable per company profile.
- **Tier escalation mid-analysis:** Can a Tier 1 consult escalate to Tier 2 mid-conversation if the C-suite agent realizes the question is bigger than it seemed?
- **Mode blending:** Could users create custom modes that blend dispositions? (e.g., "growth-oriented but weight security concerns heavily") — probably v2.
- **Conversation history in Tier 1:** Does the C-suite agent in direct consult mode remember previous hallway questions? (Connects to institutional memory thread.)

## Recommendation to Arbiter

**Strongly recommended as the second core idea for the spec.** The cascade architecture (Report #1) is the engine. The engagement model is the interface. Without it, the skill is a powerful machine with no practical way for users to interact with it at the right level of depth for each decision. The three tiers ensure daily adoption. The four decision modes ensure the output is genuinely useful for decision-makers with different styles. Flag as "interesting."
