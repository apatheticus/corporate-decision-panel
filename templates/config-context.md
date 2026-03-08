# CDP Configuration

> **Usage:** Copy this file to `.cdp-context/config.md` and fill in your API key.
> All other settings have defaults -- only change what you need.
>
> This file is gitignored by default (it lives in `.cdp-context/`).
>
> Get a Gemini API key at: https://aistudio.google.com/apikey

---

## Image Generation

- **Gemini API Key:** (paste your key here)
- **Image Model:** (default: gemini-2.5-flash-image)
- **Retry Limit:** (default: 2)

## Agent Logging

- **Agent Logging:** (default: off)

## Agent Models

### Tier Defaults

- **CEO:** (default: opus)
- **C-Suite:** (default: sonnet)
- **Team Leads:** (default: haiku)

### Per-Agent Overrides

> Override specific agents. Use agent filename without .md extension.
> Valid models: opus, sonnet, haiku
>
> Examples:
> - **cfo:** opus
> - **vp-sales:** haiku
> - **editor:** sonnet
