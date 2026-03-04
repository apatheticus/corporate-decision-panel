# Requirements: CDP Image Generation API Migration

**Defined:** 2026-03-04
**Core Value:** Infographic generation must work without browser interaction — a single API call per infographic that returns a PNG, driven by the same Decision Record data.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### API Setup

- [ ] **SETUP-01**: API key stored in `.cdp-context/config.md` with clear field format
- [ ] **SETUP-02**: Pre-flight validation probes API key and billing status before any generation
- [ ] **SETUP-03**: Model ID configurable in `.cdp-context/config.md` (not hardcoded)

### Image Generation

- [ ] **GEN-01**: Generate infographics via `generate_content()` with `response_modalities=["TEXT", "IMAGE"]` and `image_size="2K"`
- [ ] **GEN-02**: Serialize existing JSON prompt templates to text and pass as prompt content
- [ ] **GEN-03**: Assign optimal aspect ratio per infographic type (6 types)
- [ ] **GEN-04**: Enable thinking mode for complex infographic types (Fault-Line Map, Mode Comparison)

### Quality Validation

- [ ] **QUAL-01**: After generation, send image back to Gemini vision with expected data labels to verify text accuracy and readability
- [ ] **QUAL-02**: If validation fails, retry generation with corrective feedback (up to configurable max attempts)
- [ ] **QUAL-03**: Configurable retry limit stored in `.cdp-context/config.md`

### Error Handling

- [ ] **ERR-01**: Exponential backoff with jitter on 429/timeout errors
- [ ] **ERR-02**: Distinguish content/safety blocks (no retry) from transient errors (retry)
- [ ] **ERR-03**: Placeholder PNG + saved prompt JSON on total failure
- [ ] **ERR-04**: Inter-call delay (3-5s) between sequential infographic generations

### Documentation

- [ ] **DOC-01**: Update `templates/production/infographics.md` Task A spec for API-based flow
- [ ] **DOC-02**: Update `templates/config-context.md` template with API key, model ID, and retry limit fields
- [ ] **DOC-03**: Update `agents/ceo.md` Task A spawn instruction
- [ ] **DOC-04**: Remove all browser automation references from image generation workflow

## v2 Requirements

### Model Management

- **MODEL-01**: Model profile switch — Flash for development, Pro for production
- **MODEL-02**: Per-infographic model selection — Pro for text-heavy types, Flash for simpler ones

### Performance

- **PERF-01**: Concurrent generation with IPM-aware rate limiting
- **PERF-02**: Imagen 4 as alternative model option

## Out of Scope

| Feature | Reason |
|---------|--------|
| ChatGPT/OpenAI API support | Gemini-only — simplifies to one platform |
| Browser-based fallback | Clean break — no dual-path architecture |
| Pixel-level programmatic validation (OCR, contrast) | AI vision check is sufficient for text accuracy |
| Changing infographic types or data flow | Existing 6 types and Decision Record pipeline preserved |
| Modifying downstream embedding (PPTX, DOCX, HTML, PDF) | Output contract unchanged — same filenames, format, directory |
| Environment variable API key storage | Config file pattern consistent with existing .cdp-context/ convention |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| SETUP-01 | — | Pending |
| SETUP-02 | — | Pending |
| SETUP-03 | — | Pending |
| GEN-01 | — | Pending |
| GEN-02 | — | Pending |
| GEN-03 | — | Pending |
| GEN-04 | — | Pending |
| QUAL-01 | — | Pending |
| QUAL-02 | — | Pending |
| QUAL-03 | — | Pending |
| ERR-01 | — | Pending |
| ERR-02 | — | Pending |
| ERR-03 | — | Pending |
| ERR-04 | — | Pending |
| DOC-01 | — | Pending |
| DOC-02 | — | Pending |
| DOC-03 | — | Pending |
| DOC-04 | — | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 0
- Unmapped: 18 ⚠️

---
*Requirements defined: 2026-03-04*
*Last updated: 2026-03-04 after initial definition*
