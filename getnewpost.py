from requests_html import HTMLSession, AsyncHTMLSession

newpost: dict = {}  # 新着記事

# セッション開始
session = HTMLSession()
url = "https://nemlog.nem.social/guest"
r = session.get(url)

# HTMLを生成
r.html.render(timeout=30)  # デフォルトだとタイムアウトが頻発する
selector = "div.blog-card-wrapper"

items = r.html.find(selector, first=False)
for i in items:
    title = i.text.splitlines()[2]
    print(f"記事タイトル: {title}")
    url = list(i.absolute_links)[0]
    print(f"記事URL: {url}")
    # print(f"画像を含む情報: {i.find('img')[1]}")
    newpost = {"title": title, "url": url}
    break  # 1件だけ

print(f"新着記事: {newpost}")
