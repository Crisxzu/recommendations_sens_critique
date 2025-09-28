from enum import Enum
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from nltk.corpus import stopwords
import argparse

class Movie(Enum):
    FIGHT_CLUB = 0
    INTERSTELLAR = 1


DATASETS_FOLDER = "datasets"
QUANTILE_VALUE = 0.90
REVIEW_LANGUAGE = "french"

def strip_html(x):
    soup = BeautifulSoup(x, "html.parser")

    return soup.get_text().replace("\n", " ")

def get_critiques_data(film_id : Movie):
    csv_file = Path(f"{DATASETS_FOLDER}/{film_id._name_.replace('_', '')}_critiques.csv")

    if not (csv_file.exists()):
        print(f"Error, it seems that we cannot find the csv linked to this movie : {film_id}")
        exit(1)

    critiques = pd.read_csv(csv_file, low_memory=False)

    return critiques

def get_popular_critiques(critiques: pd.DataFrame):
    m = critiques['gen_review_like_count'].quantile(QUANTILE_VALUE)

    popular_critiques = critiques.copy()
    popular_critiques = popular_critiques.loc[popular_critiques['gen_review_like_count'] >= m]

    return popular_critiques


def get_similarity_matrix(critiques: pd.DataFrame):
    final_stopwords_list = stopwords.words('english') + stopwords.words('french')
    tfidf = TfidfVectorizer(stop_words=final_stopwords_list)

    tfidf_matrix = tfidf.fit_transform(critiques['review_content'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    return cosine_sim

def get_recommendations(critique_id, similarity_matrix, n=10):
    sim_scores = list(enumerate(similarity_matrix[critique_id]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]

    critiques_indices = [i[0] for i in sim_scores]

    return critiques_indices

def is_critique_exist(critiques, critique_id):
    return not critiques[critiques['id'] == critique_id].empty

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="SensCritique recommendations algorithm",
        description="Script to get similar critiques recommendations"
    )
    parser.add_argument(
        "-m",
        "--movie-id",
        type=int,
        help="Movie ID",
        choices=[movie.value for movie in Movie],
        required=True
    )
    parser.add_argument(
        "-c",
        "--critique-id",
        type=int,
        help="Critique ID",
        required=True
    )
    args = parser.parse_args()

    critiques = get_critiques_data(Movie(args.movie_id))
    critique_id = args.critique_id

    if not is_critique_exist(critiques, critique_id):
        print(f"Error, it seems that we cannot find the critique linked to this id : {critique_id}")
        exit(1)

    critiques = get_popular_critiques(critiques)
    cosine_sim = get_similarity_matrix(critiques)
    indices = pd.Series(critiques.index, index=critiques['id'])
    recommendations_indices = get_recommendations(indices[critique_id], cosine_sim)
    print(critiques.iloc[recommendations_indices])