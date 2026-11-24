# PoE Crafter

Application Windows pour configurer et lancer les automatismes de Path of Exile.

## Installation depuis les sources

Prérequis : Python 3.12 ou plus récent.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Vérifier le code avec Ruff

Pour installer l’application et Ruff dans un environnement de développement :

```powershell
python -m pip install -r requirements-dev.txt
```

Avant de livrer des changements, lancer Ruff sur le code de l’application :

```powershell
ruff check main.py global_functions.py poe_crafter
```

La commande doit se terminer avec `All checks passed!`. Elle vérifie le code sans appliquer de corrections automatiquement.

L’interface propose le français et l’anglais dans l’onglet **Général**. La fenêtre est redimensionnable et reste au premier plan. F12 arrête l’automatisme en cours, libère les touches maintenues et ferme l’application.

## Créer l’exécutable

Depuis un environnement où les dépendances sont installées :

```powershell
pyinstaller main.spec
```

L’exécutable est généré dans `dist/PoECrafter.exe`. La compilation doit se faire sous Windows pour obtenir un exécutable Windows.

## Envoyer les changements sur Git

Après les vérifications, relire les changements et ne préparer que les fichiers concernés :

```powershell
git status --short
git diff --check
git diff
git add chemin/du/fichier
git diff --cached
git commit -m "Décrire le changement"
git push origin HEAD
git status --short --branch
```

Remplacer `chemin/du/fichier` par les fichiers réellement concernés et répéter `git add` pour chacun. Ne pas utiliser `git add .` : les réglages locaux et autres fichiers sans rapport ne doivent pas être envoyés. `git push origin HEAD` pousse la branche courante.

## Réglages

Les réglages actifs se trouvent dans `%APPDATA%\PoECrafter\settings.json`. Au premier lancement, l’application reprend les valeurs de l’ancien `settings.json` à côté des sources ou de l’exécutable si le nouveau fichier n’existe pas. L’ancien fichier n’est pas supprimé. Les coordonnées restent stockées comme valeurs propres à l’utilisateur et ne sont pas incluses dans Git.

Les fichiers de données de craft présents dans `jsons_separes/` et `jsons_separess/` sont inclus dans l’exécutable.
