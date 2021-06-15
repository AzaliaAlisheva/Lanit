import numpy as np
import re
import pandas as pd
from scipy.spatial.distance import cosine
from scipy.spatial.distance import cdist

from embeddings import vector_by_words, preprocess


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


if __name__ == "__main__":
    ans = pd.read_csv("interests.csv")
    ans = ans.fillna("")
    vectors, male_vectors, female_vectors = preprocess(ans)
    print(my_people("велик", "na"))
