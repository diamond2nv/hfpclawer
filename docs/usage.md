# 使用

[English](en/usage.md) · **中文**

五组高频用法。每条命令都在 **0.19.0** 上核对过；示例输出只给出**形状**，具体数字取决于你自己的库。

## 1. 检索 → 入库

```bash
hfpclawer search                 # 多源检索 → arXiv 核验 → 分类
hfpclawer full                   # 端到端：检索 → 下载 → 转换
hfpclawer store status           # 看库里有什么、处于什么状态
hfpclawer import-cmd 2310.10688  # 按 arXiv ID / DOI / URL 单篇入库
```

启用的源写在 `search.enabled`，每个源的参数在 `search.sources.<name>`（**两套命名空间**，
写错不会报错、只会静默回退到默认值——这是配置层最常见的坑）。

## 2. 全文 + 审计

```bash
hfpclawer fetch 2310.10688 -k pdf      -t auto   # 默认：pdf，自动选通道
hfpclawer fetch 2310.10688 -k source   -t quic   # TeX 源包，强制 QUIC
```

- `-k/--kind`：`pdf` | `source`
- `-t/--transport`：`tcp` | `quic` | `auto`
- 每次采集（成功或失败）都在 `data/download_audit.jsonl` 追加一行：

| 字段 | 含义 |
|:--|:--|
| `event` / `ts` | 事件名（`acquisition`）与时间 |
| `arxiv_id` / `kind` / `url` | 对象与来源 |
| `transport` / `ok` / `error` | 用了哪条通道、成败、失败原因 |
| `bytes` / `ms` | 字节数与耗时 |
| `tls_verified` / `sha256` | 链路校验结果与**载荷哈希** |

实践判据：**同一篇论文换通道再抓一次，比较 sha256**。哈希不一致 = 内容漂移，值得查看。
（QUIC 客户端拿不到对端证书，所以校验是"链路有效性 + 载荷哈希比对"，不是完整证书链证明。）

## 3. 库与验证状态机

```bash
hfpclawer store status                    # 状态分布
hfpclawer store search "neural operator"  # 关键词检索
hfpclawer store export                    # 导出（备份/迁移用）
hfpclawer store verify <aid>              # 单篇验证
hfpclawer store conflicts                 # 跨源标识符冲突
hfpclawer store suspect --aid <aid> "原因" # 标记可疑（可 clear-suspect 撤销）
```

| 状态 | 含义 |
|:--|:--|
| `pending` | 已入库，未验证 |
| `verified` | 元数据经验证（≥2 个标识符跨源一致，或人工确认） |
| `stale` | 长时间未复核 |
| `suspect` | 已知有问题（冲突/错误），可带原因 |

## 4. 引文图与多跳

```bash
hfpclawer graph build                                   # 建图
hfpclawer graph stats                                   # 节点/边/连通块
hfpclawer graph ingest-citations                        # 摄入引文关系
hfpclawer graph expand-hub "2310.10688,2502.05171" 3 -t 15 \
    --community --audit data/expansion_audit.jsonl      # 多跳扩散，带审计轨迹
hfpclawer graph expand-citations 2 10                   # [max_depth] [max_seeds]
```

两种模式的区别在"下一层带谁进前沿"：默认按 hub 分（PageRank + 度数）截断；
`--community` 用"种子 → 社区 → 社区内 hub"的两跳映射。`--audit` 写出的轨迹可供精排训练。

## 5. 推荐与画像（纯本地）

```bash
hfpclawer recommend --limit 10        # 三层信号融合，每行带 why
hfpclawer recommend --no-gate         # 关掉验证门（只用于观察）
hfpclawer profile                     # 查看仓库兴趣画像
hfpclawer pool stats                  # 正例池分布
hfpclawer rank train --audit data/expansion_audit.jsonl   # 精排（需 [rank]）
hfpclawer ledger                      # 运行级记账
hfpclawer check-new                   # 库变化检测（cron 入口）
```

三层信号 = 全局检索式（`search.queries`）+ 机器画像（`~/.hfpclawer/profile.yaml`）+
仓库画像（仓库根的 `REPO_USER.md`）。每行输出都带 `why`（来自哪层、命中哪条 query），
**推荐结果是可审计的**，而不是黑箱打分。

## Zotero 往返

```bash
hfpclawer zotero check                      # 本地 API 连通性
hfpclawer zotero list --limit 10
hfpclawer zotero push 2310.10688 --dry-run  # 先预览再推
hfpclawer zotero push-batch cron:coc        # 按来源批量推
hfpclawer zotero ingest 2310.10688          # 从 Zotero 拉回本地库
```

**读走本地 API（`23119/api/`），写走 Connector 协议（`23119/connector/`）**；两者都需要
Zotero 桌面端在运行。跨机访问用端口转发 + 正确的 `Host` 头，地址通过环境变量注入，不要写进代码。

## 接 Agent

```bash
hfpclawer mcp        # 启动 MCP server（Hermes Agent / OpenCode 等）
```

另外还有已发布的 Agent 技能（ClawHub，owner `diamond2nv`），装法见
[clawhub.ai/diamond2nv](https://clawhub.ai/diamond2nv)。

## 公式验证（可选）

```bash
hfpclawer verify add       # 登记一条公式
hfpclawer verify run       # 跑验证管线
hfpclawer verify fid       # 按 fid 查看
hfpclawer verify check     # 检查
hfpclawer verify cross     # 跨工具交叉验证
hfpclawer verify report    # 生成报告
hfpclawer verify stats     # 统计
hfpclawer verify list      # 列表
```
