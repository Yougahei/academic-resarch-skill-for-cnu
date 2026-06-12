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

## 快速安装

### Claude Code 插件

```text
/plugin marketplace add Yougahei/acdemic-resarch-skill-for-CNU
/plugin install acdemic-resarch-skill-for-CNU
```

### Codex / Claude Code 共用（推荐）

```bash
skillshare install https://github.com/Yougahei/acdemic-resarch-skill-for-CNU.git --all
skillshare sync --all
```

### 手动软链接

```bash
git clone https://github.com/Yougahei/acdemic-resarch-skill-for-CNU.git ~/acdemic-resarch-skill-for-CNU

mkdir -p .claude/skills
ln -s ~/acdemic-resarch-skill-for-CNU/deep-research .claude/skills/deep-research
ln -s ~/acdemic-resarch-skill-for-CNU/academic-paper .claude/skills/academic-paper
ln -s ~/acdemic-resarch-skill-for-CNU/academic-paper-reviewer .claude/skills/academic-paper-reviewer
ln -s ~/acdemic-resarch-skill-for-CNU/academic-pipeline .claude/skills/academic-pipeline
```

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
