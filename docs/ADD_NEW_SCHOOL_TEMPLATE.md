# 添加新学校/学院论文模板

本文档说明如何为本仓库添加新的学校或学院论文模板。包含两种方式：

- **方式一（推荐）：自动发现** — 放文件 + JSON 描述，零代码修改
- **方式二（旧）：手动注册** — 放文件 + 改代码

## 目录结构

所有模板文件统一放在以下目录结构中：

```text
acdemic-resarch-skill-for-CNU/
├── academic-paper/
│   ├── templates/
│   │   ├── chinese_thesis_{school}_{degree}_template.tex   # LaTeX 模板（PDF 导出）
│   │   ├── docx/
│   │   │   ├── {school}_{degree}_reference.docx             # 必需：DOCX 样式参考文件
│   │   │   ├── {school}_{degree}.json                       # 可选：侧边描述文件
│   │   │   ├── covers/
│   │   │   │   └── {school}_{degree}_thesis_cover.docx      # 可选：封面模板
│   │   │   └── profiles/                                    # 旧版方式（已废弃）
│   │   └── ... (其他上游模板，不可修改)
│   └── references/
│       └── chinese_higher_education_thesis_format.md        # 格式规范文档（可选）
└── 毕业论文（设计）格式规范和参考模板 20260422 资环材/      # 源格式文件（参考用）
```

## 命名规范

| 文件类型 | 命名模式 | 示例 |
|----------|----------|------|
| DOCX 参考文件 | `{school}_{degree}_reference.docx` | `fudan_undergrad_reference.docx` |
| JSON 描述文件 | `{school}_{degree}.json` | `fudan_undergrad.json` |
| 封面模板 | `{school}_{degree}_thesis_cover.docx` | `fudan_undergrad_thesis_cover.docx` |
| LaTeX 模板 | `chinese_thesis_{school}_{degree}_template.tex` | `chinese_thesis_fudan_undergrad_template.tex` |

命名规则：
- `{school}`: 学校英文简称，全小写、下划线分隔（如 `guangxi`、`sichuan`、`fudan`）
- `{degree}`: 学位级别，全小写（`undergrad`、`grad`）
- LaTeX 模板以 `chinese_thesis_` 为前缀以区别于上游模板

## 方式一（推荐）：自动发现

只需两步，**不需要修改任何代码**。

### 第 1 步：准备文件

**必需文件：**
- `{school}_{degree}_reference.docx` — Pandoc `--reference-doc` 带样式的空白 DOCX

**可选文件：**
- `{school}_{degree}.json` — JSON 侧边描述文件（见下方格式）
- `{school}_{degree}_thesis_cover.docx` — 封面模板
- `chinese_thesis_{school}_{degree}_template.tex` — LaTeX 模板（PDF 导出需要）

### 第 2 步：放到对应目录

```text
academic-paper/templates/docx/
├── fudan_undergrad_reference.docx     ← 放这里
├── fudan_undergrad.json               ← 放这里（可选，但推荐）
└── covers/
    └── fudan_undergrad_thesis_cover.docx  ← 封面放这里（可选）
```

### JSON 侧边描述文件格式

JOSN 文件与 reference docx 放在同一目录，文件名相同但后缀不同：

```json
{
  "label": "Fudan University Undergraduate Thesis",
  "header_text": "复旦大学本科毕业论文",
  "toc_title": "目  录",
  "school_label": "复旦大学",
  "degree_label": "本科",
  "paper_type_label": "本科毕业论文"
}
```

字段说明：

| 字段 | 必需 | 说明 | 默认值 |
|------|------|------|--------|
| `label` | 否 | 英文展示名，在阶段 ⑨ 选择时显示 | `"Chinese University Thesis ({id})"` |
| `header_text` | 否 | 页眉文字 | `"本科毕业论文"` |
| `toc_title` | 否 | 目录标题 | `"目  录"` |
| `school_label` | 否 | 学校中文全称 | `""`（空） |
| `degree_label` | 否 | 学位中文级别 | `""` |
| `paper_type_label` | 否 | 论文类型中文名 | `""` |

### 自动发现原理

启动时，系统会自动扫描 `templates/docx/` 下所有 `*_reference.docx` 文件：

1. 提取文件名中的 `{school}_{degree}` 部分
2. 查找同名的 `{school}_{degree}.json` 描述文件
3. 查找 `covers/{school}_{degree}_thesis_cover.docx` 封面文件
4. 全部合并为一个 `ExportProfile` 注册到 `PROFILES` 字典

内置的 `guangxi-undergrad`、`sichuan-grad`、`mainland-fallback` 三个 profile 是硬编码的，优先级高于自动发现（同名不会覆盖），其余全部自动发现。

### 完成

放好文件后，重启 Claude Code，阶段 ⑨（格式化输出）时会自动在可选列表中出现新学校的选项。**不需要任何代码修改。**

## 方式二（旧）：手动注册

如果 JSON 描述文件不够用（如需要特定位的封面字段映射 `COVER_LABEL_TO_FIELD`），可以在代码中手动注册。

### 1. `scripts/export_chinese_thesis.py`

在 `_BUILTIN_PROFILES` 字典中添加新条目：

```python
"fudan-undergrad": ExportProfile(
    id="fudan-undergrad",
    label="Fudan University Undergraduate Thesis",
    tex_template=ROOT / "academic-paper/templates/chinese_thesis_fudan_undergrad_template.tex",
    reference_docx=ROOT / "academic-paper/templates/docx/fudan_undergrad_reference.docx",
    school_label="复旦大学",
    degree_label="本科",
    paper_type_label="本科毕业论文",
    cover_docx=ROOT / "academic-paper/templates/docx/covers/fudan_undergrad_thesis_cover.docx",
    header_text="复旦大学本科毕业论文",
    toc_title="目  录",
),
```

`ExportProfile` 字段说明：

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 唯一标识，字母数字短横线 | `"fudan-undergrad"` |
| `label` | 英文展示名称 | `"Fudan University Undergraduate Thesis"` |
| `tex_template` | LaTeX 模板路径 | `ROOT / "academic-paper/templates/..."` |
| `reference_docx` | DOCX 参考文件路径 | `ROOT / "academic-paper/templates/docx/..."` |
| `school_label` | 学校中文全称 | `"复旦大学"` |
| `degree_label` | 学位中文级别 | `"本科"` 或 `"硕士/博士"` |
| `paper_type_label` | 论文类型中文名 | `"本科毕业论文"` 或 `"学位论文"` |
| `cover_docx` | 封面模板路径（可选） | `None` 或对应路径 |
| `header_text` | 页眉文字 | `"复旦大学本科毕业论文"` |
| `toc_title` | 目录标题 | `"目  录"` |

### 2. 覆盖封面字段映射（仅手动方式）

如果学校封面的标签不同（如"指导教师："而非"指导老师："），更新 `postprocess_chinese_thesis_docx.py` 的 `COVER_LABEL_TO_FIELD` 字典。

## 验证方法

### 基础检查

```bash
PYTHONPATH=. python3 -c "
from scripts.export_chinese_thesis import PROFILES
p = PROFILES['fudan-undergrad']
assert p.reference_docx.exists(), f'Missing: {p.reference_docx}'
if p.cover_docx:
    assert p.cover_docx.exists(), f'Missing: {p.cover_docx}'
print('All resources OK')
"
```

### 运行测试

```bash
PYTHONPATH=. python3 -m pytest scripts/test_export_chinese_thesis.py -v
```

所有现有测试必须保持通过。新增的 profile 会被 `test_discover_profiles_finds_builtin_templates` 等测试自动覆盖。

### 完整导出测试

```bash
# DOCX 导出（需要 Pandoc）
echo '# Test

正文内容。

## 第1章 绪论

正文。
' | pandoc -f markdown -t docx -o /tmp/test_output.docx

python3 scripts/postprocess_chinese_thesis_docx.py \
    /tmp/test_output.docx \
    /tmp/test_final.docx \
    --profile fudan-undergrad

# 检查输出文件
python3 -c "
from docx import Document
doc = Document('/tmp/test_final.docx')
print(f'Paragraphs: {len(doc.paragraphs)}')
for p in doc.paragraphs[:5]:
    print(f'  {p.text}')
"
```

## 提交流程

1. 创建分支：`codex/issue-N-add-{school}-template`
2. 用方式一（自动发现）只需添加模板文件 + JSON 描述文件；用方式二（手动注册）还需修改代码
3. 运行测试确保全部通过
4. 创建 PR，标题格式：`feat: add {school} {degree} thesis template (N)`
5. PR 描述中附上新学校的格式规范来源
