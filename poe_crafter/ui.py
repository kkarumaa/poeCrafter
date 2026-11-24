"""Modern bilingual Qt interface for PoE Crafter."""

from __future__ import annotations

import copy
from typing import Any

from pynput import keyboard
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCloseEvent, QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .settings import SettingsStore
from .workers import AutomationWorker

TEXT = {
    "fr": {
        "general": "Général", "currency": "Devises", "no_mod": "Craft sans mods",
        "basic": "Craft basique", "rare": "Craft rare", "map": "Craft de cartes",
        "harvest": "Échange Harvest", "expedition": "Expédition", "beast": "Récupération de bêtes",
        "cards": "Cartes de divination", "settings": "Réglages", "appearance": "Apparence et comportement",
        "language": "Langue", "french": "Français", "english": "Anglais", "random_delay": "Délais aléatoires",
        "craft_delay": "Délai de craft (secondes)", "mouse_teleport": "Déplacer la souris progressivement",
        "move_time": "Durée du déplacement (secondes)", "stop_currency": "Arrêter si la monnaie manque",
        "stash": "Ranger les objets après le craft", "stash_ids": "Identifiants des onglets de coffre",
        "currency_tab": "Devises", "compass_tab": "Boussoles", "item_tab": "Objets", "map_tab": "Cartes",
        "currency_title": "Positions des monnaies", "coordinate_hint": "Clique sur une monnaie pour définir sa position à l’écran.",
        "set_item": "Définir la position de l’objet", "set_item_short": "Définir objet",
        "craft_options": "Options de craft", "socket": "Sockets", "link": "Liens", "color": "Couleurs",
        "count": "Nombre souhaité", "red": "Rouge", "green": "Vert", "blue": "Bleu",
        "start": "Démarrer", "test_start": "Lancer le craft de test", "magic": "Objet magique",
        "use_aug": "Utiliser Augment", "regex": "Regex cible", "beast_title": "Récupération de bêtes",
        "yellow": "Bête jaune", "red_beast": "Bête rouge", "set_inventory": "Définir la grille d’inventaire",
        "set_beast": "Définir Set Beast", "columns": "Colonnes d’orbes Bestiary (1–11)",
        "fill": "Remplir les bêtes jaunes", "card_title": "Échange de cartes de divination",
        "set_trade": "Définir Trade", "set_confirm": "Définir Confirm", "exchange": "Échanger les cartes",
        "inventory_grid": "Grille d’inventaire", "grid_instructions": "Place cette fenêtre au-dessus de la zone du jeu. Les points rouges indiquent les positions mémorisées.",
        "save_positions": "Enregistrer les positions", "cancel": "Annuler", "target": "Cible",
        "coming": "Cette section est prévue, mais ses automatismes ne sont pas encore disponibles.",
        "status_ready": "Prêt", "stop": "Arrêter", "running": "Automatisme en cours…", "stop_requested": "Arrêt demandé…",
        "topmost": "La fenêtre reste toujours au premier plan", "migration_warning": "Les anciens réglages n’ont pas pu être lus.",
    },
    "en": {
        "general": "General", "currency": "Currency", "no_mod": "No Mod Craft", "basic": "Basic Craft",
        "rare": "Rare Craft", "map": "Map Craft", "harvest": "Harvest Exchange", "expedition": "Expedition",
        "beast": "Beast Recovery", "cards": "Divination Cards", "settings": "Settings",
        "appearance": "Appearance and behavior", "language": "Language", "french": "French", "english": "English",
        "random_delay": "Random delays", "craft_delay": "Craft delay (seconds)",
        "mouse_teleport": "Move the mouse gradually", "move_time": "Mouse movement duration (seconds)",
        "stop_currency": "Stop if currency is missing", "stash": "Stash items after crafting",
        "stash_ids": "Stash tab IDs", "currency_tab": "Currency", "compass_tab": "Compasses",
        "item_tab": "Items", "map_tab": "Maps", "currency_title": "Currency positions",
        "coordinate_hint": "Select a currency to set its screen position.", "set_item": "Set item position",
        "set_item_short": "Set item", "craft_options": "Craft options", "socket": "Sockets", "link": "Links",
        "color": "Colors", "count": "Target count", "red": "Red", "green": "Green", "blue": "Blue",
        "start": "Start", "test_start": "Run craft test", "magic": "Magic item", "use_aug": "Use Augment",
        "regex": "Target regex", "beast_title": "Beast recovery", "yellow": "Yellow Beast", "red_beast": "Red Beast",
        "set_inventory": "Set inventory grid", "set_beast": "Set Beast position", "columns": "Bestiary Orb columns (1–11)",
        "fill": "Fill Yellow Beasts", "card_title": "Divination card exchange", "set_trade": "Set Trade position",
        "set_confirm": "Set Confirm position", "exchange": "Exchange cards", "inventory_grid": "Inventory grid",
        "grid_instructions": "Place this window over the game area. Red dots mark the saved positions.",
        "save_positions": "Save positions", "cancel": "Cancel", "target": "Target",
        "coming": "This section is planned, but its automation is not available yet.", "status_ready": "Ready",
        "stop": "Stop", "running": "Automation running…", "stop_requested": "Stop requested…",
        "topmost": "Keep the window always on top", "migration_warning": "The previous settings could not be read.",
    },
}


NAVIGATION = ["general", "currency", "no_mod", "basic", "rare", "map", "harvest", "expedition", "beast", "cards"]
CURRENCIES = [
    ["Chromatic", "Stacked Deck", "Chance", "Reso 1", "Reso 2"],
    ["Fusing", "Scouring", "Chaos", "Fossil 1", "Reso 3"],
    ["Jeweller", "Transmut", "Alchemy", "Fossil 2", "Chisel"],
    ["Elevated", "Regal", "Fossil 3", "Exal", "Ichor"],
    ["Ember", "Harvest", "Space (Fossil)", "Annul", "Alteration"],
    ["Wisdom", "Compass", "Augment", "Alter 2nd", "Vaal"],
    ["GemCP", "Catalyst", "Essence", "Alter 3rd", "Flask Currency"],
    ["Haggle", "", "", "", ""],
]


class CoordinateDialog(QDialog):
    def __init__(self, parent: QWidget, language: str, rows: int = 0, columns: int = 0):
        super().__init__(parent, Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.language = language
        self.rows = rows
        self.columns = columns
        self.points: list[QWidget] = []
        self.setWindowTitle(TEXT[language]["inventory_grid"] if rows else TEXT[language]["target"])
        self.setWindowOpacity(0.88)
        self.setMinimumSize(260, 180)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(TEXT[language]["grid_instructions"]))
        if rows and columns:
            grid_host = QWidget(self)
            grid = QGridLayout(grid_host)
            grid.setSpacing(5)
            for row in range(rows):
                for column in range(columns):
                    dot = QLabel("●")
                    dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    dot.setMinimumSize(24, 24)
                    dot.setStyleSheet("color:#e34d58; font-size:17px; background:#eef1f6; border-radius:8px;")
                    grid.addWidget(dot, row, column)
                    self.points.append(dot)
            layout.addWidget(grid_host, 1)
        else:
            target = QLabel("●")
            target.setAlignment(Qt.AlignmentFlag.AlignCenter)
            target.setStyleSheet("color:#e34d58; font-size:36px; background:#eef1f6; border-radius:12px;")
            layout.addWidget(target, 1)
            self.points.append(target)
        actions = QHBoxLayout()
        actions.addStretch(1)
        cancel = QPushButton(TEXT[language]["cancel"])
        cancel.clicked.connect(self.reject)
        save = QPushButton(TEXT[language]["save_positions"])
        save.setObjectName("primaryButton")
        save.clicked.connect(self.accept)
        actions.addWidget(cancel)
        actions.addWidget(save)
        layout.addLayout(actions)
        self.resize(720 if rows else 300, 420 if rows else 220)
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            self.move(geometry.center() - self.rect().center())

    def global_points(self) -> list[dict[str, int]]:
        result = []
        for widget in self.points:
            center = widget.mapToGlobal(widget.rect().center())
            result.append({"x": center.x(), "y": center.y()})
        return result


class MainWindow(QMainWindow):
    exit_requested = Signal()

    def __init__(self, store: SettingsStore | None = None):
        super().__init__()
        self.store = store or SettingsStore()
        self.settings = self.store.load()
        self.current_page = "general"
        self.worker: AutomationWorker | None = None
        self.close_after_worker = False
        self.ignore_setting_signals = False
        self.nav_buttons: dict[str, QPushButton] = {}
        self.pages: dict[str, QWidget] = {}
        self.language = self.settings.get("language", "fr")
        self.setWindowTitle("KaruCrafter")
        self.setMinimumSize(900, 640)
        self.resize(1120, 780)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self._apply_style()
        self._build_shell()
        self._build_pages()
        self._show_page(self.current_page)
        self.exit_requested.connect(self._handle_f12)
        self._start_f12_listener()
        if self.store.warning:
            self.statusBar().showMessage(self.tr("migration_warning"), 10000)

    def tr(self, key: str) -> str:
        return TEXT[self.language].get(key, key)

    def _apply_style(self) -> None:
        QApplication.setStyle("Fusion")
        QApplication.instance().setFont(QFont("Segoe UI", 10))
        QApplication.instance().setStyleSheet("""
            QWidget { color:#e8edf5; background:#111827; }
            QMainWindow { background:#0b1220; }
            QFrame#sidebar { background:#111a2b; border-right:1px solid #263248; }
            QLabel#eyebrow { color:#8fa2bd; font-size:10px; font-weight:700; }
            QLabel#pageTitle { color:#f4f7fb; font-size:22px; font-weight:700; }
            QLabel#muted { color:#9aabc1; }
            QPushButton { background:#202c41; border:1px solid #34435b; border-radius:8px; padding:9px 12px; text-align:left; }
            QPushButton:hover { background:#293951; }
            QPushButton:checked { background:#2456a6; border-color:#4c85e5; }
            QPushButton#primaryButton { background:#2876d2; border:0; font-weight:600; }
            QPushButton#primaryButton:hover { background:#3988e4; }
            QPushButton#dangerButton { background:#74313a; border-color:#a64b57; }
            QPushButton:disabled { color:#6f7e92; background:#1a2230; }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox { background:#0d1523; border:1px solid #34435b; border-radius:6px; padding:7px; selection-background-color:#2876d2; }
            QCheckBox { spacing:9px; }
            QCheckBox::indicator { width:17px; height:17px; }
            QFrame#card { background:#151f30; border:1px solid #28364c; border-radius:12px; }
            QStatusBar { color:#a9b7c9; background:#111a2b; border-top:1px solid #263248; }
            QScrollArea { border:0; }
        """)

    def _build_shell(self) -> None:
        shell = QWidget(self)
        root = QHBoxLayout(shell)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(225)
        side = QVBoxLayout(self.sidebar)
        side.setContentsMargins(16, 22, 16, 16)
        brand = QLabel("KARU\nCRAFTER")
        brand.setStyleSheet("font-size:19px;font-weight:800;letter-spacing:2px;color:#e9b866;padding:4px 8px 18px;")
        side.addWidget(brand)
        self.navigation_layout = side
        side.addStretch(1)
        self.set_item_button = QPushButton()
        self.set_item_button.clicked.connect(lambda: self._set_single_point("set_item", "set_item"))
        side.addWidget(self.set_item_button)
        self.stop_button = QPushButton()
        self.stop_button.setObjectName("dangerButton")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_automation)
        side.addWidget(self.stop_button)
        root.addWidget(self.sidebar)
        right = QVBoxLayout()
        right.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()
        right.addWidget(self.stack, 1)
        root.addLayout(right, 1)
        self.setCentralWidget(shell)
        self.statusBar().showMessage(self.tr("status_ready"))
        self._translate_shell()

    def _translate_shell(self) -> None:
        self.set_item_button.setText(f"＋  {self.tr('set_item_short')}")
        self.stop_button.setText(f"■  {self.tr('stop')}")

    def _build_pages(self) -> None:
        while self.stack.count():
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()
        for button in self.nav_buttons.values():
            self.navigation_layout.removeWidget(button)
            button.deleteLater()
        self.nav_buttons.clear()
        self.pages.clear()
        for key in NAVIGATION:
            button = QPushButton(self.tr(key))
            button.setCheckable(True)
            button.clicked.connect(lambda checked=False, page=key: self._show_page(page))
            self.navigation_layout.insertWidget(len(self.nav_buttons) + 1, button)
            self.nav_buttons[key] = button
            page = self._make_page(key)
            self.pages[key] = page
            self.stack.addWidget(page)
        self._translate_shell()

    def _page(self, title_key: str, intro: str = "") -> tuple[QWidget, QVBoxLayout]:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(34, 28, 34, 24)
        outer.setSpacing(18)
        eyebrow = QLabel("POE CRAFTER  /  " + self.tr(title_key).upper())
        eyebrow.setObjectName("eyebrow")
        title = QLabel(self.tr(title_key))
        title.setObjectName("pageTitle")
        outer.addWidget(eyebrow)
        outer.addWidget(title)
        if intro:
            note = QLabel(intro)
            note.setObjectName("muted")
            note.setWordWrap(True)
            outer.addWidget(note)
        return page, outer

    def _card(self, layout: QVBoxLayout, title: str) -> QFormLayout:
        frame = QFrame()
        frame.setObjectName("card")
        card_layout = QVBoxLayout(frame)
        card_layout.setContentsMargins(18, 16, 18, 18)
        heading = QLabel(title)
        heading.setStyleSheet("font-size:14px;font-weight:650;color:#e3ebf7;")
        card_layout.addWidget(heading)
        form = QFormLayout()
        form.setHorizontalSpacing(24)
        form.setVerticalSpacing(12)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        card_layout.addLayout(form)
        layout.addWidget(frame)
        return form

    def _make_page(self, key: str) -> QWidget:
        title = key
        if key in {"rare", "map", "harvest", "expedition"}:
            page, layout = self._page(title, self.tr("coming"))
            placeholder = QFrame()
            placeholder.setObjectName("card")
            placeholder_layout = QVBoxLayout(placeholder)
            label = QLabel("◌")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size:46px;color:#e9b866;")
            placeholder_layout.addWidget(label)
            text = QLabel(self.tr("coming"))
            text.setObjectName("muted")
            text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text.setWordWrap(True)
            placeholder_layout.addWidget(text)
            layout.addWidget(placeholder)
            layout.addStretch(1)
            return self._scroll(page)
        if key == "general":
            return self._general_page()
        if key == "currency":
            return self._currency_page()
        if key == "no_mod":
            return self._no_mod_page()
        if key == "basic":
            return self._basic_page()
        if key == "beast":
            return self._beast_page()
        if key == "cards":
            return self._cards_page()
        return self._scroll(QWidget())

    def _scroll(self, page: QWidget) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(page)
        return scroll

    def _general_page(self) -> QScrollArea:
        page, layout = self._page("general")
        appearance = self._card(layout, self.tr("appearance"))
        language = QComboBox()
        language.addItem(self.tr("french"), "fr")
        language.addItem(self.tr("english"), "en")
        language.setCurrentIndex(0 if self.language == "fr" else 1)
        language.currentIndexChanged.connect(lambda _index: self._change_language(language.currentData()))
        appearance.addRow(self.tr("language"), language)
        delay = QDoubleSpinBox()
        delay.setRange(0, 10)
        delay.setDecimals(3)
        delay.setSingleStep(0.01)
        delay.setValue(float(self.settings.get("craft_delay", 0.07)))
        delay.valueChanged.connect(lambda value: self._set_setting("craft_delay", value))
        appearance.addRow(self.tr("craft_delay"), delay)
        move = QDoubleSpinBox()
        move.setRange(0, 10)
        move.setDecimals(2)
        move.setSingleStep(0.05)
        move.setValue(float(self.settings.get("mouse_move_time", 0.2)))
        move.valueChanged.connect(lambda value: self._set_setting("mouse_move_time", value))
        appearance.addRow(self.tr("move_time"), move)
        for setting_key, label_key in [
            ("random_delay", "random_delay"), ("disable_mouse_teleport", "mouse_teleport"),
            ("stop_if_no_currency", "stop_currency"), ("stash_items_after_craft", "stash"),
        ]:
            checkbox = QCheckBox(self.tr(label_key))
            checkbox.setChecked(bool(self.settings.get(setting_key, False)))
            checkbox.toggled.connect(lambda value, setting=setting_key: self._set_setting(setting, value))
            appearance.addRow(checkbox)
        topmost = QCheckBox(self.tr("topmost"))
        topmost.setChecked(True)
        topmost.setEnabled(False)
        appearance.addRow(topmost)

        tabs = self._card(layout, self.tr("stash_ids"))
        for setting_key, label_key in [("currency_tab_id", "currency_tab"), ("compass_tab_id", "compass_tab"),
                                       ("item_tab_id", "item_tab"), ("map_tab_id", "map_tab")]:
            field = QLineEdit(str(self.settings.get(setting_key, "")))
            field.textChanged.connect(lambda value, setting=setting_key: self._set_setting(setting, value))
            tabs.addRow(self.tr(label_key), field)
        layout.addStretch(1)
        return self._scroll(page)

    def _currency_page(self) -> QScrollArea:
        page, layout = self._page("currency", self.tr("coordinate_hint"))
        form = self._card(layout, self.tr("currency_title"))
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(9)
        box = QWidget()
        box.setLayout(grid)
        form.addRow(box)
        for row, names in enumerate(CURRENCIES):
            for column, name in enumerate(names):
                if not name:
                    continue
                button = QPushButton(name)
                self._style_coordinate_button(button, bool(self.settings.get("currency_button_states", {}).get(name)))
                button.clicked.connect(lambda checked=False, value=name: self._set_single_point("currency_button_states", value))
                grid.addWidget(button, row, column)
        layout.addStretch(1)
        return self._scroll(page)

    @staticmethod
    def _style_coordinate_button(button: QPushButton, is_set: bool) -> None:
        button.setStyleSheet("QPushButton { text-align:center; background:%s; min-height:38px; }" % ("#215b58" if is_set else "#202c41"))

    def _no_mod_page(self) -> QScrollArea:
        page, layout = self._page("no_mod")
        form = self._card(layout, self.tr("craft_options"))
        settings = self.settings.get("no_mod", {})
        for setting, label in [("socket", "socket"), ("link", "link"), ("color", "color")]:
            check = QCheckBox(self.tr(label))
            check.setChecked(bool(settings.get(setting, False)))
            check.toggled.connect(lambda value, key=setting: self._set_nested_setting("no_mod", key, value))
            form.addRow(check)
        for setting, label in [("socket_count", "socket"), ("link_count", "link")]:
            spin = QSpinBox()
            spin.setRange(1, 6)
            spin.setValue(int(settings.get(setting, 6 if setting == "socket_count" else 5)))
            spin.valueChanged.connect(lambda value, key=setting: self._set_nested_setting("no_mod", key, value))
            form.addRow(self.tr("count") + " · " + self.tr(label), spin)
        for setting in ("red", "green", "blue"):
            spin = QSpinBox()
            spin.setRange(0, 6)
            spin.setValue(int(settings.get(setting, {"red": 0, "green": 1, "blue": 5}[setting])))
            spin.valueChanged.connect(lambda value, key=setting: self._set_nested_setting("no_mod", key, value))
            form.addRow(self.tr(setting), spin)
        start = QPushButton(self.tr("start"))
        start.setObjectName("primaryButton")
        start.clicked.connect(lambda: self.start_automation("no_mod"))
        layout.addWidget(start, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(1)
        return self._scroll(page)

    def _basic_page(self) -> QScrollArea:
        page, layout = self._page("basic")
        form = self._card(layout, self.tr("craft_options"))
        self.magic_check = QCheckBox(self.tr("magic"))
        self.magic_check.setChecked(bool(self.settings.get("magic", False)))
        self.magic_check.toggled.connect(lambda value: self._set_setting("magic", value))
        form.addRow(self.magic_check)
        self.augment_check = QCheckBox(self.tr("use_aug"))
        self.augment_check.setChecked(bool(self.settings.get("use_aug", False)))
        self.augment_check.setEnabled(self.magic_check.isChecked())
        self.magic_check.toggled.connect(self.augment_check.setEnabled)
        self.augment_check.toggled.connect(lambda value: self._set_setting("use_aug", value))
        form.addRow(self.augment_check)
        regex = QLineEdit(str(self.settings.get("basic_regex", "")))
        regex.setMaxLength(250)
        regex.textChanged.connect(lambda value: self._set_setting("basic_regex", value))
        form.addRow(self.tr("regex"), regex)
        buttons = QHBoxLayout()
        start = QPushButton(self.tr("start"))
        start.setObjectName("primaryButton")
        start.clicked.connect(lambda: self.start_automation("basic"))
        test = QPushButton(self.tr("test_start"))
        test.clicked.connect(lambda: self.start_automation("basic_test"))
        buttons.addWidget(start)
        buttons.addWidget(test)
        buttons.addStretch(1)
        layout.addLayout(buttons)
        layout.addStretch(1)
        return self._scroll(page)

    def _beast_page(self) -> QScrollArea:
        page, layout = self._page("beast")
        form = self._card(layout, self.tr("beast_title"))
        self.yellow_toggle = QCheckBox(self.tr("yellow"))
        self.yellow_toggle.setChecked(bool(self.settings.get("yellow_beast", False)))
        self.yellow_toggle.toggled.connect(lambda value: self._set_setting("yellow_beast", value))
        form.addRow(self.yellow_toggle)
        status = QLabel(self.tr("yellow") if self.yellow_toggle.isChecked() else self.tr("red_beast"))
        self.yellow_toggle.toggled.connect(lambda checked: status.setText(self.tr("yellow" if checked else "red_beast")))
        form.addRow(status)
        inventory = QPushButton(self.tr("set_inventory"))
        inventory.clicked.connect(lambda: self._set_grid("chain_beast_points"))
        form.addRow(inventory)
        beast = QPushButton(self.tr("set_beast"))
        beast.clicked.connect(lambda: self._set_single_point("set_beast", "set_beast"))
        form.addRow(beast)
        columns = QSpinBox()
        columns.setRange(1, 11)
        columns.setValue(int(self.settings.get("bestiary_columns", 1)))
        columns.valueChanged.connect(lambda value: self._set_setting("bestiary_columns", value))
        form.addRow(self.tr("columns"), columns)
        fill = QPushButton(self.tr("fill"))
        fill.setObjectName("primaryButton")
        fill.clicked.connect(lambda: self.start_automation("beast"))
        layout.addWidget(fill, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(1)
        return self._scroll(page)

    def _cards_page(self) -> QScrollArea:
        page, layout = self._page("cards")
        form = self._card(layout, self.tr("card_title"))
        inventory = QPushButton(self.tr("set_inventory"))
        inventory.clicked.connect(lambda: self._set_grid("div_card_points"))
        form.addRow(inventory)
        trade = QPushButton(self.tr("set_trade"))
        trade.clicked.connect(lambda: self._set_single_point("set_trade", "set_trade"))
        form.addRow(trade)
        confirm = QPushButton(self.tr("set_confirm"))
        confirm.clicked.connect(lambda: self._set_single_point("set_confirm", "set_confirm"))
        form.addRow(confirm)
        exchange = QPushButton(self.tr("exchange"))
        exchange.setObjectName("primaryButton")
        exchange.clicked.connect(lambda: self.start_automation("divination"))
        layout.addWidget(exchange, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(1)
        return self._scroll(page)

    def _show_page(self, key: str) -> None:
        if key not in self.pages:
            return
        self.current_page = key
        self.stack.setCurrentWidget(self.pages[key])
        for name, button in self.nav_buttons.items():
            button.setChecked(name == key)

    def _set_setting(self, key: str, value: Any) -> None:
        if self.ignore_setting_signals:
            return
        self.settings[key] = value
        self._save_settings()

    def _set_nested_setting(self, group: str, key: str, value: Any) -> None:
        group_values = dict(self.settings.get(group, {}))
        group_values[key] = value
        self._set_setting(group, group_values)

    def _save_settings(self) -> None:
        try:
            self.store.save(self.settings)
        except OSError as exc:
            self.statusBar().showMessage(f"Impossible d’enregistrer les réglages : {exc}", 10000)

    def _change_language(self, language: str) -> None:
        if language not in TEXT or language == self.language:
            return
        self.language = language
        self.settings["language"] = language
        self._save_settings()
        self._build_pages()
        self._show_page(self.current_page)

    def _set_single_point(self, key: str, label: str) -> None:
        dialog = CoordinateDialog(self, self.language)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        point = dialog.global_points()[0]
        if key == "currency_button_states":
            currencies = dict(self.settings.get(key, {}))
            currencies[label] = f"{point['x']};{point['y']}"
            self.settings[key] = currencies
        else:
            self.settings[key] = f"{point['x']};{point['y']}"
        self._save_settings()
        if self.current_page == "currency":
            self._build_pages()
            self._show_page("currency")

    def _set_grid(self, key: str) -> None:
        dialog = CoordinateDialog(self, self.language, rows=5, columns=12)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        self.settings[key] = dialog.global_points()
        self._save_settings()

    def start_automation(self, action: str) -> None:
        if self.worker and self.worker.isRunning():
            return
        snapshot = copy.deepcopy(self.settings)
        self.worker = AutomationWorker(action, snapshot)
        self.worker.progress.connect(self._automation_progress)
        self.worker.completed.connect(self._automation_completed)
        self.worker.failed.connect(self._automation_failed)
        self.worker.finished.connect(self._automation_thread_finished)
        self.stop_button.setEnabled(True)
        self.statusBar().showMessage(self.tr("running"))
        self.worker.start()

    def stop_automation(self) -> None:
        if self.worker and self.worker.isRunning():
            self.worker.stop_event.set()
            self.statusBar().showMessage(self.tr("stop_requested"))

    def _automation_progress(self, message: str) -> None:
        self.statusBar().showMessage(message)

    def _automation_completed(self, message: str) -> None:
        self.stop_button.setEnabled(False)
        self.statusBar().showMessage(message, 10000)
        if self.close_after_worker:
            self.close()

    def _automation_failed(self, message: str) -> None:
        self.stop_button.setEnabled(False)
        self.statusBar().showMessage(message, 10000)
        QMessageBox.warning(self, "PoE Crafter", message)
    def _automation_thread_finished(self) -> None:
        if self.close_after_worker:
            self.close()

    def _start_f12_listener(self) -> None:
        self.listener = keyboard.Listener(on_press=self._on_global_key)
        self.listener.start()

    def _on_global_key(self, key: Any) -> None:
        if key == keyboard.Key.f12:
            if self.worker and self.worker.isRunning():
                self.worker.stop_event.set()
            self.exit_requested.emit()
            return False
        return None

    def _handle_f12(self) -> None:
        if self.worker and self.worker.isRunning():
            self.close_after_worker = True
            self.statusBar().showMessage(self.tr("stop_requested"))
            self.worker.stop_event.set()
        else:
            self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.worker and self.worker.isRunning():
            self.close_after_worker = True
            self.worker.stop_event.set()
            self.statusBar().showMessage(self.tr("stop_requested"))
            event.ignore()
            return
        if getattr(self, "listener", None):
            self.listener.stop()
        event.accept()
