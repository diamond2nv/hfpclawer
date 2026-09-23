# 安装

[English](en/install.md) · **中文**

## 要求

- Python **≥ 3.10**
- 一个可写的状态目录（检出运行时用仓库内的 `data/`，装成 wheel 后用 XDG 目录，见下）
- 可选：网络能访问 arXiv / Crossref / PyPI；国内链路建议装 `[quic]`

## 推荐方式：uv

```bash
uv tool install hfpclawer            # 核心路径
uv tool install "hfpclawer[quic]"    # + UDP/443 QUIC 抓取
hfpclawer version                    # 确认手里的版本
```

`pip install hfpclawer` 等价，但 CLI 会装进当前环境；`uv tool` 把它放进独立环境，更干净。

**轻装起步**：重依赖都是可选的，用到再加。

| extra | 用途 |
|:--|:--|
| `quic` | UDP/443 QUIC 抓取（arXiv 的 TCP 在国内链路可能被重置） |
| `zotero` | Zotero 适配（本地 API 读 + Connector 写） |
| `nlp` | spaCy，实体/关键词处理 |
| `nlp-full` | 上面的 + wordcloud/matplotlib（可视化） |
| `graph` | 引文图相关增强（networkx / geopy） |
| `pdf` | PDF → Markdown 转换 |
| `rank` | 学习式精排（lightgbm / scikit-learn / onnxruntime） |
| `rank-gpu` | 上面的 + torch |
| `llm` | LLM 辅助命令（`sniff` 等） |
| `scrapy` | 反爬抓取管线 |
| `arxiv` | arXiv 相关可选依赖 |
| `audit` | 审计相关可选依赖 |
| `dev` | 开发用（ruff / pyright / pytest 等） |

## 两个第一天的坑

!!! warning "`uvx hfpclawer` 可能静默跑旧版本"
    `uv tool run` 会优先复用**已存在**的 tool 环境。如果你之前装过旧版，`uvx hfpclawer` 会继续用那个，
    而 `--refresh` 不会改变这一点。需要版本确定就用 `uv tool install --force hfpclawer`，
    或者显式钉住：`uvx hfpclawer==0.19.0`。

!!! warning "uv 的 tool 环境里没有 `pip`"
    `…/bin/python -m pip install …` 会报 `No module named pip`。这不是故障，两条路：
    ```bash
    uv tool install --force "hfpclawer[nlp]"                            # 重新解析，带 extras
    uv pip install --python "$(uv tool dir)/hfpclawer/bin/python" spacy # 往该环境里注入一个包
    ```

## 初始化

```bash
hfpclawer init          # 生成 config.yaml + .env.template（交互）
hfpclawer init --quick  # 用默认值，不交互
hfpclawer config        # 打印合并后的最终配置
```

## 配置：公开壳 + 私有覆盖

`config.yaml` 是随包发布的公开文件，**不要**往里写个人内容。机器相关的值放
`config.local.yaml`（已被 .gitignore），启动时深度合并：

```bash
hfpclawer config   # 输出里会出现 "Applied local config overlay" 提示
```

!!! note "list 是整体替换，不是逐项合并"
    覆盖 `stepping.layers` 这类**列表**时，必须把整块搬进 `config.local.yaml`
    （公开文件里留 `layers: []`），否则其余项会被清空。嵌套 dict 才是逐键合并。

## 数据放哪

状态只有一个根：**检出运行时用仓库内路径；装成 wheel 后用系统的用户目录**
（数据 `~/.local/share/hfpclawer`，配置 `~/.config/hfpclawer`）。
`HFPCLAWER_STATE_DIR` / `HFPCLAWER_CONFIG_DIR` 可整体覆盖。**不会**往 `site-packages` 里写任何东西。

| 路径（状态根下） | 内容 |
|:--|:--|
| `data/papers.db` | 论文库（SQLite）：题录、标识符、验证状态 |
| `data/download_audit.jsonl` | 追加式的采集审计（通道 / 字节 / 毫秒 / sha256） |
| `pdfs/`、`mds/` | 抓到的 PDF 与转换出的 Markdown |
| `config.yaml` / `config.local.yaml` | 公开配置 / 私有覆盖 |

## 冒烟测试

```bash
hfpclawer source-list                  # 源适配器在不在
hfpclawer fetch 2310.10688 -k pdf      # 传输阶梯 + 一行 sha256 审计
hfpclawer store status                 # 库可读、迁移已应用
hfpclawer check-new                    # 变化检测（cron 入口）
```
