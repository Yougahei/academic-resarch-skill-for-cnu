# 添加新学校/学院论文模板

本文档说明如何为本仓库添加新的学校或学院论文模板。包含文件存放规范、命名规则、代码修改流程和验证方法。

## 目录结构

所有模板文件统一放在以下目录结构中：

```text
acdemic-resarch-skill-for-CNU/
├── academic-paper/
│   ├── templates/
│   │   ├── chinese_thesis_{school}_{degree}_template.tex   # LaTeX 模板（PDF 导出）
│   │   ├── docx/
│   │   │   ├── {school}_{degree}_reference.docx             # DOCX 样式参考文件
│   │   │   └── covers/
│   │   │       └── {school}_{degree}_thesis_cover.docx      # 封面模板（可选）
│   │   └── ... (其他上游模板，不可修改)
│   └── references/
│       └── chinese_higher_education_thesis_format.md        # 格式规范文档（可选）
└── 毕业论文（设计）格式规范和参考模板 20260422 资环材/      # 源格式文件（参考用）
```

## 命名规范

| 文件类型 | 命名模式 | 示例 |
|----------|----------|------|
| LaTeX 模板 | `chinese_thesis_{school}_{degree}_template.tex` | `chinese_thesis_fudan_undergrad_template.tex` |
| DOCX 参考文件 | `{school}_{degree}_reference.docx` | `fudan_undergrad_reference.docx` |
| 封面模板 | `{school}_{degree}_thesis_cover.docx` | `fudan_undergrad_thesis_cover.docx` |

命名规则：
- `{school}`: 学校英文简称，全小写、下划线分隔（如 `guangxi`、`sichuan`、`fudan`）
- `{degree}`: 学位级别，全小写（`undergrad`、`grad`）
- LaTeX 模板以 `chinese_thesis_` 为前缀以区别于上游模板

## 需要准备的文件

### 1. DOCX 参考文件（必需）

`{school}_{degree}_reference.docx` 是一个带样式的空白 DOCX，作为 Pandoc `--reference-doc` 参数使用。它定义了：

- 默认字体（中文宋体、英文 Times New Roman）
- 标题样式（黑体）
- 页面尺寸和边距
- 正文段落格式（首行缩进 2 字符、行距等）

**创建方法**：复制一份现有的参考文件（如 `guangxi_undergrad_reference.docx`），打开后调整个别样式设置，另存为新文件。

### 2. LaTeX 模板（PDF 导出需要）

`chinese_thesis_{school}_{degree}_template.tex` 是 Pandoc 的 LaTeX 模板，用于 PDF 生成。

**创建方法**：复制一份现有的 `.tex` 模板（如 `chinese_thesis_guangxi_undergrad_template.tex`），在学校英文名称、中文名称、页眉内容、页边距等参数处做对应修改。

模板使用 `$if(fontenc)$` 等 Pandoc 条件参数语法。核心需要修改的部分：
- `\title{}` 中文化
- 页眉页脚格式
- 字体配置
- 页面边距

### 3. 封面模板（可选）

如果学校有独立的封面页，可以提供 `{school}_{degree}_thesis_cover.docx`。

**封面占位符系统**：封面 DOCX 中的表格通过「左列标签 → 右列值」的映射关系自动填充。代码中的 `COVER_LABEL_TO_FIELD` 字典定义标签到字段的映射：

```python
COVER_LABEL_TO_FIELD = {
    "学院：": "college",
    "专业：": "major",
    "班级：": "class-name",
    "学号：": "student-id",
    "姓名：": "author",
    "指导老师：": "advisor",
}
```

封面 DOCX 需要：
- 使用表格布局，左列为标签（如"姓名："），右列为空（将被填充）
- 表格至少有 2 列
- 如果封面不含表格，字段不会填充，封面原样插入

## 代码修改清单

### 1. `scripts/export_chinese_thesis.py` — 注册导出配置

在 `PROFILES` 字典中添加新条目。建议位置：按 profile id 字母顺序排列。

```python
# 在 PROFILES 字典中添加（约第 35-64 行）
"fudan-undergrad": ExportProfile(
    id="fudan-undergrad",
    label="Fudan University Undergraduate Thesis",
    tex_template=ROOT / "academic-paper/templates/chinese_thesis_fudan_undergrad_template.tex",
    reference_docx=ROOT / "academic-paper/templates/docx/fudan_undergrad_reference.docx",
    school_label="复旦大学",
    degree_label="本科",
    paper_type_label="本科毕业论文",
    cover_docx=ROOT / "academic-paper/templates/docx/covers/fudan_undergrad_thesis_cover.docx",
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

### 2. `scripts/postprocess_chinese_thesis_docx.py` — 添加后处理配置

在 `PROFILE_HEADER_TEXT` 字典中添加页眉文字（约第 29 行）：

```python
PROFILE_HEADER_TEXT: dict[str, str] = {
    # ... 已有条目
    "fudan-undergrad": "复旦大学本科毕业论文",
}
```

在 `PROFILE_TOC_TITLE` 字典中添加目录标题（约第 35 行）：

```python
PROFILE_TOC_TITLE: dict[str, str] = {
    # ... 已有条目
    "fudan-undergrad": "目  录",
}
```

如果学校有特殊的封面字段标签（如"指导教师："而非"指导老师："），还需更新 `COVER_LABEL_TO_FIELD` 字典（约第 52 行）。

### 3. 可选：添加格式规范文档

如果学校有公开的格式规范文件，可以在 `academic-paper/references/chinese_higher_education_thesis_format.md` 中添加对应学校的格式要求说明。

## 验证方法

### 基础检查

```bash
# 确认所有资源存在
python3 -c "
from scripts.export_chinese_thesis import PROFILES
p = PROFILES['fudan-undergrad']
assert p.tex_template.exists(), f'Missing: {p.tex_template}'
assert p.reference_docx.exists(), f'Missing: {p.reference_docx}'
if p.cover_docx:
    assert p.cover_docx.exists(), f'Missing: {p.cover_docx}'
print('All resources OK')
"
```

### 运行测试

```bash
PYTHONPATH=. pytest scripts/test_export_chinese_thesis.py -v
```

所有现有测试必须保持通过。新学校的测试建议添加在 `scripts/test_export_chinese_thesis.py` 中（如 `test_profile_assets_exist` 会自动检查所有 profile 的资源文件）。

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
2. 添加模板文件 + 修改代码
3. 运行测试确保全部通过
4. 创建 PR，标题格式：`feat: add {school} {degree} thesis template (N)`
5. PR 描述中附上新学校的格式规范来源
