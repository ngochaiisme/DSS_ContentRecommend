import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# For Text
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Capture similarity
from sklearn.metrics.pairwise import linear_kernel


data = pd.read_csv("netflix_titles.csv")
data.head()


data.dropna(subset=["cast", "title", "description", "listed_in"], inplace=True, axis=0)
data = data.reset_index(drop=True)

data["listed_in"] = [re.sub(r"[^\w\s]", "", t) for t in data["listed_in"]]
data["cast"] = [re.sub(",", " ", re.sub(" ", "", t)) for t in data["cast"]]
data["description"] = [re.sub(r"[^\w\s]", "", t) for t in data["description"]]
data["title"] = [re.sub(r"[^\w\s]", "", t) for t in data["title"]]

data["combined"] = (
    data["listed_in"]
    + "  "
    + data["cast"]
    + " "
    + data["title"]
    + " "
    + data["description"]
)
data.drop(["listed_in", "cast", "description"], axis=1, inplace=True)

# Content Similarity
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(data["combined"])
cosine_similarities = linear_kernel(matrix, matrix)
movie_title = data["title"]
indices = pd.Series(data.index, index=data["title"])


def content_recommender(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_similarities[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return movie_title.iloc[movie_indices]


print(movie_title)
print(data.head())
