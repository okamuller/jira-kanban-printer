from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .service import IdempotencyStore, PrintDispatcher

app = FastAPI(title="Jira Kanban Printer", version="0.1.0")
idempotency = IdempotencyStore()
dispatcher = PrintDispatcher()


class IssuePayload(BaseModel):
    key: str
    summary: str


class AssigneePayload(BaseModel):
    accountId: str = Field(min_length=1)


class WebhookPayload(BaseModel):
    event_id: str = Field(min_length=1)
    issue: IssuePayload
    assignee: AssigneePayload


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhooks/jira")
def jira_webhook(payload: WebhookPayload) -> dict[str, str]:
    if not idempotency.mark_once(payload.event_id):
        return {"status": "duplicate", "event_id": payload.event_id}

    job = dispatcher.create_job(
        issue_key=payload.issue.key,
        summary=payload.issue.summary,
        assignee_account_id=payload.assignee.accountId,
    )
    if not job.printer_id:
        raise HTTPException(status_code=500, detail="printer resolution failed")

    return {
        "status": "queued",
        "event_id": payload.event_id,
        "issue_key": job.issue_key,
        "printer_id": job.printer_id,
    }
