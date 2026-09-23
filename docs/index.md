# hfpclawer

[English](en/index.md) · **中文**

**精确地"爪"论文。** 一个本地优先的命令行工具，把"找论文 → 抓全文 → 建可验证的库 → 交给 Agent"
这条链做成四层机器，而不是一堆脚本。

```bash
uv tool install hfpclawer      # 核心路径，11 个直接依赖
```

装上之后你会得到 37 个子命令。下面这张表是本工具的骨架：

| 环节 | 机制 | 这一层存在的理由 |
|:--|:--|:--|
| **找论文** | 多源检索：HF Papers、Papers with Code、OpenReview、arXiv API；可扩 Europe PMC、bioRxiv | 某个源超时后**静默返回 0 条**，看起来像"这题没有论文" |
| **抓全文** | 传输阶梯 TCP → QUIC（UDP/443，能穿过 arXiv 的连接重置）→ 浏览器取证；Range 续传；每次采集记一行 sha256 审计 | 连接被重置、`.part` 卡在完整大小、半成品被当成完成 |
| **建库** | SQLite paper store + 显式验证状态机（`pending → verified / stale / suspect`）+ Crossref 交叉验证 | 题录之间静默互相矛盾，而没人发现 |
| **接 Agent** | CLI + MCP server + 已发布的 Agent 技能 | Agent 不知道你手里已经有什么 |

## 三个典型用法

1. **每日发现 → 落笔记**：`hfpclawer search` 找候选，`hfpclawer store status` 看手里有什么，
   `hfpclawer check-new` 判断库有没有变化（无变化这条路径不调用模型）。
2. **国内链路取全文**：`hfpclawer fetch 2310.10688 -k source -t auto` —— 阶梯自动挑可用通道，
   并在 `data/download_audit.jsonl` 追加一行，"拿到的是不是真文件"有据可查。
3. **Zotero 往返**：`hfpclawer zotero push` 经 Connector 协议推送；`hfpclawer zotero ingest`
   把本地 PDF 拉回库里，走同一套检索与去重逻辑。

## 它不做什么

- **不替代 Zotero**：Zotero 是文献管理器（阅读、写作、引文），这里是**采集与验证**层，两者互补。
- **不替代学术搜索**：它不做相关性排名研究，只做多源聚合 + 可核对的入库。
- **不上传你的数据**：库、PDF、审计都在本地。

## 从哪开始

- [安装](install.md) —— uv/pip、13 个可选 extras、两个常见的坑
- [使用](usage.md) —— 五组高频用法，每条命令都经过核对
- [常见问题](faq.md) —— 数据在哪、要不要 API key、国内链路、版本口径
- [术语表](glossary.md) —— claw vs crawler、验证状态机、三层画像

> 本站描述**已发布版本 `0.19.0`**。代码与发布在
> [diamond2nv/hfpapers-crawler](https://github.com/diamond2nv/hfpapers-crawler)，安装包在
> [PyPI](https://pypi.org/project/hfpclawer/)。
