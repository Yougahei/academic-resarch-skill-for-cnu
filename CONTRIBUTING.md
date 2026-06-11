# 贡献说明

`acdemic-resarch-skill-for-CNU` 是基于 `Imbad0202/academic-research-skills` 的中国高校论文场景二开版。贡献时请尽量保持核心源码、agent 协议和测试结构与上游一致，把本 fork 的差异集中在中文文档、学校规范适配、模板和本土化流程上。

## 优先欢迎的贡献

- 中国高校论文格式规范整理
- GB/T 7714 引用格式检查与示例
- 本科毕业论文、硕士论文、博士论文模板适配
- 开题报告、任务书、中期检查、答辩稿等过程材料模板
- 中文学术写作表达和术语统一指南
- 面向导师意见、盲审意见的修订流程样例
- 原 README、教程、示例的中文化改写

## 修改边界

可以直接改：

- `README.md`
- `QUICKSTART.md`
- `docs/SETUP.md`
- 示例、模板和面向用户的中文教程
- 与中国高校格式规范相关的 reference 文件

需要谨慎改：

- `*/SKILL.md`
- `*/agents/*.md`
- `shared/`
- `scripts/`
- `evals/`
- `tests/`

这些文件影响运行行为。修改前建议先说明动机，并尽量保持与上游结构可合并。

## 分支与提交建议

```bash
git checkout -b docs/cn-university-adaptation
git add .
git commit -m "docs: localize project for Chinese university paper workflows"
```

提交信息建议说明“改了什么”和“为什么改”，避免把文档翻译、行为修改和测试调整混在一个提交里。

## 学术诚信原则

本项目服务论文写作流程，但不鼓励也不支持代写、伪造数据、伪造引用、规避查重或规避 AI 检测。所有功能都应保持“人主导、AI 协作、过程可解释、材料可追溯”的边界。

## 许可

本 fork 继承原项目的 CC BY-NC 4.0 许可。贡献即表示你同意贡献内容按同一许可发布。
