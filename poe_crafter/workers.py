"""Qt worker wrapper for long-running automation sequences."""

from __future__ import annotations

import threading
from typing import Any

from PySide6.QtCore import QThread, Signal

from .automation import AutomationService


class AutomationWorker(QThread):
    progress = Signal(str)
    completed = Signal(str)
    failed = Signal(str)

    def __init__(self, action: str, settings: dict[str, Any]):
        super().__init__()
        self.action = action
        self.settings = settings
        self.stop_event = threading.Event()

    def run(self) -> None:
        service = AutomationService(self.settings, self.stop_event, self.progress.emit)
        try:
            self.completed.emit(service.run(self.action))
        except Exception as exc:  # noqa: BLE001 - surface automation failures in the UI.
            self.failed.emit(str(exc))
