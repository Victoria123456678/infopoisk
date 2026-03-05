# src/download_documents.py
import os
import wikipediaapi
import arxiv
import requests
import re

# --- Папки ---
wiki_folder = "../data/raw/wikipedia"
arxiv_folder = "../data/raw/arxiv"

os.makedirs(wiki_folder, exist_ok=True)
os.makedirs(arxiv_folder, exist_ok=True)

# --- Wikipedia ---
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="ir-lab-corpus-bot/1.0"
)

wiki_titles = [
    "Python (programming language)",
    "Information retrieval",
    "Machine learning",
    "Search engine",
    "Natural language processing",
    "Deep learning",
    "Neural network",
    "Data mining",
    "Artificial intelligence",
    "Recommender system"
]

wiki_count = 0

for title in wiki_titles:
    page = wiki.page(title)
    if page.exists():
        safe_title = re.sub(r"[^\w\- ]", "_", title)
        path = os.path.join(wiki_folder, safe_title + ".txt")

        with open(path, "w", encoding="utf-8") as f:
            f.write(page.text)

        wiki_count += 1
        print(f"📄 Wikipedia: сохранено {safe_title}")

print(f"✅ Wikipedia: скачано {wiki_count} документов")


# --- arXiv ---
search_query = "information retrieval OR search engine OR machine learning"
max_results = 10

search = arxiv.Search(
    query=search_query,
    max_results=max_results
)

arxiv_count = 0

print(f"🔎 Поиск arXiv: {search_query}")

for result in search.results():
    try:
        safe_title = re.sub(r"[^\w\- ]", "_", result.title)

        pdf_url = result.pdf_url
        pdf_path = os.path.join(arxiv_folder, safe_title + ".pdf")

        print(f"📥 Скачивание: {safe_title}")

        r = requests.get(pdf_url, timeout=30)
        r.raise_for_status()

        with open(pdf_path, "wb") as f:
            f.write(r.content)

        # сохраняем также метаданные
        meta_path = os.path.join(arxiv_folder, safe_title + "_meta.txt")
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write("Title: " + result.title + "\n")
            f.write("Authors: " + ", ".join(a.name for a in result.authors) + "\n")
            f.write("Published: " + str(result.published) + "\n\n")
            f.write("Abstract:\n" + result.summary)

        arxiv_count += 1

    except Exception as e:
        print("Ошибка скачивания:", e)

print(f"✅ arXiv: скачано {arxiv_count} документов")