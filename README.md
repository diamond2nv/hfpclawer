# hfpclawer

[![Docs](https://img.shields.io/badge/docs-diamond2nv.github.io%2Fhfpclawer-blue)](https://diamond2nv.github.io/hfpclawer/)
[![PyPI](https://img.shields.io/pypi/v/hfpclawer)](https://pypi.org/project/hfpclawer/)
[![License](https://img.shields.io/github/license/diamond2nv/hfpapers-crawler)](https://github.com/diamond2nv/hfpapers-crawler/blob/master/LICENSE)

**Claw papers with precision.** A local-first command-line tool for academic literature:
multi-source search → CN-aware full-text fetching → a verifiable local paper store →
signals an agent can use.

| | |
|:--|:--|
| **Package** (install this) | [pypi.org/project/hfpclawer](https://pypi.org/project/hfpclawer/) — latest `0.19.0` |
| **Code, tests, releases** | [diamond2nv/hfpapers-crawler](https://github.com/diamond2nv/hfpapers-crawler) |
| **Agent skills** (ClawHub) | [clawhub.ai/diamond2nv](https://clawhub.ai/diamond2nv) |
| **中文说明** | [README.zh-CN.md](README.zh-CN.md) |

> **What this repository is.** The user-facing landing page and documentation site for `hfpclawer`.
> The implementation itself lives in **hfpapers-crawler** — releases, tags and the full history are
> there. Nothing here is a second copy of the source.

## Install

```bash
uv tool install hfpclawer            # core: 11 direct dependencies
uv tool install "hfpclawer[quic]"    # + UDP/443 QUIC fetching, for networks that reset arXiv TCP
uv tool install "hfpclawer[zotero]"  # + Zotero adapter
uv tool install "hfpclawer[rank]"    # + learned re-ranking (lightgbm)
```

Start light — the heavier pieces (NLP, PDF, ranking, Zotero, Scrapy) are opt-in and normally added
once you know you need them. Two traps worth knowing on day one:

- **`uvx hfpclawer` can silently run an old version.** `uv tool run` prefers an already-installed
  tool environment; use `uv tool install hfpclawer` (or pin: `uvx hfpclawer==0.19.0`).
- **A uv tool environment ships no `pip`.** To add a package later, either re-resolve with extras
  (`uv tool install --force "hfpclawer[extra]"`) or inject it
  (`uv pip install --python "$(uv tool dir)/hfpclawer/bin/python" <pkg>`).

## What it does

| Step | Mechanism | Failure mode this layer exists for |
|:--|:--|:--|
| **Find papers** | Multi-source search — HF Papers, Papers with Code, OpenReview, arXiv API; extensible to Europe PMC and bioRxiv | A source times out and silently returns nothing, which looks like "no such paper exists" |
| **Fetch full text** | A transport ladder: TCP → QUIC (UDP/443, survives the arXiv TCP reset) → browser hint, plus range-resumable downloads with a sha256 audit row per acquisition | Reset connections, `.part` files stuck at full size, a half-download treated as complete |
| **Build a library** | SQLite paper store with an explicit verification state machine (`pending → verified / stale / suspect`) and Crossref cross-validation | Metadata that quietly disagrees with itself |
| **Feed an agent** | CLI + MCP server + published agent skills | An agent that cannot see what you already have |

Also included, each opt-in: a citation-graph layer with hub-guided multi-hop expansion
(`hfpclawer graph …`), local-only recommendations with a per-row `why` (`hfpclawer recommend`),
a positive-example pool and a learned re-ranker trained on expansion audit trails
(`hfpclawer pool …`, `hfpclawer rank train`), Zotero round-tripping, and run-level accounting
(`hfpclawer ledger`).

## Three use cases

1. **Daily discovery → notes.** `hfpclawer search` finds candidates, `hfpclawer store status` shows
   what you already hold, `hfpclawer cron` + `hfpclawer check-new` keep it current with a
   deterministic change check (no model call on the unchanged path).
2. **Full text on a CN link.** `hfpclawer fetch 2310.10688 --kind source --transport auto` — the
   ladder picks a working transport and appends a `data/download_audit.jsonl` row
   (transport, bytes, ms, sha256) so "did I get the real file?" has an answer.
3. **Zotero round-trip.** `hfpclawer zotero push` sends store entries to Zotero over the Connector
   protocol; `hfpclawer zotero ingest` pulls a local PDF back into the store.

## Version note

These docs describe the **published release, `0.19.0`**. The `hfpapers-crawler` default branch
tracks ahead of the latest release between aligned cuts, so its `pyproject.toml` version is not a
release marker: run `hfpclawer version` to see what you actually have, and reproduce documented
behaviour with the released version.

## Part of the Exo suite

Three independent CLIs that meet through files and CLI calls, never through imports:

| Layer | Tool | Install |
|:--|:--|:--|
| Literature | **hfpclawer** ← this project | `uv tool install hfpclawer` |
| Experiments | **expflow-pde** | `uv tool install expflow-pde` |
| Proofs | **omega-architect** (`omega`) | `uv tool install "omega-architect @ git+https://github.com/diamond2nv/omega-architect@v0.2.3"` |

## License

MIT. See [LICENSE](LICENSE).
