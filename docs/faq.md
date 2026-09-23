# 常见问题

[English](en/faq.md) · **中文**

## 它是什么？给谁用？

一个本地优先的学术论文命令行工具：多源检索 → 抓全文 → 建可验证的库 → 供 Agent 使用。
面向做计算研究的开发者/研究者（论文量大、需要可核对的采集与状态，而不是一个网页收藏夹）。

## 它和 Zotero 是什么关系？

**互补，不是替代。** Zotero 管阅读、写作、引文；hfpclawer 管采集与验证。两者通过
`hfpclawer zotero push` / `ingest` 往返。Zotero 适配是**可选增强**：离线推荐层不依赖它。

## 它替代 Google Scholar / 学术搜索吗？

不。它不研究相关性排序，只做**多源聚合 + 可核对的入库 + 状态机**。检索结果好不好取决于你配的源与检索式。

## 需要 API key 吗？

核心路径**不需要**：检索用公开 API（HF Papers CLI / Papers with Code / OpenReview / arXiv），
Crossref 也是公开端点。只有可选能力（`[llm]` 的 LLM 辅助命令等）才需要你自己配 key。

## 我的数据会上传吗？

不会。库（SQLite）、PDF、审计文件都在你本机（检出运行时在仓库内，装成 wheel 后在用户目录）。
唯一的对外网络访问是检索与下载本身。

## 国内网络能抓 arXiv 吗？

**TCP 可能被中途重置，但 QUIC（UDP/443）通常能通。** 装 `hfpclawer[quic]` 后，
`hfpclawer fetch … -t auto` 会按 TCP → QUIC → 浏览器取证的顺序自动降级。抓取会留审计行，
方便判断"这次是不是真的拿到文件"。

## 能离线用吗？

能，但分两层：**检索/下载**需要网络；**库操作**（`store status/search/export`、
`recommend`、`graph stats`、`ledger`、`check-new`）都是本地读写，离线可用。

## 怎么和 Agent 集成？

三种方式：① `hfpclawer mcp` 起 MCP server；② 直接让 Agent 调 CLI（CLI 输出是稳定的、可解析的）；
③ 装已发布的技能（ClawHub，owner `diamond2nv`）。

## 文档说的版本和我装的不一样怎么办？

本站以**已发布版本 `0.19.0`** 为口径。代码仓 `hfpapers-crawler` 的默认分支在两次对齐切版之间
**领先**最新发布，它的 `pyproject.toml` 版本号**不是发布标记**。所以：

```bash
hfpclawer version     # 以这个号为准；复现文档描述的行为请用已发布版本
```

## 花了多少钱？需要买什么吗？

工具本身 MIT、可离线跑；机械路径不调用模型。检索/下载会消耗**带宽、磁盘、CPU**，并且有
上游限流（arXiv / Crossref 等的公共配额）；只有你显式启用 LLM 相关能力时才会产生模型调用成本。
