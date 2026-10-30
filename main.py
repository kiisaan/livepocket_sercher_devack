import requests

BASE = "https://livepocket.jp"

def debug_fetch():
    url = f"{BASE}/event/search?sort=1&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス長: {len(response.text)} 文字")
        print("--- 先頭300文字のプレビュー ---")
        print(response.text[:300])
        
        if response.status_code == 403 or "cloudflare" in response.text.lower():
            print("⚠️ 注意: Cloudflare等のボットブロックが検出されました。")
        elif "event-card-list__item" not in response.text:
            print("⚠️ 注意: 期待するイベントカードのHTML構造が見つかりません。")
        else:
            print("✨ 正常にイベント一覧のHTMLが取得できています！")
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")

if __name__ == "__main__":
    debug_fetch()
