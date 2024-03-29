import math
from pathlib import Path
from collections import defaultdict
import pandas as pd

current_script_path = Path(__file__).resolve()


def load_inverted_index(file_path: str | Path) -> dict:
    inverted_index_dict = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            term, doc_ids_str = line.strip().split(': ')
            doc_ids = set(map(int, doc_ids_str.split(', ')))
            inverted_index_dict[term] = doc_ids
    return inverted_index_dict


# Шаг 1: Расчет TF
def calculate_tf(doc_words):
    tf_dict = defaultdict(float)
    word_count = len(doc_words)
    for word in doc_words:
        tf_dict[word] += 1 / word_count
    return tf_dict


# Шаг 2: Расчет IDF
def calculate_idf(documents):
    idf_dict = defaultdict(float)
    total_docs = len(documents)
    for doc in documents.values():
        for word in set(doc):
            idf_dict[word] += 1

    for word, count in idf_dict.items():
        idf_dict[word] = math.log(total_docs / count)

    return idf_dict


# Шаг 3: Расчет TF-IDF
def calculate_tfidf(tf_dict, idf_dict):
    tfidf_dict = {}
    for word, tf_val in tf_dict.items():
        tfidf_dict[word] = tf_val * idf_dict.get(word, 0)
    return tfidf_dict


index_path_ = current_script_path.parent.parent / 'Lab3' / 'inverted_index.txt'
inverted_index_dict_ = load_inverted_index(index_path_)

# Выполнение расчетов
tf_dicts_ = {doc_id: calculate_tf(words) for doc_id, words in inverted_index_dict_.items()}
idf_dict_ = calculate_idf(inverted_index_dict_)

tfidf_dicts = {doc_id: calculate_tfidf(tf_dict, idf_dict_) for doc_id, tf_dict in tf_dicts_.items()}


# Преобразование в DataFrame и сохранение
tf_df = pd.DataFrame(tf_dicts_).T.fillna(0)
idf_df = pd.DataFrame(idf_dict_.items(), columns=['Term', 'IDF'])
tfidf_df = pd.DataFrame(tfidf_dicts).T.fillna(0)

# Округление до 6 знаков после запятой
tf_df = tf_df.round(6)
idf_df = idf_df.round(6)
tfidf_df = tfidf_df.round(6)

# Сохранение в CSV
tf_df.to_csv('tf.csv')
idf_df.to_csv('idf.csv')
tfidf_df.to_csv('tfidf.csv')
