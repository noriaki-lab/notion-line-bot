import os
from datetime import datetime, timedelta, timezone
import httpx

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
LINE_ACCESS_TOKEN = os.environ["LINE_ACCESS_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]

# 日本時間
JST = timezone(timedelta(hours=9))


def get_tomorrow_events():
    now = datetime.now(JST)
    tomorrow = now.date() + timedelta(days=1)
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(days=1)).isoformat()
    
    date_property = "日付"  # 自分のDBに合わせる
    
    response = httpx.post(
        f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query",
        headers={
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        json={
            "filter": {
                "property": date_property,
                "date": {
                    "on_or_after": start,
                    "before": end,
                }
            },
            "sorts": [{"property": date_property, "direction": "ascending"}]
        }
    )
    
    data = response.json()
    print(f"Query date: {start}")  # デバッグ用
    print(f"Response: {data}")      # デバッグ用
    
    events = []
    for page in data.get("results", []):
        title_prop = page["properties"].get("名前") or page["properties"].get("Name")
        if title_prop and title_prop["title"]:
            title = title_prop["title"][0]["plain_text"]
        else:
            title = "（無題）"
        
        time_str = ""
        date_prop = page["properties"].get(date_property)
        if date_prop and date_prop.get("date"):
            date_start = date_prop["date"].get("start", "")
            if "T" in date_start:
                time_str = date_start.split("T")[1][:5]
        
        events.append({"title": title, "time": time_str})
    
    return events


def send_line_message(text: str):
    response = httpx.post(
        "https://api.line.me/v2/bot/message/push",
        headers={
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "to": LINE_USER_ID,
            "messages": [{"type": "text", "text": text}]
        }
    )
    print(f"LINE API response: {response.status_code} {response.text}")


def main():
    events = get_tomorrow_events()
    
    if events:
        lines = []
        for e in events:
            if e["time"]:
                lines.append(f"・{e['time']} {e['title']}")
            else:
                lines.append(f"・{e['title']}")
        msg = "📅 明日の予定:\n" + "\n".join(lines)
    else:
        msg = "明日の予定はありません"
    
    send_line_message(msg)
    print(f"Sent: {msg}")


if __name__ == "__main__":
    main()
