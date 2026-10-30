import requests
import re

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
        
        # HTML内にどんなクラス名（class="..."）があるか、それらしいものをいくつか抽出して表示
        classes = set(re.findall(r'class="([^"]*event[^"]*)"', response.text))
        print("--- 'event' を含むクラス名の一覧 ---")
        for c in sorted(classes)[:30]:  # 多すぎるので先頭30個
            print(f" - {c}")
            
        # もし全く見つからない場合はHTML全体の一部をダンプ
        if not classes:
            print("--- 'event' を含むクラス名が1つも見つかりませんでした。HTMLの先頭1000文字 ---")
            print(response.text[:1000])
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")

if __name__ == "__main__":
    debug_fetch()
