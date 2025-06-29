import random
import time
import tkinter as tk
from tkinter import ttk
import pyautogui
import pyperclip
from global_functions import background_color, button_color, text_color, safe_copy


def create_divination_card_content(app):
    app.divination_card_frame = tk.Frame(app.root, bg=background_color)

    title = tk.Label(app.divination_card_frame, text="Divination Card Exchange",
                     font=("Arial", 14), bg=background_color, fg=text_color)
    title.pack(pady=10)

    btn_frame = tk.Frame(app.divination_card_frame, bg=background_color)
    btn_frame.pack(pady=10)

    set_btn = tk.Button(btn_frame, text="Set Inventory", command=app.open_div_card_inventory_popup,
                        bg=button_color, fg=text_color)
    set_btn.grid(row=0, column=0, padx=5)

    set_trade_button = tk.Button(btn_frame, text="Set Trade",
                                 command=lambda: set_trade_action(app), bg=button_color, fg=text_color)
    set_trade_button.grid(row=0, column=1, padx=5)

    set_confirm_button = tk.Button(btn_frame, text="Set Confirm",
                                   command=lambda: set_confirm_action(app), bg=button_color, fg=text_color)
    set_confirm_button.grid(row=0, column=2, padx=5)

    empty_space = tk.Label(btn_frame, text="", bg=background_color, height=1)
    empty_space.grid(row=1, column=0, columnspan=2)

    exchange_btn = tk.Button(btn_frame, text="Échanger les cartes", command=lambda: exchange_divination_cards(app),
                             bg="green", fg="white")
    exchange_btn.grid(row=2, column=0, padx=5)


def set_trade_action(app):
    app.create_popup("Set Trade")


def set_confirm_action(app):
    app.create_popup("Set Confirm")


def open_div_card_inventory_popup(app):
    popup = tk.Toplevel(app.root)
    popup.title("Set Inventory - Divination Card")
    popup.geometry("600x400")
    popup.minsize(400, 300)
    popup.attributes("-topmost", True)
    popup.attributes("-alpha", 0.4)
    popup.overrideredirect(True)

    popup.grid_rowconfigure(0, weight=1)
    popup.grid_rowconfigure(1, weight=0)
    popup.grid_columnconfigure(0, weight=1)

    points_frame = tk.Frame(popup, bg='white')
    points_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    rows, cols = 5, 12
    app.div_card_canvases = []

    for row in range(rows):
        for col in range(cols):
            canvas = tk.Canvas(points_frame, width=20, height=20, bg='white', highlightthickness=0)
            canvas.create_oval(5, 5, 15, 15, fill='red')
            canvas.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            app.div_card_canvases.append(canvas)

    for col in range(cols):
        points_frame.grid_columnconfigure(col, weight=1, uniform="col")
    for row in range(rows):
        points_frame.grid_rowconfigure(row, weight=1)

    close_button_frame = tk.Frame(popup, bg='white')
    close_button_frame.grid(row=1, column=0, sticky="ew")

    def save_and_close():
        app.div_card_points = []
        for canvas in app.div_card_canvases:
            x = canvas.winfo_rootx() + canvas.winfo_width() // 2
            y = canvas.winfo_rooty() + canvas.winfo_height() // 2
            app.div_card_points.append({"x": x, "y": y})
        app.save_settings()
        popup.destroy()

    close_button = tk.Button(close_button_frame, text="Close", command=save_and_close, bg="green", fg="white")
    close_button.pack(pady=10)

    def resize_points(event):
        new_width = event.width // cols - 10
        new_height = event.height // rows - 10
        for canvas in app.div_card_canvases:
            canvas.config(width=new_width, height=new_height)
            canvas.delete("all")
            canvas.create_oval(5, 5, new_width - 5, new_height - 5, fill='red')

    points_frame.bind("<Configure>", resize_points)

    def start_move(event):
        popup.x = event.x
        popup.y = event.y

    def stop_move(event):
        popup.x = None
        popup.y = None

    def on_move(event):
        deltax = event.x - popup.x
        deltay = event.y - popup.y
        x = popup.winfo_x() + deltax
        y = popup.winfo_y() + deltay
        popup.geometry(f"+{x}+{y}")

    popup.bind("<ButtonPress-1>", start_move)
    popup.bind("<ButtonRelease-1>", stop_move)
    popup.bind("<B1-Motion>", on_move)

    def start_resize(event):
        popup.resizing = {'x': event.x, 'y': event.y}

    def stop_resize(event):
        popup.resizing = None

    def on_resize(event):
        if popup.resizing:
            deltax = event.x - popup.resizing['x']
            deltay = event.y - popup.resizing['y']
            new_width = popup.winfo_width() + deltax
            new_height = popup.winfo_height() + deltay
            popup.geometry(f"{new_width}x{new_height}")
            popup.resizing['x'] = event.x
            popup.resizing['y'] = event.y

    popup.bind("<ButtonPress-3>", start_resize)
    popup.bind("<B3-Motion>", on_resize)
    popup.bind("<ButtonRelease-3>", stop_resize)


def exchange_divination_cards(app):
    app.load_settings()

    div_card_points = getattr(app, 'div_card_points', None)
    set_trade_str = getattr(app, 'set_trade_value', None)
    set_confirm_str = getattr(app, 'set_confirm_value', None)

    missing_settings = []
    if not div_card_points:
        missing_settings.append('div_card_points')
    if not set_trade_str:
        missing_settings.append('set_trade')
    if not set_confirm_str:
        missing_settings.append('set_confirm')

    if missing_settings:
        print("Les paramètres suivants ne sont pas configurés :", ", ".join(missing_settings))
        return

    if not isinstance(div_card_points, list) or not all(isinstance(pos, dict) and 'x' in pos and 'y' in pos for pos in div_card_points):
        print("Format invalide pour div_card_points.")
        return

    try:
        trade_x, trade_y = map(int, set_trade_str.split(";"))
        confirm_x, confirm_y = map(int, set_confirm_str.split(";"))
    except ValueError:
        print("Format invalide pour set_trade ou set_confirm.")
        return

    pyautogui.PAUSE = 0.001

    try:
        poe_window = gw.getWindowsWithTitle('Path of Exile')[0]
        poe_window.activate()
    except IndexError:
        print("Fenêtre Path of Exile non trouvée.")
        return

    total_columns = 12
    grid = [div_card_points[i:i+total_columns] for i in range(0, len(div_card_points), total_columns)]

    for col in range(total_columns):
        for row in range(len(grid)):
            try:
                pos = grid[row][col]
                pyautogui.moveTo(pos['x'], pos['y'])
                time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.1)

                copied_text = pyperclip.paste()

                if "Item Class: Divination Cards" not in copied_text:
                    print("L'élément n'est pas une carte de divination. Operation annulée.")
                    return

                pyautogui.keyDown('ctrl')
                pyautogui.click(button='left')
                pyautogui.keyUp('ctrl')
                time.sleep(random.uniform(0.17, 0.25))

                pyautogui.moveTo(trade_x, trade_y)
                time.sleep(random.uniform(0.17, 0.25))
                pyautogui.click()
                time.sleep(random.uniform(0.17, 0.25))

                pyautogui.moveTo(confirm_x, confirm_y)
                new_copied_text = safe_copy(copied_text)

                if "Item Class: Stackable Currency" not in new_copied_text:
                    print("Erreur : la classe de l'objet n'a pas changé. Operation annulée.")
                    return

                if copied_text == new_copied_text or new_copied_text == "":
                    print("Erreur : le contenu n'a pas changé après la confirmation. Operation annulée.")
                    return

                pyautogui.keyDown('ctrl')
                pyautogui.click(button='left')
                pyautogui.keyUp('ctrl')
                time.sleep(0.25)

            except Exception as e:
                print(f"Erreur lors du traitement de la position {pos} : {e}")
                return


def show_divination_card_module(app):
    app.update_tab_color(app.divination_card_tab)
    create_divination_card_content(app)
    app.divination_card_frame.grid(row=0, column=1, sticky="nsew")
    app.load_settings()

