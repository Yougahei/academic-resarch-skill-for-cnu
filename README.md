# Academic Research Skills — 中国高校论文版

[![Version](https://img.shields.io/badge/version-v3.12.0-blue)](https://github.com/Yougahei/academic-research-skill-for-cnu/releases/tag/v3.12.0)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

本仓库是 [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) 的 fork，在原版 4 个 Skill（deep-research、academic-paper、academic-paper-reviewer、academic-pipeline）基础上，增加了**中国高校论文格式导出**能力。

> 这不是自动代写论文的工具，而是一个研究与写作协作框架。核心原则：人主导、AI 协作、过程可追溯、引用可核验。

---

## 相比原版的新增功能

- **中国高校论文格式支持** — 广西大学本科毕业论文/设计、四川大学硕士/博士学位论文的 LaTeX 和 DOCX 导出
- **DOCX 后处理管线** — 通过 `scripts/postprocess_chinese_thesis_docx.py` 自动设置字体、字号、行距、页眉页脚、页码、目录、分节分页、图表题注、公式编号、三线表
- **独立 CLI 导出** — `scripts/export_chinese_thesis.py` 一条命令将 Markdown 论文转为符合学校规范的 Word/PDF/LaTeX
- **格式审计报告** — 按学校规范逐项检查论文格式，生成结构化审查报告
- **封面模板系统** — 预置广西大学本科封面 DOCX 模板，支持字段自动填入
- **DOCX 封面模板** — `academic-paper/templates/docx/covers/guangxi_undergrad_thesis_cover.docx`
- **中文化入口** — README、快速开始、模式注册表等已全部中文化
- **Slash 命令** — 14 个 `/ars-*` 命令快速调用各 Skill 模式
- **GB/T 7714 引用方向** — 为后续中文引文格式检查提供基础

---

## 四个核心 Skill

### Deep Research（深度研究，8 种模式）— 13 Agent

| 这样说 | 触发模式 |
|---|---|
| "研究 AI 对高等教育的影响" | `full` — 完整研究 |
| "给我一份 X 的快速摘要" | `quick` — 快速简报 |
| "帮我做 X 的系统性文献回顾，含 PRISMA" | `systematic-review` — 系统综述 |
| "引导我研究 X" | `socratic` — 苏格拉底引导 |
| "帮我核查这些说法" | `fact-check` — 事实核查 |
| "帮我做文献回顾" | `lit-review` — 文献回顾 |
| "审查这篇论文的研究质量" | `review` — 论文审查 |

### Academic Paper（学术论文撰写，11 种模式）— 12 Agent

| 这样说 | 触发模式 |
|---|---|
| "帮我写一篇论文" | `full` — 完整撰写 |
| "引导我写论文" | `plan` — 引导规划 |
| "先帮我搭论文大纲" | `outline-only` — 只做大纲 |
| "我有初稿，这是审稿意见" | `revision` — 修订 |
| "帮我整理这些审稿意见成修订路线图" | `revision-coach` — 修订教练 |
| "帮我写这篇的摘要" | `abstract-only` — 摘要 |
| "把这批数据写成文献回顾论文" | `lit-review` — 文献回顾论文 |
| "转换成 LaTeX" / "引用格式转 IEEE" | `format-convert` — 格式转换 |
| "检查引用格式" | `citation-check` — 引用检查 |
| "帮我生成 AI 使用声明" | `disclosure` — AI 使用声明 |

### Academic Paper Reviewer（论文审查，6 种模式）— 7 Agent

| 这样说 | 触发模式 |
|---|---|
| "审查这篇论文" | `full` — 主编 + R1/R2/R3 + 魔鬼代言人 |
| "快速评估这篇论文" | `quick` — 快速评估 |
| "引导我改进这篇论文" | `guided` — 引导改进 |
| "检查研究方法" | `methodology-focus` — 方法论聚焦 |
| "验收修订" | `re-review` — 再审验收 |
| "用我的 gold set 校准 reviewer" | `calibration` — 校准 |

### Academic Pipeline（全流程调度器）— 5 Agent

| 这样说 | 触发阶段 |
|---|---|
| "我想做一篇完整的研究论文" | 从 Stage 1 开始完整 pipeline |
| "我已经有论文，帮我审查" | 从 Stage 2.5 进入（先做学术诚信审查） |
| "我收到审稿意见了" | 从 Stage 4 进入 |

### 上游关键功能

本 fork 继承上游全部特性，包括：

- **Experiment Provenance Intake**（#260）— Material Passport 可选 `experiment_provenance[]` 记录外部实验凭据，fail-closed 的 `experiment_intake_declaration` 在 Stage 1 明确决定
- **Socratic Reading Probe**（v3.5.1）— 由 `ARS_SOCRATIC_READING_PROBE` 环境变量控制，在 goal-oriented Socratic 会话中触发一次性阅读检查探针

---

## 安装

### 环境依赖

流水线本身不需要安装。只有**导出 PDF 或 DOCX** 时需要以下工具：

| 工具 | 用途 | macOS | Windows | Linux |
|------|------|-------|---------|-------|
| Pandoc | Markdown 转 DOCX/PDF | `brew install pandoc` | [pandoc.org](https://pandoc.org/installing.html) | `apt install pandoc` |
| LaTeX 引擎 | 生成 PDF | `brew install tectonic`（无需 sudo）<br>或 `brew install --cask basictex` | [MiKTeX](https://miktex.org/download) | `apt install texlive-xetex` |
| Python | 运行导出脚本 | 系统自带 | [python.org](https://python.org) | 系统自带 |

### Claude Code 插件安装

```text
/plugin marketplace add Yougahei/academic-research-skill-for-cnu
/plugin install academic-research-skill-for-cnu
```

### 手动克隆（macOS / Linux）

```bash
git clone https://github.com/Yougahei/academic-research-skill-for-cnu.git

mkdir -p ~/.claude/skills
ln -s $(pwd)/academic-research-skill-for-cnu/deep-research ~/.claude/skills/deep-research
ln -s $(pwd)/academic-research-skill-for-cnu/academic-paper ~/.claude/skills/academic-paper
ln -s $(pwd)/academic-research-skill-for-cnu/academic-paper-reviewer ~/.claude/skills/academic-paper-reviewer
ln -s $(pwd)/academic-research-skill-for-cnu/academic-pipeline ~/.claude/skills/academic-pipeline
```

> 如果之前安装过原版 `Imbad0202/academic-research-skills`，两个插件的 skill 名称相同会导致覆盖。建议先卸载原版再安装本 fork。

---

## 使用方式

有三种使用途径：

### 1. 完整流水线（10 阶段）

```
① 研究选题 → ② 写作 → ③ 完整性检查 → ④ 评审 → ⑤ 修改
                                         ↓
⑩ 过程总结 ← ⑨ 格式化输出 ← ⑧ 终稿完整性 ← ⑦ 再修改 ← ⑥ 复审
```

在 Claude Code 中启动流水线：

```text
/ars-full 课题：生成式人工智能对高校学生学习投入的影响研究
          目标格式：广西大学本科毕业论文（guangxi-undergrad profile）
```

### 2. Slash 命令快速调用

| 命令 | 用途 |
|------|------|
| `/ars-full` | 启动完整流水线 |
| `/ars-plan` | 论文结构规划（Socratic 引导） |
| `/ars-outline` | 仅生成论文大纲 |
| `/ars-abstract` | 生成中英文摘要 |
| `/ars-lit-review` | 文献综述 |
| `/ars-reviewer` | 多视角模拟评审 |
| `/ars-revision` | 按评审意见修改论文 |
| `/ars-revision-coach` | 解析评审意见，生成修订路线图 |
| `/ars-format-convert` | 格式转换 + 格式审计报告 |
| `/ars-citation-check` | 引用格式检查 |
| `/ars-disclosure` | AI 使用声明生成 |
| `/ars-mark-read` / `/ars-unmark-read` | 标记已读/未读里程碑 |

### 3. 独立 CLI 导出（最直接的方式）

> 这是**中国高校论文版特有**的功能，原版没有。

写好 Markdown 论文后，一条命令导出为符合学校规范的 DOCX：

```bash
# 导出广西大学本科毕业论文 DOCX
python3 scripts/export_chinese_thesis.py \
  --input thesis.md \
  --profile guangxi-undergrad \
  --format docx \
  --output thesis.docx \
  --bibliography refs.bib

# 导出 PDF（需要 LaTeX 引擎）
python3 scripts/export_chinese_thesis.py \
  --input thesis.md \
  --profile sichuan-grad \
  --format pdf \
  --output thesis.pdf

# 同时导出 DOCX + PDF + LaTeX
python3 scripts/export_chinese_thesis.py \
  --input thesis.md \
  --profile guangxi-undergrad \
  --format all \
  --output thesis.docx \
  --bibliography refs.bib

# 导出时附带格式审计报告
python3 scripts/export_chinese_thesis.py \
  --input thesis.md \
  --profile guangxi-undergrad \
  --format docx \
  --output thesis.docx \
  --report thesis_format_report.md

# 使用自定义封面模板
python3 scripts/export_chinese_thesis.py \
  --input thesis.md \
  --profile guangxi-undergrad \
  --format docx \
  --output thesis.docx \
  --cover-docx my_official_cover.docx
```

CLI 参数：

| 参数 | 说明 |
|------|------|
| `--input` | 输入 Markdown 文件 |
| `--output` | 输出文件路径 |
| `--profile` | 学校模板：`guangxi-undergrad`、`sichuan-grad`、`mainland-fallback` |
| `--format` | 输出格式：`docx` / `pdf` / `latex` / `all` |
| `--bibliography` | BibTeX 参考文献文件 |
| `--csl` | CSL 引文格式文件（如 GB/T 7714） |
| `--cover-docx` | 自定义封面 DOCX 模板 |
| `--reference-docx` | 自定义 DOCX 参考模板 |
| `--tex-template` | 自定义 LaTeX 模板 |
| `--report` | 格式审计报告输出路径 |
| `--force` | 覆盖已有输出文件 |

#### Markdown 输入格式

Markdown 文件通过 frontmatter 填写论文元数据，正文正常使用 Markdown 标题：

```markdown
---
title: 生成式人工智能对高校学生学习投入的影响研究
title-en: The Impact of Generative AI on College Students' Learning Engagement
author: 张三
student-id: 2201234567
college: 资源环境与材料学院
major: 环境工程
class: 环境工程 221 班
supervisor: 李四 教授
abstract-zh: 摘要正文...
keywords-zh: 人工智能；学习投入；高等教育
abstract-en: Abstract text...
keywords-en: artificial intelligence; learning engagement; higher education
---

# 第一章 绪论

## 1.1 研究背景

论文正文...

## 参考文献

## 致　谢
```

---

## 中国高校论文格式支持

### 已支持模板

| Profile | 学校 | 用途 | LaTeX | DOCX | 封面 |
|---------|------|------|-------|------|------|
| `guangxi-undergrad` | 广西大学 | 本科毕业论文/设计 | ✅ | ✅ | ✅ |
| `sichuan-grad` | 四川大学 | 硕士/博士学位论文 | ✅ | ✅ | ❌ |
| `mainland-fallback` | 通用 | 大陆高校通用回退 | ✅ | ✅ | ❌ |

> 需要添加新学校模板？参见 [添加学校模板指南](docs/ADD_NEW_SCHOOL_TEMPLATE.md)。

### DOCX 自动格式化项

导出 DOCX 时，后处理管线会自动处理以下格式：

| 项目 | 说明 |
|------|------|
| **字体字号** | 正文宋体/TNR 小四，标题黑体，英文 TNR |
| **行距** | 固定 20 磅 |
| **首行缩进** | 2 字符 |
| **段落对齐** | 两端对齐（正文），居中（标题） |
| **章标题** | 黑体，chapter heading 自动分页 |
| **节标题** | 1.1 / 1.1.1 层级标题，字号递减 |
| **摘要** | 中英文摘要独立页，黑体三号/32pt 居中标题 |
| **关键词** | 黑体标签 + 宋体词，缩进 2 字符，分号分隔 |
| **目录** | TOC Field 自动插入，仅显示一二级标题 |
| **页眉** | 校名 + 论文题目 |
| **页脚** | 正文阿拉伯页码（起始 1），前置部分无页码 |
| **分节分页** | 封面 → 摘要 → 目录 → 正文各章分节分页 |
| **参考文献** | 正文后、致谢前 |
| **图表题注** | 居中、黑体、五号、固定 20 磅 |
| **三线表** | 顶线、表头线、底线三条线 |
| **公式编号** | 右对齐制表位编号 |
| **封面** | DOCX 封面模板插入 + 字段自动填入 |

### 格式审计报告

使用 `--report` 参数生成格式审计报告，按学校规范逐项检查：

```bash
python3 scripts/export_chinese_thesis.py \
  --input thesis.md \
  --profile guangxi-undergrad \
  --format docx \
  --output thesis.docx \
  --report audit.md
```

审计报告包含字体、字号、行距、页边距、标题层级、摘要格式、目录结构等项目的检查结果。

---

## 论文示例

`academic-paper/examples/` 目录包含可直接参考的论文示例：

| 文件 | 内容 |
|------|------|
| `chinese_thesis_guangxi_undergrad_example.md` | 广西大学本科毕业论文完整示例 |
| `chinese_thesis_sichuan_grad_example.md` | 四川大学硕士论文完整示例 |
| `chinese_thesis_format_quickstart.md` | 中国高校论文格式导出快速开始 |
| `chinese_paper_example.md` | 中文期刊论文示例 |
| `plan_mode_guided_writing.md` | Plan 模式引导写作示例 |
| `imrad_hei_example.md` | IMRaD 结构论文示例 |

---

## 开发与测试

### 运行测试

```bash
cd academic-research-skill-for-cnu
python3 -m pip install -r requirements-dev.txt
PYTHONPATH=. pytest scripts/test_export_chinese_thesis.py -v
```

44 个测试覆盖：章节分页判断、标题层级、图表题注、公式编号、三线表、封面字段提取、Markdown 预处理、Pandoc 参数构建、DOCX 格式审计等。

### 代码结构

```
academic-research-skill-for-cnu/
├── scripts/
│   ├── export_chinese_thesis.py        # 主导出脚本（CLI + 管线入口）
│   ├── postprocess_chinese_thesis_docx.py  # DOCX 后处理（~1500 行）
│   ├── build_chinese_reference_docx.py     # 构建 DOCX 参考模板
│   └── test_export_chinese_thesis.py       # 测试（44 项）
├── academic-paper/
│   ├── templates/
│   │   ├── chinese_thesis_*_template.tex   # LaTeX 模板
│   │   ├── docx/
│   │   │   ├── covers/                     # DOCX 封面模板
│   │   │   └── *reference.docx             # DOCX 参考文件
│   │   └── ...
│   ├── examples/
│   │   ├── chinese_thesis_*.md             # 论文示例
│   │   └── thesis_refs.bib                # 参考文献示例
│   └── references/
│       ├── chinese_higher_education_thesis_format.md   # 格式规范文档
│       └── chinese_thesis_format_audit_report.md       # 审计报告规范
├── docs/
│   ├── ADD_NEW_SCHOOL_TEMPLATE.md         # 添加新学校模板指南
│   ├── UPSTREAM_CAPABILITY_AUDIT.md       # 上游能力审计
│   └── BASELINE_CHECK.md                  # 基线检查
└── commands/
    ├── ars-format-convert.md              # 格式转换 slash 命令
    └── ...                                # 其他 13 个 slash 命令
```

### 项目工作流

Issue-driven development：每个迭代从 GitHub Issue 开始，每个分支一个 issue（`codex/issue-N-<slug>`），合并到 `main` 时提交引用 issue 编号。

---

## 推荐流程

1. **`deep-research`** — 确定研究问题、范围、方法和文献基础
2. **`academic-paper`** — 生成论文结构、章节计划和初稿
3. **`academic-pipeline`** — 做引用、材料、论证一致性检查
4. **`academic-paper-reviewer`** — 模拟导师/评审视角提出修改意见
5. **`academic-paper`** — 根据意见完成修订和回应
6. **`export_chinese_thesis.py`** — 导出符合学校规范的 DOCX/PDF

---

## 许可与引用

本仓库继承原项目许可：CC BY-NC 4.0。仅限非商业学术用途。

原项目作者：Cheng-I Wu / Imbad0202 — [academic-research-skills](https://github.com/Imbad0202/academic-research-skills)

使用本仓库进行研究或教学时，请保留对原项目的引用：

```text
Wu, C.-I. (2026). Academic Research Skills for Claude Code [Computer software].
https://github.com/Imbad0202/academic-research-skills
```

---

## 相关文档

- [快速开始](QUICKSTART.md)
- [项目定位](POSITIONING.md)
- [模式注册表](MODE_REGISTRY.md)
- [安装与环境配置](docs/SETUP.md)
- [添加学校模板](docs/ADD_NEW_SCHOOL_TEMPLATE.md)
- [上游能力审计](docs/UPSTREAM_CAPABILITY_AUDIT.md)
- [基线检查](docs/BASELINE_CHECK.md)
- [架构说明](docs/ARCHITECTURE.md)
- [性能与长会话](docs/PERFORMANCE.md)
