# acdemic-resarch-skill-for-CNU

[![Version](https://img.shields.io/badge/version-v3.12.0-blue)](https://github.com/Yougahei/acdemic-resarch-skill-for-CNU)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

面向中国高校论文场景的 Academic Research Skills，在原作者 [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) 的基础上增加了中国高校论文格式支持。

> 这不是自动代写论文的工具，而是一个研究与写作协作框架。核心原则：人主导、AI 协作、过程可追溯、引用可核验。

## 包含的四个 Skills

| Skill | 用途 | Agent 数 |
|---|---|---|
| `deep-research` | 研究选题、文献检索、证据综述、系统综述 | 13 |
| `academic-paper` | 论文结构规划、正文草拟、文献综述、修改、格式转换、引用检查 | 12 |
| `academic-paper-reviewer` | 多视角模拟评审（主编 + 3 位同行 + 反方） | 7 |
| `academic-pipeline` | 全流程编排：研究 → 写作 → 完整性检查 → 评审 → 修改 → 终稿 | 5 |

## 相比原版的新增功能

- **中国高校论文格式支持**：广西大学本科毕业论文/设计、四川大学硕士/博士学位论文的完整 LaTeX 模板和 DOCX 输出
- **格式审计报告**：按学校规范逐项检查论文格式，生成结构化审查报告
- **中文化入口**：README、快速开始、模式注册表等文档已全部中文化
- **DOCX 导出**：通过 Pandoc 将 Markdown 论文转为符合学校规范的 Word 文档
- **GB/T 7714 引用方向**：为后续引用检查和格式转换提供基础

## 完整流水线：十个阶段

从研究选题到终稿输出，流水线包含十个阶段。每个阶段由专门的 Agent 团队负责，阶段之间设有用户确认点，可选择全流程运行或单独使用某一环节。

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ ① 研究   │ → │ ② 写作   │ → │ ③ 完整性 │ → │ ④ 评审   │ → │ ⑤ 修改   │
│ 选题开题 │    │ 草拟正文 │    │ 引用检查 │    │ 模拟审稿 │    │ 逐条回应 │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                                    │
                                              ┌─────────────────────┘
                                              ↓
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ ⑩ 过程   │ ← │ ⑨ 格式   │ ← │ ⑧ 终稿   │ ← │ ⑦ 再修改 │ ← │ ⑥ 复审   │
│ 总结归档 │    │ 化输出   │    │ 完整性   │    │ (如需要) │    │ 修改验收 │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### 各阶段说明

| 阶段 | 说明 | 负责 Skill / Agent | 产出 |
|------|------|-------------------|------|
| **① 研究** | 澄清研究问题，检索文献，设计方法论 | deep-research（13 Agent） | 研究问题简报、文献目录、方法论蓝图 |
| **② 写作** | 规划论文结构，草拟正文 | academic-paper（12 Agent） | 论文初稿 |
| **③ 完整性检查** | 核验引用真实性、数据准确性、论证一致性 | integrity_verification_agent | 检查报告及修正后的论文 |
| **④ 评审** | 模拟主编 + 三位同行 + 反方共五视角评审 | academic-paper-reviewer（7 Agent） | 评审报告、编辑决定、修改路线图 |
| **⑤ 修改** | 按评审意见逐条修订并回应 | academic-paper | 修改稿、逐条回应函 |
| **⑥ 复审** | 检验修改是否回应了评审意见 | academic-paper-reviewer | 复审报告 |
| **⑦ 再修改** | 针对复审中的遗留问题做最终修改 | academic-paper | 二修稿 |
| **⑧ 终稿完整性** | 重新从头验证所有引用和数据 | integrity_verification_agent | 终审报告（必须零问题通过） |
| **⑨ 格式化输出** | 按目标格式输出终稿，支持中国高校论文模板 | academic-paper | LaTeX / PDF / DOCX |
| **⑩ 过程总结** | 生成论文创作过程记录及 AI 自省报告 | pipeline_orchestrator | 过程记录文档 |

### 强制确认点

每个阶段完成后需要用户确认才能继续。其中以下三个为强制确认点，不可自动跳过：

| 确认点 | 阶段 | 阻断条件 |
|------|------|---------|
| 投稿前完整性检查 | 阶段 ③ | 引用不实、数据错误、论证缺陷 |
| 终稿完整性检查 | 阶段 ⑧ | 从头独立验证，存在任何未解决问题 |
| 格式化前确认 | 阶段 ⑨ | 用户确认目标格式及学校模板选择 |

### 中途进入

不需要每次都从阶段 ① 开始。系统会根据已有材料自动判断入口：

- **仅有选题方向** → 从 ① 开始
- **已有论文初稿** → 从 ③ 开始，先做完整性检查
- **已收到导师或评审意见** → 从 ⑤ 开始
- **仅需审读论文** → 单独调用 ④

### 流水线 vs 单独 Skill

| 场景 | 使用方式 |
|------|---------|
| 从选题到终稿全流程 | `academic-pipeline` |
| 仅需文献检索或综述 | `deep-research` |
| 仅需起草论文正文 | `academic-paper` |
| 仅需评审论文 | `academic-paper-reviewer` |
| 仅需格式转换 | `academic-paper` 的 `format-convert` 模式 |

流水线是可选的 —— 如果只需要某一个功能，直接调用对应的 skill 即可。

## 快速安装

> ⚠️ 如果你之前安装过原版 `Imbad0202/academic-research-skills`，两个插件的 skill 名称相同（`deep-research`、`academic-paper` 等），会导致覆盖。建议先卸载原版再安装本 fork，或者用手动软链接方式分别指向不同目录。

### 环境依赖

流水线本身不需要安装任何东西。只有当你需要**导出 PDF 或 DOCX** 时才需要以下工具：

| 工具 | 用途 | macOS | Windows | Linux |
|------|------|-------|---------|-------|
| Pandoc | Markdown 转 DOCX/PDF | `brew install pandoc` | [pandoc.org](https://pandoc.org/installing.html) 下载安装器 | `apt install pandoc` |
| LaTeX 引擎 | 生成 PDF | `brew install tectonic`（无需 sudo）<br>或 `brew install --cask basictex`（完整版） | 安装 [MiKTeX](https://miktex.org/download) 或 [TeX Live](https://tug.org/texlive/) | `apt install texlive-xetex` |

Windows 用户注意：系统自带宋体、黑体、楷体、隶书，无需额外安装中文字体。macOS 和 Linux 用户若缺少字体，LaTeX 会自动回退到系统可用字体。

### Claude Code 插件

```text
/plugin marketplace add Yougahei/acdemic-resarch-skill-for-CNU
/plugin install acdemic-resarch-skill-for-CNU
```

### 手动克隆（macOS / Linux）

```bash
git clone https://github.com/Yougahei/acdemic-resarch-skill-for-CNU.git ~/acdemic-resarch-skill-for-CNU

mkdir -p .claude/skills
ln -s ~/acdemic-resarch-skill-for-CNU/deep-research .claude/skills/deep-research
ln -s ~/acdemic-resarch-skill-for-CNU/academic-paper .claude/skills/academic-paper
ln -s ~/acdemic-resarch-skill-for-CNU/academic-paper-reviewer .claude/skills/academic-paper-reviewer
ln -s ~/acdemic-resarch-skill-for-CNU/academic-pipeline .claude/skills/academic-pipeline
```

Windows 用户推荐使用上方的 Claude Code 插件或 skillshare 方式安装，无需手动处理软链接。

## 快速开始

进入你的论文项目目录，启动 Claude Code 或 Codex，描述任务：

```text
# 选题与开题
我准备写一篇本科毕业论文，方向是人工智能对大学生学习投入的影响，
请用追问的方式帮我收敛研究问题。

# 文献综述
请围绕"生成式 AI 对高校学生学习成效的影响"做一份文献综述。

# 论文写作
请帮我规划一篇中国高校本科毕业论文的结构。

# 格式转换（中国高校论文格式）
请按广西大学本科毕业论文格式输出这篇论文。

# 初稿审阅
我已经有论文初稿，请帮我从结构、论证、方法、引用、格式、
中文学术表达六个方面审阅。

# 修改导师意见
我收到了导师修改意见，请拆成修订清单，标出优先级。
```

## 选择哪个 Skill

| 你的目标 | 建议使用 |
|---|---|
| 选题、研究问题、文献检索、证据综述 | `deep-research` |
| 写论文、写摘要、写文献综述、改初稿、格式转换 | `academic-paper` |
| 模拟审稿、盲审前检查、导师视角评阅 | `academic-paper-reviewer` |
| 从选题一路做到终稿 | `academic-pipeline` |

## 中国高校论文格式支持

### 已支持的学校模板

| 模板 | 用途 | 格式 |
|---|---|---|
| `guangxi-undergrad` | 广西大学本科毕业论文/设计 | LaTeX + DOCX |
| `sichuan-grad` | 四川大学硕士/博士学位论文 | LaTeX + DOCX |
| `mainland-fallback` | 大陆高校通用回退模板 | LaTeX + DOCX |

> 需要添加新学校模板？参见 [添加学校模板指南](docs/ADD_NEW_SCHOOL_TEMPLATE.md)，包含文件命名规范、目录结构和完整操作流程。

### 格式规范来源

广西大学模板严格对照资源环境与材料学院的格式规范文件和参考模板设计。四川大学模板严格对照学校学位论文格式文件设计。学校/学院/导师的具体要求优先级最高，遇到冲突时以用户提供的正式文件为准。

## 推荐流程

1. `deep-research` — 确定研究问题、范围、方法和文献基础
2. `academic-paper` — 生成论文结构、章节计划和初稿
3. `academic-pipeline` — 做引用、材料、论证一致性检查
4. `academic-paper-reviewer` — 模拟导师/评审视角提出修改意见
5. `academic-paper` — 根据意见完成修订和回应

## 许可与引用

本仓库继承原项目许可：CC BY-NC 4.0。仅限非商业学术用途。

原项目作者：Cheng-I Wu / Imbad0202 — [academic-research-skills](https://github.com/Imbad0202/academic-research-skills)

使用本仓库进行研究或教学时，请保留对原项目的引用：

```text
Wu, C.-I. (2026). Academic Research Skills for Claude Code [Computer software].
https://github.com/Imbad0202/academic-research-skills
```

## 相关文档

- [快速开始](QUICKSTART.md)
- [项目定位](POSITIONING.md)
- [模式注册表](MODE_REGISTRY.md)
- [安装与环境配置](docs/SETUP.md)
- [上游能力审计](docs/UPSTREAM_CAPABILITY_AUDIT.md)
- [基线检查](docs/BASELINE_CHECK.md)
