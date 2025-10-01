# Test technique Sens Critique

Ce programme a été réalisé afin de répondre au test technique de Sens Critique.<br>
Le sujet pourra être retrouvé [ici](https://senscritique.notion.site/Data-26b153dee42880739411fb70d697a001).<br>
Le but étant de mettre en place un programme Python qui recommande des critiques semblables à une critique en cours de lecture.<br>
Les recommandations doivent bien sûr être lié au même film.

## Prérequis

- Python 3.10
- pip

## Installation

- Cloner le repo

```bash
git clone https://github.com/Crisxzu/recommendations_sens_critique.git
```

- Créer l'environnement virtuel et l'activer

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

- Installer les dépendances

```bash
pip install -r requirements.txt
```

- Lancer le projet

```bash
python main.py
```

## Configuration

Différentes options sont disponibles en fonction de ce que vous souhaitez.

- Choisir le film concernée par la critique (obligatoire)

Cela se fait via l'option `-m` ou `--movie-id` et là vous précisez l'identifiant du film.<br>
Pour le moment, avec les données à disposition seuls Fight Club (0) et Interstellar (1) sont disponibles.<br>

- Fournir l'identifiant de la critique (obligatoire)

Cela se fait via l'option `-r` ou `--review-id` et là vous précisez l'identifiant de la critique.<br>

- Décider du nombre de recommandations à proposer

Cela se fait via l'option `-n` et là vous précisez le nombre de recommandations souhaités.<br>

## Explications choix de design 

<a href="https://ibb.co/gb7n3ndT"><img src="https://i.ibb.co/ZRJZVZS8/Capture-d-e-cran-2025-10-01-a-09-24-56.png" alt="Capture-d-e-cran-2025-10-01-a-09-24-56" border="0"></a>

L'utilisateur pourra regarder sa critique via un site ou une app.<br>
La requête nous sera ensuite envoyé et elle va passer par un load balancer qui va pouvoir envoyer la requête à une de nos instances API nous permettant d'éviter de limiter les surcharges et d'assurer une haute disponibilité.<br>
L'api va ensuite utiliser notre script python pour récupérer les données de recommandations liées à la critique et la renvoyer à l'utilisateur.<br>
Avec ce code python séparé de notre API, nous gardons une approche modulaire et facilement modifiable par la suite.<br>
Pour l'algorithme de recommandation, je suis parti sur une approche de filtrage par contenu car avec les données en ma possession, il n'est pas possible de faire un filtrage collaboratif qui aurait potentiellement été plus efficace. Nous ne savons pas quel utilisateur a lié tel critique, ni quelles sont les préférences qu'on avait déjà sur l'utilisateur avant la lecture de cette critique.<br>
J'ai utilisé Pandas afin de faciliter la manipulation et le prétraitement des données et ScikitLearn, pour leur outil simple et fiable pour le calcul de la matrice de TF-IDF et de similarité.<br>
Afin de garder des données de départ pertinentes, je fais un premier filtrage pour garder les critiques les plus populaires en me basant sur le nombre de likes et en gardant ceux ayant plus de likes que 90 % des critiques présentes.<br>
Ensuite je détermine une matrice TF-IDF à partir du contenu de chaque critique afin de déterminer la fréquence de chaque mot présent.<br>
Et avec cette matrice, je détermine une matrice de similarité de chaque utilisateur avec tous les autres.<br>
Je termine en triant du score de similarité le plus élevé au plus faible et je renvoie le résultat comme recommandations de critiques.<br>

Des améliorations auxquelles je pense, ça serait de sauvegarder la matrice de similarité calculée, au moins un certain temps puis la recalculer quand on déterminera que nouvelles données sont entrés en jeu et qu'il faut le refaire.<br>
Cela pourra se faire en cache via Redis qui est plutôt efficace pour permettre d'accéder à des données qu'on souhaite garder temporairement rapidement.<br>
Mon approche aussi a plein de faiblesses, les recommandations ne sont pas toujours assez pertinents et c'est avec plaisir que j'aimerais recevoir vos retours par la suite.

---

Créé avec ❤️ par Dazu
