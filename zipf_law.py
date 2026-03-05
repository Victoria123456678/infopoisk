import os
import json
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

# --- Настройка путей ---
CORPUS_FILE = "stemmed_tokens.json"  # JSON с токенами после стемминга
REPORT_DIR = "report_plots"
os.makedirs(REPORT_DIR, exist_ok=True)

# --- Загружаем токены ---
with open(CORPUS_FILE, "r", encoding="utf-8") as f:
    all_stemmed = json.load(f)

# Собираем все токены в один список
all_tokens = [token for tokens in all_stemmed.values() for token in tokens]

# --- Считаем частоты токенов ---
counter = Counter(all_tokens)
frequencies = sorted(counter.values(), reverse=True)
ranks = np.arange(1, len(frequencies) + 1)

# --- Построение графика закона Ципфа ---
plt.figure(figsize=(8,6))
plt.loglog(ranks, frequencies, marker=".", linestyle="none", label="Слова корпуса")

# Теоретическая кривая Ципфа
s = 1.0  # коэффициент Ципфа
frequencies_zipf = frequencies[0] / ranks**s
plt.loglog(ranks, frequencies_zipf, linestyle="--", color="red", label="Закон Ципфа")

# Настройка графика
plt.xlabel("Ранг слова (log)")
plt.ylabel("Частота слова (log)")
plt.title("Распределение слов по закону Ципфа")
plt.legend()
plt.grid(True, which="both", ls="--")

# Сохраняем график
plt.savefig(os.path.join(REPORT_DIR, "zipf_law.png"))
plt.show()

# --- Выводим 20 самых частых токенов для отчета ---
most_common = counter.most_common(20)
print("20 самых частых токенов:")
for token, freq in most_common:
    print(f"{token}: {freq}")