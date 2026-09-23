# FAQ

**中文** → [常见问题](../faq.md) · **English**

## What is it, and who is it for?

A local-first command-line tool for academic literature: multi-source search → full-text fetching →
a verifiable library → something an agent can use. It targets developers and researchers with large
reading volume who need auditable acquisition and state, not another bookmark page.

## How does it relate to Zotero?

**Complementary, not a replacement.** Zotero handles reading, writing and citations; hfpclawer handles
acquisition and verification, and the two round-trip via `hfpclawer zotero push` / `ingest`. The Zotero
adapter is an optional enhancement — the offline recommendation layer never depends on it.

## Does it replace academic search engines?

No. It does not research relevance ranking; it aggregates sources and stores what it can verify. How
good the results are depends on the sources and queries you configure.

## Do I need an API key?

Not for the core path: search uses public APIs (HF Papers CLI / Papers with Code / OpenReview / arXiv)
and Crossref is a public endpoint too. Only optional capabilities (LLM-assisted commands behind
`[llm]`) need a key you provide.

## Is my data uploaded?

No. The library (SQLite), PDFs and audit files stay on your machine (inside the checkout when you run
from one, in user directories when installed from a wheel). The only outbound traffic is search and
download itself.

## Can it fetch from arXiv on a CN network?

**TCP may be reset mid-flight, while QUIC (UDP/443) usually gets through.** With `hfpclawer[quic]`,
`hfpclawer fetch … -t auto` walks TCP → QUIC → browser hint automatically, and every acquisition leaves
an audit row so you can tell whether you really got the file.

## Does it work offline?

Partly: **search/download** need network; **library operations** (`store status/search/export`,
`recommend`, `graph stats`, `ledger`, `check-new`) are local reads and writes and work offline.

## How do I integrate it with an agent?

Three ways: ① `hfpclawer mcp` starts an MCP server; ② let the agent call the CLI directly (its output
is stable and parseable); ③ install the published skills (ClawHub, owner `diamond2nv`).

## The docs describe a version other than the one I have?

This site documents the **published release `0.19.0`**. The `hfpapers-crawler` default branch tracks
ahead of the latest release between aligned cuts and its `pyproject.toml` version is **not** a release
marker, so:

```bash
hfpclawer version     # trust this number; use the released version to reproduce documented behaviour
```

## What does it cost?

The tool is MIT-licensed and runs offline; the mechanical paths make no model calls. Search and
download consume **bandwidth, disk and CPU**, and are subject to upstream rate limits (arXiv,
Crossref, …). Model-call cost appears only when you explicitly enable the LLM-backed capabilities.
