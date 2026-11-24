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

Après les vérifications, relire le diff et ne préparer explicitement que les fichiers concernés :

```powershell
git status --short
git diff --check
git diff
git add chemin/du/fichier
git diff --cached
git diff --cached --check
git commit -m "Décrire le changement" -m "Expliquer en français ce qui change et son impact pour l’utilisateur."
git push origin main
git fetch origin
git status --short --branch
```

Remplacer `chemin/du/fichier` par les fichiers réellement concernés et répéter `git add` pour chacun. Ne pas utiliser `git add .` : les réglages locaux et autres fichiers sans rapport ne doivent pas être envoyés. Chaque commit doit avoir un titre court et un corps en français qui résume le changement et son impact utilisateur.

Quand une demande de modification est claire et terminée, effectuer les vérifications, créer le commit et pousser directement sur `origin main`, sans demander de confirmation supplémentaire. Si la modification est incomplète, si une vérification échoue de manière bloquante ou si le diff contient des changements étrangers, suspendre le push et expliquer le problème.

Après le push, vérifier que `main` est propre et synchronisée avec `origin/main` : `git status --short --branch` doit indiquer `main...origin/main` sans fichiers modifiés ni commits en avance ou en retard.

## Réglages

Les réglages actifs se trouvent dans `%APPDATA%\PoECrafter\settings.json`. Au premier lancement, l’application reprend les valeurs de l’ancien `settings.json` à côté des sources ou de l’exécutable si le nouveau fichier n’existe pas. L’ancien fichier n’est pas supprimé. Les coordonnées restent stockées comme valeurs propres à l’utilisateur et ne sont pas incluses dans Git.

Les fichiers de données de craft présents dans `jsons_separes/` et `jsons_separess/` sont inclus dans l’exécutable.
