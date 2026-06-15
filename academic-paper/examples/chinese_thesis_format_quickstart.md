# 中国高校论文排版快速上手指南

本指南说明如何使用 ARS 管道的阶段 ⑨（FINALIZE）进行中国高校毕业论文/学位论文的格式排版。

---

## 一、整体流程

```
撰写（Markdown） → 阶段⑨ FINALIZE → Pandoc转DOCX → 后处理格式化 → 输出规范DOCX
```

完成论文内容的撰写后，只需在阶段 ⑨ 选择对应的学校模板，系统自动完成所有格式处理。

---

## 二、Markdown 输入要求

### 2.1 标题层级

使用 markdown 标题，系统会自动映射到对应的 DOCX 样式：

```markdown
# 第一章 绪论              → Heading 1（一级标题：黑体小二号居中）
## 1.1 研究背景            → Heading 2（二级标题：黑体小三号左对齐）
### 1.1.1 国内研究现状     → Heading 3（三级标题：黑体四号左对齐）
#### 1.1.1.1 综述         → Heading 4（四级标题：黑体小四号左对齐）
```

### 2.2 封面信息

在 markdown 文件开头用 YAML 块提供封面信息：

```yaml
title: "论文题目"
title_en: "Thesis Title in English"
author: "张三"
student_id: "2104301001"
school: "资源环境与材料学院"
major: "环境工程"
advisor: "李华教授"
date: "二〇二六年五月"
```

### 2.3 图表

图表使用标准 markdown 语法，图题在图片下方，表题在表格上方：

```markdown
![图片描述](figures/image_name.png)

**图1-1 图片标题**（图题在下方，五号加粗居中）

**注：** 英文图题为可选。

**表1-1 表格标题**（表题在上方，五号加粗居中）

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| ... | ... | ... |
```

### 2.4 公式

公式使用 LaTeX 语法，行内公式用 `$...$`，独立公式用 `$$...$$`：

```markdown
$$
E = mc^2 \tag{1-1}
$$
```

公式编号 `\tag{...}` 在输出 DOCX 中自动右对齐。

---

## 三、在阶段 ⑨ 使用 format-convert

在 `academic-paper` 管道的最后阶段（FINALIZE / 阶段 ⑨），系统会提示您选择输出格式。选择中国的论文模板后，按以下步骤操作：

### 步骤 1：启动 format-convert

运行以下命令之一：

```
/ars-format-convert
```

或在完整管道的阶段 ⑨ 中按提示选择 "Chinese University Thesis"。

### 步骤 2：选择学校模板

当前支持的学校模板：

| 模板 ID | 适用学校 | 适用学位 | 说明 |
|---------|---------|----------|------|
| `guangxi-undergrad` | 广西大学 | 本科毕业论文/设计 | 资源环境与材料学院格式规范 |
| `sichuan-grad` | 四川大学 | 硕士/博士学位论文 | 研究生院统一格式规范 |
| `mainland-fallback` | 大陆高校通用 | 通用 | 无学校模板时的回退方案 |

### 步骤 3：完成输出

选择模板后，系统自动完成：
1. Markdown → DOCX 转换（调用 Pandoc）
2. 封面插入（使用学校专用封面模板）
3. 摘要页格式化
4. 目录生成
5. 页眉页脚设置
6. 三线表格式
7. 图题格式化
8. 公式编号
9. 正文样式（字体、字号、行距）

---

## 四、格式覆盖优先级

| 优先级 | 说明 |
|-------|------|
| 最高 | 学校官方模板（.docx 样式文件） |
| 高 | 学院/指导教师具体要求 |
| 中 | Profile 内置格式规范 |
| 低 | 通用回退设置 |

如果发现系统处理的格式与学校最新要求不一致，请检查 `academic-paper/templates/docx/` 下的参考文件，或提交 Issue。

---

## 五、添加新学校模板

参考 `docs/ADD_NEW_SCHOOL_TEMPLATE.md`，只需两步：

1. 准备 `{school}_{degree}_reference.docx` 文件
2. 放入 `academic-paper/templates/docx/` 目录

**无需修改任何代码。** 系统自动发现新模板并在阶段 ⑨ 的下拉列表中显示。

---

## 六、相关文件

| 文件 | 说明 |
|------|------|
| `examples/chinese_thesis_guangxi_undergrad_example.md` | 广西大学本科毕业论文完整示例 |
| `examples/chinese_thesis_sichuan_grad_example.md` | 四川大学硕士学位论文完整示例 |
| `docs/ADD_NEW_SCHOOL_TEMPLATE.md` | 添加新学校模板的操作指南 |
| `references/chinese_higher_education_thesis_format.md` | 中国高校论文格式规范参考 |
| `scripts/export_chinese_thesis.py` | 格式导出核心脚本 |
| `scripts/postprocess_chinese_thesis_docx.py` | DOCX 后处理（表格/图/公式格式化） |
