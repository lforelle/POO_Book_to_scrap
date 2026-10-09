# Book to Scrape

Script Python d'extraction des informations du site d'entraînement
[Books to Scrape](https://books.toscrape.com/). Le programme parcourt les
catégories, récupère les données de chaque livre, puis enregistre un fichier
CSV et l'image associée.

## Fonctionnalités

- Récupération des catégories de livres disponibles sur le site ;
- parcours des pages d'une catégorie ;
- extraction des informations d'un livre : titre, UPC, prix, taxe,
  disponibilité, description, catégorie, note et URL de l'image ;
- génération d'un fichier CSV par livre ;
- téléchargement de la couverture du livre.

## Prérequis

- Python 3.10 ou plus récent ;
- `pip`.

Installez les dépendances depuis la racine du projet :

```bash
python -m pip install requests beautifulsoup4
```

## Structure du projet

```text
.
├── scraper.py                 # Téléchargement des pages HTML
├── parser/
│   ├── __init__.py             # Définit le package Python parser
│   ├── bookparser.py           # Extraction des données d'un livre
│   ├── categoryparser.py       # Extraction des livres d'une catégorie
│   └── categoriesparser.py     # Parcours de toutes les catégories
├── book.py                     # Modèle de données d'un livre
└── category.py                 # Modèle de données d'une catégorie
```

## Exécution

Placez-vous à la racine du projet :

```bash
cd /chemin/vers/POO_Book_to_scrap
```

Lancez les fichiers situés dans `parser/` comme des modules Python. Cela est
nécessaire pour que les imports relatifs (`from .bookparser import BookParser`)
fonctionnent correctement.

Extraire un livre :

```bash
python -m parser.bookparser
```

Extraire une catégorie :

```bash
python -m parser.categoryparser
```

Extraire toutes les catégories :

```bash
python -m parser.categoriesparser
```

> Ne lancez pas directement un fichier du package avec
> `python parser/bookparser.py`. Utilisez toujours la forme `python -m ...`.

## Fichiers générés

Les données sont enregistrées dans des dossiers créés automatiquement :

- `Books_details/` contient les fichiers CSV et les images des livres ;
- `Extracts/<nom_de_categorie>/` contient le fichier CSV avec les URL des
  livres de la catégorie.

Chaque CSV de livre possède notamment les colonnes suivantes :

```text
title, UPC, Price (incl. tax), Price (excl. tax), Tax, Availability,
product_description, category, review_rating, image_url
```

## Débogage dans VS Code

Pour déboguer un parseur, utilisez une configuration qui lance un **module** :

```json
{
  "name": "Debug CategoriesParser",
  "type": "debugpy",
  "request": "launch",
  "module": "parser.categoriesparser",
  "cwd": "${workspaceFolder}",
  "console": "integratedTerminal"
}
```

La clé `module` est importante : `program` attend le chemin d'un fichier,
alors que `parser.categoriesparser` est le nom d'un module.
