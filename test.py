import json
import os
import re

from RePoE import mods, item_classes


def creer_correspondance_item_classes():
    """
    Crée un dictionnaire de correspondance entre les tags dans mods
    et les identifiants (clés) de item_classes.
    """
    correspondance = {}
    for identifiant in item_classes.keys():
        # Convertir l'identifiant en format utilisé dans mods (minuscules, remplacement des espaces par des underscores)
        format_mods = re.sub(r'(?<!^)([A-Z])', r'_\1', identifiant).lower()
        correspondance[format_mods] = identifiant
    return correspondance


def trier_et_sauvegarder_json(dossier_sortie):
    """
    Trie les données JSON par 'domain' et 'generation_type', en utilisant les tags de 'spawn_weights'
    comme domaine si le domaine est 'item'. Ne crée des fichiers que pour les types contenus dans item_classes,
    en utilisant les identifiants de item_classes.
    Sauvegarde les résultats dans des fichiers JSON séparés.
    """
    donnees = mods
    correspondance_classes = creer_correspondance_item_classes()
    print(correspondance_classes)

    # Initialiser une nouvelle structure pour le tri
    donnees_triees = {}

    # Itérer à travers le dictionnaire et trier par 'domain' et 'generation_type'
    for cle, valeur in donnees.items():
        domain = valeur.get('domain', 'Inconnu')
        type_generation = valeur.get('generation_type', 'Inconnu')

        # Utiliser les tags de 'spawn_weights' comme domaine si le domaine est 'item'
        if domain == 'item':
            tags_spawn_weights = [tag['tag'] for tag in valeur.get('spawn_weights', [])]
            # Transformer les tags en identifiants de item_classes
            domain = next((correspondance_classes[tag] for tag in tags_spawn_weights if tag in correspondance_classes),
                          'Inconnu')

        # Vérifier si le domaine ou le type de génération est dans item_classes
        if domain in item_classes or type_generation in item_classes:
            # Initialiser le domaine dans donnees_triees si non présent
            if domain not in donnees_triees:
                donnees_triees[domain] = {}

            # Initialiser le type de génération dans le domaine si non présent
            if type_generation not in donnees_triees[domain]:
                donnees_triees[domain][type_generation] = {}

            # Ajouter l'élément sous le bon 'domain' et 'generation_type'
            donnees_triees[domain][type_generation][cle] = valeur

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(dossier_sortie, exist_ok=True)

    # Sauvegarder les données triées dans des fichiers JSON séparés
    for domain, types in donnees_triees.items():
        for type_generation, elements in types.items():
            nom_fichier = f"{domain}_{type_generation}.json"
            chemin_fichier = os.path.join(dossier_sortie, nom_fichier)
            with open(chemin_fichier, 'w') as fichier:
                json.dump(elements, fichier, indent=4)


# Utilisation de la fonction
dossier_sortie = 'jsons_separess'
trier_et_sauvegarder_json(dossier_sortie)
