# jira-kanban-printer

JIRA の担当者アサインイベントを受けて、担当者ごとのプリンタへ印刷ジョブを振り分ける PoC です。

## 起動

```bash
uvicorn jira_kanban_printer.app:app --app-dir src --reload
```

## Webhook 例

```json
{
  "event_id": "evt-100",
  "issue": {"key": "KAN-100", "summary": "Inspect line"},
  "assignee": {"accountId": "acc-001"}
}
```
