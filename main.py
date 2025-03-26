import random
import re
import time
import tkinter as tk
from tkinter import ttk
import os
import json
import pygetwindow as gw

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


def safe_copy(old_copy):
    for _ in range(7):
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.05)  # petit délai
        text = pyperclip.paste()
        if text.strip() != "" and text != old_copy:
            return text
    return ""


class App:

    def __init__(self, root):
        self.currency_button_states = {}
        self.root = root
        # Empêcher le redimensionnement de la fenêtre
        self.root.resizable(False, False)
        # Garder la fenêtre toujours au premier plan
        self.root.attributes('-topmost', True)
        self.root.title("KaruCrafter")

        # Configuration du style pour les éléments ttk
        style = ttk.Style()
        style.configure("TFrame", background=background_color)
        style.configure("TButton", foreground=text_color)
        style.configure("TCheckbutton", background=background_color, foreground=text_color)
        style.map("TButton", background=[("active", general_tab_color)])

        # Création de la barre de navigation latérale
        self.nav_frame = tk.Frame(root, width=200, height=500, bg=nav_bar_color)
        self.nav_frame.grid(row=0, column=0, sticky="ns")
        self.general_tab = tk.Button(self.nav_frame, text="Général", command=self.show_general, bg=button_color,
                                     fg=text_color)
        self.currency_tab = tk.Button(self.nav_frame, text="Currency", command=self.show_currency, bg=button_color,
                                      fg=text_color)
        self.no_mod_craft_tab = tk.Button(self.nav_frame, text="No Mod Craft", command=self.show_no_mod_craft,
                                          bg=button_color, fg=text_color)
        self.basic_craft = tk.Button(self.nav_frame, text="Basic Craft", command=self.show_basic_craft,
                                     bg=button_color, fg=text_color)
        self.rare_craft = tk.Button(self.nav_frame, text="Rare Craft", command=self.show_rare_craft,
                                    bg=button_color, fg=text_color)
        self.map_craft_tab = tk.Button(self.nav_frame, text="Map Craft", command=self.show_map_craft, bg=button_color,
                                       fg=text_color)
        self.harvest_exchange_tab = tk.Button(self.nav_frame, text="Harvest Exchange",
                                              command=self.show_harvest_exchange, bg=button_color, fg=text_color)
        self.sextant_tab = tk.Button(self.nav_frame, text="Sextant", command=self.show_sextant, bg=button_color,
                                     fg=text_color)
        self.expedition_tab = tk.Button(self.nav_frame, text="Expedition", command=self.show_expedition,
                                        bg=button_color, fg=text_color)
        self.beast_module_tab = tk.Button(self.nav_frame, text="Beast Recuperation",
                                              command=self.show_beast_module, bg=button_color, fg=text_color)
        self.divination_card_tab = tk.Button(self.nav_frame, text="Divination Card",
                                             command=self.show_divination_card_module, bg=button_color, fg=text_color)

        # Liste des onglets
        self.tabs = [self.general_tab, self.currency_tab, self.no_mod_craft_tab, self.basic_craft, self.rare_craft,
                     self.map_craft_tab, self.harvest_exchange_tab, self.sextant_tab, self.expedition_tab, self.beast_module_tab, self.divination_card_tab]

        # Positionner les boutons
        for tab in self.tabs:
            tab.pack(pady=10, fill=tk.X)

        # Initialisation de l'onglet général
        self.selected_tab = self.general_tab
        self.show_general()
        self.create_footer()

    def create_general_content(self):

        """ Créer le contenu de l'onglet général """
        self.general_frame = tk.Frame(self.root, width=800, height=500, bg=background_color)

        # Ajout du titre 'Behavior Simulation'
        self.behavior_simulation_label = tk.Label(
            self.general_frame,
            text="Behavior Simulation:",
            font=("Arial", 14),
            foreground=text_color,
            background=background_color
        )

        # Positionnez ce label au-dessus des premiers champs que nous avons créés,
        # ajustez le numéro de la ligne (row) selon l'endroit où vous voulez que le titre apparaisse.
        self.behavior_simulation_label.grid(row=0, column=0, padx=20, pady=10, sticky="w", columnspan=3)

        self.random_delay_var = tk.BooleanVar()
        self.random_delay_checkbox = ttk.Checkbutton(self.general_frame, text="Random Delay Action",
                                                     variable=self.random_delay_var, command=self.save_settings)
        self.random_delay_checkbox.grid(row=1, column=0, padx=20, pady=10)
        self.craft_delay_label = tk.Label(self.general_frame, text="Craft Delay (secondes):",
                                          foreground=text_color, background=background_color)
        self.craft_delay_label.grid(row=1, column=1, padx=(20, 5), pady=10)
        self.craft_delay_var = tk.DoubleVar(value=0.07)
        self.craft_delay_entry = tk.Entry(self.general_frame, textvariable=self.craft_delay_var, width=6)
        self.craft_delay_entry.grid(row=1, column=2, padx=(5, 20), pady=10)
        self.craft_delay_entry.bind("<KeyRelease>", self.save_inputs)

        # Checkbutton pour 'Disable mouse teleport'
        self.disable_mouse_teleport_var = tk.BooleanVar()
        self.disable_mouse_teleport_checkbox = ttk.Checkbutton(
            self.general_frame,
            text="Disable mouse teleport",
            variable=self.disable_mouse_teleport_var,
            command=self.save_settings
        )
        self.disable_mouse_teleport_checkbox.grid(row=2, column=0, padx=20, pady=10)

        # Checkbutton pour 'Stop if no currency'
        self.stop_if_no_currency_var = tk.BooleanVar()
        self.stop_if_no_currency_checkbox = ttk.Checkbutton(
            self.general_frame,
            text="Stop if no currency",
            variable=self.stop_if_no_currency_var,
            command=self.save_settings
        )
        # Utilisez 'row=2' pour le placer sous 'Mouse move time', et 'columnspan=3' pour couvrir toute la largeur
        self.stop_if_no_currency_checkbox.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="w")

        # Entry pour 'Mouse move time'
        self.mouse_move_time_label = tk.Label(
            self.general_frame,
            text="Mouse move time (secondes):",
            foreground=text_color,
            background=background_color
        )
        # Cette fois, nous utilisons row=1 pour être juste en dessous de 'Craft Delay'
        self.mouse_move_time_label.grid(row=2, column=1, pady=10)

        self.mouse_move_time_var = tk.DoubleVar(value=0.2)
        self.mouse_move_time_entry = tk.Entry(
            self.general_frame,
            textvariable=self.mouse_move_time_var,
            width=6
        )
        # Même rangée que le label, mais dans la colonne suivante
        self.mouse_move_time_entry.grid(row=2, column=2, pady=10)
        self.mouse_move_time_entry.bind("<KeyRelease>", self.save_inputs)

        # Section 'Stash manager'
        self.stash_manager_label = tk.Label(
            self.general_frame,
            text="Stash manager:",
            font=("Arial", 14),
            foreground=text_color,
            background=background_color
        )
        self.stash_manager_label.grid(row=4, column=0, padx=20, pady=10, sticky="w", columnspan=3)

        # Checkbutton pour 'Stash items after fresh craft'
        self.stash_items_after_craft_var = tk.BooleanVar()
        self.stash_items_after_craft_checkbox = ttk.Checkbutton(
            self.general_frame,
            text="Stash items after fresh craft",
            variable=self.stash_items_after_craft_var,
            command=self.save_settings
        )
        self.stash_items_after_craft_checkbox.grid(row=5, column=0, padx=20, pady=10, sticky="w", columnspan=3)

        # Création d'un nouveau Frame pour les IDs des onglets.
        self.tabs_id_frame = tk.Frame(self.general_frame, bg=background_color)
        self.tabs_id_frame.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

        # Maintenant, vous placez les labels et les entries dans ce nouveau Frame.
        tab_ids = {
            "Currency": tk.StringVar(),
            "Compass": tk.StringVar(),
            "Item": tk.StringVar(),
            "Map": tk.StringVar()
        }

        for i, (tab_name, var) in enumerate(tab_ids.items()):
            label = tk.Label(
                self.tabs_id_frame,
                text=f"{tab_name} tab id:",
                foreground=text_color,
                background=background_color
            )
            label.grid(row=i, column=0, padx=(0, 5), pady=5, sticky="e")
            entry = tk.Entry(
                self.tabs_id_frame,
                textvariable=var,
                width=6
            )
            entry.grid(row=i, column=1, padx=(5, 0), pady=5)
            entry.bind("<KeyRelease>", self.save_inputs)
            setattr(self, f"{tab_name.lower()}_tab_id_var", var)

        # Après avoir créé tous les widgets dans l'onglet général
        self.root.grid_rowconfigure(0, weight=1)  # Ceci permet à la rangée 0 de se développer
        self.root.grid_columnconfigure(1, weight=1)  # Ceci permet à la colonne 1 de se développer

        # Et assurez-vous que self.general_frame se développe et remplit l'espace disponible
        self.general_frame.grid(sticky="nsew")

    def create_currency_content(self):
        self.currency_button_states = {}
        # Création du Frame pour les contenus de l'onglet 'Currency'
        self.currency_frame = tk.Frame(self.root, bg=background_color)

        # Liste des noms des boutons, organisée par rangées comme sur la maquette
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

        # Créer et placer les boutons dans la grille
        for row_index, row_values in enumerate(button_names):
            for col_index, button_name in enumerate(row_values):
                if button_name:
                    # Initialiser l'état du bouton à False
                    self.currency_button_states[button_name] = ""

                    # Création du bouton
                    button = tk.Button(
                        self.currency_frame,
                        text=button_name,
                        bg="#63748d",
                        fg=text_color,
                        height=2,
                        command=lambda bn=button_name: self.on_currency_button_click(bn)
                    )
                    button.grid(row=row_index, column=col_index, sticky="ew", padx=5, pady=5)

        # Configuration de la grille pour l'espacement et l'alignement
        for i in range(5):  # Selon le nombre de colonnes
            self.currency_frame.grid_columnconfigure(i, weight=1)
        for i in range(len(button_names)):  # Selon le nombre de lignes
            self.currency_frame.grid_rowconfigure(i, weight=1)

        # Placer le Frame dans la fenêtre principale
        self.currency_frame.grid(row=0, column=1, sticky="nsew")

    def on_currency_button_click(self, button_name):
        # Appel de la popup
        self.create_popup(button_name)

    def create_popup(self, button_name):
        # Création de la fenêtre popup
        popup = tk.Toplevel(self.root)

        # Garder la fenêtre toujours au premier plan
        popup.attributes('-topmost', True)
        popup.resizable(False, False)

        popup.title(f"Popup for {button_name}")
        popup.geometry("200x100")  # Taille de la popup
        popup.attributes("-alpha", 0.4)  # Rendre la fenêtre semi-transparente

        # Supprimer le bouton de maximisation/minimisation
        popup.attributes("-toolwindow", 1)
        # Retirer la barre de titre standard
        popup.overrideredirect(True)

        # Taille de la popup
        window_width = 200
        window_height = 100
        popup.geometry(f"{window_width}x{window_height}")

        # Obtenir les dimensions de l'écran
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        # Calculer x et y pour centrer la fenêtre
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        # Positionner la fenêtre au centre de l'écran
        popup.geometry(f"+{x}+{y}")

        # Fonction pour déplacer la fenêtre
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

        # Liaison des événements de la souris pour le déplacement
        popup.bind("<ButtonPress-1>", start_move)
        popup.bind("<ButtonRelease-1>", stop_move)
        popup.bind("<B1-Motion>", on_move)

        # Création du marqueur rouge
        canvas = tk.Canvas(popup, width=20, height=20, bg='white', highlightthickness=0)
        canvas.create_oval(5, 5, 15, 15, fill='red')
        canvas.grid(row=0, column=0, sticky='nw', padx=5, pady=5)

        # Ajout d'un label ou d'autres widgets si nécessaire
        label = tk.Label(popup, text=f"{button_name}")
        label.grid(row=0, column=1, padx=10, pady=10)

        # Fonction pour gérer l'action de confirmation
        def on_confirm():
            x = popup.winfo_x() + canvas.winfo_x() + 10
            y = popup.winfo_y() + canvas.winfo_y() + 10
            if button_name != "Set item":
                self.currency_button_states[button_name] = str(x) + ";" + str(y)
                self.update_button_colors()
            else:
                self.set_item_var = str(x) + ";" + str(y)
            print(f"Centre du point rouge sur l'écran pour {button_name}: ({x}, {y})")
            self.save_settings()
            popup.destroy()

        # Ajout d'un bouton de confirmation
        confirm_button = tk.Button(popup, text="Confirm", command=on_confirm, bg="green")
        confirm_button.grid(row=1, column=0, padx=10, pady=10)

    def update_button_colors(self):
        """ Mettre à jour les couleurs des boutons en fonction de leur état """
        # Vérifier si currency_frame existe avant de procéder
        if hasattr(self, 'currency_frame') and self.currency_frame is not None:
            for button in self.currency_frame.winfo_children():
                if isinstance(button, tk.Button):
                    button_name = button.cget("text")
                    if self.currency_button_states.get(button_name, "") != "":
                        button.config(bg="#5f918b")
                    else:
                        button.config(bg="#63748d")


    def create_no_mod_craft_content(self):
        self.no_mod_craft_frame = tk.Frame(self.root, width=800, height=500, bg=background_color)
        bold_font = ('Helvetica', 10, 'bold')  # Création d'une police en gras

        # Ajout de la CheckBox ttk et de la section 'Socket'
        self.socket_var = tk.BooleanVar()
        self.socket_check = ttk.Checkbutton(self.no_mod_craft_frame, text="Socket", variable=self.socket_var,
                                            onvalue=True, offvalue=False)
        self.socket_check.grid(row=0, column=0, padx=20, pady=(80, 10), sticky="w")

        self.socket_entry = tk.Entry(self.no_mod_craft_frame, width=6)
        self.socket_entry.grid(row=0, column=2, padx=5, pady=(80, 10), sticky="e")
        self.socket_entry.insert(0, "6")  # Default value

        # Ajout de la CheckBox ttk et de la section 'Link'
        self.link_var = tk.BooleanVar()
        self.link_check = ttk.Checkbutton(self.no_mod_craft_frame, text="Link", variable=self.link_var, onvalue=True,
                                          offvalue=False)
        self.link_check.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.link_entry = tk.Entry(self.no_mod_craft_frame, width=6)
        self.link_entry.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.link_entry.insert(0, "5")  # Default value

        # Ajout de la CheckBox ttk et de la section 'Color'
        self.color_var = tk.BooleanVar()
        self.color_check = ttk.Checkbutton(self.no_mod_craft_frame, text="Color", variable=self.color_var, onvalue=True,
                                           offvalue=False)
        self.color_check.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        # Exemple d'entrées textuelles avec fond coloré
        self.red_entry = tk.Entry(self.no_mod_craft_frame, bg="red", font=bold_font, width=2)
        self.red_entry.grid(row=2, column=3, padx=5, pady=5)
        self.red_entry.insert(0, "0")  # Valeur par défaut

        self.green_entry = tk.Entry(self.no_mod_craft_frame, bg="green", font=bold_font, width=2)
        self.green_entry.grid(row=2, column=4, padx=5, pady=5)
        self.green_entry.insert(0, "1")  # Valeur par défaut

        self.blue_entry = tk.Entry(self.no_mod_craft_frame, bg="#4ba6ff", font=bold_font, width=2)
        self.blue_entry.grid(row=2, column=5, padx=5, pady=5)
        self.blue_entry.insert(0, "5")  # Valeur par défaut

        # Afficher le Frame
        self.no_mod_craft_frame.grid(row=0, column=1, sticky="nsew")

    def create_basic_craft(self):
        self.basic_craft_frame = tk.Frame(self.root, bg=background_color)
        self.check_vars = {}
        self.check_buttons = {}  # Pour stocker les références des boutons Checkbutton

        # Sous-frame pour les Checkbuttons
        buttons_frame = tk.Frame(self.basic_craft_frame, bg=background_color)
        buttons_frame.grid(row=0, column=0, padx=10, pady=10)

        # Définition des options de crafting
        crafting_options = [
            "Magic", "Fossil 1", "Rare (chaos)",
            "Use Aug?", "Fossil 2", "Rare (alchemy)",
            "Implicit blue", "Fossil 3", "Essence",
            "Implicit red", "Flask enchant", "Harvest"
        ]

        # Création des Checkbuttons pour les options de crafting
        for i, option in enumerate(crafting_options):
            self.check_vars[option] = tk.BooleanVar()

            # Création du Checkbutton et enregistrement de sa référence
            self.check_buttons[option] = ttk.Checkbutton(buttons_frame, text=option, variable=self.check_vars[option])

            # Configuration de la commande à exécuter sur action
            if option == "Magic":
                self.check_buttons[option].config(command=self.toggle_use_aug)

            row = i // 3  # Calcule la rangée actuelle en divisant l'index par 3 (le nombre de colonnes)
            column = i % 3  # Calcule la colonne actuelle en utilisant le modulo de 3
            self.check_buttons[option].grid(row=row, column=column, padx=5, pady=5, sticky="w")

        # Initialisation de "Use Aug?" comme désactivé si "Magic" n'est pas coché
        self.toggle_use_aug()

        # Barre de recherche
        search_frame = tk.Frame(self.basic_craft_frame, bg=background_color)
        search_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Champ de saisie pour la recherche
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, fg='white', bg='#142131',
                                insertbackground='white')
        search_entry.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ew")
        search_entry.insert(0, "Search something...")

        # Fonction pour vider le texte du champ de recherche lorsqu'il est cliqué
        def clear_search_entry(event):
            search_entry.delete(0, tk.END)

        # Fonction pour restaurer le texte du champ de recherche si vide lorsque le champ perd le focus
        def restore_search_entry(event):
            if not search_entry.get():
                search_entry.insert(0, "Search something...")

        # Liaison de la fonction au clic gauche sur le champ de recherche
        search_entry.bind("<Button-1>", clear_search_entry)
        search_entry.bind("<FocusOut>", restore_search_entry)

        # Combobox pour les options de recherche avec les éléments de la capture d'écran
        combobox_options = [
            "abyss_p", "abyss_s", "cluster_p", "cluster_s", "flask_p", "flask_s",
            "implicit", "item_p", "item_s", "jewel_p", "jewel_s"
        ]

        # Combobox pour les options de recherche
        self.search_options = tk.StringVar()
        search_combobox = ttk.Combobox(search_frame, textvariable=self.search_options, values=combobox_options,
                                       state='readonly')
        search_combobox.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="ew")
        search_combobox.set('abyss_p')

        # Configuration de la sous-frame pour étendre le champ de saisie en fonction de l'espace disponible
        search_frame.grid_columnconfigure(0, weight=1)

        # Afficher le cadre de crafting de base
        self.basic_craft_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def toggle_use_aug(self):
        # Activer ou désactiver "Use Aug?" en fonction de l'état de "Magic"
        if self.check_vars["Magic"].get():
            self.check_buttons["Use Aug?"].config(state='normal')
        else:
            self.check_vars["Use Aug?"].set(False)  # Décocher "Use Aug?"
            self.check_buttons["Use Aug?"].config(state='disabled')

    def show_general(self):
        """ Afficher l'onglet général """
        self.update_tab_color(self.general_tab)
        self.create_general_content()  # Assurez-vous que le contenu est créé
        self.general_frame.grid(row=0, column=1, sticky="nsew")
        self.load_settings()  # Charger les paramètres lors de l'affichage de cet onglet

    def show_currency(self):
        """ Afficher l'onglet Currency """
        self.update_tab_color(self.currency_tab)
        self.create_currency_content()  # Assurez-vous que le contenu est créé
        self.currency_frame.grid(row=0, column=1, sticky="nsew")
        self.load_settings()  # Charger les paramètres lors de l'affichage de cet onglet

    def show_no_mod_craft(self):
        """ Afficher l'onglet No Mod Craft """
        self.update_tab_color(self.no_mod_craft_tab)
        self.create_no_mod_craft_content()  # Assurez-vous que le contenu est créé
        self.no_mod_craft_frame.grid(row=0, column=1, sticky="nsew")
        self.load_settings()  # Charger les paramètres lors de l'affichage de cet onglet

    def show_basic_craft(self):
        """ Afficher l'onglet Basic Craft """
        self.update_tab_color(self.basic_craft)
        self.create_basic_craft()  # Assurez-vous que le contenu est créé
        self.basic_craft_frame.grid(row=0, column=1, sticky="nsew")
        self.load_settings()  # Charger les paramètres lors de l'affichage de cet onglet

    def show_rare_craft(self):
        """ Afficher l'onglet Rare Craft """
        self.update_tab_color(self.rare_craft)
        self.general_frame.grid_forget()
        self.craft_with_mods_frame = tk.Frame(self.root, width=800, height=500,
                                              bg="#00f")  # Exemple de contenu de l'onglet Craft with Mods
        self.craft_with_mods_frame.grid(row=0, column=1, sticky="nsew")
        tk.Label(self.craft_with_mods_frame, text="Craft with Mods Tab", bg="#00f", fg="white").pack(pady=20)

    def show_map_craft(self):
        """ Afficher l'onglet Map Craft """
        self.update_tab_color(self.map_craft_tab)
        self.general_frame.grid_forget()
        self.map_craft_frame = tk.Frame(self.root, width=800, height=500,
                                        bg="#0ff")  # Exemple de contenu de l'onglet Map Craft
        self.map_craft_frame.grid(row=0, column=1, sticky="nsew")
        tk.Label(self.map_craft_frame, text="Map Craft Tab", bg="#0ff", fg="white").pack(pady=20)

    def show_harvest_exchange(self):
        """ Afficher l'onglet Harvest Exchange """
        self.update_tab_color(self.harvest_exchange_tab)
        self.general_frame.grid_forget()
        self.harvest_exchange_frame = tk.Frame(self.root, width=800, height=500,
                                               bg="#ff0")  # Exemple de contenu de l'onglet Harvest Exchange
        self.harvest_exchange_frame.grid(row=0, column=1, sticky="nsew")
        tk.Label(self.harvest_exchange_frame, text="Harvest Exchange Tab", bg="#ff0", fg="white").pack(pady=20)

    def show_sextant(self):
        """ Afficher l'onglet Sextant """
        self.update_tab_color(self.sextant_tab)
        self.general_frame.grid_forget()
        self.sextant_frame = tk.Frame(self.root, width=800, height=500,
                                      bg="#f0f")  # Exemple de contenu de l'onglet Sextant
        self.sextant_frame.grid(row=0, column=1, sticky="nsew")
        tk.Label(self.sextant_frame, text="Sextant Tab", bg="#f0f", fg="white").pack(pady=20)

    def show_expedition(self):
        """ Afficher l'onglet Expedition """
        self.update_tab_color(self.expedition_tab)
        self.general_frame.grid_forget()
        self.expedition_frame = tk.Frame(self.root, width=800, height=500,
                                         bg="#0a0")  # Exemple de contenu de l'onglet Expedition
        self.expedition_frame.grid(row=0, column=1, sticky="nsew")
        tk.Label(self.expedition_frame, text="Expedition Tab", bg="#0a0", fg="white").pack(pady=20)

    def show_beast_module(self):
        """ Afficher l'onglet Beast Module """
        self.update_tab_color(self.beast_module_tab)
        self.general_frame.grid_forget()  # Masquer les autres cadres
        self.create_beast_module_content()  # Créer le contenu de l'onglet Beast Module
        self.beast_module_frame.grid(row=0, column=1, sticky="nsew")
        self.load_settings()  # Charger les paramètres pour cet onglet

        # Si des points rouges sont présents, les afficher dans le tableau
        #if self.chain_beast_points:
            #self.update_points_table()

    def create_beast_module_content(self):
        self.beast_module_frame = tk.Frame(self.root, bg=background_color)

        # Variable pour stocker l'état (True pour Yellow Beast, False pour Red Beast)
        self.beast_switch_var = tk.BooleanVar(value=False)

        # Label pour afficher l'état actuel de la bête
        self.beast_label = tk.Label(self.beast_module_frame, text="Current Beast: Red Beast",
                                    foreground=text_color, background=background_color, font=("Arial", 12))
        self.beast_label.pack(pady=10)

        # Checkbutton pour basculer entre "Red Beast" et "Yellow Beast"
        self.switch_button = ttk.Checkbutton(self.beast_module_frame, text="Yellow Beast",
                                             variable=self.beast_switch_var, onvalue=True, offvalue=False,
                                             command=self.toggle_beast_state)
        self.switch_button.pack(pady=10)

        # Cadre pour contenir les boutons "Set Inventory" et "Set Beast"
        self.buttons_frame = tk.Frame(self.beast_module_frame, bg=background_color)

        # Bouton "Set Inventory"
        self.set_inventory_button = tk.Button(self.buttons_frame, text="Set Inventory",
                                              command=self.open_chain_beast_popup, bg=button_color, fg=text_color)
        self.set_inventory_button.pack(side=tk.LEFT, padx=5)

        # Bouton "Set Beast"
        self.set_beast_button = tk.Button(self.buttons_frame, text="Set Beast",
                                          command=self.set_beast_action, bg=button_color, fg=text_color)
        self.set_beast_button.pack(side=tk.LEFT, padx=5)

        # Afficher le cadre des boutons
        self.buttons_frame.pack_forget()

        # Cadre pour l'intitulé et l'input côte à côte
        self.bestiary_input_frame = tk.Frame(self.beast_module_frame, bg=background_color)

        # Ajout d'un champ d'entrée pour "nombre de colonnes Bestiary Orb"
        self.bestiary_columns_label = tk.Label(self.bestiary_input_frame, text="Nombre de colonnes Bestiary Orb : ",
                                               bg=background_color, fg=text_color)
        self.bestiary_columns_input = tk.Entry(self.bestiary_input_frame)

        # Placer le label et l'input côte à côte
        self.bestiary_columns_label.pack(side=tk.LEFT, padx=5)
        self.bestiary_columns_input.pack(side=tk.LEFT, padx=5)

        # Cacher le champ d'entrée par défaut
        self.bestiary_input_frame.pack_forget()

        # Ajouter le bouton "Remplir Yellow Beast"
        self.fill_yellow_beast_button = tk.Button(self.beast_module_frame, text="Remplir Yellow Beast",
                                                  command=self.fill_yellow_beast, bg="green", fg="white")
        # Cacher le bouton par défaut
        self.fill_yellow_beast_button.pack_forget()

        # Bouton pour tester les positions (masqué après création)
        self.test_position_button = tk.Button(self.beast_module_frame, text="Tester Position",
                                              command=self.test_positions, bg="blue", fg="white")
        self.test_position_button.pack(pady=10)
        self.test_position_button.pack_forget()  # Masqué par défaut

        # Bouton pour appeler la fonction check avec le premier élément de chain_beast_points
        self.check_button = tk.Button(self.beast_module_frame, text="Check First Beast Position",
                                      command=self.check_first_beast_position, bg="blue", fg="white")
        self.check_button.pack(pady=10)
        self.check_button.pack_forget()  # Masqué par défaut (car un élément de test)

        # Nouveau bouton "Compter Bestiary Orb"
        self.count_bestiary_orb_button = tk.Button(self.beast_module_frame, text="Compter Bestiary Orb",
                                                   command=self.count_bestiary_orb, bg="blue", fg="white")
        self.count_bestiary_orb_button.pack(pady=10)
        self.count_bestiary_orb_button.pack_forget()  # Masqué par défaut (car un élément de test)

        # Nouveau bouton "Vérifier les emplacements vides"
        self.check_empty_positions_button = tk.Button(self.beast_module_frame, text="Vérifier les emplacements vides",
                                                      command=self.check_empty_positions, bg="blue", fg="white")
        self.check_empty_positions_button.pack(pady=10)
        self.check_empty_positions_button.pack_forget()  # Masqué par défaut

        # Afficher le cadre du Beast Module
        self.beast_module_frame.grid(row=0, column=1, sticky="nsew")



    def toggle_beast_state(self):
        # Si l'état est True, la bête est "Yellow Beast", sinon "Red Beast"
        if self.beast_switch_var.get():
            self.beast_label.config(text="Current Beast: Yellow Beast")
            self.switch_button.config(text="Red Beast")

            # Créer un cadre pour contenir les deux boutons côte à côte
            if not hasattr(self, 'buttons_frame'):
                self.buttons_frame = tk.Frame(self.beast_module_frame, bg=background_color)

            self.buttons_frame.pack(pady=10)
            # Afficher les boutons côte à côte dans le nouveau cadre
            self.set_beast_button.pack(in_=self.buttons_frame, side=tk.LEFT, padx=5)
            self.set_inventory_button.pack(in_=self.buttons_frame, side=tk.LEFT, padx=5)

            self.bestiary_input_frame.pack(pady=5)
            self.bestiary_columns_label.pack(pady=5)
            self.bestiary_columns_input.pack(pady=5)
            self.fill_yellow_beast_button.pack(pady=5)

        else:
            self.beast_label.config(text="Current Beast: Red Beast")
            self.switch_button.config(text="Yellow Beast")

            # Masquer le cadre contenant les deux boutons
            self.buttons_frame.pack_forget()
            self.bestiary_input_frame.pack_forget()
            self.fill_yellow_beast_button.pack_forget()


    def set_beast_action(self):
        """ Afficher 'Set Beast' dans la console """
        self.create_popup("Set Beast")


    def update_points_table(self):
        """ Mettre à jour le tableau avec les coordonnées des points rouges """
        # Vider le tableau existant
        for item in self.points_table.get_children():
            self.points_table.delete(item)

        # Charger les points rouges depuis self.chain_beast_points
        for point in self.chain_beast_points:
            self.points_table.insert('', tk.END, values=(point['x'], point['y']))

    def test_positions(self):
        """ Simuler un clic gauche sur chaque position des points rouges, toutes les 5 secondes """
        if not self.chain_beast_points:
            print("Aucune position à tester.")
            return

        for point in self.chain_beast_points:
            x = point['x']
            y = point['y']
            print(f"Cliquant à la position: ({x}, {y})")

            # Déplacer la souris à la position et effectuer un clic gauche
            pyautogui.moveTo(x, y)
            pyautogui.click()

            # Attendre 5 secondes avant de passer au point suivant
            time.sleep(5)

    def check_first_beast_position(self):
        """ Appelle la fonction check avec la première position de chain_beast_points et 'beast' comme texte """
        if self.chain_beast_points:
            # Extraire la première position
            first_point = self.chain_beast_points[0]
            x, y = first_point['x'], first_point['y']
            # Appeler la fonction check avec les coordonnées et le texte 'beast'
            self.check(x, y, "beast")
        else:
            print("Aucune position de Beast disponible.")

    def count_bestiary_orb(self):
        """ Parcourt toutes les positions de chain_beast_points et compte combien contiennent 'Bestiary Orb' """
        if not self.chain_beast_points:
            print("Aucune position de Beast disponible.")
            return

        total_orbs = 0
        pyautogui.PAUSE = 0.001

        # Ramener "Path of Exile" au premier plan
        poe_window = gw.getWindowsWithTitle('Path of Exile')[0]  # Remplacez par le titre exact de la fenêtre
        poe_window.activate()

        # Parcourir toutes les positions et utiliser la fonction check
        for point in self.chain_beast_points:
            x, y = point['x'], point['y']
            is_bestiary_orb, copied_text = self.check(x, y, "Bestiary Orb")

            if is_bestiary_orb:
                # Rechercher le stack size dans le texte
                match = re.search(r"Stack Size: (\d+)/10", copied_text)
                if match:
                    # Extraire le nombre avant /10
                    orb_count = int(match.group(1))
                    total_orbs += orb_count
                    print(f"Orbes trouvés à la position ({x}, {y}): {orb_count}")

        # Afficher le résultat dans la console
        print(f"Nombre de 'Bestiary Orb' trouvés : {total_orbs}")

    def check_empty_positions(self):
        """ Parcourt les positions de chain_beast_points et détermine si un emplacement est vide
            en comparant avec le texte copié de la position précédente.
        """
        if not self.chain_beast_points or len(self.chain_beast_points) < 2:
            print("Pas assez de positions pour vérifier les emplacements vides.")
            return

        previous_text = "None"
        empty_positions = []

        pyautogui.PAUSE = 0.001

        # Ramener "Path of Exile" au premier plan
        poe_window = gw.getWindowsWithTitle('Path of Exile')[0]  # Remplacez par le titre exact de la fenêtre
        poe_window.activate()

        # Parcourir toutes les positions, sauf la première
        for index, point in enumerate(self.chain_beast_points[1:], start=1):
            x, y = point['x'], point['y']

            # Vérifier la position actuelle par rapport à la précédente
            is_empty, copied_text = self.check(x, y, previous_text)

            if is_empty:
                empty_positions.append(index)

            # Mettre à jour le texte précédent avec le texte actuel copié
            previous_text = copied_text

        # Afficher les emplacements vides
        if empty_positions:
            for pos in empty_positions:
                print(f"Position {pos} : Emplacement vide")
        else:
            print("Aucun emplacement vide trouvé.")

    def fill_yellow_beast(self):
        """ Vérifie l'input et effectue un check sur la première position si l'input est valide """

        # Charger les paramètres depuis le fichier
        self.load_settings()

        try:

            # Vérifier la valeur de set_beast_value pour voir si elle contient une position valide
            if not self.set_beast_value:
                print("Veuillez définir la position de 'Set Beast'.")
                return

            try:
                x, y = map(int, self.set_beast_value.split(';'))
            except ValueError:
                print("La position 'Set Beast' n'est pas valide. Veuillez la définir correctement.")
                return


            # Récupérer la valeur de l'input
            columns_value = int(self.bestiary_columns_input.get())

            # Vérifier si la valeur est comprise entre 1 et 11
            if 1 <= columns_value <= 11:
                print(f"Nombre de colonnes validé : {columns_value}")

                # Diviser le tableau 1D en lignes selon le nombre de colonnes (12 colonnes par ligne)
                total_columns = 12  # Hypothèse : chaque ligne a 12 colonnes
                grid = [self.chain_beast_points[i:i+total_columns] for i in range(0, len(self.chain_beast_points), total_columns)]

                # Diviser le tableau grid en deux : Bestiary Orb et fill
                bestiary_orb = []  # Tableau Bestiary Orb
                fill = []  # Tableau fill

                # Pour chaque ligne dans le grid, diviser selon le nombre de colonnes spécifié
                for row in grid:
                    bestiary_orb.append(row[:columns_value])  # Les premières colonnes
                    fill.append(row[columns_value:])  # Les colonnes restantes

                print(f"Tableau 'Bestiary Orb' : {bestiary_orb}")
                print(f"Tableau 'fill' : {fill}")

                # Aplatir les tableaux Bestiary Orb et fill en une seule dimension
                bestiary_orb_flat = [pos for sublist in bestiary_orb for pos in sublist]
                fill_flat = [pos for sublist in fill for pos in sublist]

                pyautogui.PAUSE = 0.001

                # Ramener "Path of Exile" au premier plan
                poe_window = gw.getWindowsWithTitle('Path of Exile')[0]  # Remplacez par le titre exact de la fenêtre
                poe_window.activate()

                # Boucle sur chaque position de bestiary_orb_flat
                for first_point in bestiary_orb_flat:
                    first_x, first_y = first_point['x'], first_point['y']

                    # Appeler la méthode check sur la position actuelle
                    is_orb_found, copied_text = self.check(first_x, first_y, "Bestiary Orb")

                    if is_orb_found:
                        # Utiliser une regex pour trouver "Stack Size: X/10"
                        match = re.search(r"Stack Size: (\d+)/10", copied_text)
                        if match:
                            # Extraire le nombre d'orbes avant /10
                            orb_count = int(match.group(1))
                            print(f"Orbes trouvés à la position ({first_x}, {first_y}): {orb_count}")

                            # Vérifier si le nombre d'orbes est compris entre 1 et 10
                            if 1 <= orb_count <= 10:
                                total_orbs = orb_count
                                print(f"Nombre d'orbes disponible : {total_orbs}")
                                # Appeler la fonction verify_and_iterate_positions avec les bons paramètres
                                self.verify_and_iterate_positions(fill_flat, total_orbs, first_x, first_y)
                        else:
                            print("Aucun orbe trouvé à cette position.")
                    else:
                        print(f"Check n'a pas trouvé d'orbe à la position ({first_x}, {first_y}).")
            else:
                print("Le nombre de colonnes doit être compris entre 1 et 11.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    def verify_and_iterate_positions(self, tableau, nombre, pos_x, pos_y):
        """
        Vérifie si le tableau contient suffisamment de positions pour le nombre passé en paramètre.
        Si le nombre de positions >= nombre, effectue les actions avec des délais aléatoires entre 0.17 et 0.25 secondes.
        """
        if len(tableau) >= nombre:
            print("ok")

            # Boucle pour effectuer l'action 'nombre' fois
            for i in range(nombre):
                if not tableau:
                    print("Tableau vide, arrêt de la boucle.")
                    break

                # Positionnement sur la position x;y et clic droit
                pyautogui.moveTo(pos_x, pos_y)
                time.sleep(random.uniform(0.17, 0.25))  # Délai aléatoire
                pyautogui.rightClick()
                time.sleep(random.uniform(0.17, 0.25))  # Délai aléatoire

                # Aller à la position set_beast_value (extraire x et y de set_beast_value)
                try:
                    beast_x, beast_y = map(int, self.set_beast_value.split(';'))
                    pyautogui.moveTo(beast_x, beast_y)
                    time.sleep(random.uniform(0.17, 0.25))  # Délai aléatoire
                    pyautogui.click()
                    time.sleep(random.uniform(0.17, 0.25))  # Délai aléatoire
                except ValueError:
                    print("set_beast_value n'est pas valide.")
                    return

                # Aller à la première position du tableau fill
                first_position = tableau[0]
                pyautogui.moveTo(first_position['x'], first_position['y'])
                time.sleep(random.uniform(0.17, 0.25))  # Délai aléatoire
                pyautogui.click()
                time.sleep(random.uniform(0.17, 0.25))  # Délai aléatoire

                # Retirer la première position du tableau
                tableau.pop(0)
                print(f"Position {i+1} effectuée. Restant: {len(tableau)} positions.")
        else:
            print(f"Nombre de positions insuffisant. Nombre requis: {nombre}, trouvé: {len(tableau)}")



    def check(self, x, y, text):
        """
        Déplace la souris à la position x, y, effectue un copier,
        et retourne True si la chaîne text est présente dans le texte copié, False sinon
        """

        # Déplacer la souris à la position x, y
        pyautogui.moveTo(x, y)

        # Simuler un clic gauche pour activer la zone
        #pyautogui.click()

        # Attendre une petite pause pour s'assurer que la zone est activée
        time.sleep(0.05)

        # Simuler le raccourci clavier Ctrl+C pour copier
        pyautogui.hotkey('ctrl', 'c')

        # Attendre un moment pour que le texte soit copié
        time.sleep(0.05)

        # Récupérer le texte copié depuis le presse-papiers
        copied_text = pyperclip.paste()

        # Afficher le texte copié dans la console
        #print(f"Texte copié après déplacement à ({x}, {y}): {copied_text}")

        # Vérifier si la chaîne est présente dans le texte copié
        if text in copied_text:
            return True, copied_text
        else:
            return False, copied_text



    def open_chain_beast_popup(self):
        # Créer la fenêtre popup
        popup = tk.Toplevel(self.root)
        popup.title("Chain Beast Popup")
        popup.geometry("600x400")  # Taille initiale de la popup
        popup.minsize(400, 300)  # Taille minimale pour éviter que le contenu ne disparaisse
        popup.attributes("-topmost", True)  # Garder la fenêtre toujours au premier plan
        popup.attributes("-alpha", 0.4)  # Rendre la fenêtre semi-transparente
        popup.overrideredirect(True)  # Supprimer la barre de titre et la croix de fermeture

        # Configuration de la grille pour le layout
        popup.grid_rowconfigure(0, weight=1)  # Row 0 pour les points rouges
        popup.grid_rowconfigure(1, weight=0)  # Row 1 pour le bouton Close
        popup.grid_columnconfigure(0, weight=1)

        # Créer une frame pour les points rouges
        points_frame = tk.Frame(popup, bg='white')
        points_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Créer une grille de 12x5 points rouges (60 points au total)
        rows, cols = 5, 12  # Définir la grille de 12 colonnes et 5 rangées
        self.point_canvases = []  # Liste pour stocker les canvases (pour les redimensionner ensuite)

        for row in range(rows):
            for col in range(cols):
                # Canvas pour créer un point rouge
                canvas = tk.Canvas(points_frame, width=20, height=20, bg='white', highlightthickness=0)
                canvas.create_oval(5, 5, 15, 15, fill='red')  # Créer un cercle rouge
                canvas.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')  # Répartir uniformément
                self.point_canvases.append(canvas)

        # Configuration pour que les colonnes et lignes se redimensionnent
        for col in range(cols):
            points_frame.grid_columnconfigure(col, weight=1, uniform="col")
        for row in range(rows):
            points_frame.grid_rowconfigure(row, weight=1)

        # Frame séparée pour le bouton "Close"
        close_button_frame = tk.Frame(popup, bg='white')
        close_button_frame.grid(row=1, column=0, sticky="ew")

        # Fonction pour récupérer les positions des centres des points rouges et les sauvegarder
        def save_and_close():
            print("Positions des centres des points rouges :")
            self.chain_beast_points = []  # Initialiser une liste pour stocker les coordonnées
            for canvas in self.point_canvases:
                # Obtenir la position du canvas sur l'écran
                x = canvas.winfo_rootx() + canvas.winfo_width() // 2
                y = canvas.winfo_rooty() + canvas.winfo_height() // 2
                self.chain_beast_points.append({"x": x, "y": y})  # Stocker les coordonnées
                print(f"Centre du point rouge: ({x}, {y})")

            # Appeler la fonction save_settings pour sauvegarder les données
            self.save_settings()

            # Mettre à jour le tableau avec les nouvelles coordonnées
            #self.update_points_table()

            # Fermer la fenêtre après avoir sauvegardé les positions
            popup.destroy()

        # Ajouter un bouton de fermeture en bas de la fenêtre
        close_button = tk.Button(close_button_frame, text="Close", command=save_and_close, bg="green", fg="white")
        close_button.pack(pady=10)

        # Fonction pour redimensionner les points lors du redimensionnement de la fenêtre
        def resize_points(event):
            # Calculer la nouvelle taille des points en fonction de la taille de la fenêtre
            new_width = event.width // cols - 10  # 10 pixels de marge
            new_height = event.height // rows - 10  # 10 pixels de marge
            for canvas in self.point_canvases:
                canvas.config(width=new_width, height=new_height)
                canvas.delete("all")  # Effacer l'ancien point
                canvas.create_oval(5, 5, new_width - 5, new_height - 5, fill='red')

        # Associer l'événement de redimensionnement
        points_frame.bind("<Configure>", resize_points)

        # Fonction pour déplacer la fenêtre sans barre de titre
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

        # Liaison des événements de la souris pour déplacer la fenêtre
        popup.bind("<ButtonPress-1>", start_move)
        popup.bind("<ButtonRelease-1>", stop_move)
        popup.bind("<B1-Motion>", on_move)

        # Permettre le redimensionnement via les bords
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

        # Associer l'événement de redimensionnement
        popup.bind("<ButtonPress-3>", start_resize)  # Utiliser le clic droit pour commencer le redimensionnement
        popup.bind("<B3-Motion>", on_resize)  # Maintenir le clic droit pour redimensionner
        popup.bind("<ButtonRelease-3>", stop_resize)  # Relâcher le clic droit pour arrêter le redimensionnement




    def show_divination_card_module(self):
        self.update_tab_color(self.divination_card_tab)
        self.create_divination_card_content()
        self.divination_card_frame.grid(row=0, column=1, sticky="nsew")
        self.load_settings()

    def create_divination_card_content(self):
        self.divination_card_frame = tk.Frame(self.root, bg=background_color)

        title = tk.Label(self.divination_card_frame, text="Divination Card Exchange",
                     font=("Arial", 14), bg=background_color, fg=text_color)
        title.pack(pady=10)

        btn_frame = tk.Frame(self.divination_card_frame, bg=background_color)
        btn_frame.pack(pady=10)

        set_btn = tk.Button(btn_frame, text="Set Inventory", command=self.open_div_card_inventory_popup,
                        bg=button_color, fg=text_color)
        set_btn.grid(row=0, column=0, padx=5)

        # Bouton "Set Trade"
        set_trade_button = tk.Button(btn_frame, text="Set Trade",
                                          command=self.set_trade_action, bg=button_color, fg=text_color)
        set_trade_button.grid(row=0, column=1, padx=5)

        # Bouton "Set Confirm"
        set_confirm_button = tk.Button(btn_frame, text="Set Confirm",
                                     command=self.set_confirm_action, bg=button_color, fg=text_color)
        set_confirm_button.grid(row=0, column=2, padx=5)


        empty_space = tk.Label(btn_frame, text="", bg=background_color, height=1)
        empty_space.grid(row=1, column=0, columnspan=2)

        exchange_btn = tk.Button(btn_frame, text="Échanger les cartes", command=self.exchange_divination_cards,
                             bg="green", fg="white")
        exchange_btn.grid(row=2, column=0, padx=5)


    def set_trade_action(self):
        """ Afficher 'Set Beast' dans la console """
        self.create_popup("Set Trade")

    def set_confirm_action(self):
        """ Afficher 'Set Beast' dans la console """
        self.create_popup("Set Confirm")

    def open_div_card_inventory_popup(self):
        popup = tk.Toplevel(self.root)
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
        self.div_card_canvases = []

        for row in range(rows):
            for col in range(cols):
                canvas = tk.Canvas(points_frame, width=20, height=20, bg='white', highlightthickness=0)
                canvas.create_oval(5, 5, 15, 15, fill='red')
                canvas.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
                self.div_card_canvases.append(canvas)

        for col in range(cols):
            points_frame.grid_columnconfigure(col, weight=1, uniform="col")
        for row in range(rows):
            points_frame.grid_rowconfigure(row, weight=1)

        close_button_frame = tk.Frame(popup, bg='white')
        close_button_frame.grid(row=1, column=0, sticky="ew")

        def save_and_close():
            print("Positions des centres des cartes divination :")
            self.div_card_points = []
            for canvas in self.div_card_canvases:
                x = canvas.winfo_rootx() + canvas.winfo_width() // 2
                y = canvas.winfo_rooty() + canvas.winfo_height() // 2
                self.div_card_points.append({"x": x, "y": y})
                print(f"Centre du point rouge: ({x}, {y})")

            self.save_settings()
            popup.destroy()

        close_button = tk.Button(close_button_frame, text="Close", command=save_and_close, bg="green", fg="white")
        close_button.pack(pady=10)

        # Gestion du redimensionnement
        def resize_points(event):
            new_width = event.width // cols - 10
            new_height = event.height // rows - 10
            for canvas in self.div_card_canvases:
                canvas.config(width=new_width, height=new_height)
                canvas.delete("all")
                canvas.create_oval(5, 5, new_width - 5, new_height - 5, fill='red')

            points_frame.bind("<Configure>", resize_points)

        # Déplacement de la popup
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

        # Redimensionnement à la souris via clic droit
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

    def exchange_divination_cards(self):
        self.load_settings()

        # Récupération des paramètres
        div_card_points = getattr(self, 'div_card_points', None)
        set_trade_str = getattr(self, 'set_trade_value', None)
        set_confirm_str = getattr(self, 'set_confirm_value', None)

        # Vérification des paramètres manquants
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

        # Vérification du format de div_card_points
        if not isinstance(div_card_points, list) or not all(
                isinstance(pos, dict) and 'x' in pos and 'y' in pos for pos in div_card_points):
            print("Format invalide pour div_card_points. Attendu : liste de dictionnaires {'x': int, 'y': int}")
            return

        # Vérification du format de set_trade et set_confirm
        try:
            trade_x, trade_y = map(int, set_trade_str.split(";"))
            confirm_x, confirm_y = map(int, set_confirm_str.split(";"))
        except ValueError:
            print("Format invalide pour set_trade ou set_confirm. Attendu : chaîne 'x;y'")
            return

        pyautogui.PAUSE = 0.001

        # Activation de la fenêtre du jeu
        try:
            poe_window = gw.getWindowsWithTitle('Path of Exile')[0]
            poe_window.activate()
        except IndexError:
            print("Fenêtre Path of Exile non trouvée.")
            return

        # Diviser les points en lignes de 12 colonnes
        total_columns = 12
        grid = [div_card_points[i:i+total_columns] for i in range(0, len(div_card_points), total_columns)]

        # Parcours colonne par colonne
        for col in range(total_columns):
            for row in range(len(grid)):
                try:
                    pos = grid[row][col]
                    pyautogui.moveTo(pos['x'], pos['y'])
                    time.sleep(0.1)
                    pyautogui.hotkey('ctrl', 'c')
                    time.sleep(0.1)

                    copied_text = pyperclip.paste()
                    print(f"Contenu copié : {copied_text}")

                    if "Item Class: Divination Cards" not in copied_text:
                        print("L'élément n'est pas une carte de divination. Opération annulée.")
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
                    print(f"Contenu après confirm : {new_copied_text}")

                    if "Item Class: Stackable Currency" not in new_copied_text:
                        print("Erreur : la classe de l'objet n'a pas changé. Opération annulée.")
                        return

                    if copied_text == new_copied_text or new_copied_text == "":
                        print("Erreur : le contenu n'a pas changé après la confirmation. Opération annulée.")
                        return

                    pyautogui.keyDown('ctrl')
                    pyautogui.click(button='left')
                    pyautogui.keyUp('ctrl')
                    time.sleep(0.25)

                except Exception as e:
                    print(f"Erreur lors du traitement de la position {pos} : {e}")
                    return



    def create_footer(self):
        # Création d'un Frame pour le footer
        self.footer_frame = tk.Frame(self.root, bg=background_color)
        self.footer_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Ajout du label 'Currency used'
        footer_label = tk.Label(self.footer_frame, text="Currency used : " + str(currency_used), bg=background_color,
                                fg=text_color)
        footer_label.pack(pady=5)  # Centrer le label dans le footer

        # Création d'un Frame pour les boutons dans le footer pour une meilleure organisation
        buttons_frame = tk.Frame(self.footer_frame, bg=background_color)
        buttons_frame.pack(pady=10, fill=tk.X, expand=True)  # Le Frame se développe horizontalement

        # Création et positionnement des boutons avec la méthode grid
        buttons_text = ["Start", "Set item", "Chain craft", "Chain area"]
        for i, text in enumerate(buttons_text):
            button = tk.Button(buttons_frame, text=text, bg="#567eab",
                               fg=text_color)  # Utilisation d'une lambda fonction pour appeler on_currency_button_click avec le nom du bouton
            if text == "Set item":
                button.config(command=lambda t=text: self.on_currency_button_click(t))
            elif text == "Start":
                button.config(command=lambda t=text: self.craft_item())

            button.grid(row=0, column=i, sticky="ew",
                        padx=10)  # Les boutons sont alignés horizontalement avec de l'espace entre eux

            # Configurez la colonne i du buttons_frame pour qu'elle s'étende équitablement
            buttons_frame.grid_columnconfigure(i, weight=1)

        # Configuration de la grille pour que le footer ne prenne pas trop d'espace
        self.root.grid_rowconfigure(1, minsize=60)  # Augmenter si nécessaire pour accommoder deux rangées de contenu

    def craft_item(self):
        pyautogui.PAUSE = 0.001
        # Ramener "Path of Exile" au premier plan
        poe_window = gw.getWindowsWithTitle('Path of Exile')[0]  # Remplacez par le titre exact de la fenêtre
        poe_window.activate()

        print("Start Craft " + str(currency_used))
        print(self.set_item_var)
        # Extraction des coordonnées x et y à partir de self.set_item_var
        x, y = map(int, self.set_item_var.split(';'))

        # Déplacement de la souris vers les coordonnées x, y
        pyautogui.moveTo(x, y, duration=self.mouse_move_time_var.get())
        # Pause de 10 millisecondes
        time.sleep(0.01)
        # Simulation de la pression des touches Ctrl+C
        pyautogui.hotkey('ctrl', 'C')

        # Accès au contenu du presse-papier
        clipboard_content = pyperclip.paste()
        # print(clipboard_content)
        if self.get_current_tab() == "No Mod Craft":
            g_count, r_count, b_count = self.extract_socket_colors(clipboard_content)
            socket = g_count + r_count + b_count
            if socket > 0:
                # print("Green (G):", g_count)
                # print("Red (R):", r_count)
                # print("Blue (B):", b_count)
                if self.socket_var.get() and self.currency_button_states["Jeweller"] != "":
                    # print(self.currency_button_states["Jeweller"])
                    if 0 < int(self.socket_entry.get()) <= 6:
                        #print(self.socket_entry.get())
                        x, y = map(int, self.currency_button_states["Jeweller"].split(';'))
                        # Déplacer la souris vers x, y avec une durée de 50 ms
                        pyautogui.moveTo(x, y, duration=self.mouse_move_time_var.get())
                        # Déplacer la souris vers x, y et effectuer un clic droit
                        pyautogui.rightClick()
                        x, y = map(int, self.set_item_var.split(';'))
                        # Déplacement de la souris vers les coordonnées x, y
                        pyautogui.moveTo(x, y, duration=self.mouse_move_time_var.get())
                        # Maintenir la touche Shift
                        pyautogui.keyDown('shift')
                        while socket < int(self.socket_entry.get()):
                            # Obtenir la position actuelle de la souris
                            x_mouse, y_mouse = pyautogui.position()
                            # Calculer la distance entre la position actuelle de la souris et la cible
                            distance = ((x_mouse - x) ** 2 + (y_mouse - y) ** 2) ** 0.5
                            if distance > 10:
                                break
                            time.sleep(self.craft_delay_var.get()/3)
                            pyautogui.leftClick()
                            time.sleep(self.craft_delay_var.get()/3)
                            # Simulation de la pression des touches Ctrl+C
                            # Presser et relâcher la touche 'Ctrl'
                            pyautogui.keyDown('ctrl')
                            pyautogui.press('c')
                            pyautogui.keyUp('ctrl')
                            # Accès au contenu du presse-papier
                            clipboard_content = pyperclip.paste()
                            time.sleep(self.craft_delay_var.get()/3)
                            g_count, r_count, b_count = self.extract_socket_colors(clipboard_content)
                            socket = g_count + r_count + b_count
                            if socket >= int(self.socket_entry.get()):
                                break
                            # print(socket)
                        print("STOP --------------------------------")
                        # Relâcher la touche Shift
                        pyautogui.keyUp('shift')
                if self.link_var.get() and self.currency_button_states["Fusing"] != "":
                    # print(self.currency_button_states["Fusing"])
                    if 0 < int(self.link_entry.get()) <= 6:
                        #print(self.link_entry.get())
                        x, y = map(int, self.set_item_var.split(';'))
                        # Déplacement de la souris vers les coordonnées x, y
                        pyautogui.moveTo(x, y, duration=self.mouse_move_time_var.get())
                        # Simulation de la pression des touches Ctrl+C
                        pyautogui.hotkey('ctrl', 'C')
                        # Accès au contenu du presse-papier
                        clipboard_content = pyperclip.paste()
                        g_count, r_count, b_count = self.extract_socket_colors(clipboard_content)
                        socket = g_count + r_count + b_count
                        if socket >= int(self.link_entry.get()):
                            #print("ok on peux fuse")
                            x, y = map(int, self.currency_button_states["Fusing"].split(';'))
                            # Déplacer la souris vers x, y avec une durée de 50 ms
                            pyautogui.moveTo(x, y, duration=self.mouse_move_time_var.get())
                            # Déplacer la souris vers x, y et effectuer un clic droit
                            pyautogui.rightClick()
                            x, y = map(int, self.set_item_var.split(';'))
                            # Déplacement de la souris vers les coordonnées x, y
                            pyautogui.moveTo(x, y, duration=self.mouse_move_time_var.get())
                            # Maintenir la touche Shift
                            pyautogui.keyDown('shift')
                            link = self.extract_link_count(clipboard_content)
                            while link + 1 < int(self.link_entry.get()):
                                # Obtenir la position actuelle de la souris
                                x_mouse, y_mouse = pyautogui.position()
                                # Calculer la distance entre la position actuelle de la souris et la cible
                                distance = ((x_mouse - x) ** 2 + (y_mouse - y) ** 2) ** 0.5
                                if distance > 10:
                                    break
                                time.sleep(self.craft_delay_var.get()/3)
                                pyautogui.leftClick()
                                time.sleep(self.craft_delay_var.get()/3)
                                # Simulation de la pression des touches Ctrl+C
                                # Presser et relâcher la touche 'Ctrl'
                                pyautogui.keyDown('ctrl')
                                pyautogui.press('c')
                                pyautogui.keyUp('ctrl')
                                # Accès au contenu du presse-papier
                                clipboard_content = pyperclip.paste()
                                time.sleep(self.craft_delay_var.get()/3)
                                link = self.extract_link_count(clipboard_content)
                                # print(link)
                            print("STOP --------------------------------")
                            # Relâcher la touche Shift
                            pyautogui.keyUp('shift')
                if self.color_var.get() and self.currency_button_states["Chromatic"] != "":
                    # print(self.currency_button_states["Chromatic"])
                    number_color = int(self.red_entry.get()) + int(self.green_entry.get()) + int(self.blue_entry.get())
                    if 0 < number_color <= 6:
                        #print(self.red_entry.get())
                        #print(self.green_entry.get())
                        #print(self.blue_entry.get())

                        x, y = map(int, self.set_item_var.split(';'))
                        # Déplacement de la souris vers les coordonnées x, y
                        pyautogui.moveTo(x, y, duration=self.mouse_move_time_var.get())
                        # Simulation de la pression des touches Ctrl+C
                        pyautogui.hotkey('ctrl', 'C')
                        # Accès au contenu du presse-papier
                        clipboard_content = pyperclip.paste()
                        g_count, r_count, b_count = self.extract_socket_colors(clipboard_content)
                        socket = g_count + r_count + b_count
                        good_color = False
                        if g_count >= int(self.green_entry.get()) and r_count >= int(
                                self.red_entry.get()) and b_count >= int(self.blue_entry.get()):
                            good_color = True
                        if socket >= number_color and not good_color:
                            x, y = map(int, self.currency_button_states["Chromatic"].split(';'))
                            # Déplacer la souris vers x, y avec une durée de 50 ms
                            pyautogui.moveTo(x, y, duration=self.mouse_move_time_var.get())
                            # Déplacer la souris vers x, y et effectuer un clic droit
                            pyautogui.rightClick()
                            x, y = map(int, self.set_item_var.split(';'))
                            # Déplacement de la souris vers les coordonnées x, y
                            pyautogui.moveTo(x, y, duration=self.mouse_move_time_var.get())
                            # Maintenir la touche Shift
                            pyautogui.keyDown('shift')
                            while not good_color:
                                # Obtenir la position actuelle de la souris
                                x_mouse, y_mouse = pyautogui.position()
                                # Calculer la distance entre la position actuelle de la souris et la cible
                                distance = ((x_mouse - x) ** 2 + (y_mouse - y) ** 2) ** 0.5
                                if distance > 10:
                                    break
                                time.sleep(self.craft_delay_var.get()/3)
                                pyautogui.leftClick()
                                time.sleep(self.craft_delay_var.get()/3)
                                # Simulation de la pression des touches Ctrl+C
                                # Presser et relâcher la touche 'Ctrl'
                                pyautogui.keyDown('ctrl')
                                pyautogui.press('c')
                                pyautogui.keyUp('ctrl')
                                # Accès au contenu du presse-papier
                                clipboard_content = pyperclip.paste()
                                time.sleep(self.craft_delay_var.get()/3)
                                g_count, r_count, b_count = self.extract_socket_colors(clipboard_content)
                                if g_count >= int(self.green_entry.get()) and r_count >= int(self.red_entry.get()) \
                                        and b_count >= int(self.blue_entry.get()):
                                    good_color = True
                                # print(link)
                            print("STOP --------------------------------")
                            # Relâcher la touche Shift
                            pyautogui.keyUp('shift')

    def extract_socket_colors(self, clipboard_content):
        lines = clipboard_content.split('\n')
        for line in lines:
            if line.startswith("Sockets:"):
                g_count = line.count('G')
                r_count = line.count('R')
                b_count = line.count('B')
                return g_count, r_count, b_count
        return 0, 0, 0  # Retourner 0, 0, 0 si 'Sockets:' n'est pas trouvé

    def extract_link_count(self, clipboard_content):
        lines = clipboard_content.split('\n')
        max_links = 0
        for line in lines:
            if line.startswith("Sockets:"):
                # Diviser la ligne en groupes de sockets
                socket_groups = line.split()[1:]
                # Compter le nombre de liens dans chaque groupe (nombre de tirets)
                for group in socket_groups:
                    # Calculer le nombre de liens dans ce groupe
                    link_count = group.count('-')
                    # Mettre à jour le nombre maximal de liens
                    max_links = max(max_links, link_count)
                return max_links
        return 0  # Retourner 0 si 'Sockets:' n'est pas trouvé

    def save_settings(self):
        """ Sauvegarder les paramètres dans un fichier """
        new_settings = {
            "random_delay": self.random_delay_var.get(),
            "craft_delay": self.craft_delay_var.get(),
            "disable_mouse_teleport": self.disable_mouse_teleport_var.get(),
            "stop_if_no_currency": self.stop_if_no_currency_var.get(),
            "mouse_move_time": self.mouse_move_time_var.get(),
            "stash_items_after_craft": self.stash_items_after_craft_var.get(),
            "currency_tab_id": self.currency_tab_id_var.get(),
            "compass_tab_id": self.compass_tab_id_var.get(),
            "item_tab_id": self.item_tab_id_var.get(),
            "map_tab_id": self.map_tab_id_var.get(),
            "set_item": self.set_item_var
        }
        if self.get_current_tab() == "Currency":
            # Ajouter l'état des boutons de currency
            new_settings['currency_button_states'] = {name: var for name, var in self.currency_button_states.items()}

        # Si l'onglet "Beast Recuperation" est actif, ajouter les coordonnées des points rouges
        if self.get_current_tab() == "Beast Recuperation":
            new_settings['chain_beast_points'] = self.chain_beast_points
            new_settings['set_beast'] = self.currency_button_states.get("Set Beast", "")

        if self.get_current_tab() == "Divination Card":
            new_settings['div_card_points'] = self.div_card_points
            new_settings['set_trade'] = self.currency_button_states.get("Set Trade", "")
            new_settings['set_confirm'] = self.currency_button_states.get("Set Confirm", "")

            # Charger les paramètres existants
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {}

        # Mettre à jour ou ajouter de nouveaux paramètres
        settings.update(new_settings)

        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def save_inputs(self, event):
        """ Sauvegarder Craft Delay après chaque modification """
        self.save_settings()

    def load_settings(self):
        """ Charger les paramètres depuis un fichier """
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.random_delay_var.set(settings.get("random_delay", False))
                self.craft_delay_var.set(settings.get("craft_delay", 0.07))
                self.disable_mouse_teleport_var.set(settings.get("disable_mouse_teleport", False))
                self.stop_if_no_currency_var.set(settings.get("stop_if_no_currency", False))
                self.mouse_move_time_var.set(settings.get("mouse_move_time", 0.2))
                self.stash_items_after_craft_var.set(settings.get("stash_items_after_craft", False))
                self.currency_tab_id_var.set(settings.get("currency_tab_id", ""))
                self.compass_tab_id_var.set(settings.get("compass_tab_id", ""))
                self.item_tab_id_var.set(settings.get("item_tab_id", ""))
                self.map_tab_id_var.set(settings.get("map_tab_id", ""))
                self.set_item_var = settings.get("set_item", "")

                # Charger l'état des boutons de currency
                for name, state in settings.get('currency_button_states', {}).items():
                    self.currency_button_states[name] = state
                # Vérifier si l'onglet 'Currency' est actif avant de charger les états des boutons
                if self.get_current_tab() == "Currency":
                    self.update_button_colors()

                # Charger les points rouges si l'onglet "Beast Recuperation" est actif
                if self.get_current_tab() == "Beast Recuperation":
                    self.chain_beast_points = settings.get("chain_beast_points", [])
                    self.set_beast_value = settings.get("set_beast", "")

                if self.get_current_tab() == "Divination Card":
                    self.div_card_points = settings.get("div_card_points", "")
                    self.set_trade_value = settings.get("set_trade", "")
                    self.set_confirm_value = settings.get("set_confirm", "")

    def update_tab_color(self, selected_tab):
        """ Mettre à jour la couleur de fond du bouton d'onglet sélectionné """
        for tab in self.tabs:
            if tab == selected_tab:
                tab.config(bg="#2395e0")  # Couleur d'onglet sélectionné
            else:
                tab.config(bg="#142131")  # Couleur d'onglet non sélectionné

    def get_current_tab(self):
        """ Obtenir l'onglet actuellement sélectionné en fonction de la couleur de fond """
        for tab in self.tabs:
            if tab.cget("bg") == "#2395e0":  # Couleur d'onglet sélectionné
                return tab.cget("text")  # Retourner le texte du bouton d'onglet pour identifier l'onglet actif
        return None  # Si aucun onglet n'est sélectionné, retourner None

    def hide_other_frames(self):
        """ Masquer tous les autres cadres """
        self.currency_frame.grid_forget() if hasattr(self, 'currency_frame') else None
        self.no_mod_craft_frame.grid_forget() if hasattr(self, 'no_mod_craft_frame') else None
        # Répétez cette ligne pour les autres cadres


# Créer la fenêtre principale
root = tk.Tk()
app = App(root)
root.geometry("800x800")  # Définir une taille de fenêtre plus grande
root.mainloop()
