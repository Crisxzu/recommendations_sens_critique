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
DEFAULT_NB_RECOMMENDATIONS = 10
OUTPUT_FILE = "reviews_recommendations.csv"

def strip_html(x):
    soup = BeautifulSoup(x, "html.parser")

    return soup.get_text().replace("\n", " ")

def get_reviews_data(film_id : Movie):
    csv_file = Path(f"{DATASETS_FOLDER}/{film_id._name_.replace('_', '')}_critiques.csv")

    if not (csv_file.exists()):
        print(f"Error, it seems that we cannot find csv linked to this movie : {film_id}")
        exit(1)

    reviews = pd.read_csv(csv_file, low_memory=False)

    return reviews

def get_popular_reviews(reviews: pd.DataFrame):
    print("Finding most popular reviews...")

    m = reviews['gen_review_like_count'].quantile(QUANTILE_VALUE)

    popular_reviews = reviews.copy()
    popular_reviews = popular_reviews.loc[popular_reviews['gen_review_like_count'] >= m]

    return popular_reviews


def get_similarity_matrix(reviews: pd.DataFrame):
    print("Finding similarity with this review...")
    final_stopwords_list = stopwords.words('english') + stopwords.words('french')
    tfidf = TfidfVectorizer(stop_words=final_stopwords_list)

    reviews['review_content'] = reviews['review_content'].fillna("")
    tfidf_matrix = tfidf.fit_transform(reviews['review_content'])


    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    return cosine_sim

def get_recommendations(review_id, similarity_matrix, n=10):
    print("Getting recommendations...")
    sim_scores = list(enumerate(similarity_matrix[review_id]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]

    review_indices = [i[0] for i in sim_scores]

    return review_indices

def is_review_exist(reviews, review_id):
    return not reviews[reviews['id'] == review_id].empty

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="SensCritique recommendations algorithm",
        description="Script to get similar reviews recommendations"
    )

    possibles_movies = [movie for movie in Movie]

    parser.add_argument(
        "-m",
        "--movie-id",
        type=int,
        help=f"Movie ID. {', '.join([f'{movie.value}: {movie.name}' for movie in possibles_movies])}",
        choices=[movie.value for movie in possibles_movies],
        required=True
    )
    parser.add_argument(
        "-r",
        "--review-id",
        type=int,
        help="Review ID",
        required=True
    )
    parser.add_argument(
        "-n",
        type=int,
        help=f"Number of recommendations. By default, {DEFAULT_NB_RECOMMENDATIONS}.",
        default=DEFAULT_NB_RECOMMENDATIONS,
    )
    args = parser.parse_args()

    reviews = get_reviews_data(Movie(args.movie_id))
    review_id = args.critique_id
    nb_recommendations = args.n

    if nb_recommendations < 1:
        print(f"Error, the number of recommendations cannot be less than 1.")
        exit(1)

    if not is_review_exist(reviews, review_id):
        print(f"Error, it seems that we cannot find review linked to this id : {review_id}")
        exit(1)

    reviews = get_popular_reviews(reviews)
    cosine_sim = get_similarity_matrix(reviews)
    indices = pd.Series(reviews.index, index=reviews['id'])
    recommendations_indices = get_recommendations(indices[review_id], cosine_sim, n=nb_recommendations)
    results = reviews.iloc[recommendations_indices]

    results.to_csv(OUTPUT_FILE)
    print(f"Everything is done! You can find your recommendations here: {OUTPUT_FILE}")