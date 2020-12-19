# Qiitaアドベントカレンダー2020年12月20日用の記事


## はじめに

nemlogの新着記事のタイトルとURLをLineで通知する方法を簡単に紹介します。

この手法はスクレイピングを使っていますので、もし、ご紹介したコードをご利用する前、にnemlog管理者の「しゅうさん」に必ず了解を得ましょう。
私は忘れてしまったので、事後報告とともに「しゅうさん」にご連絡するつもりです。

動作確認はUbuntu 20.04LTSで行っています。

```
(venv) nao@330:~/naoland/advent20201220$ neofetch
            .-/+oossssoo+/-.               nao@330
        `:+ssssssssssssssssss+:`           -------
      -+ssssssssssssssssssyyssss+-         OS: Ubuntu 20.04.1 LTS x86_64
    .ossssssssssssssssssdMMMNysssso.       Host: 81D0 Lenovo ideapad 330-14IGM
   /ssssssssssshdmmNNmmyNMMMMhssssss/      Kernel: 5.4.0-58-generic
  +ssssssssshmydMMMMMMMNddddyssssssss+     Uptime: 1 day, 15 hours, 47 mins
 /sssssssshNMMMyhhyyyyhmNMMMNhssssssss/    Packages: 1684 (dpkg), 15 (snap)
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Shell: bash 5.0.17
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   Resolution: 1366x768
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   Terminal: /dev/pts/0
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   CPU: Intel Celeron N4100 (4) @ 2.400GHz
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   GPU: Intel UHD Graphics 605
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Memory: 2427MiB / 3758MiB
 /sssssssshNMMMyhhyyyyhdNMMMNhssssssss/
  +sssssssssdmydMMMMMMMMddddyssssssss+
   /ssssssssssshdmNNNNmyNMMMMhssssss/
    .ossssssssssssssssssdMMMNysssso.
      -+sssssssssssssssssyyyssss+-
        `:+ssssssssssssssssss+:`
            .-/+oossssoo+/-.

```

Python環境は導入済みであることを前提として、以降の説明をすすめていきます。

## 事前準備

> sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev

JavaScriptによって動的に生成される新着記事を取得するために、Pythonパッケージをインストールします。

> pip install requests_html

pipは事前にアップデートしておいた方がよいかもしれません。


## nemlogの新着記事を取得

次のPythonコードを`getnewpost.py`として任意の場所に保存してください

```python
from requests_html import HTMLSession, AsyncHTMLSession

newpost: dict = {}

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
    url = list(i.absolute_links)[0]
    newpost = {"title": title, "url": url}
    break  # 1件だけ

print(f"新着ポスト: {newpost}")
```
このコードでは説明の便宜上、適切なエラー処理を行っていません。

次のようにコードを実行します。

> python getnewpost.py

初回のプログラム実行時には、ヘッドレスchromiumがダウンロードされます。

```
[W:pyppeteer.chromium_downloader] start chromium download.
Download may take a few minutes.
100%|███████████████████████████████████████████████████████████████████████████████████████████| 108773488/108773488 [03:24<00:00, 531491.68it/s]
[W:pyppeteer.chromium_downloader] 
chromium download done.
```

しかし、初回のプログラム実行時には次のようにタイムアウトエラーが発生するかもしれません。

```
(venv) $ python getnewpost.py 
Traceback (most recent call last):
  File "getnewpost.py", line 9, in <module>
    r.html.render(timeout=30)  # デフォルトだとタイムアウトが頻発する
  File "/home/nao/naoland/advent20201220/venv/lib/python3.8/site-packages/requests_html.py", line 598, in render
    content, result, page = self.session.loop.run_until_complete(self._async_render(url=self.url, script=script, sleep=sleep, wait=wait, content=self.html, reload=reload, scrolldown=scrolldown, timeout=timeout, keep_page=keep_page))
  File "/usr/local/lib/python3.8/asyncio/base_events.py", line 616, in run_until_complete
    return future.result()
  File "/home/nao/naoland/advent20201220/venv/lib/python3.8/site-packages/requests_html.py", line 512, in _async_render
    await page.goto(url, options={'timeout': int(timeout * 1000)})
  File "/home/nao/naoland/advent20201220/venv/lib/python3.8/site-packages/pyppeteer/page.py", line 885, in goto
    raise error
pyppeteer.errors.TimeoutError: Navigation Timeout Exceeded: 30000 ms exceeded.
```

私もタイムアウトエラーが発生したのですが、何度実行しなおしても同じエラーが発生していました

そのため、タイムアウトを30秒に指定しましたが、たまにタイムアウトエラーが発生します。

このコードの正常な実行結果は次のようになります。

```
(venv) $ python getnewpost.py 
新着ポスト: {'title': 'ネムツア12/19 空き時間でランと筋トレ', 'url': 'https://nemlog.nem.social/blog/53235'}
```

ご紹介したコードでは1件のみの新着情報を




## Lineで通知する
## 今後の改良点

今回の記事では新着記事1件のみを取得していますが、お好みの件数分取得したり、前回の記事取得時から更新された分だけ取得するなど、工夫してみるとよいでしょう。

nemlogの新着記事を定期的ににチェックして、Lineで通知します。

## 最後に

ご紹介した整理後のコードを見るととても簡単そうに見えますが、作成中は`requests_html`が返すオブジェクトの中身を逐一チェックして調整をおこなっています。
結構面倒くさかったです。 

新着記事の箇所を見つけるために、

> selector = "div.blog-card-wrapper"

という「CSSセレクター」を指定していますが、「XPath」という方式で指定する方法もあります。

この記事ではスクレイピングについては詳しく説明していませんが、興味のある方は`スクレイピング` というキーワードでググってみてください。


いや～、こういう処理には`Python`はもってこいですね！

## 参考情報へのリンク

- [psf/requests-html: Pythonic HTML Parsing for Humans™](https://github.com/psf/requests-html)
- [nemlog|暗号通貨 nemを使用した寄付機能付きブログコミュニケーションブログコミュニケーションプラットフォーム](https://nemlog.nem.social/guest)
- [LINE Notify](https://notify-bot.line.me/ja/)