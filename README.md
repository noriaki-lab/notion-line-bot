# Notion LINE 予定通知 Bot

Notionのカレンダーデータベースから明日の予定を取得し、毎晩LINEに通知するBotです。

## 背景

「明日の予定を忘れがち」という課題を解決するために作成しました。通知アプリだと見逃しやすいため、毎日確実に見るLINEに予定を送る仕組みにしています。

## 技術スタック

- **Python 3.11**
- **Notion API** - カレンダーデータベースから予定を取得
- **LINE Messaging API** - プッシュ通知
- **GitHub Actions** - 毎晩の定期実行（サーバーレス）

## アーキテクチャ
```
GitHub Actions (毎晩21時 JST)
    ↓
Notion API で明日の予定を取得
    ↓
LINE Messaging API でプッシュ通知
```

## 通知イメージ
```
📅 明日の予定:
・09:00 チームMTG
・14:00 クライアント打ち合わせ
・タスク: 資料作成
```

## セットアップ

### 1. Notion設定

1. [Notion Integrations](https://www.notion.so/my-integrations) でインテグレーションを作成
2. カレンダー用のデータベースを作成（日付プロパティ: `日付`）
3. データベースの「…」→「コネクト」で作成したインテグレーションを接続

### 2. LINE設定

1. [LINE Developers](https://developers.line.biz/) でMessaging APIチャネルを作成
2. チャネルアクセストークンを発行
3. 自分のLINEユーザーIDを取得

### 3. GitHub設定

1. このリポジトリをフォーク
2. Settings → Secrets and variables → Actions で以下を設定:

| Secret名 | 値 |
|----------|-----|
| `NOTION_API_KEY` | Notionインテグレーションのシークレット |
| `NOTION_DATABASE_ID` | カレンダーDBのID |
| `LINE_ACCESS_TOKEN` | LINEチャネルアクセストークン |
| `LINE_USER_ID` | 通知先のLINEユーザーID |

### 4. 動作確認

Actions → Notify Tomorrow Events → Run workflow で手動実行

## カスタマイズ

### 通知時間の変更

`.github/workflows/notify.yml` の cron を編集:
```yaml
schedule:
  - cron: '0 12 * * *'  # UTC 12:00 = JST 21:00
```

### 日付プロパティ名の変更

`notify.py` の `date_property` を自分のDBに合わせて変更:
```python
date_property = "日付"  # または "Date" など
```

## ライセンス

MIT
