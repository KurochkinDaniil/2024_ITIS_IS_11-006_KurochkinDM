import os
import re
import nltk
import pymorphy3

from pathlib import Path
from nltk.corpus import stopwords

nltk.download("stopwords")
morph = pymorphy3.MorphAnalyzer()
russian_stopwords = set(stopwords.words('russian'))


def tokenize_and_lemmatize_document(file_path: Path) -> [str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    tokens = re.findall(r'\w+', text.lower())
    lemmas = [morph.parse(token)[0].normal_form for token in tokens]
    lemmas_without_stopwords = [lemma for lemma in lemmas if lemma not in russian_stopwords]
    return lemmas_without_stopwords


def process_documents(data_directory: Path, processed_directory: Path) -> None:
    if not processed_directory.exists():
        processed_directory.mkdir(parents=True)

    for filename in os.listdir(data_directory):
        if filename.endswith('_page.txt'):
            file_path = data_directory / filename
            try:
                processed_text = tokenize_and_lemmatize_document(file_path)
                processed_file_path = processed_directory / f'processed_{filename}'
                with open(processed_file_path, 'w', encoding='utf-8') as processed_file:
                    processed_file.write(' '.join(processed_text))
                print(f"Файл '{filename}' успешно обработан и сохранен.")
            except Exception as e:
                print(f"Ошибка при обработке файла '{filename}': {e}")


if __name__ == "__main__":
    current_script_path = Path(__file__).resolve()
    data_directory_ = current_script_path.parent.parent / 'Lab1' / 'data'
    processed_directory_ = current_script_path.parent / 'processed_data'

    process_documents(data_directory_, processed_directory_)
