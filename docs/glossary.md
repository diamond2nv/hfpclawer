# 术语表

[English](en/glossary.md) · **中文**

| 词 | 含义 |
|:--|:--|
| **claw vs crawler** | 名字里的 `claw` 是"精确抓取"，不是"爬"。项目自称 `hfpclawer`（HuggingFace Papers + claw + er） |
| **dev line / public line** | 两条血统：`main` 是开发线（NAS 私有），`public`/GitHub 是公开发布线。版本号对齐（同一号在两处各有一个提交） |
| **paper store** | 本地 SQLite 库：题录、标识符（arXiv/DOI/…）、验证状态 |
| **验证状态机** | `pending → verified / stale / suspect` 四态；`suspect` 会带原因，可撤销 |
| **标识符冲突** | 同一篇论文在不同源上的标识符不一致（如 DOI 解析出的 arXiv ID 与记录不符）——会被标出，需人工裁决 |
| **采集审计** | `data/download_audit.jsonl`：每行一次采集（通道、字节、毫秒、sha256），失败也记 |
| **传输阶梯** | 抓取时的通道顺序：TCP → QUIC（UDP/443）→ 浏览器取证 |
| **Range 续传** | 断点续传：落 `.part`，续传发 `Range: bytes=N-`，完成校验 sha256 后才改名 |
| **hub 扩散 / 2-hop** | 引文图上的层进扩展：默认按 hub 分截断；`--community` 用"种子 → 社区 → 社区内 hub"的两跳映射 |
| **三层画像** | 推荐用的三路信号：全局检索式 · 机器画像 · 仓库画像；融合后每行附 `why` |
| **正例池** | 本地训练信号（弱标签分层）：人工确认 / 收藏 / 扩散采纳等，用于精排训练 |
| **精排（rank）** | 可选的学习式重排（`[rank]`），用扩散审计轨迹训练，特征重要性即解释 |
| **extras** | 可选的依赖组（`quic` / `zotero` / `nlp` / `rank` …），用 `hfpclawer[extra]` 安装 |
| **状态根** | 唯一的数据根目录：检出运行时是仓库内路径，装成 wheel 后是 XDG 用户目录 |
| **MCP** | Model Context Protocol：`hfpclawer mcp` 把能力暴露给 Agent |
