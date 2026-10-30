import asyncio
from playwright.async_api import async_playwright

BASE = "https://livepocket.jp"

async def debug_fetch_playwright():
    url = f"{BASE}/event/search?sort=1&page=1"
    async with async_playwright() as p:
        # ヘッドレスブラウザを起動（必要に応じて headless=False で視覚的に確認も可能）
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print(f"Navigating to: {url}")
        try:
            # WAFのJSチャレンジが自動実行されるのを待つため、networkidleなどを指定
            response = await page.goto(url, wait_until="networkidle", timeout=30000)
            print(f"ステータスコード: {response.status}")
            
            # 少し待機してWAFクリア後のコンテンツを描画させる
            await page.wait_for_timeout(3000)
            
            html_content = await page.content()
            print(f"レスポンスの長さ: {len(html_content)} 文字")
            
            # イベントカードが含まれているかチェック
            if "event-card-list__item" in html_content:
                print("✨ 成功！WAFを突破し、イベントカードのHTML構造が取得できました！")
            else:
                print("⚠️ まだイベントカードが見つかりません。画面のスクリーンショットなどを確認してみてください。")
                
        except Exception as e:
            print(f"❌ エラー発生: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_fetch_playwright())
