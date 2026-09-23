# hfpclawer

**中文** → [中文文档](../index.md) · **English** ← you are here

**Claw papers with precision.** A local-first command-line tool that turns "find papers → fetch full
text → build a verifiable library → hand it to an agent" into four layers of machinery instead of a
pile of scripts.

```bash
uv tool install hfpclawer      # core path, 11 direct dependencies
```

You get 37 subcommands. This table is the skeleton:

| Step | Mechanism | Failure mode this layer exists for |
|:--|:--|:--|
| **Find papers** | Multi-source search: HF Papers, Papers with Code, OpenReview, arXiv API; extensible to Europe PMC, bioRxiv | A source times out and **silently returns nothing** — which looks like "no such paper exists" |
| **Fetch full text** | Transport ladder TCP → QUIC (UDP/443, survives arXiv connection resets) → browser hint; range-resumable downloads; one sha256 audit row per acquisition | Reset connections, `.part` files stuck at full size, a half-download treated as complete |
| **Build a library** | SQLite paper store + explicit verification state machine (`pending → verified / stale / suspect`) + Crossref cross-validation | Metadata that quietly disagrees with itself |
| **Feed an agent** | CLI + MCP server + published agent skills | An agent that cannot see what you already hold |

## Three use cases

1. **Daily discovery → notes.** `hfpclawer search` finds candidates, `hfpclawer store status` shows what
   you hold, `hfpclawer check-new` tells you whether anything changed (the unchanged path makes no model call).
2. **Full text on a CN link.** `hfpclawer fetch 2310.10688 -k source -t auto` — the ladder picks a working
   transport and appends a row to `data/download_audit.jsonl`, so "is this the real file?" has an answer.
3. **Zotero round-trip.** `hfpclawer zotero push` sends entries over the Connector protocol;
   `hfpclawer zotero ingest` pulls a local PDF back through the same search and de-duplication logic.

## What it does not do

- **Not a Zotero replacement**: Zotero manages reading, writing and citations; this is the
  **acquisition and verification** layer. They complement each other.
- **Not an academic search engine**: no relevance research — it aggregates sources and stores
  what it can verify.
- **Does not upload your data**: library, PDFs and audit files stay local.

## Start here

- [Install](install.md) — uv/pip, 13 optional extras, two traps
- [Usage](usage.md) — five groups of high-frequency commands, each verified
- [FAQ](faq.md) — where data lives, API keys, CN links, version discipline
- [Glossary](glossary.md) — claw vs crawler, verification states, three-layer profile

> This site documents the **published release `0.19.0`**. Code and releases live in
> [diamond2nv/hfpapers-crawler](https://github.com/diamond2nv/hfpapers-crawler); the package is on
> [PyPI](https://pypi.org/project/hfpclawer/).
