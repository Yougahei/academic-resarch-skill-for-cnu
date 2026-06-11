# 安装与环境配置

本文档面向 `acdemic-resarch-skill-for-CNU`，说明如何在 Claude Code、Codex 和本地二开环境中使用这套 skills。

## 最小可用配置

1. 安装 Claude Code 或 Codex。
2. 准备对应模型服务的 API Key。
3. 安装本仓库的四个 skills。
4. 重启客户端，让新 skills 被重新扫描。

只输出 Markdown 时不需要 Pandoc、LaTeX 或 PDF 工具链。

## 推荐安装方式：skillshare 共用

如果你希望 Codex 和 Claude Code 同时使用，并且后续还要二次开发，推荐用 `skillshare`：

```bash
skillshare install https://github.com/Yougahei/acdemic-resarch-skill-for-CNU.git --all
skillshare sync --all
```

同步后通常会形成这样的结构：

```text
~/.config/skillshare/skills/        # 中心开发目录
~/.codex/skills/                    # Codex 软链接
~/.claude/skills/                   # Claude Code 软链接
~/.claude/agents/                   # Claude Code agents 软链接
```

后续改 skill 时，优先修改中心目录，然后执行：

```bash
skillshare sync --all
```

## Claude Code 插件方式

如果本仓库已经发布到 Claude Code plugin marketplace，可以用：

```text
/plugin marketplace add Yougahei/acdemic-resarch-skill-for-CNU
/plugin install acdemic-resarch-skill-for-CNU
```

这种方式更适合普通使用者；二开时仍建议使用 git clone 或 skillshare 中心源。

## 手动安装到项目

```bash
git clone https://github.com/Yougahei/acdemic-resarch-skill-for-CNU.git ~/acdemic-resarch-skill-for-CNU

cd /path/to/your/project
mkdir -p .claude/skills
ln -s ~/acdemic-resarch-skill-for-CNU/deep-research .claude/skills/deep-research
ln -s ~/acdemic-resarch-skill-for-CNU/academic-paper .claude/skills/academic-paper
ln -s ~/acdemic-resarch-skill-for-CNU/academic-paper-reviewer .claude/skills/academic-paper-reviewer
ln -s ~/acdemic-resarch-skill-for-CNU/academic-pipeline .claude/skills/academic-pipeline
```

Claude Code 需要在 `<install-root>/<skill-name>/SKILL.md` 这一层发现 skill。不要把整个仓库作为一个嵌套目录放进 `.claude/skills/acdemic-resarch-skill-for-CNU/`，否则四个 `SKILL.md` 会多一层，无法被正确发现。

## 可选：DOCX 输出

如果需要 `.docx`，安装 Pandoc：

```bash
# macOS
brew install pandoc

# Ubuntu/Debian
sudo apt-get install pandoc
```

如果没有 Pandoc，skill 仍然可以输出 Markdown，并给出转换建议。

## 可选：LaTeX / PDF 输出

PDF 输出依赖 `tectonic` 和中文字体。中国高校论文通常更常用 Word 模板，建议优先完善 DOCX 流程；PDF 可以作为预览或归档格式。

```bash
brew install tectonic
```

建议准备字体：

- Times New Roman
- 思源宋体 / Noto Serif CJK
- Courier New

## 可选环境变量

| 变量 | 作用 |
|---|---|
| `ARS_CROSS_MODEL` | 启用跨模型复核 |
| `ARS_PASSPORT_RESET=1` | 把完整检查点提升为可恢复边界 |
| `ARS_CLAIM_AUDIT=1` | 启用引用主张一致性审计 |
| `ARS_VERIFICATION_CACHE_PATH` | 指定引用验证缓存数据库路径 |

这些变量默认关闭，不设置也可以正常使用。

## 面向中国高校的资料准备

建议每个论文项目准备一个资料夹，至少包含：

- 学校或学院论文格式规范
- Word 模板或格式样例
- 开题报告、任务书、中期检查表等过程材料
- 导师反馈、评审意见或盲审意见
- 已确认可使用的文献清单
- 数据、访谈、问卷、实验或其他材料来源说明

把这些材料交给 skill 前，请明确哪些是“必须遵守”的学校规范，哪些只是参考样例。
