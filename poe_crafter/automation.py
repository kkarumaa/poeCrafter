"""Game automation services. These functions must run outside the Qt UI thread."""

from __future__ import annotations

import logging
import random
import re
import threading
import time
from collections.abc import Callable
from typing import Any

import pyautogui
import pygetwindow as gw
import pyperclip

from global_functions import extract_link_count, extract_socket_colors

logger = logging.getLogger(__name__)


class AutomationCancelled(Exception):
    """Raised when the user requests that a running action stop."""


class AutomationService:
    def __init__(self, settings: dict[str, Any], stop_event: threading.Event,
                 report: Callable[[str], None] | None = None):
        self.settings = settings
        self.stop_event = stop_event
        self.report = report or (lambda message: None)

    def message(self, french: str, english: str) -> str:
        return french if self.settings.get("language", "fr") == "fr" else english

    def run(self, action: str) -> str:
        try:
            if action in {"basic", "basic_test"}:
                self.basic_craft(test=action == "basic_test")
            elif action == "no_mod":
                self.no_mod_craft()
            elif action == "beast":
                self.fill_yellow_beast()
            elif action == "divination":
                self.exchange_divination_cards()
            else:
                raise ValueError("Action inconnue.")
            return self.message("Opération terminée.", "Operation completed.")
        except AutomationCancelled:
            return self.message("Opération arrêtée.", "Operation stopped.")
        finally:
            self.release_keys()

    def stop(self) -> None:
        self.stop_event.set()

    def check_cancelled(self) -> None:
        if self.stop_event.is_set():
            raise AutomationCancelled

    def pause(self, seconds: float) -> None:
        deadline = time.monotonic() + max(0, seconds)
        while True:
            self.check_cancelled()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return
            self.stop_event.wait(min(remaining, 0.05))

    @staticmethod
    def release_keys() -> None:
        for key in ("shift", "ctrl"):
            try:
                pyautogui.keyUp(key)
            except Exception:
                logger.debug("Unable to release %s during automation cleanup.", key, exc_info=True)

    def activate_game(self) -> None:
        self.check_cancelled()
        try:
            windows = gw.getWindowsWithTitle("Path of Exile")
            if not windows:
                raise RuntimeError(self.message("Fenêtre Path of Exile non trouvée.", "Path of Exile window was not found."))
            windows[0].activate()
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError(self.message(f"Impossible d’activer Path of Exile : {exc}",
                                            f"Could not activate Path of Exile: {exc}")) from exc

    def point(self, value: Any, label: str) -> tuple[int, int]:
        if isinstance(value, dict):
            try:
                return int(value["x"]), int(value["y"])
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(self.message(f"Coordonnées invalides : {label}.", f"Invalid coordinates: {label}.")) from exc
        try:
            x, y = str(value).split(";", maxsplit=1)
            return int(x), int(y)
        except (TypeError, ValueError) as exc:
            raise ValueError(self.message(f"Coordonnées invalides : {label}.", f"Invalid coordinates: {label}.")) from exc

    def move(self, x: int, y: int) -> None:
        duration = float(self.settings.get("mouse_move_time", 0.2)) if self.settings.get("disable_mouse_teleport") else 0
        pyautogui.moveTo(x, y, duration=max(0, duration))
        if self.settings.get("random_delay"):
            self.pause(random.uniform(0.10, 0.17))

    def click(self, x: int, y: int, button: str = "left") -> None:
        self.check_cancelled()
        self.move(x, y)
        pyautogui.click(button=button)
        if self.settings.get("random_delay"):
            self.pause(random.uniform(0.10, 0.17))

    def copy_item(self, x: int, y: int) -> str:
        self.check_cancelled()
        pyautogui.moveTo(x, y)
        self.pause(0.05)
        pyautogui.hotkey("ctrl", "c")
        self.pause(0.05)
        return pyperclip.paste()

    def check_text(self, x: int, y: int, expected: str) -> tuple[bool, str]:
        copied = self.copy_item(x, y)
        return expected in copied, copied

    def basic_craft(self, test: bool = False) -> None:
        alteration = self.point(self.settings.get("currency_button_states", {}).get("Alteration", ""), "Alteration")
        item = self.point(self.settings.get("set_item", ""), "objet")
        use_aug = bool(self.settings.get("use_aug", False))
        augment = None
        if use_aug:
            augment = self.point(self.settings.get("currency_button_states", {}).get("Augment", ""), "Augment")
        pattern = str(self.settings.get("basic_regex", "")).strip()
        if not pattern:
            raise ValueError(self.message("La regex est vide.", "The target regex is empty."))
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as exc:
            raise ValueError(self.message(f"Regex invalide : {exc}", f"Invalid regex: {exc}")) from exc

        self.activate_game()
        pyautogui.PAUSE = 0.01
        try:
            if not use_aug:
                self.click(*alteration, button="right")
                pyautogui.moveTo(*item)
                self.check_cancelled()
                pyautogui.keyDown("shift")

            steps = 100 if test else None
            step = 0
            while steps is None or step < steps:
                self.check_cancelled()
                step += 1
                _, text = self.check_text(*item, "")
                if regex.search(text):
                    self.report(self.message("Objet cible trouvé.", "Target item found."))
                    return
                if use_aug:
                    if augment is None:
                        raise ValueError(self.message("La position Augment est manquante.", "The Augment position is missing."))
                    same, _ = self.check_text(*alteration, text)
                    if same:
                        self.report(self.message("Craft arrêté : l’altération n’a pas changé le texte.",
                                                 "Craft stopped: the Alteration did not change the item text."))
                        return
                    self.check_cancelled()
                    pyautogui.rightClick()
                    self.click(*item)
                    self.pause(float(self.settings.get("craft_delay", 0.07)))
                    same, _ = self.check_text(*augment, text)
                    if same:
                        self.report(self.message("Craft arrêté : l’augmentation n’a pas changé le texte.",
                                                 "Craft stopped: the Augment did not change the item text."))
                        return
                    self.check_cancelled()
                    pyautogui.rightClick()
                    self.click(*item)
                    self.pause(float(self.settings.get("craft_delay", 0.07)))
                else:
                    self.check_cancelled()
                    pyautogui.click()
                    self.pause(random.uniform(0.05, 0.17))
                self.report((f"Essai {step}" if self.settings.get("language", "fr") == "fr" else f"Attempt {step}")
                            if test else self.message("Craft en cours…", "Crafting…"))
        finally:
            if not use_aug:
                self.release_keys()
        if test:
            self.report(self.message("Simulation terminée après 100 essais.", "Test run completed after 100 attempts."))

    def no_mod_craft(self) -> None:
        item = self.point(self.settings.get("set_item", ""), "objet")
        currencies = self.settings.get("currency_button_states", {})
        options = self.settings.get("no_mod", {})
        targets: dict[str, Any] = {}
        if options.get("socket"):
            targets["socket_count"] = int(options.get("socket_count", 6))
            if not 1 <= targets["socket_count"] <= 6:
                raise ValueError(self.message("Le nombre de sockets doit être entre 1 et 6.", "Socket count must be between 1 and 6."))
            self.point(currencies.get("Jeweller", ""), "Jeweller")

        if options.get("link"):
            targets["link_count"] = int(options.get("link_count", 5))
            if not 1 <= targets["link_count"] <= 6:
                raise ValueError(self.message("Le nombre de liens doit être entre 1 et 6.", "Link count must be between 1 and 6."))
            self.point(currencies.get("Fusing", ""), "Fusing")

        if options.get("color"):
            targets["target_colors"] = (
                int(options.get("green", 1)), int(options.get("red", 0)), int(options.get("blue", 5)))
            target_colors = targets["target_colors"]
            target_sockets = sum(target_colors)
            if not 1 <= target_sockets <= 6:
                raise ValueError(self.message("La somme des couleurs doit être entre 1 et 6.", "The color total must be between 1 and 6."))
            self.point(currencies.get("Chromatic", ""), "Chromatic")

        self.activate_game()
        pyautogui.PAUSE = 0.001
        text = self.copy_item(*item)
        green, red, blue = extract_socket_colors(text)
        sockets = green + red + blue
        if sockets <= 0:
            raise ValueError(self.message("Impossible de lire les sockets de l’objet.", "Could not read the item's sockets."))

        if options.get("socket") and sockets < targets["socket_count"]:
            target = targets["socket_count"]
            self._apply_until(currencies, "Jeweller", item, lambda value: sum(extract_socket_colors(value)) >= target)

        if options.get("link"):
            target = targets["link_count"]
            text = self.copy_item(*item)
            if sum(extract_socket_colors(text)) >= target:
                self._apply_until(currencies, "Fusing", item, lambda value: extract_link_count(value) + 1 >= target)

        if options.get("color"):
            target_colors = targets["target_colors"]
            target_sockets = sum(target_colors)
            text = self.copy_item(*item)
            current = extract_socket_colors(text)
            if sum(current) >= target_sockets and any(a < b for a, b in zip(current, target_colors)):
                self._apply_until(currencies, "Chromatic", item,
                                  lambda value: all(a >= b for a, b in zip(extract_socket_colors(value), target_colors)))

    def _apply_until(self, currencies: dict[str, Any], name: str, item: tuple[int, int], condition: Callable[[str], bool]) -> None:
        currency = self.point(currencies.get(name, ""), name)
        text = self.copy_item(*item)
        if condition(text):
            return
        self.click(*currency, button="right")
        pyautogui.moveTo(*item)
        self.check_cancelled()
        pyautogui.keyDown("shift")
        try:
            while True:
                self.check_cancelled()
                if pyautogui.position() and ((pyautogui.position()[0] - item[0]) ** 2 + (pyautogui.position()[1] - item[1]) ** 2) ** 0.5 > 10:
                    return
                self.pause(float(self.settings.get("craft_delay", 0.07)) / 3)
                self.check_cancelled()
                pyautogui.click()
                self.pause(float(self.settings.get("craft_delay", 0.07)) / 3)
                self.check_cancelled()
                pyautogui.hotkey("ctrl", "c")
                self.pause(float(self.settings.get("craft_delay", 0.07)) / 3)
                if condition(pyperclip.paste()):
                    return
        finally:
            self.release_keys()

    def fill_yellow_beast(self) -> None:
        points = self.settings.get("chain_beast_points", [])
        set_beast = self.point(self.settings.get("set_beast", ""), "Set Beast")
        columns = int(self.settings.get("bestiary_columns", 0))
        if len(points) < 60:
            raise ValueError(self.message("La grille d’inventaire Bestiary doit contenir 60 positions.", "The Bestiary inventory grid must contain 60 positions."))
        if not 1 <= columns <= 11:
            raise ValueError(self.message("Le nombre de colonnes doit être compris entre 1 et 11.", "The column count must be between 1 and 11."))
        for point in points:
            self.point(point, "grille Bestiary")
        self.activate_game()
        rows = [points[index:index + 12] for index in range(0, len(points), 12)]
        orb_points = [point for row in rows for point in row[:columns]]
        fill_points = [point for row in rows for point in row[columns:]]
        pyautogui.PAUSE = 0.001
        for orb in orb_points:
            self.check_cancelled()
            x, y = self.point(orb, "Bestiary Orb")
            copied = self.copy_item(x, y)
            if "Bestiary Orb" in copied:
                match = re.search(r"Stack Size: (\d+)/10", copied)
                if not match:
                    continue
                quantity = int(match.group(1))
                if not 1 <= quantity <= 10 or len(fill_points) < quantity:
                    continue
                for _ in range(quantity):
                    self.check_cancelled()
                    self.click(x, y, button="right")
                    self.pause(random.uniform(0.17, 0.25))
                    self.click(*set_beast)
                    self.pause(random.uniform(0.17, 0.25))
                    self.click(*self.point(fill_points.pop(0), "emplacement Bestiary"))
                    self.pause(random.uniform(0.17, 0.25))

    def exchange_divination_cards(self) -> None:
        points = self.settings.get("div_card_points", [])
        if not points:
            raise ValueError(self.message("La grille de cartes n’est pas configurée.", "The card grid has not been configured."))
        trade = self.point(self.settings.get("set_trade", ""), "Set Trade")
        confirm = self.point(self.settings.get("set_confirm", ""), "Set Confirm")
        self.activate_game()
        pyautogui.PAUSE = 0.001
        columns = 12
        if len(points) < 60:
            raise ValueError(self.message("La grille de divination doit contenir 60 positions.", "The divination grid must contain 60 positions."))
        for point in points:
            self.point(point, "grille de divination")
        grid = [points[index:index + columns] for index in range(0, len(points), columns)]
        for column in range(columns):
            for row in range(len(grid)):
                self.check_cancelled()
                point = grid[row][column]
                x, y = self.point(point, "carte")
                copied = self.copy_item(x, y)
                if "Item Class: Divination Cards" not in copied:
                    raise RuntimeError(self.message("La position sélectionnée ne contient pas une carte de divination.", "The selected position does not contain a divination card."))
                try:
                    self.check_cancelled()
                    pyautogui.keyDown("ctrl")
                    pyautogui.click(button="left")
                    pyautogui.keyUp("ctrl")
                    self.pause(random.uniform(0.17, 0.25))
                    self.click(*trade)
                    self.pause(random.uniform(0.17, 0.25))
                    self.move(*confirm)
                    new_text = self.safe_copy(copied)
                    if "Item Class: Stackable Currency" not in new_text:
                        raise RuntimeError(self.message("La confirmation de l’échange n’a pas été détectée.", "The exchange confirmation was not detected."))
                    if copied == new_text or not new_text:
                        raise RuntimeError(self.message("Le presse-papiers n’a pas confirmé le changement d’objet.", "The clipboard did not confirm the item change."))
                    self.check_cancelled()
                    pyautogui.keyDown("ctrl")
                    pyautogui.click(button="left")
                    pyautogui.keyUp("ctrl")
                    self.pause(0.25)
                finally:
                    self.release_keys()

    def safe_copy(self, old_text: str) -> str:
        for _ in range(7):
            self.check_cancelled()
            pyautogui.hotkey("ctrl", "c")
            self.pause(0.05)
            text = pyperclip.paste()
            if text.strip() and text != old_text:
                return text
        return ""
