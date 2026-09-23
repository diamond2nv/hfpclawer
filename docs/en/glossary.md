# Glossary

**中文** → [术语表](../glossary.md) · **English**

| Term | Meaning |
|:--|:--|
| **claw vs crawler** | `claw` means precise grasping, not creeping. The project name is `hfpclawer` (HuggingFace Papers + claw + er) |
| **dev line / public line** | Two lineages: `main` (private development) and the public line on GitHub. Version numbers are aligned — one number has one commit on each line |
| **paper store** | the local SQLite library: records, identifiers (arXiv/DOI/…), verification state |
| **verification state machine** | `pending → verified / stale / suspect`; `suspect` may carry a reason and can be cleared |
| **identifier conflict** | the same paper carrying inconsistent identifiers across sources (e.g. a DOI resolving to a different arXiv ID) — flagged, then decided by a human |
| **acquisition audit** | `data/download_audit.jsonl`: one row per acquisition (transport, bytes, ms, sha256); failures are recorded too |
| **transport ladder** | the fetch order: TCP → QUIC (UDP/443) → browser hint |
| **range resume** | `.part` files, `Range: bytes=N-` continuation, sha256 checked before the file is renamed into place |
| **hub expansion / 2-hop** | layer-by-layer expansion on the citation graph: hub-score truncation by default; `--community` uses "seed → community → community hubs" |
| **three-layer profile** | the three signal sources behind recommendations: global queries · machine profile · repo profile; every row carries `why` |
| **positive-example pool** | local training signal (layered weak labels): manual confirmation / favourites / expansion adoption … feeding the re-ranker |
| **re-ranking (rank)** | optional learned re-ranker (`[rank]`) trained on expansion audit trails; feature importance is the explanation |
| **extras** | optional dependency groups (`quic` / `zotero` / `nlp` / `rank` …), installed as `hfpclawer[extra]` |
| **state root** | the single data root: inside the checkout when you run from one, XDG user directories when installed |
| **MCP** | Model Context Protocol: `hfpclawer mcp` exposes the tool to an agent |
