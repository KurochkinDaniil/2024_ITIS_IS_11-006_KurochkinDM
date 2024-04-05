import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import sys

current_script_path = Path(__file__).resolve()
processed_directory = current_script_path.parent.parent / 'Lab2' / 'processed_data'


def make_word_dict(n: int):
    doc_id2word_dict = {}
    for i in tqdm(range(1, n + 1)):
        path = processed_directory / f"processed_{i}_page.txt"
        with open(path, "r", encoding="utf-8") as file:
            doc_id2word_dict[i] = file.read().split()
    return doc_id2word_dict


class SearchEngine:
    def __init__(self, tf_idf_file, passing_score=0.05):
        self.__data: pd.DataFrame = self.__load_tf_idf(tf_idf_file)
        self.doc_vecs = [(doc_id, self.vectorize_doc(tokens)) for doc_id, tokens in make_word_dict(100).items()]
        self.passing_score = passing_score

    @staticmethod
    def __load_tf_idf(tf_idf_file: str) -> pd.DataFrame:
        return pd.read_csv(tf_idf_file)

    def vectorize_doc(self, tokens: list[str]) -> np.ndarray:
        return self.__data.loc[self.__data['Term'].isin(tokens)].drop('Term', axis=1).mean().to_numpy()

    @staticmethod
    def cosine_similarity_for_vectors(vector1: np.ndarray, vector2: np.ndarray) -> float:
        res = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

        if str(res) == "nan":
            return 0.0
        return res

    def cosine_similarity(self, document1: list[str], document2: list[str]) -> float:
        v1 = self.vectorize_doc(document1)
        v2 = self.vectorize_doc(document2)
        return self.cosine_similarity_for_vectors(v1, v2)

    def search(self, query: str):
        doc = query.split()
        vec = self.vectorize_doc(doc)
        doc2similarity = list(map(lambda x: (x[0], self.cosine_similarity_for_vectors(vec, x[1])), self.doc_vecs))
        result_docs = sorted(doc2similarity, key=lambda x: -x[1])
        return result_docs


if __name__ == '__main__':
    if len(sys.argv) > 1:
        tf_idf_path = current_script_path.parent.parent / 'Lab4' / 'tf_idf_table.csv'
        se = SearchEngine(tf_idf_path)
        query_ = ' '.join(sys.argv[1:])
        print("Search result:")
        print(f"Query: '{query_}'\nDocument: \n" + "\n".join(map(lambda x: f"Document {x[0]}, match - {x[1]}",
                                                                 se.search(query_))))
    else:
        print("Передайте запрос аргументом командной строки при запуске")
