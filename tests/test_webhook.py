from fastapi.testclient import TestClient

from jira_kanban_printer.app import app


def test_webhook_routes_to_mapped_printer() -> None:
    client = TestClient(app)
    payload = {
        "event_id": "evt-1",
        "issue": {"key": "KAN-1", "summary": "Check conveyor"},
        "assignee": {"accountId": "acc-001"},
    }

    response = client.post("/webhooks/jira", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
    assert response.json()["printer_id"] == "printer-warehouse-a"


def test_webhook_deduplicates_event() -> None:
    client = TestClient(app)
    payload = {
        "event_id": "evt-dup",
        "issue": {"key": "KAN-2", "summary": "Refill labels"},
        "assignee": {"accountId": "acc-999"},
    }

    first = client.post("/webhooks/jira", json=payload)
    second = client.post("/webhooks/jira", json=payload)

    assert first.status_code == 200
    assert first.json()["status"] == "queued"
    assert first.json()["printer_id"] == "printer-general"

    assert second.status_code == 200
    assert second.json() == {"status": "duplicate", "event_id": "evt-dup"}
