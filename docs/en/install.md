# Install

**中文** → [安装](../install.md) · **English**

## Requirements

- Python **≥ 3.10**
- A writable state directory (inside the checkout when you run from one, XDG user dirs when installed from a wheel)
- Optional: network access to arXiv / Crossref / PyPI; a `[quic]` install is recommended on CN links

## Recommended: uv

```bash
uv tool install hfpclawer            # core path
uv tool install "hfpclawer[quic]"    # + UDP/443 QUIC fetching
hfpclawer version                    # what you actually have
```

`pip install hfpclawer` is equivalent for the package, but the CLI lands in the current environment;
`uv tool` gives it its own. **Start light** — every heavy dependency is opt-in.

| extra | Purpose |
|:--|:--|
| `quic` | UDP/443 QUIC fetching (arXiv TCP may be reset on CN links) |
| `zotero` | Zotero adapter (local API read + Connector write) |
| `nlp` | spaCy — entities / keywords |
| `nlp-full` | the above + wordcloud/matplotlib |
| `graph` | citation-graph extras (networkx / geopy) |
| `pdf` | PDF → Markdown conversion |
| `rank` | learned re-ranking (lightgbm / scikit-learn / onnxruntime) |
| `rank-gpu` | the above + torch |
| `llm` | LLM-assisted commands (`sniff`, …) |
| `scrapy` | anti-crawl pipeline |
| `arxiv` | optional arXiv dependencies |
| `audit` | optional audit dependencies |
| `dev` | development (ruff / pyright / pytest, …) |

## Two traps on day one

!!! warning "`uvx hfpclawer` can silently run an old version"
    `uv tool run` prefers an **already installed** tool environment, and `--refresh` does not change
    that. Use `uv tool install --force hfpclawer`, or pin explicitly: `uvx hfpclawer==0.19.0`.

!!! warning "A uv tool environment ships no `pip`"
    `…/bin/python -m pip install …` fails with `No module named pip`. That is not a malfunction — either
    ```bash
    uv tool install --force "hfpclawer[nlp]"                            # re-resolve with extras
    uv pip install --python "$(uv tool dir)/hfpclawer/bin/python" spacy # inject one package
    ```

## Initialise

```bash
hfpclawer init          # writes config.yaml + .env.template (interactive)
hfpclawer init --quick  # defaults, no interaction
hfpclawer config        # print the merged configuration
```

## Configuration: public shell + private overlay

`config.yaml` ships with the package — never put personal values in it. Machine-specific values go in
`config.local.yaml` (gitignored), deep-merged at load time.

!!! note "Lists replace, they do not merge"
    Overriding a **list** such as `stepping.layers` means moving the whole block into
    `config.local.yaml` (leave `layers: []` in the public file), otherwise the other entries are wiped.
    Nested dicts merge key by key.

## Where data lives

One state root: **the checkout when you run from one, otherwise the platform's user directories**
(data `~/.local/share/hfpclawer`, config `~/.config/hfpclawer`). `HFPCLAWER_STATE_DIR` /
`HFPCLAWER_CONFIG_DIR` override it. Nothing is ever written into `site-packages`.

| Path (under the state root) | Content |
|:--|:--|
| `data/papers.db` | the library (SQLite): records, identifiers, verification state |
| `data/download_audit.jsonl` | append-only acquisition audit (transport / bytes / ms / sha256) |
| `pdfs/`, `mds/` | fetched PDFs and converted Markdown |
| `config.yaml` / `config.local.yaml` | public config / private overlay |

## Smoke test

```bash
hfpclawer source-list                  # adapters exist at all
hfpclawer fetch 2310.10688 -k pdf      # transport ladder + one sha256 audit row
hfpclawer store status                 # store readable, migrations applied
hfpclawer check-new                    # change detection (cron entry point)
```
