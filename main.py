import asyncio
import re
import html
from playwright.async_api import async_playwright

BASE = "https://livepocket.jp"
MAX_TEST_PAGES = 3  # まずは動作確認用に最初の3ページまでテスト

def _text(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()

def _parse_cards(page_html: str) -> list[dict]:
    cards = []
    # イベントカードのHTMLブロックを抽出
    card_matches = re.findall(r'<li class="event-card-list__item">(.*?)</li>', page_html, re.S)
    for card in card_matches:
        href = re.search(r'href="(/e/[^"]+)"', card)
        if not href:
            continue
        title = re.search(r'event-card__title">(.*?)</h3>', card, re.S)
        place = re.search(r'event-card__place">[^<]*</span>(.*?)</p>', card, re.S)
        cards.append({
            "path": href.group(1),
            "title": _text(title.group(1)) if title else "",
            "tags": sorted(set(re.findall(r'event-card__tag">([^<]+)<', card))),
            "venue": _text(place.group(1)) if place else "",
        })
    return cards

async def test_pagination():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        all_events = {}

        for page_num in range(1, MAX_TEST_PAGES + 1):
            url = f"{BASE}/event/search?sort=1&page={page_num}"
            print(f"Fetching ページ {page_num}: {url}")
            
            try:
                response = await page.goto(url, wait_until="networkidle", timeout=30000)
                if response.status != 200:
                    print(f"⚠️ ステータスコード {response.status} のため中断します")
                    break
                
                # レスポンスが完全に描画されるのを少し待つ
                await page.wait_for_timeout(1500)
                html_content = await page.content()
                
                cards = _parse_cards(html_content)
                print(f" -> 取得成功: {len(cards)}件のカードを検出")
                
                if not cards:
                    print("これ以上カードが見つからないため終了します。")
                    break

                for card in cards:
                    all_events[card["path"]] = card

            except Exception as e:
                print(f"❌ エラー発生 (ページ {page_num}): {e}")
                break

        await browser.close()
        print(f"\n✨ テスト完了！合計 {len(all_events)}件のユニークなイベントを集約しました。")

if __name__ == "__main__":
    asyncio.run(test_pagination())
