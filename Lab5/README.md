# Задание №5:
Разработать поисковую систему на основе векторного поиска по построенному индексу. На каждый введённый поисковый запрос выводится список документов с их “весами” отсортированный по релевантности.


## Примеры запуска:
1. ```python search.py force > force.txt ```
2. ```python search.py force jedi > force_jedi.txt ```
3. ```python search.py force jedi tatooine > force_jedi_tatooine.txt ```
4. ```python search.py "клон" > force_jedi_tatooine.txt ```
Пример поиска редкого слова:
1. ```python search.py "зугурука" > zuguruka.txt ```


