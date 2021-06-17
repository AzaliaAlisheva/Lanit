# -*- coding: utf-8 -*-
import re
import numpy as np
import re
import pandas as pd
from scipy.spatial.distance import cosine
from scipy.spatial.distance import cdist

from embeddings import vector_by_words, preprocess

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


def append_each(a, to):
    for n in a:
        n = n.strip()
        if n != "":
            if n.find("нет ") == -1:
                to.append(n.replace('"', "").replace(" ", "_"))


def my_people(interests, gender):
    spliter = re.compile(r'[;,]|\"\"| и ')
    deleter = re.compile(r'[!()\[\]{}\\<>/?@#$%^*_~:.-]')
    item = re.split(spliter, re.sub(deleter, '', interests.lower()))
    new_cell = []
    without_interest = ans[ans["Все интересы"] == ""]
    without_interest_female = ans[(ans["Все интересы"] == "") & (ans["Пол"] == 0)]
    without_interest_male = ans[(ans["Все интересы"] == "") & (ans["Пол"] == 1)]
    append_each(item, new_cell)
    if new_cell:
        int_string = " ".join(new_cell)
        my_vector = vector_by_words(int_string.split()).reshape(1, 300)
        my_matrix = cdist(vectors, my_vector, cosine)
        my_male_matrix = cdist(male_vectors, my_vector, cosine)
        my_female_matrix = cdist(female_vectors, my_vector, cosine)
        nearest = ans.iloc[np.argsort(my_matrix, axis=0)[:3].reshape(1, 3)[0]]
        female_nearest = ans.iloc[np.argsort(my_female_matrix, axis=0)[:3].reshape(1, 3)[0]]
        male_nearest = ans.iloc[np.argsort(my_male_matrix, axis=0)[:3].reshape(1, 3)[0]]
        if gender == "na":
            return nearest
        elif gender == "f":
            return female_nearest
        elif gender == "m":
            return male_nearest
    else:
        if gender == "na":
            return without_interest.head(3)
        elif gender == "f":
            return without_interest_female.head(3)
        elif gender == "m":
            return without_interest_male.head(3)


# App creation
app = FastAPI()


class User(BaseModel):
    interests: str
    movies: str
    books: str
    music: str


@app.post('/companions')
def find_companions(user: User):
    nearest = my_people(user.interests, "na")
    return nearest[["Все интересы"]].to_json()


@app.post('/female_companions')
def find_females(user: User):
    nearest = my_people(user.interests, "f")
    return nearest["Все интересы"].to_json()


@app.post('/male_companions')
def find_males(user: User):
    nearest = my_people(user.interests, "m")
    return nearest["Все интересы"].to_json()


@app.post('/movies')
def find_movies(user: User):
    nearest = my_people(user.interests, "na")
    return nearest["Фильмы"].to_json()


@app.post('/books')
def find_books(user: User):
    nearest = my_people(user.interests, "na")
    return nearest["Книги"].to_json()


@app.post('/music')
def find_music(user: User):
    nearest = my_people(user.interests, "na")
    return nearest["Музыка"].to_json()


if __name__ == '__main__':
    # Run server using given host and port
    ans = pd.read_csv("interests.csv")
    ans = ans.fillna("")
    vectors, male_vectors, female_vectors = preprocess(ans)
    uvicorn.run(app, host='127.0.0.1', port=80)