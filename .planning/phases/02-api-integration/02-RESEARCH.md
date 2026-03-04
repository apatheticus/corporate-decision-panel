# Phase 2: API Integration - Research

**Researched:** 2026-03-04
**Domain:** Gemini API image generation via google-genai Python SDK
**Confidence:** HIGH

## Summary

Phase 2 builds `scripts/generate_infographic.py` -- a pure-function Python module that serializes JSON prompt templates to natural language, calls the Gemini API's `generate_content()` with image modalities, and saves the resulting PNG. The core API surface is well-understood: `client.models.generate_content()` with `response_modalities=["TEXT", "IMAGE"]`, `ImageConfig(aspect_ratio=..., image_size="2K")`, and response iteration via `part.as_image()` to get a PIL Image for saving.

The most significant finding is that **the current default model `gemini-2.5-flash-image` does NOT support thinking mode** (confirmed by official Vertex AI docs and the Gemini API model card). GEN-04 requires thinking mode for Fault-Line Map and Mode Comparison types. The solution is to make `thinking_config` conditional: only apply it when the configured model supports thinking (Gemini 3 image models). The script should accept an optional `thinking_config` parameter and apply it when the model ID indicates support (e.g., `gemini-3-pro-image-preview` or `gemini-3.1-flash-image-preview`). This keeps the default model working while allowing operators to upgrade.

The prompt serialization strategy (flattening JSON templates to natural language with hex color codes) aligns well with Google's official guidance: "Describe the scene, don't just list keywords." The template structure (core/style/technical/composition/quality_keywords/extras) maps cleanly to prompt sections.

**Primary recommendation:** Build a single `scripts/generate_infographic.py` module with `generate_infographic()` function that handles template loading, prompt assembly, API call, and PNG save. Make thinking_config model-aware. Use `response_modalities=["TEXT", "IMAGE"]` and `image_size="2K"` for all types.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Flatten JSON templates to natural language prompts (not raw JSON, not structured text blocks)
- Include hex color codes from template `extras.color_mapping` in the prompt for brand consistency (e.g., "Use #2E7D32 for Approve, #C62828 for Oppose")
- Always save the assembled prompt to `{output_dir}/INFOGRAPHIC_<type-slug>_PROMPT.txt` alongside the PNG, for debugging and iteration
- CEO agent (or Image Agent) creates a data JSON file with populated placeholder values extracted from the Decision Record
- Script reads the data JSON file path as input -- it does not extract data from RECORD.md itself
- Script is a pure function: template type + data file + output path -> PNG
- If `.cdp-context/style.md` exists, append its contents to the generated prompt as additional style guidance
- style.md is optional -- if absent, generate with template defaults only
- Auto-run preflight before generation by default
- Provide `--skip-preflight` flag for when CEO agent has already validated in the session
- Hard stop on preflight failure -- no PNG produced, no placeholder, operator must fix config
- Print structured status lines during generation: GENERATING, PROMPT assembled, IMAGE received, SAVED -- parseable by CEO agent
- Expose an importable Python function `generate_infographic(type, data_path, output_path, skip_preflight=False)` as the core API
- CLI wrapper via `python -m scripts.generate_infographic` for standalone invocation
- Matches Phase 1 pattern where `run_preflight()` is both importable and CLI-accessible

### Claude's Discretion
- Data layout in prompt: inline vs separate data section -- pick what produces better images
- Quality cue selection: which `quality_keywords` and `technical` specs are meaningful for Gemini image gen vs noise
- CLI interface details: exact flag names, positional vs named arguments
- Data JSON schema: whether to use template `{{PLACEHOLDER}}` token names or a cleaner schema
- Whether to include `.cdp-context/company.md` context in the prompt for branding
- Module structure within `scripts/` (new file vs extending existing)

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| GEN-01 | Generate infographics via `generate_content()` with `response_modalities=["TEXT", "IMAGE"]` and `image_size="2K"` | Verified: google-genai SDK v1.65.0 supports `GenerateContentConfig(response_modalities=["TEXT", "IMAGE"], image_config=ImageConfig(image_size="2K"))`. Response parts iterable via `part.as_image()` returning PIL Image. 2K = 2048px on longest edge, exceeds 2000px requirement. |
| GEN-02 | Serialize existing JSON prompt templates to text and pass as prompt content | 6 JSON templates in `templates/infographic-prompts/` with core/style/technical/composition/quality_keywords/extras structure. Flatten to natural language following Google's prompt guide: descriptive paragraphs, not keyword lists. |
| GEN-03 | Assign optimal aspect ratio per infographic type (6 types) | `ImageConfig.aspect_ratio` supports: "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9". Requirements specify 4:3 for matrix/scorecard, 16:9 for routing/fault-line. |
| GEN-04 | Enable thinking mode for complex infographic types (Fault-Line Map, Mode Comparison) | CRITICAL: `gemini-2.5-flash-image` does NOT support thinking. Only Gemini 3 image models support thinking (via `thinking_level`). Implement as conditional: apply `ThinkingConfig` only when model supports it. Use `thinking_budget` for 2.5 models, `thinking_level` for 3.x models. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| google-genai | >=1.65.0 (installed: 1.65.0) | Gemini API client for image generation | Official Google Gen AI SDK; already in use from Phase 1 preflight |
| Pillow | >=10.0.0 (installed: 12.1.1) | PNG image save/validate, dimension check | Industry standard; `part.as_image()` returns PIL Image |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pathlib | stdlib | File path handling | All path operations (templates, output, config) |
| json | stdlib | Template loading | Read JSON prompt templates |
| argparse | stdlib | CLI interface | `python -m scripts.generate_infographic` entry point |
| dataclasses | stdlib | Result types | Follow Phase 1 pattern (PreflightResult -> GenerationResult) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| gemini-2.5-flash-image | gemini-3-pro-image-preview | Better text rendering + thinking support, but higher cost ($0.134/image vs $0.039/image) and may not be in operator's API tier |
| gemini-2.5-flash-image | gemini-3.1-flash-image-preview | Thinking support + 2K default, but preview model -- less stable |

**Installation:**
```bash
# Already installed from Phase 1
pip install google-genai>=1.65.0 Pillow>=10.0.0
```

## Architecture Patterns

### Recommended Project Structure
```
scripts/
├── __init__.py             # existing
├── config.py               # existing (load_config, ConfigError)
├── preflight.py            # existing (run_preflight, PreflightResult)
└── generate_infographic.py # NEW -- core generation module
```

### Pattern 1: Pure Function with Structured Result
**What:** Follow Phase 1's pattern -- importable function returns a dataclass result, CLI wrapper calls it.
**When to use:** Always -- this is the established project pattern.
**Example:**
```python
# Source: Phase 1 pattern (scripts/preflight.py)
from dataclasses import dataclass
from pathlib import Path

@dataclass
class GenerationResult:
    """Result of an infographic generation attempt."""
    success: bool
    output_path: Path | None = None
    error_code: str | None = None
    prompt_path: Path | None = None

def generate_infographic(
    infographic_type: str,
    data_path: Path,
    output_path: Path,
    skip_preflight: bool = False,
    config_dir: Path = Path(".cdp-context"),
) -> GenerationResult:
    """Generate a single infographic PNG via Gemini API."""
    ...
```

### Pattern 2: Template-to-Prompt Serialization
**What:** Load JSON template, substitute data placeholders, flatten to natural language prompt.
**When to use:** Every generation call -- templates are the prompt source.
**Example:**
```python
# Source: Google prompt engineering guide + CONTEXT.md decisions
def serialize_template(template: dict, data: dict) -> str:
    """Flatten JSON template + data into a natural language prompt.

    Approach: Build descriptive paragraphs, not keyword lists.
    Include hex colors from extras.color_mapping.
    """
    sections = []
    # Core: subject + data-populated objects
    sections.append(f"Create a {template['core']['subject']}.")
    for obj in template["core"]["objects"]:
        # Replace {{PLACEHOLDER}} tokens with actual data
        populated = _substitute_placeholders(obj, data)
        sections.append(populated)
    # Style cues (meaningful subset)
    sections.append(f"Style: {template['style']['primary_style']}, "
                    f"{template['style']['render_quality']}.")
    # Color mapping
    colors = template.get("extras", {}).get("color_mapping", {})
    if colors:
        color_lines = [f"Use {hex_val} for {name.replace('_', ' ')}"
                       for name, hex_val in colors.items()]
        sections.append("Color coding: " + ", ".join(color_lines) + ".")
    return "\n\n".join(sections)
```

### Pattern 3: Model-Aware Thinking Config
**What:** Apply thinking_config only when the model supports it.
**When to use:** For Fault-Line Map and Mode Comparison types when model is Gemini 3+.
**Example:**
```python
# Source: Official Gemini API docs
THINKING_MODELS = {"gemini-3-pro-image-preview", "gemini-3.1-flash-image-preview"}
THINKING_TYPES = {"fault-line-map", "mode-comparison"}

def _build_config(
    infographic_type: str,
    aspect_ratio: str,
    model_id: str,
) -> types.GenerateContentConfig:
    """Build GenerateContentConfig with conditional thinking."""
    config_kwargs = {
        "response_modalities": ["TEXT", "IMAGE"],
        "image_config": types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size="2K",
        ),
    }
    # Only add thinking for supported models + complex types
    if (infographic_type in THINKING_TYPES
            and any(model_id.startswith(m.rstrip("-preview"))
                    for m in THINKING_MODELS)):
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_level="High",
        )
    return types.GenerateContentConfig(**config_kwargs)
```

### Pattern 4: Structured Status Output
**What:** Print machine-parseable status lines for CEO agent consumption.
**When to use:** Every generation -- matches Phase 1's dual-audience pattern.
**Example:**
```python
# Source: CONTEXT.md decision + Phase 1 preflight pattern
def _status(stage: str, detail: str = "") -> None:
    """Print a structured status line parseable by CEO agent."""
    if detail:
        print(f"{stage} {detail}")
    else:
        print(stage)

# Usage during generation flow:
_status("GENERATING", infographic_type)
_status("PROMPT", "assembled")
_status("IMAGE", "received")
_status("SAVED", str(output_path))
```

### Anti-Patterns to Avoid
- **Raw JSON as prompt:** Never pass the JSON template directly to Gemini -- flatten to natural language paragraphs. Models generate better images from descriptive text.
- **Hardcoded model IDs:** Use `load_config()` model_id, not a hardcoded string. Operator may use a different model.
- **Silent thinking failure:** Do NOT pass `thinking_config` to models that don't support it -- it returns HTTP 400, not a silent ignore.
- **sys.exit() in library code:** Return `GenerationResult` dataclass from the function. Only `main()` should call `sys.exit()`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Image bytes to PIL | Manual bytes/BytesIO handling | `part.as_image()` | SDK method handles MIME type detection and conversion |
| PNG validation | Custom magic byte checking | `Image.open().verify()` or size check via PIL | Pillow handles all PNG format edge cases |
| API client construction | Custom HTTP/REST calls | `genai.Client(api_key=key)` | SDK handles auth, headers, retries, serialization |
| Config loading | Re-parse config.md | `from scripts.config import load_config` | Already built in Phase 1 with error handling |
| Preflight validation | Re-check API connectivity | `from scripts.preflight import run_preflight` | Already built in Phase 1 with all 4 validation steps |

**Key insight:** The google-genai SDK provides the entire API surface needed. The only custom code is template serialization (JSON to natural language) and the orchestration glue.

## Common Pitfalls

### Pitfall 1: Thinking Config on Non-Thinking Models
**What goes wrong:** Passing `thinking_config` to `gemini-2.5-flash-image` causes HTTP 400 error.
**Why it happens:** The 2.5-flash-image model is a dedicated image model without thinking support. Only Gemini 3 image models support thinking.
**How to avoid:** Check model ID before adding thinking_config. Only apply for models in a known-supported set.
**Warning signs:** `ClientError(400)` with message about unsupported parameters.

### Pitfall 2: Lowercase 'k' in image_size
**What goes wrong:** `image_size="2k"` is rejected by the API.
**Why it happens:** The API requires uppercase K: `"2K"`, `"4K"`, `"1K"`.
**How to avoid:** Always use uppercase: `image_size="2K"`.
**Warning signs:** API error about invalid image_size value.

### Pitfall 3: Response Has No Image Parts
**What goes wrong:** Iterating `response.parts` finds only text, no image data.
**Why it happens:** Content safety filters may block image generation silently, or the prompt triggered a text-only response.
**How to avoid:** Check `response.parts` for `inline_data` presence. If no image part found, return error result with descriptive message.
**Warning signs:** `response.parts` contains only `Part(text=...)` entries.

### Pitfall 4: Large Prompt Exceeding Token Limits
**What goes wrong:** Template + data + style.md exceeds input token limit (65,536 for 2.5-flash-image).
**Why it happens:** Domain Scorecard is the most text-dense type; if data JSON is very large, the assembled prompt may be enormous.
**How to avoid:** The token limit is generous (65K input). Keep prompt focused -- don't dump raw data, summarize where appropriate.
**Warning signs:** API error about input too long.

### Pitfall 5: Output Directory Doesn't Exist
**What goes wrong:** `image.save(output_path)` fails with FileNotFoundError.
**Why it happens:** The `{session}/images/` directory may not be created yet.
**How to avoid:** `output_path.parent.mkdir(parents=True, exist_ok=True)` before save.
**Warning signs:** FileNotFoundError on save.

### Pitfall 6: Template Type Slug Mismatch
**What goes wrong:** Script can't find the template JSON because the type slug doesn't match the filename.
**Why it happens:** Template files use hyphens (`domain-scorecard.json`), but the type argument might use underscores or different casing.
**How to avoid:** Normalize the type slug: lowercase, replace underscores with hyphens, strip whitespace.
**Warning signs:** FileNotFoundError when loading template.

## Code Examples

Verified patterns from official sources:

### Complete Image Generation Call
```python
# Source: https://ai.google.dev/gemini-api/docs/image-generation
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model=model_id,
    contents=prompt_text,
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="4:3",
            image_size="2K",
        ),
    ),
)

# Extract image from response
for part in response.parts:
    if part.text is not None:
        print(part.text)  # Model may return explanatory text
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("output.png")
```

### Thinking Config for Gemini 3 Models
```python
# Source: https://ai.google.dev/gemini-api/docs/thinking
config = types.GenerateContentConfig(
    response_modalities=["TEXT", "IMAGE"],
    image_config=types.ImageConfig(
        aspect_ratio="16:9",
        image_size="2K",
    ),
    thinking_config=types.ThinkingConfig(
        thinking_level="High",  # Only "minimal" or "High" for image models
    ),
)
```

### Aspect Ratio Mapping (Per Requirements)
```python
# Source: CONTEXT.md requirements + Gemini API supported ratios
ASPECT_RATIOS: dict[str, str] = {
    "domain-scorecard":       "4:3",   # matrix/scorecard layout
    "risk-opportunity-matrix": "4:3",   # matrix layout
    "routing-diagram":        "16:9",  # diagram layout
    "fault-line-map":         "16:9",  # diagram layout
    "mode-comparison":        "16:9",  # divergence tree layout
    "action-plan-timeline":   "16:9",  # Gantt-style timeline layout
}
```

### Template Loading and Placeholder Substitution
```python
# Source: Project templates in templates/infographic-prompts/
import json
import re
from pathlib import Path

TEMPLATE_DIR = Path("templates/infographic-prompts")
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")

def load_template(infographic_type: str) -> dict:
    """Load a JSON prompt template by type slug."""
    slug = infographic_type.lower().replace("_", "-").strip()
    path = TEMPLATE_DIR / f"{slug}.json"
    if not path.exists():
        raise ConfigError(
            error_code="TEMPLATE_NOT_FOUND",
            message=f"No template found for type '{infographic_type}'",
            remediation=f"Available types: {', '.join(t.stem for t in TEMPLATE_DIR.glob('*.json'))}",
        )
    return json.loads(path.read_text())

def substitute_placeholders(text: str, data: dict) -> str:
    """Replace {{PLACEHOLDER}} tokens with data values."""
    def replacer(match):
        key = match.group(1)
        return str(data.get(key, f"[{key}]"))
    return PLACEHOLDER_RE.sub(replacer, text)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `response_modalities=["IMAGE"]` only | `["TEXT", "IMAGE"]` combined | Gemini 2.5+ (2025) | Model returns both explanatory text and image; text is useful for debugging |
| `thinking_budget` (token count) | `thinking_level` ("minimal"/"High") | Gemini 3 (2025) | Semantic levels replace numeric budgets; 2.5 still uses budget |
| `gemini-2.0-flash-exp` | `gemini-2.5-flash-image` | Nov 2025 (2.0-exp shutdown) | Project already updated in Phase 1 |
| 1K default output | 2K default on Gemini 3.1 Flash Image | Feb 2026 | Newer models default to higher res; 2.5 needs explicit `image_size="2K"` |

**Deprecated/outdated:**
- `gemini-2.0-flash-exp`: Shut down Nov 2025, replaced by `gemini-2.5-flash-image`
- `thinking_budget` on Gemini 3 models: Use `thinking_level` instead. Passing both returns 400.

## Open Questions

1. **Text rendering accuracy on Domain Scorecard**
   - What we know: This is the most text-dense infographic type. Google acknowledges "long-form text rendering" needs improvement. Flash model has ~90% accuracy; Pro has sub-10% error rate.
   - What's unclear: Whether the actual data density of a real Domain Scorecard produces legible text at 2K.
   - Recommendation: Generate with real data during implementation. If text is unreadable, this is a Phase 3 quality validation concern, not a Phase 2 blocker.

2. **Thinking mode availability for operators**
   - What we know: GEN-04 requires thinking for Fault-Line Map and Mode Comparison. The default model (`gemini-2.5-flash-image`) does NOT support thinking.
   - What's unclear: Whether operators will have access to `gemini-3-pro-image-preview` (may require different API tier/billing).
   - Recommendation: Make thinking conditional on model support. Document that operators should configure a Gemini 3 image model in config.md to enable thinking for complex types. Log a warning (not error) when thinking is requested but model doesn't support it.

3. **Optimal prompt structure for infographics**
   - What we know: Google recommends descriptive paragraphs over keyword lists. Templates have clear sections.
   - What's unclear: Whether inline data (woven into description) or a separate data section produces better results.
   - Recommendation: This is in Claude's discretion. Start with a structured approach: description paragraph first, then data section, then style cues. Iterate based on output quality.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (no config file -- uses defaults) |
| Config file | none -- pytest discovers tests/ automatically |
| Quick run command | `python -m pytest tests/test_generate_infographic.py -x` |
| Full suite command | `python -m pytest tests/ -x` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| GEN-01 | generate_content called with correct response_modalities and image_size | unit (mocked API) | `python -m pytest tests/test_generate_infographic.py::TestGeneration::test_api_call_config -x` | No -- Wave 0 |
| GEN-02 | JSON template serialized to natural language prompt with data substitution | unit | `python -m pytest tests/test_generate_infographic.py::TestPromptSerialization -x` | No -- Wave 0 |
| GEN-03 | Correct aspect ratio assigned per infographic type | unit | `python -m pytest tests/test_generate_infographic.py::TestAspectRatios -x` | No -- Wave 0 |
| GEN-04 | thinking_config applied only for supported models + complex types | unit | `python -m pytest tests/test_generate_infographic.py::TestThinkingConfig -x` | No -- Wave 0 |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/test_generate_infographic.py -x`
- **Per wave merge:** `python -m pytest tests/ -x`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_generate_infographic.py` -- covers GEN-01 through GEN-04
- [ ] Update `tests/conftest.py` -- add fixtures for mock genai client with image response, sample template data, sample data JSON
- [ ] No framework install needed (pytest already available)

## Sources

### Primary (HIGH confidence)
- [google-genai SDK v1.65.0] - Verified locally: `types.ImageConfig` fields (aspect_ratio, image_size), `types.ThinkingConfig` fields (thinking_level, thinking_budget, include_thoughts), `types.GenerateContentConfig` fields, `Part.as_image()` method
- [Gemini Image Generation Guide](https://ai.google.dev/gemini-api/docs/image-generation) - Response handling, model IDs, image_size options ("512px", "1K", "2K", "4K"), aspect ratio options, thinking config for image models
- [Gemini Thinking Docs](https://ai.google.dev/gemini-api/docs/thinking) - ThinkingConfig parameters, thinking_level values ("minimal", "High"), thinking_budget for 2.5 models
- [Gemini 2.5 Flash Image Model Card](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image) - Confirmed: thinking NOT supported, input limit 65K tokens, output limit 32K tokens
- [Vertex AI 2.5-flash-image docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash-image) - Confirmed: thinking NOT supported, supported aspect ratios: 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9

### Secondary (MEDIUM confidence)
- [Google Prompt Engineering Guide](https://developers.googleblog.com/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/) - Descriptive paragraphs > keyword lists, hyper-specificity, purpose-driven prompts
- [Gemini 3 Developer Guide](https://ai.google.dev/gemini-api/docs/gemini-3) - Thought signatures for multi-turn, thinking_level for 3.x models, pricing comparison
- [Gemini Models Overview](https://ai.google.dev/gemini-api/docs/models) - Model IDs: gemini-3-pro-image-preview, gemini-3.1-flash-image-preview, gemini-2.5-flash-image

### Tertiary (LOW confidence)
- Text rendering accuracy claims (~90% Flash, sub-10% error Pro) from third-party reviews -- needs empirical validation with actual Decision Record data

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - SDK verified locally, API patterns confirmed in official docs
- Architecture: HIGH - Follows established Phase 1 patterns, SDK API surface verified
- Pitfalls: HIGH - Thinking mode limitation confirmed across multiple official sources
- Prompt serialization: MEDIUM - Google's guidance is clear, but optimal infographic prompt structure needs empirical testing

**Research date:** 2026-03-04
**Valid until:** 2026-04-04 (stable -- SDK and model IDs are GA)
