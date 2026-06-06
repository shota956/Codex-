---
description: 納品書・請求書自動化システムのセットアップとPDF生成
---

以下の手順で、自動化システムの環境構築と実行を行います。
このファイルは旧エージェント向けの参照用です。Codex では `AGENTS.md` と `.codex/skills/invoice-pdf-workflow/` を優先してください。

1. 必要なライブラリをインストールする
// turbo
run_command(CommandLine="python3 -m pip install -r requirements.txt", Cwd="/Users/shota/Documents/New project", SafeToAutoRun=true, WaitMsBeforeAsync=0)

2. Playwright のブラウザエンジンをインストールする
// turbo
run_command(CommandLine="python3 -m playwright install chromium", Cwd="/Users/shota/Documents/New project", SafeToAutoRun=true, WaitMsBeforeAsync=0)

3. システムを実行してPDFを生成する
// turbo
run_command(CommandLine="python3 generate_pdf.py", Cwd="/Users/shota/Documents/New project", SafeToAutoRun=true, WaitMsBeforeAsync=0)
