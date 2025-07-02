import random
import time
import pyautogui
import pyperclip

# Configuration des couleurs et styles
background_color = "#242f3d"
nav_bar_color = "#142131"
general_tab_color = "#2395e0"
text_color = "white"
button_color = "#142131"  # Couleur des boutons
button_menu_color = "#0d1623"  # Couleur d'arrière-plan des boutons dans le menu

currency_used = 0


def move_mouse(app, x, y):
    """Move the mouse according to global settings."""
    duration = app.mouse_move_time_var.get() if app.disable_mouse_teleport_var.get() else 0
    pyautogui.moveTo(x, y, duration=duration)


def safe_copy(old_copy: str) -> str:
    for _ in range(7):
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.05)
        text = pyperclip.paste()
        if text.strip() != "" and text != old_copy:
            return text
    return ""


def check(x: int, y: int, text: str):
    pyautogui.moveTo(x, y)
    time.sleep(0.05)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.05)
    copied_text = pyperclip.paste()
    return (text in copied_text), copied_text


def extract_socket_colors(clipboard_content: str):
    lines = clipboard_content.split('\n')
    for line in lines:
        if line.startswith("Sockets:"):
            g_count = line.count('G')
            r_count = line.count('R')
            b_count = line.count('B')
            return g_count, r_count, b_count
    return 0, 0, 0


def extract_link_count(clipboard_content: str):
    lines = clipboard_content.split('\n')
    max_links = 0
    for line in lines:
        if line.startswith("Sockets:"):
            socket_groups = line.split()[1:]
            for group in socket_groups:
                link_count = group.count('-')
                max_links = max(max_links, link_count)
            return max_links
    return 0
