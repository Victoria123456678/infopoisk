# search.py
from boolean_index import build_boolean_index


def boolean_search(query, index):
    # Простая реализация: только AND между словами
    tokens = query.lower().split()
    if not tokens:
        return set()

    # Начинаем с документов первого токена
    result = index.get(tokens[0], set()).copy()

    for token in tokens[1:]:
        result &= index.get(token, set())  # пересечение множеств (AND)

    return result


if __name__ == "__main__":
    index = build_boolean_index()
    while True:
        query = input("Введите запрос (или 'exit' для выхода): ")
        if query.lower() == "exit":
            break
        results = boolean_search(query, index)
        if results:
            print("Найдены документы:", results)
        else:
            print("Документы не найдены.")