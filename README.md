# acdemic-resarch-skill-for-CNU

面向中国高校论文场景的 Academic Research Skills 二次开发版。

本仓库 fork 自 [`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills)，保留原版的核心技能、agent、协议、测试与质量门禁，主要把入口文档、安装说明、使用教程和插件描述改为中文，并把应用场景调整为中国高校论文服务。

> 说明：仓库名按当前二开目标保留为 `acdemic-resarch-skill-for-CNU`。如果后续要对外发布，也可以再建立拼写更正的别名仓库。

## 项目定位

`acdemic-resarch-skill-for-CNU` 不是自动代写论文的工具，而是一个研究与写作协作框架。它适合服务中国高校常见论文流程：

- 本科毕业论文、课程论文、学年论文、创新训练项目论文
- 硕士/博士论文的开题、文献综述、章节草拟、修改与答辩前检查
- 中文论文与中英双语摘要写作
- 参考文献、引用一致性、格式规范和学术诚信检查
- 导师反馈、评审意见、盲审意见的拆解与修订路线规划

核心原则是“人主导、AI 协作”。研究问题、材料取舍、方法判断、结论解释和最终署名责任必须由研究者自己承担。

## 包含的四个 skills

| Skill | 用途 |
|---|---|
| `deep-research` | 研究选题、研究问题澄清、文献检索、证据综述、事实核查、系统综述 |
| `academic-paper` | 论文结构规划、正文草拟、文献综述、摘要、修改、格式转换、引用检查 |
| `academic-paper-reviewer` | 模拟多视角论文评审，给出编辑决定、问题清单和修改路线 |
| `academic-pipeline` | 串联“研究 → 写作 → 完整性检查 → 评审 → 修改 → 终稿”的完整流程 |

## 快速安装

### Claude Code 插件方式

如果你准备通过 Claude Code plugin 安装本 fork：

```text
/plugin marketplace add Yougahei/acdemic-resarch-skill-for-CNU
/plugin install acdemic-resarch-skill-for-CNU
```

### Codex / Claude Code 共用方式

本机推荐用 `skillshare` 作为中心源，方便 Codex 和 Claude Code 共用并继续二开：

```bash
skillshare install https://github.com/Yougahei/acdemic-resarch-skill-for-CNU.git --all
skillshare sync --all
```

同步后，中心开发目录通常在：

```text
~/.config/skillshare/skills/
```

Codex 和 Claude Code 会通过软链接读取同一份 skill 内容。

## 快速开始

进入你的论文项目目录后，打开 Claude Code 或 Codex，然后直接描述任务：

```text
我需要写一篇本科毕业论文，题目方向是人工智能对大学生学习投入的影响，请先帮我梳理研究问题和论文结构。
```

```text
我已经有论文初稿，请按中国高校毕业论文要求帮我检查结构、引用、摘要、格式和学术表达问题。
```

```text
我收到了导师修改意见，请帮我拆成可执行的修订清单，并生成逐条回应草稿。
```

## 中国高校论文适配方向

当前版本主要完成了“入口文档中文化 + 项目定位调整”。后续二开建议优先补强这些方向：

- 中国高校本科/研究生论文模板适配
- GB/T 7714 参考文献格式与学校格式差异处理
- 开题报告、任务书、中期检查、答辩稿等中国高校过程材料
- 学院/学校自定义 Word 模板解析与格式检查
- 中文学术写作表达、术语统一、摘要与关键词规范
- 学术诚信、AI 使用声明和学校政策对齐

## 与原版保持一致的部分

为了方便以后从上游合并更新，本 fork 暂时保留以下内容的原始结构：

- agents 定义
- shared 协议与 schema
- scripts 与测试
- evals、fixtures、设计记录
- 内部英文模式名和环境变量

这意味着核心运行逻辑尽量不偏离原版，中文化主要集中在用户入口、安装教程和项目描述。

## 文档入口

- [快速开始](QUICKSTART.md)
- [安装与环境配置](docs/SETUP.md)
- [项目定位](POSITIONING.md)
- [贡献说明](CONTRIBUTING.md)
- [安全策略](SECURITY.md)
- [原作者声明与许可说明](NOTICE.md)

## 许可

本 fork 继承原项目许可：CC BY-NC 4.0。仅限非商业学术用途。使用、修改和分发时请保留原作者署名与许可信息。

原项目作者：Cheng-I Wu / Imbad0202
本 fork 维护方向：中国高校论文服务与中文高校写作流程适配。
