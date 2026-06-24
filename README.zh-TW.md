# Academic Research Skills for Claude Code

[![Version](https://img.shields.io/badge/version-v3.12.0-blue)](https://github.com/Yougahei/acdemic-resarch-skill-for-CNU/releases/tag/v3.12.0)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

[English](README.md) | [简体中文版](README.zh-CN.md) | [日本語版](README.ja-JP.md)

一套完整的學術研究 Claude Code 技能包，涵蓋從研究到論文出版的全流程。

**30 秒安裝**（Claude Code CLI / VS Code / JetBrains，v3.7.0+）：

```text
/plugin marketplace add Yougahei/acdemic-resarch-skill-for-CNU
/plugin install acdemic-resarch-skill-for-CNU
```

裝完跑 `/ars-plan`，ARS 會用蘇格拉底對話幫你規劃章節結構。需要前置條件或傳統 symlink 安裝請看 [快速安裝](#快速安裝)。

> **AI 是你的副駕駛，不是機長。** 這工具不會幫你寫論文。它處理苦工 — 搜文獻、排格式、驗數據、查邏輯一致性 — 讓你專注在真正需要你腦子的事：定義問題、選方法、詮釋數據的意義、寫出「我認為」後面那句話。
>
> 跟 humanizer 不同，這工具不是幫你隱藏用 AI 協作的事實，而是幫你把關文章品質。風格校準從你過去的文章學習你的聲音，寫作品質檢查抓出讓文字讀起來像機器產的模式。目標是品質，不是遮掩。

### 為什麼選「人機協作」而不是「全自動」？

Lu 等人（2026，*Nature* 651:914-919）發表的 **The AI Scientist** 是第一個端到端全自動的 AI 研究系統，其生成的論文通過 ICLR 2025 workshop 的盲審（評分 6.33/10，workshop 平均 4.87）。他們自己的 Limitations 段落也列出了這類系統會遇到的結構性失敗模式：實作錯誤、幻覺實驗結果、取巧特徵依賴、實作錯誤被包裝成「意外發現」、方法論偽造、框架鎖定、引用幻覺。

ARS 建立在這個前提上：**人類研究者 + AI 的組合，比純自動或純人工都更能避開這些失敗模式**。Stage 2.5 與 Stage 4.5 誠信閘門執行 7 類阻斷式檢查清單（見 [`academic-pipeline/references/ai_research_failure_modes.md`](academic-pipeline/references/ai_research_failure_modes.md)），reviewer 也提供 opt-in 的 calibration mode 用使用者自備的 gold set 測量 FNR/FPR。

[**Zhao 等人**](https://arxiv.org/abs/2605.07723)（2026-05）盤點了 arXiv、bioRxiv、SSRN、PMC 上 250 萬篇論文裡的 1.11 億筆引用，保守估計 2025 年單年就有 146,932 筆幻覺引用，並觀察到 2024 年中是上升的拐點；bioRxiv-to-PMC 這條配對的「預印本進到正式發表」幻覺存活率達 85.3%。他們把「真實引用被用來支撐被引文獻其實沒有提出的主張」描述為當前未解的問題。ARS v3.7.1 為來源 provenance 加上 trust-chain frontmatter，v3.7.3 為未來的 claim-level 稽核鋪上 locator 基礎建設（三層引用 anchor），並在引用時段帶出 advisory 風險訊號（ARS 內部把這條 claim-faithfulness 缺口標記為「L3」，此為 ARS 的用詞，不是論文的用詞）。v3.7.x 的設計動機來自 Zhao 等人的 corpus-scale 發現；ARS 本身的 corpus-scale 評估仍是未來工作。

v3.8 補上 L3 缺口的另一半。v3.7.3 讓每一筆引用都帶 locator anchor，v3.8 在這個基礎上加一道 opt-in 稽核（`ARS_CLAIM_AUDIT=1`）：抓回每一個 anchor 指向的原始文本，判斷論文裡的 claim 是否真有被該引用支撐。五類新的 HIGH-WARN annotation（claim-not-supported、negative-constraint-violation、fabricated-reference、anchorless、constraint-violation-uncited）會在 formatter terminal hard gate 直接攔下輸出。Calibration 隨 release 出 20 筆 gold set，採 FNR<0.15、FPR<0.10 雙閾值；正式放大投入前要先有 calibration 證據（v3.8 spec §5）。

v3.3 的靈感來自 [**PaperOrchestra**](https://arxiv.org/abs/2604.05018)（Song, Song, Pfister & Yoon, 2026, Google）：Semantic Scholar API 驗證、反洩漏協議、VLM 圖表驗證、分數軌跡追蹤。

---

## 架構與 pipeline

**👉 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — 完整 pipeline 視圖：流程圖、階段 × 維度矩陣、資料存取流、skill 依賴圖、品質閘門、模式清單。

這份架構文件取代了原本散在 README 各處的 pipeline 描述。關於「哪個階段跑什麼」的所有資訊都集中在一個地方。

## 快速安裝

**前置條件**

- [Claude Code](https://docs.claude.com/en/docs/claude-code/setup)（建議最新版；plugin packaging 需要近期版本）
- 已 export `ANTHROPIC_API_KEY`，或第一次跑 `claude` 時設定
- *選用：* Pandoc 用於 DOCX 輸出，tectonic + 思源宋體 TC 用於 APA 7.0 PDF（純 Markdown 輸出兩個都不需要）

**Plugin 安裝（v3.7.0+，推薦）：**

```text
/plugin marketplace add Yougahei/acdemic-resarch-skill-for-CNU
/plugin install acdemic-resarch-skill-for-CNU
```

**驗證可用：** 跑 `/ars-plan` 並描述你正在寫的論文，ARS 會用蘇格拉底對話幫你規劃章節結構。想要單次測試的話改跑 `/ars-lit-review "你的主題"`。

**👉 [docs/SETUP.zh-TW.md](docs/SETUP.zh-TW.md)** — 完整指南：安裝 Claude Code、設定 API key、選用的 Pandoc/tectonic（DOCX/PDF）、跨模型驗證（`ARS_CROSS_MODEL`），以及五種安裝方式（Plugin、專案 skills、全域 skills、claude.ai Project、repo clone）。

**用 Codex CLI？** 請改裝姊妹版：[`Imbad0202/academic-research-skills-codex`](https://github.com/Imbad0202/academic-research-skills-codex)。同一套 workflow 內容，Codex 原生包裝為單一 `$academic-research-suite` skill，提供 `ars-*` 別名。

## 效能與費用

**👉 [docs/PERFORMANCE.zh-TW.md](docs/PERFORMANCE.zh-TW.md)** — 各模式 token 預算、完整 pipeline 估算（一篇 15k 字論文約 ~$4–6），以及建議的 Claude Code 設定（Skip Permissions；Agent Team 選用）。

## 使用指南與文章

- [學術寫作不該是一個人的事：一套開源 AI 協作工具如何改變研究者的工作流](https://open.substack.com/pub/edwardwu223235/p/ai?r=4dczl&utm_medium=ios) — 完整使用指南（繁體中文）
- [Academic Writing Shouldn't Be a Solo Act](https://open.substack.com/pub/edwardwu223235/p/academic-writing-shouldnt-be-a-solo?r=4dczl&utm_medium=ios) — Full pipeline walkthrough (English)

---

## 功能特色一覽

- **Deep Research** — 13 個 Agent 的研究團隊，支援蘇格拉底引導、PRISMA 系統性回顧、意圖偵測、對話健康度監控、可選跨模型 DA、Semantic Scholar API 驗證。
- **Academic Paper** — 12 個 Agent 的論文撰寫團隊，含風格校準、寫作品質檢查、LaTeX 輸出強化、視覺化、修訂教練、引用格式轉換、反洩漏協議、VLM 圖表驗證。
- **Academic Paper Reviewer** — 7 個 Agent 的多視角同儕審查，0-100 品質量表（主編 + 3 位動態審查者 + 魔鬼代言人），含讓步門檻協議、攻擊強度保持、可選跨模型 DA critique / calibration、R&R 追溯矩陣、唯讀約束。
- **Academic Pipeline** — 10 階段全流程調度器，含自適應 checkpoint、宣稱驗證、素材護照、可選 `repro_lock`、可選跨模型誠信驗證、中途強化機制、分數軌跡追蹤。
- **資料存取層級標註**（v3.3.2+）— 每個 skill 宣告 `data_access_level`（`raw` / `redacted` / `verified_only`），由 `scripts/check_data_access_level.py` 強制執行。設計靈感來自 Anthropic 的 automated-w2s-researcher（2026）。詳見 [`shared/ground_truth_isolation_pattern.md`](shared/ground_truth_isolation_pattern.md)。
- **任務類型標註**（v3.3.2+）— 每個 skill 宣告 `task_type`（`open-ended` 或 `outcome-gradable`）。目前 ARS 所有 skills 皆為 `open-ended`。
- **Benchmark 報告 Schema**（v3.3.5+）— JSON Schema + lint script，要求誠實的 benchmark 比較報告。詳見 [`shared/benchmark_report_pattern.md`](shared/benchmark_report_pattern.md)。
- **Artifact 可重現性 Lockfile**（v3.3.5+）— Material Passport 新增可選 `repro_lock` 子區塊。**是設定文件化，不是重播保證** — LLM 輸出不是位元可重現。詳見 [`shared/artifact_reproducibility_pattern.md`](shared/artifact_reproducibility_pattern.md)。
- **實驗來源憑證登錄**（#260）— Material Passport 可選的 `experiment_provenance[]` 記錄研究者在**外部**跑過的實驗（ARS 從不執行實驗），論文宣稱透過 `claim_intent_manifest.planned_experiment_ids[]` 與之 join。誠信 gate（Stage 2.5/4.5）逐條比對實驗支撐型宣稱與登錄憑證 — `ALIGNED` / `OVERSTATED` / `NOT_SUPPORTED_BY_PROVENANCE` / `PROVENANCE_INSUFFICIENT` — **但不判定實驗本身是否正確**。fail-closed 的 `experiment_intake_declaration` 讓「有沒有跑實驗」成為 Stage 1 明確決定。詳見 [`shared/handoff_schemas.md`](shared/handoff_schemas.md)。
- **蘇格拉底閱讀探針**（v3.5.1）— 由 `ARS_SOCRATIC_READING_PROBE` 環境變數控制，在 goal-oriented Socratic 會話中觸發一次性閱讀誠實檢查。詳見 [`deep-research/agents/socratic_mentor_agent.md`](deep-research/agents/socratic_mentor_agent.md)。

---

## 實際產出展示

查看完整 10 階段 pipeline 的實際產出 — 包含**同儕審查報告、誠信驗證報告、完稿論文**：

**[瀏覽所有 pipeline 產出 →](examples/showcase/)**

| 產出物 | 說明 |
|---|---|
| [完稿論文（英文）](examples/showcase/full_paper_apa7.pdf) | APA 7.0 格式，LaTeX 編譯 |
| [完稿論文（中文）](examples/showcase/full_paper_zh_apa7.pdf) | 中文版，APA 7.0 |
| [誠信報告 — 審稿前](examples/showcase/integrity_report_stage2.5.pdf) | Stage 2.5：抓出 15 個虛構引用 + 3 個統計錯誤 |
| [誠信報告 — 最終](examples/showcase/integrity_report_stage4.5.pdf) | Stage 4.5：確認零回歸 |
| [同儕審查第一輪](examples/showcase/stage3_review_report.pdf) | 主編 + 3 審查者 + 魔鬼代言人 |
| [複審](examples/showcase/stage3prime_rereview_report.pdf) | 修訂後驗證審查 |
| [同儕審查第二輪](examples/showcase/stage3_review_report_r2.pdf) | 追蹤審查 |
| [回覆審查意見](examples/showcase/response_to_reviewers_r2.pdf) | 逐點回覆 |
| [出版後稽核報告](examples/showcase/post_publication_audit_2026-03-09.pdf) | 獨立全引用稽核：發現 21/68 篇問題，通過了 3 輪誠信審查仍漏網 |

---

## 搭配工具：Experiment Agent

如果你的研究需要在寫作前跑實驗（程式碼或人工研究），[Experiment Agent](https://github.com/Imbad0202/experiment-agent) 技能填補 ARS Stage 1（研究）和 Stage 2（寫作）之間的空缺。

```
ARS Stage 1 研究      →  RQ Brief + Methodology Blueprint
        ↓
  experiment-agent     →  執行/管理實驗 → 驗證結果
        ↓
ARS Stage 2 寫作      →  用驗證過的實驗結果撰寫論文
```

**功能**：執行程式碼實驗（Python、R 等）並即時監控、管理人工研究 protocol 與 IRB 倫理審查、11 種統計謬誤偵測、重現性驗證。

**搭配使用方式**：ARS pipeline 跑完 Stage 1 後暫停，在另一個 experiment-agent session 中跑實驗，完成後將結果（含 Material Passport）帶回 ARS Stage 2。ARS 不需要任何修改。詳見 [experiment-agent README](https://github.com/Imbad0202/experiment-agent)。

---

## 使用方式

### 快速開始

```
# 啟動完整研究 pipeline
你: "我想做一篇關於 AI 對高教品保影響的研究論文"

# 蘇格拉底引導模式
你: "引導我研究 AI 在教育評鑑中的應用"

# 引導式論文撰寫
你: "引導我寫一篇關於少子化影響的論文"

# 審查現有論文
你: "幫我審查這篇論文"（接著提供論文）

# 查看 pipeline 進度
你: "進度" 或 "status"
```

### 個別 Skill 使用

#### Deep Research（深度研究，7 種模式）

```
"研究 AI 對高等教育的影響"                    → full mode（完整研究）
"給我一份 X 的快速摘要"                       → quick mode（快速簡報）
"幫我做 X 的系統性文獻回顧，含 PRISMA"        → systematic-review mode
"引導我研究 X"                                → socratic mode（蘇格拉底引導）
"幫我查核這些說法"                            → fact-check mode（事實查核）
"幫我做文獻回顧"                              → lit-review mode（文獻回顧）
"審查這篇論文的研究品質"                      → review mode（論文審查）
```

#### Academic Paper（學術論文撰寫，10 種模式）

```
"幫我寫一篇論文"                              → full mode（完整撰寫）
"引導我寫論文"                                → plan mode（引導規劃）
"先幫我搭論文大綱"                            → outline-only mode（只做大綱）
"我有初稿，這是審稿意見"                      → revision mode（修訂）
"幫我整理這些審稿意見成修訂路線圖"            → revision-coach mode
"幫我寫這篇的摘要"                            → abstract-only mode（摘要）
"把這批資料寫成文獻回顧論文"                  → lit-review mode（文獻回顧論文）
"轉換成 LaTeX" / "引用格式轉 IEEE"            → format-convert mode（格式轉換）
"檢查引用格式"                                → citation-check mode（引用檢查）
"幫我生成 NeurIPS 的 AI 使用揭露"             → disclosure mode（AI 揭露）
```

#### Academic Paper Reviewer（論文審查，6 種模式）

```
"審查這篇論文"                                → full mode（主編 + R1/R2/R3 + 魔鬼代言人）
"快速評估這篇論文"                            → quick mode（快速評估）
"引導我改進這篇論文"                          → guided mode（引導改進）
"檢查研究方法"                                → methodology-focus mode（方法論聚焦）
"驗收修訂"                                    → re-review mode（再審驗收）
"用我的 gold set 校準 reviewer"               → calibration mode（校準）
```

#### Academic Pipeline（全流程調度器）

```
"我想做一篇完整的研究論文"                    → 從 Stage 1 開始完整 pipeline
"我已經有論文，幫我審查"                      → 從 Stage 2.5 進入（先做誠信審查）
"我收到審稿意見了"                            → 從 Stage 4 進入
```

> Pipeline 結束時自動產出 **Stage 6：過程紀錄** — 含論文創建過程紀錄與 6 維度協作品質評估（1–100 分）。

### 支援語言

- **繁體中文** — 使用者以中文對話時預設使用
- **English** — 使用者以英文對話時預設使用
- 學術論文自動產出雙語摘要（中文 + English）

> **使用其他語言？** 蘇格拉底模式（deep-research）和 Plan 模式（academic-paper）採用**意圖匹配**啟動 — 偵測你的請求含義，而非比對特定關鍵字。這代表它們**支援任何語言**，無需額外設定。
>
> 不過，一般的 `Trigger Keywords` 區塊（決定 skill 是否被啟動）仍以英文和繁體中文為主。如果你發現 skill 在你的語言下觸發不穩定，可以在各 `SKILL.md` 的 `### Trigger Keywords` 區塊中加入你的語言的關鍵字，提高匹配信心。

### 支援引用格式

- APA 7.0（預設，含中文引用規則）
- Chicago（Notes & Author-Date）
- MLA
- IEEE
- Vancouver

### 支援論文結構

- IMRaD（實證研究）
- 主題式文獻回顧
- 理論分析
- 個案研究
- 政策簡報
- 研討會論文

---

## Skill 詳細資訊

各 agent 的職責與各階段產出物現已移至 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)。版本號保留在此以維持 release metadata 集中管理。

### Deep Research (v2.9.4)

13 個 Agent 的研究團隊。模式：full、quick、review、lit-review、fact-check、socratic、systematic-review。完整 agent 名單與產出物：見 ARCHITECTURE.md §3。

### Academic Paper (v3.2.0)

12 個 Agent 的論文撰寫 pipeline。模式：full、plan、outline-only、revision、revision-coach、abstract-only、lit-review、format-convert、citation-check、disclosure。輸出：MD + DOCX（Pandoc 可用時）+ LaTeX（APA 7.0 `apa7` class / IEEE / Chicago）→ tectonic 編譯 PDF。完整 agent 名單與各 phase 職責：見 ARCHITECTURE.md §3。

### Academic Paper Reviewer (v1.10.0)

7 個 Agent 的多視角審查，搭配 **0-100 品質量表**。模式：full、re-review、quick、methodology-focus、guided、calibration。**決策對照：** ≥80 接受、65-79 小修、50-64 大修、<50 退稿。第一輪審查團隊 vs. 精簡再審團隊的分界：見 ARCHITECTURE.md §3 Stage 3 / Stage 3'。

### Academic Pipeline (v3.12.0)

10 階段調度器，含誠信驗證、兩階段審查、蘇格拉底指導、協作品質評估。Pipeline 保證：每個階段都需使用者確認 checkpoint；誠信驗證（Stage 2.5 + 4.5）不可跳過；R&R 追溯矩陣（Schema 11）獨立驗證作者修訂宣稱。v3.4 新增 Compliance Agent（PRISMA-trAIce + RAISE）於 Stage 2.5 / 4.5。v3.5 新增 **協作深度觀察員**（`collaboration_depth_agent`，僅諮詢性質、永不阻擋流程）於每一次 FULL/SLIM checkpoint 與 pipeline 完成時。MANDATORY 誠信閘門（2.5 / 4.5）明確跳過觀察員，避免稀釋合規檢查。理論基礎：Wang & Zhang (2026), IJETHE 23:11。逐階段矩陣（agent、產出物、閘門）：見 ARCHITECTURE.md §3。

---

## v3.0 優化：我們發現了 AI 的哪些結構性限制

在使用 ARS 撰寫一篇關於 AI 與高教的反思文章時，我們遇到了三個結構性問題：

1. **框架鎖定**：AI 在給定框架內越來越精緻，但無法質疑框架本身
2. **諂媚傾向**：每次挑戰魔鬼代言人的攻擊，它都讓步得太快
3. **意圖偵測錯誤**：蘇格拉底模式在使用者仍在探索時就急著收束

### 改了什麼

- **魔鬼代言人讓步門檻**：反駁必須評分 1-5，≥4 才允許讓步。不允許連續讓步。框架鎖定偵測。
- **蘇格拉底意圖偵測**：偵測使用者是「探索型」還是「目標型」。探索型模式停用自動收束。
- **對話健康度指標**：每 5 輪靜默自檢，偵測持續同意、迴避衝突、過早收束。
- **跨模型驗證**：設定 `ARS_CROSS_MODEL` 啟用第二 AI 模型獨立審查。詳見 [docs/SETUP.zh-TW.md](docs/SETUP.zh-TW.md)。
- **AI 自我反思報告**：Pipeline 結束後自動產出 AI 行為自評。

這些優化不能完全解決 AI 的結構性限制——它們讓限制變得可見、可追蹤、可被人類介入。

---

## 授權條款

本作品採用 [CC-BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 授權。

**你可以自由：**
- 分享 — 複製及散布本作品
- 改作 — 重混、轉換、以本作品為基礎進行創作

**惟須遵守以下條件：**
- **姓名標示** — 你必須給予適當的標示
- **非商業性** — 你不得將本作品用於商業目的

**標示格式：**
```
Based on Academic Research Skills by Cheng-I Wu
https://github.com/Imbad0202/academic-research-skills
```

---

## 貢獻者

**吳政宜** (Cheng-I Wu) — 作者與維護者

**[aspi6246](https://github.com/aspi6246)** — 貢獻者。v3.1 優化靈感來自 [Claude-Code-Skills-for-Academics](https://github.com/aspi6246/Claude-Code-Skills-for-Academics)：唯讀約束模式、Anti-Pattern 作為一等公民設計、認知框架方法（教「如何思考」而非只有步驟）、精簡 skill 尺寸哲學。

**[mchesbro1](https://github.com/mchesbro1)** — 貢獻者。最初提出並撰寫了 IS Basket of 8 期刊清單（[Issue #5](https://github.com/Imbad0202/academic-research-skills/issues/5)）。

**[cloudenochcsis](https://github.com/cloudenochcsis)** — 貢獻者。將 IS 章節從 *Basket of 8* 擴充為完整的 *Senior Scholars' Basket of 11*，補上 *Decision Support Systems*、*Information & Management*、*Information and Organization*（[Issue #7](https://github.com/Imbad0202/academic-research-skills/issues/7)、[PR #8](https://github.com/Imbad0202/academic-research-skills/pull/8)）。資料來源：[AIS Senior Scholars' List of Premier Journals](https://aisnet.org/research/seniorscholarsbasket/)。

**[eltociear](https://github.com/eltociear)**（Ikko Eltociear Ashimine）— 貢獻者。翻譯了日文版 README（[`README.ja-JP.md`](README.ja-JP.md)）（[PR #161](https://github.com/Imbad0202/academic-research-skills/pull/161)）。

**[xpfo-go](https://github.com/xpfo-go)**（xpfo）— 貢獻者。翻譯了簡體中文版 README（[`README.zh-CN.md`](README.zh-CN.md)）（[PR #181](https://github.com/Imbad0202/academic-research-skills/pull/181)）。

---
