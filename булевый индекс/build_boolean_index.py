# build_boolean_index.py
import os
import json
import re

def tokenize(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens

def build_boolean_index(corpus_dir):
    index = {}
    if not os.path.exists(corpus_dir):
        raise FileNotFoundError(f"Папка с корпусом не найдена: {corpus_dir}")

    for filename in os.listdir(corpus_dir):
        filepath = os.path.join(corpus_dir, filename)
        if not os.path.isfile(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        tokens = tokenize(text)
        for token in tokens:
            if token not in index:
                index[token] = []
            if filename not in index[token]:
                index[token].append(filename)

    return index

if __name__ == "__main__":
    # Здесь указываем точный путь к папке corpus
    # Замените путь на тот, где реально лежит папка corpus в вашем проекте
    CORPUS_DIR = r"C:\Users\vika\Documents\IR_lab3\corpus"

    print("Используемая папка с корпусом:", CORPUS_DIR)
    index = build_boolean_index(CORPUS_DIR)

    output_file = r"C:\Users\vika\Documents\IR_lab3\boolean_index.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4, ensure_ascii=False)

    print(f"Булев индекс построен и сохранён в {output_file}")