# Claude Code 向け Academic Research Skills

[![Version](https://img.shields.io/badge/version-v3.12.0-blue)](https://github.com/Yougahei/acdemic-resarch-skill-for-CNU/releases/tag/v3.12.0)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

[English](README.md) | [简体中文版](README.zh-CN.md) | [繁體中文版](README.zh-TW.md)

学術研究のための Claude Code スキル統合スイート。研究から論文公開までの全工程をカバーします。

**30秒でインストール**（Claude Code CLI / VS Code / JetBrains、v3.7.0+）:

```text
/plugin marketplace add Yougahei/acdemic-resarch-skill-for-CNU
/plugin install acdemic-resarch-skill-for-CNU
```

その後、`/ars-plan` を試してソクラテス式対話で論文構成を整理するか、前提条件と従来のシンボリックリンク方式については [クイックインストール](#クイックインストール) を参照してください。

> **AI はあなたの副操縦士であり、操縦士ではありません。** このツールはあなたの代わりに論文を書きません。参考文献の探索、引用のフォーマット、データ検証、論理的整合性チェックといった泥臭い作業を引き受けることで、本当に頭を使う必要のある部分 — 問いの定義、手法の選択、データの意味の解釈、「私はこう主張する」に続く文を書くこと — にあなたが集中できるようにします。
>
> 「humanizer」とは異なり、このツールは AI を使った事実を隠すためのものではありません。より良い文章を書くための助けです。Style Calibration は過去の作品からあなたの声を学習します。Writing Quality Check は機械的に見える文章のパターンを検出します。目的は品質であって、ごまかしではありません。

### なぜ完全自動化ではなく Human-in-the-Loop なのか?

Lu ら (2026, *Nature* 651:914-919) は **The AI Scientist** を構築しました — トップレベルの ML 学会（ICLR 2025 workshop、スコア 6.33/10 vs workshop 平均 4.87）でブラインドピアレビューを通過した論文を発表した、初の完全自律型 AI 研究システムです。彼らの Limitations セクションは、完全自律型 AI 研究パイプラインが継承する失敗モードを列挙しています: 実装バグ、結果のハルシネーション、ショートカット依存、バグを洞察として再フレーミング、方法論の捏造、フレームロック、引用のハルシネーション。

ARS は **人間の研究者を AI が支援する形式が、どちらか単独よりもこれらの失敗モードを回避できる** という前提に基づいて構築されています。Stage 2.5 と Stage 4.5 の整合性ゲートは 7 モードのブロッキングチェックリストを実行します（[`academic-pipeline/references/ai_research_failure_modes.md`](academic-pipeline/references/ai_research_failure_modes.md) を参照）。レビュアーはオプトインのキャリブレーションモードを提供し、ユーザー提供のゴールドセットに対して自身の FNR/FPR を測定します。

[**Zhao ら**](https://arxiv.org/abs/2605.07723)（2026-05）は arXiv、bioRxiv、SSRN、PMC の 2.5M 論文にわたる 111M 件の参考文献を監査しました。彼らの保守的見積りでは、2025年だけで 146,932 件のハルシネーション引用が観測され、2024年中頃に変曲点が観測されています。bioRxiv-to-PMC ペアリングでは、プレプリントから出版物への持続率は 85.3% と報告されています。論文は「引用された参考文献が実際には主張していない主張を支持するために配置された実在の引用」を未解決の課題として記述しています。ARS v3.7.1 はソース来歴のための trust-chain frontmatter を追加し、v3.7.3 は将来の主張レベル監査のためのロケーターインフラストラクチャ（三層引用アンカー）を追加し、引用時に advisory リスクシグナルを表面化します（ARS は主張忠実性ギャップを内部で「L3」とラベル付けしています。これは論文の用語ではなく ARS の用語です）。v3.7.x は Zhao らのコーパス規模の発見に動機付けられています。ARS 自体のコーパス規模評価は今後の課題として残されています。

v3.8 は L3 ギャップの後半を閉じます。v3.7.3 は全引用にロケーターアンカーを持たせ、v3.8 はオプトインの監査パス（`ARS_CLAIM_AUDIT=1`）を追加します。これは各アンカーに対して引用元を取得し、主張が実際に裏付けられているかを判断します。5 つの新しい HIGH-WARN クラス（claim-not-supported、negative-constraint-violation、fabricated-reference、anchorless、constraint-violation-uncited）は、formatter ターミナルハードゲートを通じて出力を gate-refuse します。キャリブレーションは 20-tuple のゴールドセットと共に FNR<0.15 + FPR<0.10 の受容閾値で出荷されます。ramp-on 計画は v3.8 spec §5 に従いキャリブレーション後の証拠まで保留されます。

v3.3 は [**PaperOrchestra**](https://arxiv.org/abs/2604.05018)（Song, Song, Pfister & Yoon, 2026, Google）に触発されました: Semantic Scholar API 検証、アンチリーケージプロトコル、VLM 図表検証、スコア軌跡追跡。

---

## アーキテクチャ＆パイプライン

**👉 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — パイプライン全体ビュー: フロー図、ステージごとのマトリクス、データアクセスフロー、スキル依存グラフ、品質ゲート、モードリスト。

アーキテクチャドキュメントは、以前ここにあった煩雑なパイプライン説明を引き継ぎます。*どのステージで何が実行されるか* に関する情報はすべて一箇所に集約されています。

## クイックインストール

**前提条件**

- [Claude Code](https://docs.claude.com/en/docs/claude-code/setup)（最新版。プラグインパッケージングは最近のバージョンが必要）
- `ANTHROPIC_API_KEY` をエクスポート、または初回 `claude` 実行時に設定
- *オプション:* DOCX 用の Pandoc、APA 7.0 PDF 用の tectonic + Source Han Serif TC（Markdown 出力はどちらがなくても動作）

**プラグインインストール（v3.7.0+、推奨）:**

```text
/plugin marketplace add Yougahei/acdemic-resarch-skill-for-CNU
/plugin install acdemic-resarch-skill-for-CNU
```

**動作確認:** `/ars-plan` を実行して取り組んでいる論文について説明してください — ARS がソクラテス式対話を開始し、章構成をマップします。代わりに単発テストを行うには、`/ars-lit-review "your topic"` を試してください。

**👉 [docs/SETUP.md](docs/SETUP.md)** — 完全ガイド: Claude Code インストール、API キー設定、DOCX/PDF 用のオプション Pandoc/tectonic、クロスモデル検証（`ARS_CROSS_MODEL`）、5 つのインストール方法（Plugin、プロジェクトスキル、グローバルスキル、claude.ai Project、リポジトリクローン）。

**Codex CLI を使用していますか?** 代わりに姉妹ディストリビューションをインストールしてください: [`Imbad0202/academic-research-skills-codex`](https://github.com/Imbad0202/academic-research-skills-codex) — 同じワークフローコンテンツ、`ars-*` エイリアスを持つ単一の `$academic-research-suite` スキルとしての Codex ネイティブパッケージング。

## パフォーマンス＆コスト

**👉 [docs/PERFORMANCE.md](docs/PERFORMANCE.md)** — モードごとのトークン予算、フルパイプライン見積り（15k 語の論文で約 $4-6）、推奨 Claude Code 設定（Skip Permissions; Agent Team オプション）。

## ガイド＆記事

- [Academic Writing Shouldn't Be a Solo Act](https://open.substack.com/pub/edwardwu223235/p/academic-writing-shouldnt-be-a-solo?r=4dczl&utm_medium=ios) — 完全なパイプラインウォークスルー（英語）
- [學術寫作不該是一個人的事：一套開源 AI 協作工具如何改變研究者的工作流](https://open.substack.com/pub/edwardwu223235/p/ai?r=4dczl&utm_medium=ios) — 完整使用指南（繁體中文）

---

## 機能概要

- **Deep Research** — 13 エージェントの研究チーム。ソクラテス式ガイドモード、PRISMA システマティックレビュー、意図検出、対話健全性モニタリング、オプションのクロスモデル DA、Semantic Scholar API 検証付き。
- **Academic Paper** — 12 エージェントの論文執筆。Style Calibration、Writing Quality Check、LaTeX ハードニング、可視化、改訂コーチング、引用変換、アンチリーケージプロトコル、VLM 図表検証付き。
- **Academic Paper Reviewer** — 0-100 品質ルーブリックを持つ 7 エージェントの多視点ピアレビュー（EIC + 3 動的レビュアー + Devil's Advocate）、譲歩閾値プロトコル、攻撃強度保持、オプションのクロスモデル DA 批評/キャリブレーション、R&R トレーサビリティマトリクス、read-only 制約。
- **Academic Pipeline** — 10 ステージのパイプラインオーケストレーター。適応的チェックポイント、主張検証、Material Passport、オプションの `repro_lock`、オプションのクロスモデル整合性検証、会話中強化、スコア軌跡追跡付き。
- **Data Access Level Metadata**（v3.3.2+）— 各スキルが `data_access_level`（`raw` / `redacted` / `verified_only`）を宣言。`scripts/check_data_access_level.py` で強制。Anthropic の automated-w2s-researcher（2026）から適応されたパターン。[`shared/ground_truth_isolation_pattern.md`](shared/ground_truth_isolation_pattern.md) を参照。
- **Task Type Annotation**（v3.3.2+）— 各スキルが `task_type`（`open-ended` または `outcome-gradable`）を宣言。現在の ARS スキルはすべて `open-ended`。
- **Benchmark Report Schema**（v3.3.5+）— 誠実なベンチマーク比較のための JSON Schema + lint。[`shared/benchmark_report_pattern.md`](shared/benchmark_report_pattern.md) を参照。
- **Artifact Reproducibility Lockfile**（v3.3.5+）— Material Passport 上のオプションの `repro_lock` サブブロック。**設定ドキュメントであり、再生保証ではありません** — LLM 出力はバイト再現可能ではありません。[`shared/artifact_reproducibility_pattern.md`](shared/artifact_reproducibility_pattern.md) を参照。
- **実験来歴インテーク**（#260）— Material Passport のオプションの `experiment_provenance[]` は、研究者が**外部で**実行した実験を記録し（ARS は実験を実行しません）、論文の主張は `claim_intent_manifest.planned_experiment_ids[]` 経由でそれに join します。整合性ゲート（Stage 2.5/4.5）は実験裏付け主張を宣言された来歴と照合します — `ALIGNED` / `OVERSTATED` / `NOT_SUPPORTED_BY_PROVENANCE` / `PROVENANCE_INSUFFICIENT` — **ただし実験自体の正しさは判定しません**。fail-closed な `experiment_intake_declaration` により「実験を実行したか」が Stage 1 の明示的な決定になります。[`shared/handoff_schemas.md`](shared/handoff_schemas.md) を参照。

---

## ショーケース: 実際のパイプライン出力

実際の 10 ステージパイプライン実行からの完全な成果物を参照してください — ピアレビューレポート、整合性検証レポート、最終論文:

**[すべてのパイプライン成果物を見る →](examples/showcase/)**

| 成果物 | 説明 |
|---|---|
| [Final Paper (EN)](examples/showcase/full_paper_apa7.pdf) | APA 7.0 フォーマット、LaTeX コンパイル済み |
| [Final Paper (ZH)](examples/showcase/full_paper_zh_apa7.pdf) | 中国語版、APA 7.0 |
| [Integrity Report — Pre-Review](examples/showcase/integrity_report_stage2.5.pdf) | Stage 2.5: 捏造参照 15 件 + 統計エラー 3 件を捕捉 |
| [Integrity Report — Final](examples/showcase/integrity_report_stage4.5.pdf) | Stage 4.5: ゼロリグレッションを確認 |
| [Peer Review Round 1](examples/showcase/stage3_review_report.pdf) | EIC + 3 Reviewers + Devil's Advocate |
| [Re-Review](examples/showcase/stage3prime_rereview_report.pdf) | 改訂後の検証 |
| [Peer Review Round 2](examples/showcase/stage3_review_report_r2.pdf) | フォローアップレビュー |
| [Response to Reviewers](examples/showcase/response_to_reviewers_r2.pdf) | ポイントごとの著者回答 |
| [Post-Publication Audit Report](examples/showcase/post_publication_audit_2026-03-09.pdf) | 独立した完全参照監査: 3 回の整合性チェックで見逃された 21/68 件の問題を発見 |

---

## コンパニオン: Experiment Agent

研究に執筆前のコード実行や人間研究が含まれる場合、[Experiment Agent](https://github.com/Imbad0202/experiment-agent) スキルが ARS Stage 1（RESEARCH）と Stage 2（WRITE）の間のギャップを埋めます。

```
ARS Stage 1 RESEARCH  →  RQ Brief + Methodology Blueprint
        ↓
  experiment-agent     →  実験の実行/管理 → 結果検証
        ↓
ARS Stage 2 WRITE     →  検証された実験結果で論文執筆
```

**機能**: コード実験（Python、R など）をリアルタイムモニタリング付きで実行、IRB 倫理チェックリスト付き人間研究プロトコルを管理、11 タイプの誤謬検出付きで統計を解釈、再現性を検証。

**併用方法**: Stage 1 後に ARS パイプラインを一時停止し、別の experiment-agent セッションで実験を実行、その後、結果（Material Passport 付き）を ARS Stage 2 に戻します。ARS は一切の変更を必要としません。セットアップ手順については [experiment-agent README](https://github.com/Imbad0202/experiment-agent) を参照してください。

---

## 使い方

### Quick Start

```
# フル研究パイプラインを開始
You: "I want to write a research paper on AI's impact on higher education QA"

# ソクラテス式ガイダンスで開始
You: "Guide my research on AI in educational evaluation"

# ガイド付きプランニングで論文を執筆
You: "Guide me through writing a paper on demographic decline"

# 既存論文をレビュー
You: "Review this paper"（その後、論文を提供）

# パイプラインステータスを確認
You: "status"
```

### 個別スキル

#### Deep Research（7 モード）

```
"Research the impact of AI on higher education"       → full モード
"Give me a quick brief on X"                          → quick モード
"Do a systematic review on X with PRISMA"             → systematic-review モード
"Guide my research on X"                              → socratic モード（ガイド付き）
"Fact-check these claims"                             → fact-check モード
"Do a literature review on X"                         → lit-review モード
"Review this paper's research quality"                → review モード
```

#### Academic Paper（10 モード）

```
"Write a paper on X"                                  → full モード
"Guide me through writing a paper"                    → plan モード（ガイド付き）
"Build a paper outline"                               → outline-only モード
"I have a draft, here are reviewer comments"          → revision モード
"Parse these reviewer comments into a roadmap"        → revision-coach モード
"Write an abstract for this paper"                    → abstract-only モード
"Turn this into a literature review paper"            → lit-review モード
"Convert to LaTeX" / "Convert citations to IEEE"      → format-convert モード
"Check citations"                                     → citation-check モード
"Generate an AI disclosure statement for NeurIPS"     → disclosure モード
```

#### Academic Paper Reviewer（6 モード）

```
"Review this paper"                                   → full モード（EIC + R1/R2/R3 + Devil's Advocate）
"Quick assessment of this paper"                      → quick モード
"Guide me to improve this paper"                      → guided モード
"Check the methodology"                               → methodology-focus モード
"Verify the revisions"                                → re-review モード
"Calibrate this reviewer against my gold set"         → calibration モード
```

#### Academic Pipeline（オーケストレーター）

```
"I want to write a complete research paper"           → Stage 1 からのフルパイプライン
"I already have a paper, review it"                   → Stage 2.5 で中間エントリー（整合性優先）
"I received reviewer comments"                        → Stage 4 で中間エントリー
```

> パイプラインは **Stage 6: Process Summary** で終了します — 6 次元の Collaboration Quality Evaluation（1-100 採点）付きの論文作成プロセスレコードを自動生成します。

### サポート言語

- **繁體中文** — ユーザーが中国語で書く場合のデフォルト
- **English** — ユーザーが英語で書く場合のデフォルト
- 学術論文用のバイリンガル要旨（中国語 + 英語）

> **異なる言語を使用していますか?** ソクラテスモード（deep-research）と Plan モード（academic-paper）は **意図ベースのアクティベーション** を使用します — リクエストの意味を検出し、特定のキーワードではありません。これは **どの言語でも** 変更なしで動作することを意味します。
>
> ただし、一般的な `Trigger Keywords` セクション（スキルがそもそも有効化されるかを決定する）は依然として英語と繁體中文のキーワードを列挙しています。あなたの言語でスキルが確実に有効化されない場合、各 `SKILL.md` ファイルの `### Trigger Keywords` セクションにあなたの言語のキーワードを追加してマッチング信頼度を向上させることができます。

### サポートされる引用フォーマット

- APA 7.0（デフォルト、中国語引用ルール含む）
- Chicago（Notes & Author-Date）
- MLA
- IEEE
- Vancouver

### サポートされる論文構造

- IMRaD（実証研究）
- Thematic Literature Review
- Theoretical Analysis
- Case Study
- Policy Brief
- Conference Paper

---

## スキル詳細

エージェントごとの責務とステージごとの成果物は [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) に集約されました。リリースメタデータを一箇所にまとめるため、バージョン番号はここにアンカーされています。

### Deep Research（v2.9.4）

13 エージェントの研究チーム。モード: full、quick、review、lit-review、fact-check、socratic、systematic-review。完全なエージェント名簿と成果物: ARCHITECTURE.md §3 を参照。

### Academic Paper（v3.2.0）

12 エージェントの論文執筆パイプライン。モード: full、plan、outline-only、revision、revision-coach、abstract-only、lit-review、format-convert、citation-check、disclosure。出力: MD + DOCX（利用可能な場合 Pandoc 経由）+ LaTeX（APA 7.0 `apa7` クラス / IEEE / Chicago）→ tectonic 経由 PDF。完全なエージェント名簿とフェーズごとの責務: ARCHITECTURE.md §3 を参照。

### Academic Paper Reviewer（v1.10.0）

**0-100 品質ルーブリック** を持つ 7 エージェントの多視点レビュー。モード: full、re-review、quick、methodology-focus、guided、calibration。**決定マッピング:** ≥80 Accept、65-79 Minor Revision、50-64 Major Revision、<50 Reject。初回レビューチーム vs. 限定的な再レビューチームの境界: ARCHITECTURE.md §3 Stage 3 / Stage 3' を参照。

### Academic Pipeline（v3.12.0）

整合性検証、二段階レビュー、ソクラテス式コーチング、コラボレーション評価を持つ 10 ステージのオーケストレーター。パイプライン保証: 各ステージにユーザー確認チェックポイントが必要。整合性検証（Stage 2.5 + 4.5）はスキップできない。R&R Traceability Matrix（Schema 11）は著者の改訂主張を独立に検証する。v3.4 は Stage 2.5 / 4.5 に Compliance Agent（PRISMA-trAIce + RAISE）を追加した。v3.5 はすべての FULL/SLIM チェックポイントとパイプライン完了時に **Collaboration Depth Observer**（`collaboration_depth_agent`、advisory のみ — 決してブロックしない）を追加する。MANDATORY 整合性ゲート（2.5 / 4.5）は、コンプライアンスチェックが希薄化されないよう observer を明示的にスキップする。Wang & Zhang（2026）, IJETHE 23:11 に基づく。エージェント、成果物、ゲートを含むステージごとのマトリクス: ARCHITECTURE.md §3 を参照。

---

## v3.0 最適化: AI の構造的限界について発見したこと

### 何が起きたか

高等教育における AI に関する反省記事を書くために ARS を使用していたとき、プロンプトエンジニアリングでは修正できない 3 つの構造的問題に遭遇しました:

1. **フレームロック**: AI に自分の論題に対して devil's advocate ディベートを実行するよう依頼しました。それは実行されました — 4 ラウンド、各ラウンドが前よりも洗練されていました。しかし、すべてのラウンドが私が設定したフレーム内に留まりました。DA は議論を攻撃しましたが、前提を攻撃しませんでした。「そもそも正しい問いを議論しているのか?」と尋ねることは決してありませんでした。これは v2.7 のストレステストで 31% の引用エラー率を引き起こしたのと同じパターンです: 検証する AI と生成する AI は同じ認知フレームを共有しています。

2. **プッシュバック下のシコファンシー**: DA の攻撃に異議を唱えるたびに、すぐに譲歩しすぎました。発見を立ち上げるよりも早く撤回しました。モデルのトレーニングは会話の調和を報酬としているため、「ユーザーがプッシュバックした」ことは攻撃が間違っていた証拠として扱われましたが、多くの場合、それは単にユーザーが粘り強かったことを意味していました。

3. **意図の誤検出**: Socratic Mentor は、私がまだ探索中であるのに、収束して成果物を生成しようとし続けました（「これをまとめましょうか?」）。「ユーザーは深い哲学的議論を望んでいる」と「ユーザーは RQ ブリーフを望んでいる」を区別できませんでした。両方ともエンゲージメントのように見えますが、反対の AI 動作を必要とします。

### 何を変更したか（v3.0）

**Devil's Advocate — 譲歩閾値プロトコル**（`deep-research` + `academic-paper-reviewer`）
- DA は応答前にすべての反論を 1-5 スケールでスコアリングする必要があります
- 譲歩はスコア ≥4（反論が証拠とともに核心攻撃に直接対処）でのみ許可
- スコア ≤3: ポジションを保持し、元の攻撃を再述
- アンチシコファンシールール: 連続譲歩なし、譲歩率追跡、各チェックポイント後のフレームロック検出

**Socratic Mentor — 意図検出層**（`deep-research`）
- 対話開始時と 3 ターンごとにユーザー意図を探索的 vs. 目標指向に分類
- 探索モード: 自動収束を無効化、最大ラウンドを 60 に引き上げ、「まとめましょうか?」プロンプトを禁止
- 目標指向モード: 標準の収束動作
- 早期終了防止ルール: 探索モードでは、ユーザーが停止のタイミングを決定

**Socratic Mentor — 対話健全性インジケーター**（`deep-research`）
- 5 ターンごとに 3 次元でサイレント自己評価: 持続的同意、対立回避、早期収束
- 同意パターンが検出されると、挑戦的な質問を自動注入
- ユーザーには不可視（ゲーミング防止のため）、ただしポストセッションレビュー用のログ利用可能

### なぜ重要か

これらの最適化は AI の構造的限界を解決するわけではありません — 限界を可視化し管理可能にします。DA はまだ十分に押されれば最終的に譲歩します。Socratic Mentor にはまだいくらかの収束バイアスがあります。しかし今や、シコファンシーを遅延させ、DA に譲歩を正当化させ、Mentor がユーザーの準備が整う前にまとめてしまうのを防ぐ明示的なチェックポイントが存在します。

より深い教訓: AI リテラシーとは、AI をツールとして使うことを学ぶこと、倫理ルールに従うこと、AI リスクを恐れることではありません。AI と十分に深く関わって、自分でその構造的限界 — そしてそのプロセスで自分自身の思考の限界 — を発見することです。

---

## ライセンス

この作品は [CC-BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) でライセンスされています。

**あなたは以下を自由に行うことができます:**
- 共有 — 素材をコピーおよび再配布
- 翻案 — 素材をリミックス、変換、構築

**以下の条件の下で:**
- **表示** — 適切なクレジットを付与する必要があります
- **非商用** — 素材を商業目的で使用してはなりません

**表示フォーマット:**
```
Based on Academic Research Skills by Cheng-I Wu
https://github.com/Imbad0202/academic-research-skills
```

---

## 貢献者

**Cheng-I Wu**（吳政宜）— 著者およびメンテナー

**[aspi6246](https://github.com/aspi6246)** — 貢献者。v3.1 最適化は [Claude-Code-Skills-for-Academics](https://github.com/aspi6246/Claude-Code-Skills-for-Academics) のパターンに触発されました: read-only 制約パターン、ファーストクラス設計としてのアンチパターン体系化、認知フレームワークアプローチ（手順だけでなく「考え方」を教える）、リーンなスキルサイズ哲学。

**[mchesbro1](https://github.com/mchesbro1)** — 貢献者。`academic-paper-reviewer/references/top_journals_by_field.md` 用の IS Basket of 8 ジャーナルを最初に提案・起草（[Issue #5](https://github.com/Imbad0202/academic-research-skills/issues/5)）。

**[cloudenochcsis](https://github.com/cloudenochcsis)** — 貢献者。IS セクションを *Basket of 8* から完全な *Senior Scholars' Basket of 11* に拡張 — *Decision Support Systems*、*Information & Management*、*Information and Organization* を追加（[Issue #7](https://github.com/Imbad0202/academic-research-skills/issues/7)、[PR #8](https://github.com/Imbad0202/academic-research-skills/pull/8)）。出典: [AIS Senior Scholars' List of Premier Journals](https://aisnet.org/research/seniorscholarsbasket/)。

**[eltociear](https://github.com/eltociear)**（Ikko Eltociear Ashimine）— 貢献者。日本語版 README（[`README.ja-JP.md`](README.ja-JP.md)）を翻訳（[PR #161](https://github.com/Imbad0202/academic-research-skills/pull/161)）。

---
