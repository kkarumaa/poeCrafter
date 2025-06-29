import tkinter as tk
from tkinter import ttk
from global_functions import background_color, button_color, text_color


def create_beast_module_content(app):
    app.beast_module_frame = tk.Frame(app.root, bg=background_color)
    app.beast_switch_var = tk.BooleanVar(value=False)

    app.beast_label = tk.Label(app.beast_module_frame, text="Current Beast: Red Beast",
                               foreground=text_color, background=background_color, font=("Arial", 12))
    app.beast_label.pack(pady=10)

    app.switch_button = ttk.Checkbutton(app.beast_module_frame, text="Yellow Beast",
                                        variable=app.beast_switch_var, onvalue=True, offvalue=False,
                                        command=lambda: toggle_beast_state(app))
    app.switch_button.pack(pady=10)

    app.buttons_frame = tk.Frame(app.beast_module_frame, bg=background_color)
    app.set_inventory_button = tk.Button(app.buttons_frame, text="Set Inventory",
                                         command=lambda: app.open_chain_beast_popup(), bg=button_color, fg=text_color)
    app.set_inventory_button.pack(side=tk.LEFT, padx=5)
    app.set_beast_button = tk.Button(app.buttons_frame, text="Set Beast",
                                     command=lambda: set_beast_action(app), bg=button_color, fg=text_color)
    app.set_beast_button.pack(side=tk.LEFT, padx=5)
    app.buttons_frame.pack_forget()

    app.bestiary_input_frame = tk.Frame(app.beast_module_frame, bg=background_color)
    app.bestiary_columns_label = tk.Label(app.bestiary_input_frame, text="Nombre de colonnes Bestiary Orb : ",
                                          bg=background_color, fg=text_color)
    app.bestiary_columns_input = tk.Entry(app.bestiary_input_frame)
    app.bestiary_columns_label.pack(side=tk.LEFT, padx=5)
    app.bestiary_columns_input.pack(side=tk.LEFT, padx=5)
    app.bestiary_input_frame.pack_forget()

    app.fill_yellow_beast_button = tk.Button(app.beast_module_frame, text="Remplir Yellow Beast",
                                             command=lambda: app.fill_yellow_beast(), bg="green", fg="white")
    app.fill_yellow_beast_button.pack_forget()

    app.beast_module_frame.grid(row=0, column=1, sticky="nsew")


def toggle_beast_state(app):
    if app.beast_switch_var.get():
        app.beast_label.config(text="Current Beast: Yellow Beast")
        app.switch_button.config(text="Red Beast")
        if not hasattr(app, 'buttons_frame'):
            app.buttons_frame = tk.Frame(app.beast_module_frame, bg=background_color)
        app.buttons_frame.pack(pady=10)
        app.set_beast_button.pack(in_=app.buttons_frame, side=tk.LEFT, padx=5)
        app.set_inventory_button.pack(in_=app.buttons_frame, side=tk.LEFT, padx=5)
        app.bestiary_input_frame.pack(pady=5)
        app.bestiary_columns_label.pack(pady=5)
        app.bestiary_columns_input.pack(pady=5)
        app.fill_yellow_beast_button.pack(pady=5)
    else:
        app.beast_label.config(text="Current Beast: Red Beast")
        app.switch_button.config(text="Yellow Beast")
        app.buttons_frame.pack_forget()
        app.bestiary_input_frame.pack_forget()
        app.fill_yellow_beast_button.pack_forget()


def set_beast_action(app):
    app.create_popup("Set Beast")


def show_beast_module(app):
    app.update_tab_color(app.beast_module_tab)
    app.general_frame.grid_forget()
    create_beast_module_content(app)
    app.beast_module_frame.grid(row=0, column=1, sticky="nsew")
    app.load_settings()

