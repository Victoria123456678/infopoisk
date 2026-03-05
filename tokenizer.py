import os
import re
import time
from collections import Counter
import matplotlib.pyplot as plt

# Папка с текстами
CORPUS_DIR = "corpus"
REPORT_DIR = "report_plots"

# Функция токенизации
def tokenize(text):
    # Разделяем слова по буквенно-цифровым последовательностям
    tokens = re.findall(r"\b\w+\b", text.lower())  # lower() для нормализации
    return tokens

def main():
    all_tokens = []
    start_time = time.time()

    # Читаем все файлы в папке corpus
    for filename in os.listdir(CORPUS_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(CORPUS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                tokens = tokenize(text)
                all_tokens.extend(tokens)

    end_time = time.time()
    elapsed = end_time - start_time

    # Статистика
    total_tokens = len(all_tokens)
    avg_length = sum(len(t) for t in all_tokens) / total_tokens if total_tokens else 0
    print(f"Всего токенов: {total_tokens}")
    print(f"Средняя длина токена: {avg_length:.2f}")
    print(f"Время токенизации: {elapsed:.2f} сек")

    # Частоты токенов
    counter = Counter(all_tokens)
    most_common = counter.most_common(20)
    print("20 самых частых токенов:", most_common)

    # Сохраняем статистику в файл
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(f"Всего токенов: {total_tokens}\n")
        f.write(f"Средняя длина токена: {avg_length:.2f}\n")
        f.write(f"Время токенизации: {elapsed:.2f} сек\n")
        f.write("20 самых частых токенов:\n")
        for token, freq in most_common:
            f.write(f"{token}: {freq}\n")

    # Закон Ципфа
    ranks = range(1, len(counter)+1)
    freqs = [freq for token, freq in counter.most_common()]
    plt.figure(figsize=(6,4))
    plt.loglog(ranks, freqs, marker=".")
    plt.title("Распределение токенов (Закон Ципфа)")
    plt.xlabel("Ранг токена (log)")
    plt.ylabel("Частота (log)")
    plt.grid(True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    plt.savefig(os.path.join(REPORT_DIR, "zipf_plot.png"))
    plt.show()

if __name__ == "__main__":
    main()