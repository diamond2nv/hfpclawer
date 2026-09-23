# Usage

**中文** → [使用](../usage.md) · **English**

Five groups of high-frequency commands. Each was verified on **0.19.0**; example outputs show the
*shape* only — the numbers depend on your own library.

## 1. Search → store

```bash
hfpclawer search                 # multi-source search → arXiv verify → classify
hfpclawer full                   # end to end: search → download → convert
hfpclawer store status           # what you hold and in which state
hfpclawer import-cmd 2310.10688  # import one paper by arXiv ID / DOI / URL
```

Enabled sources live in `search.enabled`; per-source parameters in `search.sources.<name>`
(**two namespaces** — a wrong key does not error, it silently falls back to defaults, which is the
most common configuration trap).

## 2. Full text + audit

```bash
hfpclawer fetch 2310.10688 -k pdf    -t auto   # default: pdf, auto transport
hfpclawer fetch 2310.10688 -k source -t quic   # TeX source, force QUIC
```

- `-k/--kind`: `pdf` | `source`
- `-t/--transport`: `tcp` | `quic` | `auto`

Every acquisition (success or failure) appends a row to `data/download_audit.jsonl`:

| Field | Meaning |
|:--|:--|
| `event` / `ts` | event name (`acquisition`) and time |
| `arxiv_id` / `kind` / `url` | object and origin |
| `transport` / `ok` / `error` | which channel, success, failure reason |
| `bytes` / `ms` | size and duration |
| `tls_verified` / `sha256` | link check result and the **payload hash** |

Practical rule: **fetch the same paper over another channel and compare sha256**. A mismatch means
content drift and deserves a look. (A QUIC client cannot see the peer certificate, so the check is
"link validity + payload hash", not a full certificate-chain proof.)

## 3. Library and verification state machine

```bash
hfpclawer store status                     # state distribution
hfpclawer store search "neural operator"   # keyword search
hfpclawer store export                     # export (backup / migration)
hfpclawer store verify <aid>               # verify one paper
hfpclawer store conflicts                  # cross-source identifier conflicts
hfpclawer store suspect --aid <aid> "why"  # mark suspect (clear-suspect undoes it)
```

| State | Meaning |
|:--|:--|
| `pending` | stored, not verified |
| `verified` | metadata verified (≥2 identifiers agree across sources, or human confirmation) |
| `stale` | not re-checked for a long time |
| `suspect` | known problem (conflict/error), optionally with a reason |

## 4. Citation graph and multi-hop

```bash
hfpclawer graph build                                   # build the graph
hfpclawer graph stats                                   # nodes / edges / components
hfpclawer graph ingest-citations                        # ingest citation edges
hfpclawer graph expand-hub "2310.10688,2502.05171" 3 -t 15 \
    --community --audit data/expansion_audit.jsonl      # multi-hop, with an audit trail
hfpclawer graph expand-citations 2 10                   # [max_depth] [max_seeds]
```

The two modes differ in *who enters the next frontier*: by default papers are ranked by hub score
(PageRank + degree) and truncated; `--community` uses a "seed → communities → community hubs"
two-hop mapping. `--audit` writes the trail the re-ranker trains on.

## 5. Recommendations and profile (fully local)

```bash
hfpclawer recommend --limit 10        # three signal layers, each row carries why
hfpclawer recommend --no-gate         # disable the verification gate (observation only)
hfpclawer profile                     # inspect the repo interest profile
hfpclawer pool stats                  # positive-example pool distribution
hfpclawer rank train --audit data/expansion_audit.jsonl   # re-ranker (needs [rank])
hfpclawer ledger                      # run-level accounting
hfpclawer check-new                   # store change detection (cron entry point)
```

Three layers = global queries (`search.queries`) + machine profile (`~/.hfpclawer/profile.yaml`) +
repo profile (`REPO_USER.md` at the repo root). Every row shows `why` (layer + query):
**recommendations are auditable by design**, not a black-box score.

## Zotero round-trip

```bash
hfpclawer zotero check                      # local API connectivity
hfpclawer zotero list --limit 10
hfpclawer zotero push 2310.10688 --dry-run  # preview first
hfpclawer zotero push-batch cron:coc        # batch by source
hfpclawer zotero ingest 2310.10688          # pull a PDF back into the store
```

**Reads go through the local API (`23119/api/`), writes through the Connector protocol
(`23119/connector/`)** — both need the Zotero desktop app running. For cross-machine access, use port
forwarding plus the right `Host` header and inject the address via an environment variable; do not
hard-code it.

## Agent integration

```bash
hfpclawer mcp        # start the MCP server (Hermes Agent / OpenCode, …)
```

Published agent skills live on ClawHub (owner `diamond2nv`): see
[clawhub.ai/diamond2nv](https://clawhub.ai/diamond2nv).

## Formula verification (optional)

```bash
hfpclawer verify add | run | fid | check | cross | report | stats | list
```
