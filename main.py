"""Application entry point. Importing this module does not start the UI."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from poe_crafter.ui import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("PoE Crafter")
    app.setOrganizationName("PoE Crafter")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
