import sys
from collections import defaultdict
import re


def read_inverted_index(file_path: str) -> dict:
    inverted_index = defaultdict(set)
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            word, doc_ids = line.strip().split(': ')
            doc_ids = set(map(int, doc_ids.split(', ')))
            inverted_index[word] = doc_ids
    return inverted_index


class SearchEngine:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index
        self._all = set(range(1, 101))

    def _not(self, ids: set):
        return self._all.difference(ids)

    def search(self, query: str):
        query = query.replace("ИЛИ", "|").replace("И", "&").replace("НЕ ", "!")
        query_parts = re.findall(r'[^&|\s]+|[&|]', query)
        res = self._all
        curr_op = "&"
        for part in query_parts:
            if part in ["&", "|"]:
                curr_op = part
                continue
            inverted = False
            if part.startswith("!"):
                inverted = True
                part = part[1:]
            selection = self.inverted_index.get(part, set())
            if inverted:
                selection = self._not(selection)

            if curr_op == "&":
                res = res.intersection(selection)
            else:
                res = res.union(selection)
        return sorted(res)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        inverted_index_ = read_inverted_index('inverted_index.txt')
        se = SearchEngine(inverted_index_)
        query_ = ' '.join(sys.argv[1:])
        print("Результаты поиска:")
        print(f"Запрос: '{query_}' - Документы: {se.search(query_)}")
    else:
        print("Задан пустой запрос. Для того, чтобы задать ")
