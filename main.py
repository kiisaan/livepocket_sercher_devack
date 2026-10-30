import urllib.error
from notifier.web import fetch  # 元の環境と同じfetchを使う場合

BASE = "https://livepocket.jp"

def debug_fetch():
    url = f"{BASE}/event/search?sort=1&page=1"
    print(f"Fetching: {url}")
    try:
        html_content = fetch(url)
        print(f"取得成功！ レスポンス長: {len(html_content)} 文字")
        print("--- 先頭300文字のプレビュー ---")
        print(html_content[:300])
        
        # ボット対策ページやエラーページになっていないかの簡易チェック
        if "captcha" in html_content.lower() or "cloudFlare" in html_content.lower():
            print("⚠️ 注意: ボット対策（Cloudflare等）の画面が返されている可能性があります。")
        elif "event-card-list__item" not in html_content:
            print("⚠️ 注意: 期待するカードのHTML要素が見つかりません。構造が変わった可能性があります。")
        else:
            print("✨ 正常にイベント一覧のHTML構造が含まれています！")
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")

if __name__ == "__main__":
    debug_fetch()
