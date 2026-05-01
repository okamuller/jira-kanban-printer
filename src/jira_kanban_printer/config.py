from dataclasses import dataclass


@dataclass(frozen=True)
class PrinterSettings:
    default_printer: str


ASSIGNEE_PRINTER_MAP = {
    "acc-001": "printer-warehouse-a",
    "acc-002": "printer-warehouse-b",
}

SETTINGS = PrinterSettings(default_printer="printer-general")
