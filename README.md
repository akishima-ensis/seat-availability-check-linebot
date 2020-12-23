# seat-availability-check-linebot

<a href="https://lin.ee/e3L1AGH"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png" alt="友だち追加" height="36" border="0"></a>

🐳 アキシマエンシス（昭島市教育福祉総合センター）における学習室の空席状況を調べることができるLINE Bot

## Demo
![](https://user-images.githubusercontent.com/34241526/102971274-70567280-453c-11eb-8d03-c46944e2844d.png)
## DataSource

[昭島市民図書館 - WEB予約](https://webreserv.library.akishima.tokyo.jp/webReserv/AreaInfo/Login)

使用しているデータは昭島市民図書館の公式サイトから取得したものです。当該プログラムはこのサイトのHTMLに依存しているためサイトの仕様が変更された場合、正常に動かなくなる可能性があります。

## Features
{学習室名}には```学習席（有線LAN有）```、```学習席```、```研究個室```、```インターネット・DB席```、```グループ学習室```、```ティーンズ学習室```のいずれかが入ります。空席通知予約は予約から1時間以内に空席ができなかった場合、閉館時間になった場合自動的にキャンセルされます。通常はリッチメニューから{学習室名}をタッチするだけで入力できるのでキーボードを使った入力は不要です。

```
input  > {学習室名}
output > 入力された学習室の空席状況を出力します。

input  > {学習室名} 予約
output > 学習室が満席だった場合、空席ができたら通知を行う予約を行います。

input  > {学習室名} 新規予約
output > 既に空席通知予約が行われていた場合その予約をキャンセルして新規に予約を行います。
```
## How it works
クライアントから受け取ったメッセージから学習室名を抽出、受け取った学習室名の空席状況をCloudFirestoreから取得、返信用のメッセージを生成しクライアントに返すというスクリプトです。このスクリプトはAppEngineにホスティングされています。

![](https://user-images.githubusercontent.com/34241526/102971513-e064f880-453c-11eb-9fef-a13d96e7459f.png)

[diagrams.net](https://app.diagrams.net/)
