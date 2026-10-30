import requests

BASE = "https://livepocket.jp"

def debug_fetch():
    url = f"{BASE}/event/search?sort=1&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    }
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンスの長さ: {len(response.text)} 文字")
        print("=== HTMLの先頭 1000文字 ===")
        print(response.text[:1000])
        print("==========================")
        
    except Exception as e:
        print(f"❌ エラー発生: {e}")

if __name__ == "__main__":
    debug_fetch()
