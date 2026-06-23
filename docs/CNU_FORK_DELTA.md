# CNU Fork Delta — 与 Upstream 的差异

本文件记录 `Yougahei/acdemic-resarch-skill-for-CNU` 相对于 upstream (`Imbad0202/academic-research-skills`) 的所有改动。用于维护者快速定位 CNU 增量，以及合并 upstream 时检查冲突。

> 最后同步 upstream：2026-06-23
> 当前 CNU fork HEAD：与 upstream main 合并后 + CNU 增量

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

### 原则
CNU fork 的核心价值是**中文论文格式输出层**。Agent 行为、pipeline 逻辑、学术完整性门禁等全部依赖 upstream。维护策略以此为准：

1. **优先保持输出层稳定** — `scripts/export_chinese_thesis.py` 和 `scripts/postprocess_chinese_thesis_docx.py` 是 CNU fork 的 existence reason，不轻易重构。
2. **按需合并 upstream** — 只在以下情况合并：
   - 上游修复了影响中文论文输出的关键 bug
   - 需要上游的新功能（如新的 citation verification gate）
   - 上游的安全修复
3. **定期检查但不强制合并** — 每季度检查 upstream CHANGELOG，评估是否需要合并。如果当前版本稳定且无关键需求，可以跳过。
4. **合并后检查清单**：
   - [ ] `PYTHONPATH=. pytest scripts/test_export_chinese_thesis.py -v` 全部通过
   - [ ] `python3 scripts/check_spec_consistency.py` 无新增错误
   - [ ] 4 个 SKILL.md 的 CNU 描述未被覆盖
   - [ ] formatter_agent.md 的 CNU 规则未被覆盖
   - [ ] 如果 upstream 新增了 shared/references/ 文件，检查是否与 `phase_invocation_contract.md`、`routing_discipline.md` 冲突

### 维护面 vs 改动面
- CNU 改动了 ~3700 行 Python + ~100 行 SKILL.md 修改
- 需要同步维护的 upstream 代码约 75000+ 行
- 绝大部分上游改动与 CNU 输出层无关
- **实用建议**：如果当前版本对中文论文输出已经足够稳定，不合并 upstream 是完全合理的选择

## 已知问题

### Upstream 遗留
- `deep-research/agents/timeline_extraction_agent.md` — 来自 upstream v3.9.4，但 deep-research SKILL.md 未在 agent 表或 mode 描述中引用。这是 upstream 的问题，不在 CNU fork 中修复。跟踪 upstream issue 状态。

### CNU 技术债务
- `scripts/export_chinese_thesis.py` 和 `scripts/postprocess_chinese_thesis_docx.py` 中的 `COVER_FIELD_KEYS` 定义不重复但容易误解为重复（postprocess 版本已在 #38 中删除）
- Pandoc 参考 DOCX 文件是二进制文件，无法做文本 diff。更新时需重新运行 `scripts/build_chinese_reference_docx.py`
