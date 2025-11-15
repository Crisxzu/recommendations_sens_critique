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

## Approche technique

Le système de recommandations utilise **Sentence-BERT** (SBERT) pour analyser la similarité sémantique entre les critiques.

### Modèle utilisé

- **paraphrase-multilingual-mpnet-base-v2** : Modèle SBERT multilingue optimisé pour générer des embeddings sémantiques de qualité en français
- Avantages par rapport à TF-IDF :
  - Capture le sens contextuel du texte, pas seulement les mots-clés
  - Meilleure compréhension des paraphrases et synonymes
  - Embeddings denses qui capturent les nuances sémantiques

### Pipeline de recommandation

1. **Filtrage** : Sélection des critiques populaires (90e percentile de likes)
2. **Vectorisation** : Génération d'embeddings SBERT pour chaque critique
3. **Similarité** : Calcul de la similarité cosinus entre les embeddings
4. **Recommandation** : Sélection des N critiques les plus similaires

## Configuration

Différentes options sont disponibles en fonction de ce que vous souhaitez.

- Choisir le film concernée par la critique (obligatoire)

Cela se fait via l'option `-m` ou `--movie-id` et là vous précisez l'identifiant du film.<br>
Pour le moment, avec les données à disposition seuls Fight Club (0) et Interstellar (1) sont disponibles.<br>

- Fournir l'identifiant de la critique (obligatoire)

Cela se fait via l'option `-r` ou `--review-id` et là vous précisez l'identifiant de la critique.<br>

- Décider du nombre de recommandations à proposer

Cela se fait via l'option `-n` et là vous précisez le nombre de recommandations souhaités.<br>

---

Créé avec ❤️ par Dazu
