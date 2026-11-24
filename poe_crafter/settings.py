"""Load and persist user settings while preserving legacy PoE Crafter data."""

from __future__ import annotations

import json
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

DEFAULT_SETTINGS: dict[str, Any] = {
    "language": "fr",
    "random_delay": False,
    "craft_delay": 0.07,
    "disable_mouse_teleport": False,
    "stop_if_no_currency": False,
    "mouse_move_time": 0.2,
    "stash_items_after_craft": False,
    "currency_tab_id": "",
    "compass_tab_id": "",
    "item_tab_id": "",
    "map_tab_id": "",
    "set_item": "",
    "currency_button_states": {},
    "chain_beast_points": [],
    "set_beast": "",
    "div_card_points": [],
    "set_trade": "",
    "set_confirm": "",
}


class SettingsStore:
    """Store app settings in the current user's roaming application data."""

    def __init__(self, legacy_path: Path | None = None, path: Path | None = None):
        if legacy_path is None:
            if getattr(sys, "frozen", False):
                legacy_path = Path(sys.executable).resolve().parent / "settings.json"
            else:
                legacy_path = Path(__file__).resolve().parents[1] / "settings.json"
        self.legacy_path = legacy_path
        app_data = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        self.path = path or app_data / "PoECrafter" / "settings.json"
        self.data: dict[str, Any] = dict(DEFAULT_SETTINGS)
        self.warning: str | None = None

    def load(self) -> dict[str, Any]:
        source = self.path if self.path.exists() else self.legacy_path
        loaded: dict[str, Any] = {}
        if source.exists():
            try:
                with source.open("r", encoding="utf-8") as file:
                    value = json.load(file)
                if isinstance(value, dict):
                    loaded = value
                else:
                    self.warning = "Le fichier de réglages doit contenir un objet JSON."
            except (OSError, json.JSONDecodeError) as exc:
                self.warning = f"Impossible de lire les réglages : {exc}"

        self.data = {**DEFAULT_SETTINGS, **loaded}
        for key in ("random_delay", "disable_mouse_teleport", "stop_if_no_currency", "stash_items_after_craft",
                    "magic", "use_aug", "yellow_beast"):
            if not isinstance(self.data.get(key), bool):
                self.data[key] = DEFAULT_SETTINGS.get(key, False)
        for key in ("craft_delay", "mouse_move_time"):
            try:
                number = float(self.data.get(key, DEFAULT_SETTINGS[key]))
                self.data[key] = number if math.isfinite(number) and number >= 0 else DEFAULT_SETTINGS[key]
            except (TypeError, ValueError):
                self.data[key] = DEFAULT_SETTINGS[key]
        for key in ("currency_tab_id", "compass_tab_id", "item_tab_id", "map_tab_id", "set_item",
                    "set_beast", "set_trade", "set_confirm", "basic_regex"):
            if not isinstance(self.data.get(key, ""), str):
                self.data[key] = ""
        try:
            columns = int(self.data.get("bestiary_columns", 1))
            self.data["bestiary_columns"] = columns if 1 <= columns <= 11 else 1
        except (TypeError, ValueError):
            self.data["bestiary_columns"] = 1
        self.data["currency_button_states"] = self._mapping("currency_button_states")
        no_mod = self.data.get("no_mod", {})
        self.data["no_mod"] = no_mod if isinstance(no_mod, dict) else {}
        self.data["no_mod"] = {
            "socket": False,
            "link": False,
            "color": False,
            "socket_count": 6,
            "link_count": 5,
            "red": 0,
            "green": 1,
            "blue": 5,
            **self.data["no_mod"],
        }
        for key in ("socket", "link", "color"):
            if not isinstance(self.data["no_mod"].get(key), bool):
                self.data["no_mod"][key] = False
        for key in ("socket_count", "link_count", "red", "green", "blue"):
            try:
                number = int(self.data["no_mod"].get(key))
                self.data["no_mod"][key] = max(0, min(6, number))
            except (TypeError, ValueError):
                self.data["no_mod"][key] = {"socket_count": 6, "link_count": 5, "red": 0, "green": 1, "blue": 5}[key]
        self.data["chain_beast_points"] = self._points("chain_beast_points")
        self.data["div_card_points"] = self._points("div_card_points")
        if self.data.get("language") not in {"fr", "en"}:
            self.data["language"] = "fr"
        return self.data

    def save(self, updates: dict[str, Any] | None = None) -> None:
        if updates:
            self.data.update(updates)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.warning and self.path.exists():
            backup = self.path.with_name(self.path.name + ".corrupt.bak")
            if not backup.exists():
                shutil.copy2(self.path, backup)
        descriptor, temporary_name = tempfile.mkstemp(prefix="settings-", suffix=".json", dir=self.path.parent)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=2)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary_name, self.path)
            self.warning = None
        except Exception:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
            raise

    def _mapping(self, key: str) -> dict[str, Any]:
        value = self.data.get(key, {})
        return value if isinstance(value, dict) else {}

    def _points(self, key: str) -> list[dict[str, int]]:
        value = self.data.get(key, [])
        if not isinstance(value, list):
            return []
        points = []
        for point in value:
            if not isinstance(point, dict):
                continue
            try:
                points.append({"x": int(point["x"]), "y": int(point["y"])})
            except (KeyError, TypeError, ValueError):
                continue
        return points
