from collections import defaultdict
import os
from pathlib import Path

current_script_path = Path(__file__).resolve()


def build_inverted_index(processed_directory: Path) -> dict:
    inverted_index = defaultdict(set)
    for filename in os.listdir(processed_directory):
        if filename.startswith('processed_') and filename.endswith('_page.txt'):
            file_path = processed_directory / filename
            with open(file_path, 'r', encoding='utf-8') as file:
                for word in file.read().split():
                    inverted_index[word].add(filename)
    return inverted_index


processed_directory_ = current_script_path.parent.parent / 'Lab2' / 'processed_data'
inverted_index_ = build_inverted_index(processed_directory_)


def save_inverted_index(inverted_index: dict, output_file: Path) -> None:
    with open(output_file, 'w', encoding='utf-8') as file:
        for word in sorted(inverted_index.keys()):
            document_numbers = sorted([filename.split('_')[1] for filename in inverted_index[word]])
            file.write(f"{word}: {', '.join(document_numbers)}\n")


output_file_ = Path('inverted_index.txt')
save_inverted_index(inverted_index_, output_file_)
