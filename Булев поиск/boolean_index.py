# boolean_index.py
import os
from tokenizer import tokenize  # твоя функция токенизации

def build_boolean_index(corpus_dir="corpus"):
    index = {}  # словарь токен -> set(doc_id)
    for filename in os.listdir(corpus_dir):
        if filename.endswith(".txt"):
            doc_id = filename
            with open(os.path.join(corpus_dir, filename), "r", encoding="utf-8") as f:
                text = f.read()
            tokens = tokenize(text)
            for token in tokens:
                if token not in index:
                    index[token] = set()
                index[token].add(doc_id)
    return index

if __name__ == "__main__":
    index = build_boolean_index()
    print("Индекс готов!")
    # для примера покажем первые 10 токенов
    for i, (token, docs) in enumerate(index.items()):
        print(token, docs)
        if i > 9:
            break