# hfpclawer

**精确地"爪"论文。** 一个本地优先的命令行工具：多源检索 → 适配国内链路的全文抓取 →
可验证的本地论文库 → 供 Agent 使用的信号。

| | |
|:--|:--|
| **安装包**（装这个） | [pypi.org/project/hfpclawer](https://pypi.org/project/hfpclawer/) —— 最新 `0.19.0` |
| **代码 / 测试 / 发布** | [diamond2nv/hfpapers-crawler](https://github.com/diamond2nv/hfpapers-crawler) |
| **Agent 技能**（ClawHub） | [clawhub.ai/diamond2nv](https://clawhub.ai/diamond2nv) |
| **English** | [README.md](README.md) |

> **这个仓是什么。** `hfpclawer` 的**面向用户的门面与文档站**。实现本身在 **hfpapers-crawler**：
> 发布、tag、完整历史都在那边。这里不是源码的第二份副本。

## 安装

```bash
uv tool install hfpclawer            # 核心：11 个直接依赖
uv tool install "hfpclawer[quic]"    # 加 UDP/443 QUIC 抓取（应对 arXiv 的 TCP 被重置）
uv tool install "hfpclawer[zotero]"  # 加 Zotero 适配
uv tool install "hfpclawer[rank]"    # 加学习式精排（lightgbm）
```

**轻装起步**——重依赖（NLP、PDF、精排、Zotero、Scrapy）都是可选的，通常是用到再加。两个第一天的坑：

- **`uvx hfpclawer` 可能静默跑旧版本**：`uv tool run` 会优先复用已存在的 tool 环境；请用
  `uv tool install hfpclawer`，或显式钉版本 `uvx hfpclawer==0.19.0`。
- **uv 的 tool 环境没有 pip**：事后加包有两条路 —— 重新解析（`uv tool install --force "hfpclawer[extra]"`）
  或注入（`uv pip install --python "$(uv tool dir)/hfpclawer/bin/python" <包名>`）。

## 它做什么

| 环节 | 机制 | 这一层存在的理由 |
|:--|:--|:--|
| **找论文** | 多源检索 —— HF Papers、Papers with Code、OpenReview、arXiv API；可扩 Europe PMC、bioRxiv | 某个源超时后静默返回 0 条，看起来像"这题没有论文" |
| **抓全文** | 传输阶梯：TCP → QUIC（UDP/443，能穿过 arXiv 的 TCP 重置）→ 浏览器取证；配合 Range 续传，每次采集记一行 sha256 审计 | 连接被重置、`.part` 卡在完整大小、半成品被当成完成 |
| **建库** | SQLite paper store + 显式验证状态机（`pending → verified / stale / suspect`）+ Crossref 交叉验证 | 题录之间静默互相矛盾 |
| **接 Agent** | CLI + MCP server + 已发布的 Agent 技能 | Agent 不知道你已经有什么 |

另外还有（都按需启用）：引文图与 hub 引导的多跳扩展（`hfpclawer graph …`）、
纯本地推荐且每行带 `why`（`hfpclawer recommend`）、正例池与用审计轨迹训练的精排
（`hfpclawer pool …` / `hfpclawer rank train`）、Zotero 双向、以及运行级记账（`hfpclawer ledger`）。

## 三个典型用法

1. **每日发现 → 落笔记**：`hfpclawer search` 找候选，`hfpclawer store status` 看手里有什么，
   `hfpclawer cron` + `hfpclawer check-new` 保持更新（无变化那条路径不调模型）。
2. **国内链路取全文**：`hfpclawer fetch 2310.10688 -k source -t auto` —— 阶梯自动挑可用通道，
   并在 `data/download_audit.jsonl` 追加一行（通道、字节数、毫秒、sha256），"拿到的是不是真文件"有据可查。
3. **Zotero 往返**：`hfpclawer zotero push` 经 Connector 协议推送；`hfpclawer zotero ingest` 把本地 PDF 拉回库里。

## 版本说明

本站描述的是**已发布版本 `0.19.0`**。`hfpapers-crawler` 的默认分支在两次对齐切版之间**领先**最新发布，
其 `pyproject.toml` 的版本号**不是发布标记**：用 `hfpclawer version` 确认你手里的版本，
复现文档描述的行为请用已发布版本。

## 属于 Exo 三件套

三个独立 CLI，通过文件与命令行调用衔接，永不互相 import：

| 层 | 工具 | 安装 |
|:--|:--|:--|
| 论文 | **hfpclawer** ← 本项目 | `uv tool install hfpclawer` |
| 实验 | **expflow-pde** | `uv tool install expflow-pde` |
| 证明 | **omega-architect**（`omega`） | `uv tool install "omega-architect @ git+https://github.com/diamond2nv/omega-architect@v0.2.3"` |

## 许可

MIT，见 [LICENSE](LICENSE)。
