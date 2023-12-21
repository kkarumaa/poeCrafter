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


def trier_et_sauvegarder_json_suffix_prefix(dossier_sortie):
    """
    Trie les données JSON par 'domain' et 'generation_type', et crée des fichiers uniquement
    pour les éléments dont le 'generation_type' est 'suffix' ou 'prefix'.
    Si le 'domain' est 'item', utilise les tags de 'spawn_weights' pour déterminer le domaine.
    Sauvegarde les résultats dans des fichiers JSON séparés.

    :param dossier_sortie: Chemin du dossier où sauvegarder les fichiers triés.
    :param donnees: Données JSON à trier.
    :param correspondance_classes: Dictionnaire de correspondance pour les domaines.
    """
    # Initialiser une nouvelle structure pour le tri
    donnees = mods
    correspondance_classes = creer_correspondance_item_classes()
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

        # Créer des fichiers uniquement si type_generation est 'suffix' ou 'prefix'
        if type_generation in ['suffix', 'prefix']:
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


# Vous devrez fournir les données et le dossier de sortie lors de l'appel de cette fonction.
# Utilisation de la fonction
dossier_sortie = 'jsons_separes'
trier_et_sauvegarder_json_suffix_prefix(dossier_sortie)
