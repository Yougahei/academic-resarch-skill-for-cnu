# 快速开始

这份指南帮助你用 `acdemic-resarch-skill-for-CNU` 开始一次中国高校论文协作流程。

## 1. 安装

### 推荐：Codex 与 Claude Code 共用

```bash
skillshare install https://github.com/Yougahei/acdemic-resarch-skill-for-CNU.git --all
skillshare sync --all
```

安装后重启 Codex / Claude Code。

### Claude Code 插件方式

```text
/plugin marketplace add Yougahei/acdemic-resarch-skill-for-CNU
/plugin install acdemic-resarch-skill-for-CNU
```

### 手动软链接方式

```bash
git clone https://github.com/Yougahei/acdemic-resarch-skill-for-CNU.git ~/acdemic-resarch-skill-for-CNU

cd /path/to/your/project
mkdir -p .claude/skills
ln -s ~/acdemic-resarch-skill-for-CNU/deep-research .claude/skills/deep-research
ln -s ~/acdemic-resarch-skill-for-CNU/academic-paper .claude/skills/academic-paper
ln -s ~/acdemic-resarch-skill-for-CNU/academic-paper-reviewer .claude/skills/academic-paper-reviewer
ln -s ~/acdemic-resarch-skill-for-CNU/academic-pipeline .claude/skills/academic-pipeline
```

## 2. 开始使用

进入你的论文项目目录，启动 Claude Code 或 Codex，然后用自然语言描述任务。

### 选题与开题

```text
我准备写一篇本科毕业论文，方向是人工智能对大学生学习投入的影响。请用追问的方式帮我收敛研究问题、研究对象、变量和可能的方法。
```

### 文献综述

```text
请围绕“生成式 AI 对高校学生学习成效的影响”做一份文献综述，先给检索策略、纳入排除标准和主题矩阵。
```

### 论文写作

```text
请帮我规划一篇中国高校本科毕业论文的结构，包括摘要、引言、文献综述、研究设计、结果分析、结论和参考文献。
```

### 初稿审阅

```text
我已经有论文初稿，请帮我从结构、论证、方法、引用、格式和中文学术表达六个方面审阅。
```

### 修改导师意见

```text
我收到了导师修改意见，请拆成修订清单，标出优先级，并帮我写逐条回应草稿。
```

## 3. 选择哪个 skill

| 你的目标 | 建议使用 |
|---|---|
| 选题、研究问题、文献检索、证据综述 | `deep-research` |
| 写论文、写摘要、写文献综述、改初稿 | `academic-paper` |
| 模拟审稿、盲审前检查、导师视角评阅 | `academic-paper-reviewer` |
| 从选题一路做到终稿 | `academic-pipeline` |

## 4. 中国高校论文常用流程

建议按这个顺序使用：

1. `deep-research`：确定研究问题、范围、方法和文献基础
2. `academic-paper`：生成论文结构、章节计划和初稿
3. `academic-pipeline`：做引用、材料、论证一致性检查
4. `academic-paper-reviewer`：模拟导师/评审视角提出修改意见
5. `academic-paper`：根据意见完成修订和回应

## 5. 下一步二开建议

如果要进一步服务中国高校论文，可以优先增加：

- 学校论文模板解析；默认格式参考见 [中国高校本科论文格式参考](academic-paper/references/chinese_undergraduate_thesis_format.md)
- GB/T 7714 引用格式检查；原版 APA 7 中文引用并不是大陆本科论文默认规范
- 开题报告与任务书模板
- 学院格式规范清单
- 中文摘要、英文摘要和关键词规范
- AI 使用声明与学术诚信说明模板
