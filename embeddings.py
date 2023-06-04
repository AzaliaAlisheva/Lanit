import pandas as pd
import numpy as np
import fasttext.util as fu
import fasttext

ft = fasttext.load_model('cc.ru.300.bin') # прописать свой путь к Fasttext
fu.download_model('ru', if_exists='ignore')


def vector_by_words(words):
    all_vectors = []
    for word in words:
        items = word.split("_")
        temp = " ".join(items)
        all_vectors.append(ft.get_sentence_vector(temp))
    if all_vectors:
        return np.mean(all_vectors, axis=0)
    else:
        return ft.get_sentence_vector("")


def preprocess(ans):
    interests = pd.DataFrame(columns=["Пол", "Все интересы"])
    j = 0
    for i in ans.index:
        interests.loc[j] = ans.loc[i][["Пол", "Все интересы"]]
        j += 1

    vectors = []
    j = 0
    for x in ans["Все интересы"]:
        vectors.append(vector_by_words(x.split()))
        j += 1

    female_vectors = []
    j = 0
    for x in ans[ans['Пол'] == 0]["Все интересы"]:
        female_vectors.append(vector_by_words(x.split()))
        j += 1

    male_vectors = []
    j = 0
    for x in ans[ans['Пол'] == 1]["Все интересы"]:
        male_vectors.append(vector_by_words(x.split()))
        j += 1
    return vectors, male_vectors, female_vectors
