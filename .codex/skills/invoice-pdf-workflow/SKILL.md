---
name: invoice-pdf-workflow
description: Use when working on the CSV-to-PDF invoice and delivery-note automation in this workspace, including setup, execution, template edits, issuer-info updates, CSV schema changes, or PDF generation troubleshooting.
---

# Invoice PDF Workflow

Use this skill for any task involving `generate_pdf.py`, `data.csv`, `invoice_template.html`, or `delivery_template.html`.

## Quick Start

1. Read `AGENTS.md` first for the repo rules.
2. Inspect the files relevant to the request:
   - `generate_pdf.py` for logic or issuer profile changes
   - `data.csv` for source data questions
   - `invoice_template.html` and `delivery_template.html` for design changes
3. If setup is needed, run:
   - `python3 -m pip install -r requirements.txt`
   - `python3 -m playwright install chromium`
4. For a safe validation pass, prefer `python3 -m py_compile generate_pdf.py`.

## Project-Specific Rules

- `generate_pdf.py` writes PDFs and updates `data.csv`, so avoid running it unless the user expects those changes.
- The CSV columns `会社名`, `品目`, `金額`, `ステータス` are the current contract. If that contract changes, update the script and templates together.
- Preserve the skip rule for rows already marked `PDF作成済` unless asked otherwise.

## Common Change Patterns

### Issuer info

Edit the `issuer_info` dictionary in `generate_pdf.py`.

### PDF design

Edit `invoice_template.html` and/or `delivery_template.html`. Keep shared styling decisions consistent between both templates unless the user asks for them to diverge.

### CSV schema changes

Update:

1. CSV parsing in `generate_pdf.py`
2. Data passed into `render_data`
3. Template placeholders that render the new fields

## Troubleshooting

- If PDFs do not generate, verify installed dependencies and Chromium first.
- If text renders incorrectly, inspect the template font configuration and the local environment's Japanese font availability.
- If a template is missing, check that both HTML templates still live beside `generate_pdf.py`.
