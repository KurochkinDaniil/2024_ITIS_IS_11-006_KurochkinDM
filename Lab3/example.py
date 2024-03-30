from search import SearchEngine, read_inverted_index

inverted_index_ = read_inverted_index('inverted_index.txt')
se = SearchEngine(inverted_index_)

query = "джедаи & !меч | !татуин"
print(f"Запрос: '{query}' - Документы: {se.search(query)}")
print()

query = "джедаи | меч | татуин"
print(f"Запрос: '{query}' - Документы: {se.search(query)}")
print()

query = "джедаи&татуин|меч"
print(f"Запрос: '{query}' - Документы: {se.search(query)}")
print()

query = "джедаи И меч И татуин"
print(f"Запрос: '{query}' - Документы: {se.search(query)}")
print()

query = "джедаи | !меч | !татуин"
print(f"Запрос: '{query}' - Документы: {se.search(query)}")
print()
