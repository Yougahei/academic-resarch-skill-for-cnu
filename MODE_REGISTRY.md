# 模式注册表

本文件是四个 skills 的模式索引。内部模式名保持英文，以便继续兼容原版逻辑、测试和上游合并；说明改为中文，方便中国高校论文场景使用。

## deep-research

| Mode | 用途 | 典型触发 |
|---|---|---|
| `full` | 完整研究报告 | 深度研究某主题、做学术分析 |
| `quick` | 快速研究简报 | 快速了解某主题、30 分钟综述 |
| `review` | 研究质量评阅 | 评估一篇论文或资料 |
| `lit-review` | 文献综述 | 做文献回顾、整理研究脉络 |
| `fact-check` | 事实核查 | 核验主张、数据、引用 |
| `socratic` | 苏格拉底式选题辅导 | 研究方向不清楚、需要引导 |
| `systematic-review` | 系统综述 | PRISMA、系统性回顾、Meta 分析 |

## academic-paper

| Mode | 用途 | 典型触发 |
|---|---|---|
| `full` | 完整论文草拟 | 写论文、写研究论文 |
| `plan` | 论文结构规划 | 引导我写论文、帮我规划章节 |
| `outline-only` | 只生成大纲 | 论文大纲、章节安排 |
| `revision` | 根据意见修改 | 导师意见、评审意见、返修 |
| `revision-coach` | 修订路线规划 | 拆解审稿意见、生成回应框架 |
| `abstract-only` | 摘要与关键词 | 中文摘要、英文摘要、中英双语摘要 |
| `lit-review` | 文献综述型论文 | 写文献综述论文 |
| `format-convert` | 格式转换 | 转 LaTeX、转 DOCX、改引用格式、中国高校论文格式审查/高校论文模板输出 |
| `citation-check` | 引用检查 | 检查参考文献、核验引用、GB/T 7714 论文引用检查 |
| `disclosure` | AI 使用声明 | 生成 AI 辅助写作声明 |

## academic-paper-reviewer

| Mode | 用途 | 典型触发 |
|---|---|---|
| `full` | 完整多视角评审 | 评审论文、盲审前检查 |
| `re-review` | 修改后复审 | 检查修改是否回应意见 |
| `quick` | 快速质量评估 | 快速看一下问题 |
| `methodology-focus` | 方法专项评审 | 只看方法、统计、研究设计 |
| `guided` | 引导式改进 | 带我逐项改论文 |
| `calibration` | 评审器校准 | 用金标准样本测评审准确性 |

## academic-pipeline

| Mode | 用途 | 典型触发 |
|---|---|---|
| pipeline | 研究到终稿的完整流程 | 从选题到终稿、完整论文流程 |
| `resume_from_passport=<hash>` | 从材料护照恢复流程 | 跨会话继续上次论文流程 |

## 中国高校推荐流程

1. `deep-research/socratic`：明确题目、研究对象、变量和方法。
2. `deep-research/lit-review`：形成文献矩阵和研究空白。
3. `academic-paper/plan`：确定论文结构和章节任务。
4. `academic-paper/full`：生成可审阅初稿。
5. `academic-paper-reviewer/full`：模拟导师/评审意见。
6. `academic-paper/revision`：根据意见修改。
7. `academic-pipeline`：做终稿前一致性、引用和完整性检查。
