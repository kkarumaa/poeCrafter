"""Pure helpers for parsing copied Path of Exile item text."""

from __future__ import annotations


def extract_socket_colors(clipboard_content: str) -> tuple[int, int, int]:
    for line in clipboard_content.splitlines():
        if line.startswith("Sockets:"):
            return line.count("G"), line.count("R"), line.count("B")
    return 0, 0, 0


def extract_link_count(clipboard_content: str) -> int:
    for line in clipboard_content.splitlines():
        if line.startswith("Sockets:"):
            return max((group.count("-") for group in line.split()[1:]), default=0)
    return 0
