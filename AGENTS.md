# Invoice PDF Automation

This `AGENTS.md` is the Codex-facing source of truth for this workspace. It supersedes the older `AGENT_INSTRUCTIONS.md` and `.agent/workflows/` files when Codex is deciding how to work in this project.

## Project Purpose

This workspace generates invoice and delivery-note PDFs from `data.csv` by rendering Jinja2 HTML templates and exporting them with Playwright.

## Important Files

- `generate_pdf.py`: main script
- `data.csv`: source rows with `会社名`, `品目`, `金額`, `ステータス`
- `invoice_template.html`: invoice layout
- `delivery_template.html`: delivery-note layout
- `納品書・請求書/`: output directory

## Standard Commands

- Install Python dependencies: `python3 -m pip install -r requirements.txt`
- Install Playwright browser: `python3 -m playwright install chromium`
- Run PDF generation: `python3 generate_pdf.py`
- Safe syntax check: `python3 -m py_compile generate_pdf.py`

## Working Rules

- Treat `data.csv` as user data. Running `generate_pdf.py` mutates the `ステータス` column and writes PDFs, so do not run it casually during investigation.
- Keep the CSV schema aligned with the code and templates. If a column is added or renamed, update `generate_pdf.py` and every affected template together.
- Keep the processing rule that rows with `ステータス == PDF作成済` are skipped unless the user explicitly asks to change that behavior.
- Issuer profile changes belong in the `issuer_info` dictionary inside `generate_pdf.py`.
- Layout or typography changes belong in `invoice_template.html` and `delivery_template.html`.

## Verification Guidance

- Prefer `python3 -m py_compile generate_pdf.py` for no-side-effect validation.
- If an end-to-end run is necessary, tell the user that `data.csv` and the output PDFs will change.
- When debugging PDF failures, check Python dependencies first, then Playwright/Chromium installation, then template loading.

## Codex Surfaces In This Repo

- Durable repo instructions live here in `AGENTS.md`.
- Reusable workflow knowledge lives in `.codex/skills/invoice-pdf-workflow/SKILL.md`.
- Legacy helper files in `AGENT_INSTRUCTIONS.md` and `.agent/workflows/` are retained as references, but Codex should prefer the two surfaces above.
