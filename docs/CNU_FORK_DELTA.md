# CNU Fork Delta — 与 Upstream 的差异

本文件记录 `Yougahei/acdemic-resarch-skill-for-CNU` 相对于 upstream (`Imbad0202/academic-research-skills`) 的所有改动。用于维护者快速定位 CNU 增量，以及合并 upstream 时检查冲突。

> 最后同步 upstream：2026-06-23（分叉点 `c7f42d4`，upstream 此后发布 v3.13.0）
> 当前 CNU fork HEAD：独立维护，不再持续同步上游（见下方「维护策略」）

## 新增文件（20 个）

### 脚本（4 个，~3700 行）
| 文件 | 行数 | 用途 |
|------|------|------|
| `scripts/export_chinese_thesis.py` | 708 | Pandoc 导出包装器，支持广西大学本科、四川大学硕博及大陆通用三种 profile |
| `scripts/postprocess_chinese_thesis_docx.py` | 1571 | DOCX 后处理：封面、页眉页脚、分节、三线表、目录、标题编号 |
| `scripts/build_chinese_reference_docx.py` | 271 | 构建 Pandoc 参考 DOCX（字体、样式） |
| `scripts/test_export_chinese_thesis.py` | 1123 | 中文论文导出和后处理的测试（44 个用例） |

### LaTeX 模板（2 个）
| 文件 | 用途 |
|------|------|
| `academic-paper/templates/chinese_thesis_guangxi_undergrad_template.tex` | 广西大学本科毕业论文/设计 |
| `academic-paper/templates/chinese_thesis_sichuan_grad_template.tex` | 四川大学硕博学位论文 |

### DOCX 模板（4 个）
| 文件 | 用途 |
|------|------|
| `academic-paper/templates/docx/guangxi_undergrad_reference.docx` | 广西大学本科 Pandoc 参考文档 |
| `academic-paper/templates/docx/sichuan_grad_reference.docx` | 四川大学硕博 Pandoc 参考文档 |
| `academic-paper/templates/docx/mainland_fallback_reference.docx` | 大陆高校通用回退 |
| `academic-paper/templates/docx/covers/guangxi_undergrad_thesis_cover.docx` | 广西大学本科封面 |

### 格式参考文档（2 个）
| 文件 | 用途 |
|------|------|
| `academic-paper/references/chinese_higher_education_thesis_format.md` | 中国高校论文格式规范（广西大学、四川大学、大陆通用） |
| `academic-paper/references/chinese_thesis_format_audit_report.md` | 中文论文格式审计报告模式 |

### 示例（3 个）
| 文件 | 用途 |
|------|------|
| `academic-paper/examples/chinese_thesis_format_quickstart.md` | 中文论文格式快速开始 |
| `academic-paper/examples/chinese_thesis_guangxi_undergrad_example.md` | 广西大学本科论文示例 |
| `academic-paper/examples/chinese_thesis_sichuan_grad_example.md` | 四川大学硕博论文示例 |

### 项目文档（3 个）
| 文件 | 用途 |
|------|------|
| `docs/ADD_NEW_SCHOOL_TEMPLATE.md` | 新增学校模板操作指南 |
| `docs/BASELINE_CHECK.md` | CNU 分支基线检查报告 |
| `docs/UPSTREAM_CAPABILITY_AUDIT.md` | 上游能力覆盖审计 |

### 共享引用（2 个）
| 文件 | 用途 |
|------|------|
| `shared/references/routing_discipline.md` | Routing 规则（从 4 个 SKILL.md 样板提取） |
| `shared/references/phase_invocation_contract.md` | Phase-by-phase 调用契约公共骨架 |

## 修改文件（35 个）

### SKILL.md（4 个）— CNU 本地化
- `academic-paper/SKILL.md` — 中文论文描述、版本元数据更新、routing/phase 引用替换、data_access_level 链接
- `deep-research/SKILL.md` — 中文论文描述、routing/phase 引用替换、data_access_level 链接
- `academic-paper-reviewer/SKILL.md` — 中文论文描述、routing/phase 引用替换、data_access_level 链接
- `academic-pipeline/SKILL.md` — Stage 5 中文论文格式支持、routing/phase 引用替换、data_access_level 链接、版本兼容性表

### Agent 文件（4 个）— 中文论文格式能力声明
- `academic-paper/agents/formatter_agent.md` — 添加中文论文格式审计/导出规则（~80 行增量）
- `academic-paper/agents/citation_compliance_agent.md` — 添加 GB/T 7714 引用格式支持
- `academic-paper/agents/abstract_bilingual_agent.md` — 添加简体中文摘要支持
- `academic-pipeline/agents/pipeline_orchestrator_agent.md` — Stage 5 中文论文输出路径

### Pipeline 参考文档（5 个）— 流程和格式扩展
- `academic-paper/references/citation_format_switcher.md`
- `academic-paper/references/latex_template_reference.md`
- `academic-paper/references/mode_selection_guide.md`
- `academic-paper/references/workflow_phase_details.md`
- `academic-pipeline/references/pipeline_state_machine.md`
- `academic-pipeline/references/team_collaboration_protocol.md`
- `academic-pipeline/references/mode_advisor.md`
- `academic-pipeline/references/reproducibility_audit.md`
- `academic-pipeline/templates/pipeline_status_template.md`

### 命令和配置（6 个）
- `commands/ars-citation-check.md`、`commands/ars-format-convert.md`
- `scripts/check_spec_consistency.py`、`scripts/run_codex_audit.sh`（bug 修复和增强）
- `scripts/announce-ars-loaded.sh`、`scripts/_ci_pytest_manifest.toml`

### 顶层文档（7 个）
- `README.md`、`QUICKSTART.md`、`CONTRIBUTING.md`、`SECURITY.md`、`NOTICE.md`
- `MODE_REGISTRY.md`、`docs/SETUP.md`、`POSITIONING.md`
- `.claude-plugin/marketplace.json`、`.claude-plugin/plugin.json`

## 绝对不动的区域（合并安全区）

以下目录/文件在 CNU fork 中**从未修改**。从 upstream 合并时，这些区域的冲突可直接接受 upstream 版本：

- `deep-research/agents/` — 所有 agent 定义
- `academic-paper/agents/` — 除 formatter_agent、citation_compliance_agent、abstract_bilingual_agent 之外的所有 agent
- `academic-paper-reviewer/agents/` — 所有 agent 定义
- `academic-pipeline/agents/` — 除 pipeline_orchestrator_agent 之外的所有 agent
- `shared/contracts/` — 所有 JSON schema 和契约
- `shared/references/` — 除 routing_discipline.md 和 phase_invocation_contract.md 之外的所有文件
- `scripts/` — 除 export_chinese_thesis.py、postprocess_chinese_thesis_docx.py、build_chinese_reference_docx.py、test_export_chinese_thesis.py、run_codex_audit.sh、check_spec_consistency.py、announce-ars-loaded.sh、_ci_pytest_manifest.toml 之外的所有文件
- `tests/`、`hooks/`、`.github/` — 完全未修改

## 维护策略

### 原则：独立维护，不持续同步上游

本 fork 已发展为**独立产品**，核心价值是中文论文格式输出层（~3700 行自研 Python + 模板 + 字体映射 + 测试）。upstream 的方向是多语种学术研究流水线 / reviewer / cross-model 验证，与 CNU 输出层**无重叠**。因此采取独立维护策略：**不持续合并上游**，偶尔扫描 release notes 看有没有值得借鉴的工程思路，如有则单独 `git cherry-pick` 或手工移植，不做整体合并。

### 上游扫描记录

- **2026-06-25 扫描**：upstream 已发布 v3.13.0（24 个新提交，领先分叉点 `c7f42d4`）。扫描结论：**无可借鉴内容**。
  - diff/patch revision mode（#390/423/426）、provider-agnostic 跨模型验证（#455）、Socratic adjacent-framing probe（#461）、rebuttal-audit、format_profile schema（#439）—— 均属学术研究/reviewer 流水线，与中文论文格式导出无关。
  - Windows Python hook 可移植性（#454）属上游 hook 体系，CNU fork 未使用该 hook，不适用。
  - format_profile（#439）与 CNU 的硬编码 profile 概念重叠但路线不同（上游走 JSON schema + 声明式，CNU 走 Python dataclass + 硬编码 + 模板），借鉴价值低。
  - dry-run 合并测试：15 个文件冲突，全部是文档/版本号/`check_spec_consistency.py` 检查策略冲突，**零核心代码冲突**——但解决这些冲突无业务收益，仅为同步上游文档策略付出维护税。

### 何时重新评估

以下任一情况发生时，重新扫描上游：

- 上游新增了直接影响 Pandoc DOCX/LaTeX 导出或 python-docx 后处理的功能
- 上游修复了 CNU 依赖的 shared/ 契约或 scripts/ 脚本中的 bug
- CNU 需要上游的某个具体提交（单独 cherry-pick 即可，不必整体合并）

### 稳定性优先

`scripts/export_chinese_thesis.py` 和 `scripts/postprocess_chinese_thesis_docx.py` 是 CNU fork 的 existence reason，不轻易重构。维护面（~3700 行自研）远小于上游代码面（75000+ 行），绝大部分上游改动与 CNU 输出层无关。

## 已知问题

### Upstream 遗留
- `deep-research/agents/timeline_extraction_agent.md` — 来自 upstream v3.9.4，但 deep-research SKILL.md 未在 agent 表或 mode 描述中引用。这是 upstream 的问题，不在 CNU fork 中修复。跟踪 upstream issue 状态。

### CNU 技术债务
- `scripts/export_chinese_thesis.py` 和 `scripts/postprocess_chinese_thesis_docx.py` 中的 `COVER_FIELD_KEYS` 定义不重复但容易误解为重复（postprocess 版本已在 #38 中删除）
- Pandoc 参考 DOCX 文件是二进制文件，无法做文本 diff。更新时需重新运行 `scripts/build_chinese_reference_docx.py`
