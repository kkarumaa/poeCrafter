import tkinter as tk
from global_functions import background_color, text_color


def create_currency_content(app):
    app.currency_button_states = {}
    app.currency_frame = tk.Frame(app.root, bg=background_color)

    button_names = [
        ["Chromatic", "Stacked Deck", "Chance", "Reso 1", "Reso 2"],
        ["Fusing", "Scouring", "Chaos", "Fossil 1", "Reso 3"],
        ["Jeweller", "Transmut", "Alchemy", "Fossil 2", "Chisel"],
        ["Sextant", "Elevated", "Regal", "Fossil 3", "Exal"],
        ["Ichor", "Ember", "Harvest", "Space (Fossil)", "Annul"],
        ["Alteration", "Wisdom", "Compass", "Space (Sextant)", "Augment"],
        ["Alter 2nd", "Vaal", "GemCP", "Catalyst", "Essence"],
        ["Alter 3rd", "Flask Currency", "Haggle", "", ""]
    ]

    for row_index, row_values in enumerate(button_names):
        for col_index, button_name in enumerate(row_values):
            if button_name:
                app.currency_button_states[button_name] = ""
                button = tk.Button(
                    app.currency_frame,
                    text=button_name,
                    bg="#63748d",
                    fg=text_color,
                    height=2,
                    command=lambda bn=button_name: on_currency_button_click(app, bn)
                )
                button.grid(row=row_index, column=col_index, sticky="ew", padx=5, pady=5)

    for i in range(5):
        app.currency_frame.grid_columnconfigure(i, weight=1)
    for i in range(len(button_names)):
        app.currency_frame.grid_rowconfigure(i, weight=1)

    app.currency_frame.grid(row=0, column=1, sticky="nsew")


def on_currency_button_click(app, button_name):
    create_popup(app, button_name)


def create_popup(app, button_name):
    popup = tk.Toplevel(app.root)
    popup.attributes('-topmost', True)
    popup.resizable(False, False)

    popup.title(f"Popup for {button_name}")
    popup.geometry("200x100")
    popup.attributes("-alpha", 0.4)
    popup.attributes("-toolwindow", 1)
    popup.overrideredirect(True)

    window_width = 200
    window_height = 100
    popup.geometry(f"{window_width}x{window_height}")

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    popup.geometry(f"+{x}+{y}")

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

    canvas = tk.Canvas(popup, width=20, height=20, bg='white', highlightthickness=0)
    canvas.create_oval(5, 5, 15, 15, fill='red')
    canvas.grid(row=0, column=0, sticky='nw', padx=5, pady=5)

    label = tk.Label(popup, text=f"{button_name}")
    label.grid(row=0, column=1, padx=10, pady=10)

    def on_confirm():
        x = popup.winfo_x() + canvas.winfo_x() + 10
        y = popup.winfo_y() + canvas.winfo_y() + 10
        if button_name != "Set item":
            app.currency_button_states[button_name] = str(x) + ";" + str(y)
            update_button_colors(app)
        else:
            app.set_item_var = str(x) + ";" + str(y)
        app.save_settings()
        popup.destroy()

    confirm_button = tk.Button(popup, text="Confirm", command=on_confirm, bg="green")
    confirm_button.grid(row=1, column=0, padx=10, pady=10)


def update_button_colors(app):
    if hasattr(app, 'currency_frame') and app.currency_frame is not None:
        for button in app.currency_frame.winfo_children():
            if isinstance(button, tk.Button):
                button_name = button.cget("text")
                if app.currency_button_states.get(button_name, "") != "":
                    button.config(bg="#5f918b")
                else:
                    button.config(bg="#63748d")


def show_currency(app):
    app.update_tab_color(app.currency_tab)
    create_currency_content(app)
    app.currency_frame.grid(row=0, column=1, sticky="nsew")
    app.load_settings()

