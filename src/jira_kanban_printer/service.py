from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .config import ASSIGNEE_PRINTER_MAP, SETTINGS


@dataclass(frozen=True)
class PrintJob:
    issue_key: str
    summary: str
    assignee_account_id: str
    printer_id: str
    created_at: datetime


class IdempotencyStore:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def mark_once(self, event_id: str) -> bool:
        """Returns True only when event_id is first seen."""
        if event_id in self._seen:
            return False
        self._seen.add(event_id)
        return True


class PrintDispatcher:
    def __init__(self) -> None:
        self.jobs: list[PrintJob] = []

    def resolve_printer(self, assignee_account_id: str) -> str:
        return ASSIGNEE_PRINTER_MAP.get(assignee_account_id, SETTINGS.default_printer)

    def create_job(self, issue_key: str, summary: str, assignee_account_id: str) -> PrintJob:
        job = PrintJob(
            issue_key=issue_key,
            summary=summary,
            assignee_account_id=assignee_account_id,
            printer_id=self.resolve_printer(assignee_account_id),
            created_at=datetime.now(timezone.utc),
        )
        self.jobs.append(job)
        return job
