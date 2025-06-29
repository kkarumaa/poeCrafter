import tkinter as tk
from tkinter import ttk
from global_functions import background_color, text_color


def create_no_mod_craft_content(app):
    app.no_mod_craft_frame = tk.Frame(app.root, width=800, height=500, bg=background_color)
    bold_font = ('Helvetica', 10, 'bold')

    app.socket_var = tk.BooleanVar()
    app.socket_check = ttk.Checkbutton(app.no_mod_craft_frame, text="Socket", variable=app.socket_var,
                                        onvalue=True, offvalue=False)
    app.socket_check.grid(row=0, column=0, padx=20, pady=(80, 10), sticky="w")

    app.socket_entry = tk.Entry(app.no_mod_craft_frame, width=6)
    app.socket_entry.grid(row=0, column=2, padx=5, pady=(80, 10), sticky="e")
    app.socket_entry.insert(0, "6")

    app.link_var = tk.BooleanVar()
    app.link_check = ttk.Checkbutton(app.no_mod_craft_frame, text="Link", variable=app.link_var,
                                      onvalue=True, offvalue=False)
    app.link_check.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    app.link_entry = tk.Entry(app.no_mod_craft_frame, width=6)
    app.link_entry.grid(row=1, column=2, padx=5, pady=5, sticky="e")
    app.link_entry.insert(0, "5")

    app.color_var = tk.BooleanVar()
    app.color_check = ttk.Checkbutton(app.no_mod_craft_frame, text="Color", variable=app.color_var, onvalue=True,
                                       offvalue=False)
    app.color_check.grid(row=2, column=0, padx=20, pady=10, sticky="w")

    app.red_entry = tk.Entry(app.no_mod_craft_frame, bg="red", font=bold_font, width=2)
    app.red_entry.grid(row=2, column=3, padx=5, pady=5)
    app.red_entry.insert(0, "0")

    app.green_entry = tk.Entry(app.no_mod_craft_frame, bg="green", font=bold_font, width=2)
    app.green_entry.grid(row=2, column=4, padx=5, pady=5)
    app.green_entry.insert(0, "1")

    app.blue_entry = tk.Entry(app.no_mod_craft_frame, bg="#4ba6ff", font=bold_font, width=2)
    app.blue_entry.grid(row=2, column=5, padx=5, pady=5)
    app.blue_entry.insert(0, "5")

    app.no_mod_craft_frame.grid(row=0, column=1, sticky="nsew")


def show_no_mod_craft(app):
    app.update_tab_color(app.no_mod_craft_tab)
    create_no_mod_craft_content(app)
    app.no_mod_craft_frame.grid(row=0, column=1, sticky="nsew")
    app.load_settings()

