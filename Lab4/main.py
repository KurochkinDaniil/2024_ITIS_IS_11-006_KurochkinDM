from collections import defaultdict
import math
import os
import csv


inverted_index_path = "Lab3/inverted_index.txt"
inverted_index = defaultdict(set)
with open(inverted_index_path, 'r', encoding='utf-8') as file:
    for line in file:
        term, docs = line.strip().split(': ')
        docs_set = set(map(int, docs.split(', ')))
        inverted_index[term] = docs_set


processed_docs_path = "Lab2/processed_data"
documents_list = os.listdir(processed_docs_path)
total_documents = len(documents_list)


tf = defaultdict(lambda: defaultdict(float))


for doc_name in documents_list:
    doc_path = os.path.join(processed_docs_path, doc_name)
    with open(doc_path, 'r', encoding='utf-8') as doc_file:
        words = doc_file.read().split()
        total_terms = len(words)
        terms_count = defaultdict(int)
        for word in words:
            terms_count[word] += 1

        # Расчет TF для каждого слова в документе
        for term, count in terms_count.items():
            tf[doc_name][term] = count / total_terms

# Расчет IDF для каждого термина
idf = {term: math.log(total_documents / (1 + len(docs))) for term, docs in inverted_index.items()}

# Расчет TF-IDF
tf_idf = defaultdict(dict)
for doc, terms in tf.items():
    for term, tf_value in terms.items():
        tf_idf[doc][term] = tf_value * idf.get(term, 0)


unique_terms = sorted(inverted_index.keys())
doc_names = sorted(tf.keys(), key=lambda x: int(x.split('_')[1]))

tf_rows = [[term] + [round(tf[doc].get(term, 0), 6) for doc in doc_names] for term in unique_terms]
tf_idf_rows = [[term] + [round(tf_idf[doc].get(term, 0), 6) for doc in doc_names] for term in unique_terms]

with open('idf_table_formatted.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Term', 'IDF'])
    for term, value in idf.items():
        writer.writerow([term, round(value, 6)])

with open('tf_table_formatted.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Term'] + doc_names)
    writer.writerows(tf_rows)

with open('tf_idf_table_formatted.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Term'] + doc_names)
    writer.writerows(tf_idf_rows)
