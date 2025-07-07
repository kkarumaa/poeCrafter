import random
import re
import time
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import pygetwindow as gw

import pyautogui
import pyperclip
from pynput import keyboard


from global_functions import (
    background_color,
    nav_bar_color,
    general_tab_color,
    text_color,
    button_color,
    button_menu_color,
    currency_used,
    check,
    safe_copy,
    extract_socket_colors,
    extract_link_count,
    move_mouse,
)

from tabs import general, currency, no_mod_craft, basic_craft, beast_module, divination_card


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
        general.create_general_content(self)

    def create_currency_content(self):
        currency.create_currency_content(self)

    def on_currency_button_click(self, button_name):
        currency.on_currency_button_click(self, button_name)

    def create_popup(self, button_name):
        currency.create_popup(self, button_name)

    def update_button_colors(self):
        currency.update_button_colors(self)


    def create_no_mod_craft_content(self):
        no_mod_craft.create_no_mod_craft_content(self)

    def create_basic_craft(self):
        basic_craft.create_basic_craft(self)

    def toggle_use_aug(self):
        basic_craft.toggle_use_aug(self)
    def show_general(self):
        general.show_general(self)

    def show_currency(self):
        currency.show_currency(self)

    def show_no_mod_craft(self):
        no_mod_craft.show_no_mod_craft(self)

    def show_basic_craft(self):
        basic_craft.show_basic_craft(self)
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
        beast_module.show_beast_module(self)

    def create_beast_module_content(self):
        beast_module.create_beast_module_content(self)

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
            check(x, y, "beast")
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
            is_bestiary_orb, copied_text = check(x, y, "Bestiary Orb")

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
            is_empty, copied_text = check(x, y, previous_text)

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
                    is_orb_found, copied_text = check(first_x, first_y, "Bestiary Orb")

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
        divination_card.show_divination_card_module(self)

    def create_divination_card_content(self):
        divination_card.create_divination_card_content(self)

    def set_trade_action(self):
        divination_card.set_trade_action(self)

    def set_confirm_action(self):
        divination_card.set_confirm_action(self)

    def open_div_card_inventory_popup(self):
        divination_card.open_div_card_inventory_popup(self)

    def exchange_divination_cards(self):
        divination_card.exchange_divination_cards(self)
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
        buttons_text = ["Set item", "Chain craft", "Chain area"]
        for i, text in enumerate(buttons_text):
            button = tk.Button(buttons_frame, text=text, bg="#567eab",
                               fg=text_color)  # Utilisation d'une lambda fonction pour appeler on_currency_button_click avec le nom du bouton
            if text == "Set item":
                button.config(command=lambda t=text: self.on_currency_button_click(t))

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

        if self.get_current_tab() == "Basic Craft":
            basic_craft.run_basic_craft(self)
            return

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
            g_count, r_count, b_count = extract_socket_colors(clipboard_content)
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
                            g_count, r_count, b_count = extract_socket_colors(clipboard_content)
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
                        g_count, r_count, b_count = extract_socket_colors(clipboard_content)
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
                            link = extract_link_count(clipboard_content)
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
                                link = extract_link_count(clipboard_content)
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
                        g_count, r_count, b_count = extract_socket_colors(clipboard_content)
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
                                g_count, r_count, b_count = extract_socket_colors(clipboard_content)
                                if g_count >= int(self.green_entry.get()) and r_count >= int(self.red_entry.get()) \
                                        and b_count >= int(self.blue_entry.get()):
                                    good_color = True
                                # print(link)
                            print("STOP --------------------------------")
                            # Relâcher la touche Shift
                            pyautogui.keyUp('shift')


    def save_settings(self):
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
            new_settings["currency_button_states"] = {name: var for name, var in self.currency_button_states.items()}
        if self.get_current_tab() == "Beast Recuperation":
            new_settings["chain_beast_points"] = self.chain_beast_points
            new_settings["set_beast"] = self.currency_button_states.get("Set Beast", "")
        if self.get_current_tab() == "Divination Card":
            new_settings["div_card_points"] = self.div_card_points
            new_settings["set_trade"] = self.currency_button_states.get("Set Trade", "")
            new_settings["set_confirm"] = self.currency_button_states.get("Set Confirm", "")
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {}
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


def listen_for_exit(key):
    """Stop the application when F12 is pressed."""
    if key == keyboard.Key.f12:
        # release shift in case it was held down during crafting
        pyautogui.keyUp('shift')
        os._exit(0)


# Start a background thread listening for the F12 key
listener = keyboard.Listener(on_press=listen_for_exit)
listener.start()

root.mainloop()
