import os
import sys
import csv
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

def main():
    # =============== 設定 ===============
    csv_file = "data.csv"
    output_dir = "納品書・請求書"
    
    # 発行者情報 (固定変数)
    issuer_info = {
        "name": "佐藤 翔太",
        "zip": "〒980-0000",
        "address": "宮城県〇〇市〇〇町1-2-3",
        "tel": "090-XXXX-XXXX",
        "email": "shota.sato@example.com",
        "bank": "〇〇銀行 〇〇支店",
        "account": "普通 1234567 佐藤翔太"
    }
    # ====================================

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(csv_file):
        print(f"エラー: {csv_file} が見つかりません。")
        sys.exit(1)
        
    try:
        with open(csv_file, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"エラー: CSVの読み込みに失敗しました ({e})")
        sys.exit(1)

    env = Environment(loader=FileSystemLoader('.'))
    try:
        invoice_temp = env.get_template('invoice_template.html')
        delivery_temp = env.get_template('delivery_template.html')
    except Exception as e:
        print(f"エラー: テンプレートファイルが見つかりません。({e})")
        sys.exit(1)

    created_count = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for index, row in enumerate(rows):
            company = row.get("会社名", "").strip()
            status = row.get("ステータス", "").strip()
            
            # ステータスが「PDF作成済」ではない行を処理対象とする
            if company and status != "PDF作成済":
                company_name = company
                item = row.get("品目", "")
                amount = row.get("金額", "0").replace(",", "")

                try:
                    amount_formatted = f"¥{int(amount):,}"
                except ValueError:
                    amount_formatted = str(amount)

                render_data = {
                    "company_name": company_name,
                    "item": item,
                    "amount": amount_formatted,
                    "issuer": issuer_info
                }

                # 請求書の出力
                invoice_html = invoice_temp.render(render_data)
                invoice_pdf = os.path.join(output_dir, f"{company_name}_請求書.pdf")
                page.set_content(invoice_html, wait_until="networkidle")
                page.pdf(path=invoice_pdf, format="A4", print_background=True)

                # 納品書の出力
                delivery_html = delivery_temp.render(render_data)
                delivery_pdf = os.path.join(output_dir, f"{company_name}_納品書.pdf")
                page.set_content(delivery_html, wait_until="networkidle")
                page.pdf(path=delivery_pdf, format="A4", print_background=True)

                # ステータスを更新
                rows[index]["ステータス"] = "PDF作成済"
                print(f"出力完了: {company_name}")
                created_count += 1
                
        browser.close()

    # CSVの上書き保存
    if created_count > 0:
        with open(csv_file, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"\n合計 {created_count} 件のPDFを作成しました。")
    else:
        print("新規処理データはありません。")

if __name__ == "__main__":
    main()
