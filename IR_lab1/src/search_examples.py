# src/search_examples.py

queries = [
    "machine learning site:wikipedia.org",
    "information retrieval site:wikipedia.org",
    "search engine ranking site:wikipedia.org",
    "information retrieval site:arxiv.org",
    "neural networks site:arxiv.org"
]

print("Примеры запросов Google:")
for q in queries:
    url = "https://www.google.com/search?q=" + q.replace(" ", "+")
    print(q)
    print(url)
    print("Недостаток: результаты могут не совпадать с нашим корпусом\n")


wiki_queries = [
    "machine learning",
    "information retrieval"
]

print("Поиск Wikipedia:")
for q in wiki_queries:
    url = "https://en.wikipedia.org/w/index.php?search=" + q.replace(" ", "+")
    print(q)
    print(url)
    print("Недостаток: поиск только внутри Wikipedia\n")


arxiv_queries = [
    "information retrieval",
    "natural language processing"
]

print("Поиск arXiv:")
for q in arxiv_queries:
    url = "https://arxiv.org/search/?query=" + q.replace(" ", "+")
    print(q)
    print(url)
    print("Недостаток: только научные статьи\n")