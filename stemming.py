import re
from nltk.stem import PorterStemmer
import os
import time
import json

# --- Папка с текстовыми документами ---
CORPUS_DIR = "corpus"  # путь к папке с .txt файлами
OUTPUT_FILE = "stemmed_tokens.json"  # файл для сохранения результатов

# Проверяем существование папки
if not os.path.exists(CORPUS_DIR):
    print(f"Папка {CORPUS_DIR} не найдена. Создайте её и положите туда .txt файлы.")
    exit(1)

# Создаём объект стеммера
stemmer = PorterStemmer()

# --- Функция стемминга ---
def stem_tokens(tokens):
    return [stemmer.stem(token) for token in tokens]

# --- Функция обработки текста документа ---
def process_document(text):
    # Простая токенизация через регулярные выражения
    tokens = re.findall(r"\b\w+\b", text.lower())
    stemmed_tokens = stem_tokens(tokens)
    return stemmed_tokens

# --- Главная функция ---
def main():
    all_stemmed = {}
    start_time = time.time()

    for filename in os.listdir(CORPUS_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(CORPUS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                stemmed = process_document(text)
                all_stemmed[filename] = stemmed

    end_time = time.time()

    # Статистика
    total_tokens = sum(len(t) for t in all_stemmed.values())
    all_lengths = [len(token) for tokens in all_stemmed.values() for token in tokens]
    average_length = sum(all_lengths) / len(all_lengths) if all_lengths else 0

    print("Всего токенов после стемминга:", total_tokens)
    print("Средняя длина токена после стемминга:", round(average_length, 2))
    print("Время стемминга: {:.2f} сек".format(end_time - start_time))

    # Сохраняем результат
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_stemmed, f, indent=2, ensure_ascii=False)

    # Примеры стемминга для отчёта
    print("\nПримеры стемминга:")
    examples = ["running", "jumps", "studies", "learning", "data"]
    for word in examples:
        print(f"{word} -> {stemmer.stem(word)}")

if __name__ == "__main__":
    main()