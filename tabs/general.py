import tkinter as tk
from tkinter import ttk
from global_functions import (
    background_color,
    text_color,
)


def create_general_content(app):
    app.general_frame = tk.Frame(app.root, width=800, height=500, bg=background_color)

    app.behavior_simulation_label = tk.Label(
        app.general_frame,
        text="Behavior Simulation:",
        font=("Arial", 14),
        foreground=text_color,
        background=background_color
    )
    app.behavior_simulation_label.grid(row=0, column=0, padx=20, pady=10, sticky="w", columnspan=3)

    app.random_delay_var = tk.BooleanVar()
    app.random_delay_checkbox = ttk.Checkbutton(app.general_frame, text="Random Delay Action",
                                                variable=app.random_delay_var, command=app.save_settings)
    app.random_delay_checkbox.grid(row=1, column=0, padx=20, pady=10)
    app.craft_delay_label = tk.Label(app.general_frame, text="Craft Delay (secondes):",
                                     foreground=text_color, background=background_color)
    app.craft_delay_label.grid(row=1, column=1, padx=(20, 5), pady=10)
    app.craft_delay_var = tk.DoubleVar(value=0.07)
    app.craft_delay_entry = tk.Entry(app.general_frame, textvariable=app.craft_delay_var, width=6)
    app.craft_delay_entry.grid(row=1, column=2, padx=(5, 20), pady=10)
    app.craft_delay_entry.bind("<KeyRelease>", app.save_inputs)

    app.disable_mouse_teleport_var = tk.BooleanVar()
    app.disable_mouse_teleport_checkbox = ttk.Checkbutton(
        app.general_frame,
        text="Disable mouse teleport",
        variable=app.disable_mouse_teleport_var,
        command=app.save_settings
    )
    app.disable_mouse_teleport_checkbox.grid(row=2, column=0, padx=20, pady=10)

    app.stop_if_no_currency_var = tk.BooleanVar()
    app.stop_if_no_currency_checkbox = ttk.Checkbutton(
        app.general_frame,
        text="Stop if no currency",
        variable=app.stop_if_no_currency_var,
        command=app.save_settings
    )
    app.stop_if_no_currency_checkbox.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="w")

    app.mouse_move_time_label = tk.Label(
        app.general_frame,
        text="Mouse move time (secondes):",
        foreground=text_color,
        background=background_color
    )
    app.mouse_move_time_label.grid(row=2, column=1, pady=10)

    app.mouse_move_time_var = tk.DoubleVar(value=0.2)
    app.mouse_move_time_entry = tk.Entry(
        app.general_frame,
        textvariable=app.mouse_move_time_var,
        width=6
    )
    app.mouse_move_time_entry.grid(row=2, column=2, pady=10)
    app.mouse_move_time_entry.bind("<KeyRelease>", app.save_inputs)

    app.stash_manager_label = tk.Label(
        app.general_frame,
        text="Stash manager:",
        font=("Arial", 14),
        foreground=text_color,
        background=background_color
    )
    app.stash_manager_label.grid(row=4, column=0, padx=20, pady=10, sticky="w", columnspan=3)

    app.stash_items_after_craft_var = tk.BooleanVar()
    app.stash_items_after_craft_checkbox = ttk.Checkbutton(
        app.general_frame,
        text="Stash items after fresh craft",
        variable=app.stash_items_after_craft_var,
        command=app.save_settings
    )
    app.stash_items_after_craft_checkbox.grid(row=5, column=0, padx=20, pady=10, sticky="w", columnspan=3)

    app.tabs_id_frame = tk.Frame(app.general_frame, bg=background_color)
    app.tabs_id_frame.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

    tab_ids = {
        "Currency": tk.StringVar(),
        "Compass": tk.StringVar(),
        "Item": tk.StringVar(),
        "Map": tk.StringVar()
    }

    for i, (tab_name, var) in enumerate(tab_ids.items()):
        label = tk.Label(
            app.tabs_id_frame,
            text=f"{tab_name} tab id:",
            foreground=text_color,
            background=background_color
        )
        label.grid(row=i, column=0, padx=(0, 5), pady=5, sticky="e")
        entry = tk.Entry(
            app.tabs_id_frame,
            textvariable=var,
            width=6
        )
        entry.grid(row=i, column=1, padx=(5, 0), pady=5)
        entry.bind("<KeyRelease>", app.save_inputs)
        setattr(app, f"{tab_name.lower()}_tab_id_var", var)

    app.root.grid_rowconfigure(0, weight=1)
    app.root.grid_columnconfigure(1, weight=1)
    app.general_frame.grid(sticky="nsew")


def show_general(app):
    app.update_tab_color(app.general_tab)
    create_general_content(app)
    app.general_frame.grid(row=0, column=1, sticky="nsew")
    app.load_settings()

