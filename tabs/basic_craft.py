import re
import time
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import pyperclip
import pygetwindow as gw
from global_functions import (
    background_color,
    text_color,
    button_color,
    extract_socket_colors,
    move_mouse,
    check,
)


def create_basic_craft(app):
    app.basic_craft_frame = tk.Frame(app.root, bg=background_color)
    app.check_vars = {}
    app.check_buttons = {}

    app.check_vars["Magic"] = tk.BooleanVar()
    app.check_buttons["Magic"] = ttk.Checkbutton(
        app.basic_craft_frame,
        text="Magic",
        variable=app.check_vars["Magic"],
        command=lambda: toggle_use_aug(app)
    )
    app.check_buttons["Magic"].grid(row=0, column=0, padx=10, pady=10, sticky="w")

    app.check_vars["Use Aug?"] = tk.BooleanVar()
    app.check_buttons["Use Aug?"] = ttk.Checkbutton(
        app.basic_craft_frame,
        text="Use Aug?",
        variable=app.check_vars["Use Aug?"],
    )
    app.check_buttons["Use Aug?"].grid(row=0, column=1, padx=10, pady=10, sticky="w")

    toggle_use_aug(app)

    regex_label = tk.Label(
        app.basic_craft_frame,
        text="Regex:",
        foreground=text_color,
        background=background_color
    )
    regex_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    app.regex_var = tk.StringVar()
    vcmd = app.root.register(lambda P: len(P) <= 250)
    app.regex_entry = tk.Entry(
        app.basic_craft_frame,
        textvariable=app.regex_var,
        validate="key",
        validatecommand=(vcmd, "%P"),
        fg="white",
        bg="#142131",
        insertbackground="white"
    )
    app.regex_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    app.test_basic_button = tk.Button(
        app.basic_craft_frame,
        text="Test Basic Craft",
        command=lambda: run_basic_craft_test(app),
        bg=button_color,
        fg=text_color
    )
    app.test_basic_button.grid(row=2, column=0, columnspan=2, pady=10)

    app.start_basic_button = tk.Button(
        app.basic_craft_frame,
        text="Start",
        command=lambda: run_basic_craft(app),
        bg=button_color,
        fg=text_color
    )
    app.start_basic_button.grid(row=3, column=0, columnspan=2, pady=10)

    app.basic_craft_frame.grid_columnconfigure(1, weight=1)
    app.basic_craft_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


def toggle_use_aug(app):
    if app.check_vars["Magic"].get():
        app.check_buttons["Use Aug?"].config(state='normal')
    else:
        app.check_vars["Use Aug?"].set(False)
        app.check_buttons["Use Aug?"].config(state='disabled')


def show_basic_craft(app):
    app.update_tab_color(app.basic_craft)
    create_basic_craft(app)
    app.basic_craft_frame.grid(row=0, column=1, sticky="nsew")
    app.load_settings()


def run_basic_craft(app):
    """Loop crafting for the Basic Craft tab."""
    alteration_pos = app.currency_button_states.get("Alteration", "")
    augment_pos = app.currency_button_states.get("Augment", "")

    if not app.set_item_var or alteration_pos == "":
        messagebox.showinfo("Info", "Veuillez définir Set item et Alteration")
        return

    if app.check_vars["Use Aug?"].get() and augment_pos == "":
        messagebox.showinfo("Info", "Veuillez définir Augment")
        return

    pattern = app.regex_var.get()
    if not pattern:
        messagebox.showinfo("Info", "Regex manquante")
        return

    poe_window = gw.getWindowsWithTitle('Path of Exile')[0]
    poe_window.activate()

    regex = re.compile(pattern, re.IGNORECASE)
    pattern_lower = pattern.lower()

    item_x, item_y = map(int, app.set_item_var.split(';'))
    alt_x, alt_y = map(int, alteration_pos.split(';'))
    if app.check_vars["Use Aug?"].get():
        aug_x, aug_y = map(int, augment_pos.split(';'))

    while True:
        _, item_text = check(item_x, item_y, "")
        if regex.search(item_text) or pattern_lower in item_text.lower():
            messagebox.showinfo("Info", "craft finis")
            break

        same, _ = check(alt_x, alt_y, item_text)
        if same:
            messagebox.showinfo("Info", "craft finis")
            break
        pyautogui.rightClick()
        move_mouse(app, item_x, item_y)
        pyautogui.click()
        time.sleep(app.craft_delay_var.get())

        if app.check_vars["Use Aug?"].get():
            same, _ = check(aug_x, aug_y, item_text)
            if same:
                messagebox.showinfo("Info", "craft finis")
                break
            pyautogui.rightClick()


def run_basic_craft_test(app):
    """Run basic craft 10 times and log info each step."""
    alteration_pos = app.currency_button_states.get("Alteration", "")
    augment_pos = app.currency_button_states.get("Augment", "")

    if not app.set_item_var or alteration_pos == "":
        messagebox.showinfo("Info", "Veuillez définir Set item et Alteration")
        return

    if app.check_vars["Use Aug?"].get() and augment_pos == "":
        messagebox.showinfo("Info", "Veuillez définir Augment")
        return

    pattern = app.regex_var.get()
    if not pattern:
        messagebox.showinfo("Info", "Regex manquante")
        return

    poe_window = gw.getWindowsWithTitle('Path of Exile')[0]
    poe_window.activate()

    regex = re.compile(pattern, re.IGNORECASE)
    pattern_lower = pattern.lower()

    item_x, item_y = map(int, app.set_item_var.split(';'))
    alt_x, alt_y = map(int, alteration_pos.split(';'))
    if app.check_vars["Use Aug?"].get():
        aug_x, aug_y = map(int, augment_pos.split(';'))

    for i in range(10):
        _, item_text = check(item_x, item_y, "")
        print(f"Step {i+1}: item text -> {item_text}")
        if regex.search(item_text) or pattern_lower in item_text.lower():
            print("Regex found or contained, stopping craft")
            break

        same, _ = check(alt_x, alt_y, item_text)
        print(f"Step {i+1}: alteration same -> {same}")
        if same:
            print("Alteration check failed, stopping craft")
            break
        pyautogui.rightClick()
        move_mouse(app, item_x, item_y)
        pyautogui.click()
        print(f"Applied Alteration at step {i+1}")
        time.sleep(app.craft_delay_var.get())

        if app.check_vars["Use Aug?"].get():
            same, _ = check(aug_x, aug_y, item_text)
            print(f"Step {i+1}: augment same -> {same}")
            if same:
                print("Augment check failed, stopping craft")
                break
            pyautogui.rightClick()
            move_mouse(app, item_x, item_y)
            pyautogui.click()
            print(f"Applied Augment at step {i+1}")
            time.sleep(app.craft_delay_var.get())

