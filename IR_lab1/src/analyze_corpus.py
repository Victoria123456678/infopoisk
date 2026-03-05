# src/analyze_corpus.py
import os

raw_folder = "../data/raw"
processed_folder = "../data/processed"


def analyze_folder(folder):
    sizes = []
    total = 0
    count = 0

    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)

            if not os.path.isfile(path):
                continue

            size = os.path.getsize(path)
            sizes.append(size)
            total += size
            count += 1

    avg = total / count if count else 0
    return count, total, avg


raw_count, raw_total, raw_avg = analyze_folder(raw_folder)
proc_count, proc_total, proc_avg = analyze_folder(processed_folder)

print("===== СТАТИСТИКА КОРПУСА =====")
print()
print("Сырые документы:")
print("Количество:", raw_count)
print("Общий размер:", raw_total, "байт")
print("Средний размер:", round(raw_avg, 2), "байт")
print()
print("Обработанный текст:")
print("Количество:", proc_count)
print("Общий размер:", proc_total, "байт")
print("Средний размер:", round(proc_avg, 2), "байт")