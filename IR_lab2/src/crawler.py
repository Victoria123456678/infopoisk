import yaml
import time
import requests
import hashlib
from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys


def normalize_url(url):
    parsed = urlparse(url)
    return parsed.scheme + "://" + parsed.netloc + parsed.path


def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def connect_db(config):
    client = MongoClient(config["db"]["uri"])
    db = client[config["db"]["database"]]
    return db[config["db"]["collection"]]


def get_source(url):
    if "wikipedia" in url:
        return "wikipedia"
    if "arxiv" in url:
        return "arxiv"
    return "unknown"


def fetch_page(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        return None


def hash_content(text):
    return hashlib.md5(text.encode()).hexdigest()


def save_document(collection, url, html):
    normalized = normalize_url(url)
    source = get_source(url)
    timestamp = int(time.time())
    content_hash = hash_content(html)

    existing = collection.find_one({"url": normalized})

    if existing:
        if existing["hash"] != content_hash:
            collection.update_one(
                {"url": normalized},
                {
                    "$set": {
                        "html": html,
                        "timestamp": timestamp,
                        "hash": content_hash,
                    }
                },
            )
            print("Обновлён:", normalized)
    else:
        collection.insert_one(
            {
                "url": normalized,
                "html": html,
                "source": source,
                "timestamp": timestamp,
                "hash": content_hash,
                "visited": False,
            }
        )
        print("Сохранён:", normalized)


def extract_links(base_url, html):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        link = urljoin(base_url, a["href"])
        if link.startswith("http"):
            links.append(link)

    return links


def crawl(config):
    collection = connect_db(config)

    delay = config["logic"]["delay"]
    max_pages = config["logic"]["max_pages"]

    for seed in config["seeds"]:
        save_document(collection, seed, fetch_page(seed) or "")

    while True:
        doc = collection.find_one({"visited": False})

        if not doc:
            print("Все страницы обработаны")
            break

        url = doc["url"]
        html = fetch_page(url)

        if html:
            save_document(collection, url, html)
            links = extract_links(url, html)

            for link in links[:5]:
                if not collection.find_one({"url": normalize_url(link)}):
                    collection.insert_one(
                        {
                            "url": normalize_url(link),
                            "visited": False,
                            "timestamp": 0,
                            "html": "",
                            "source": get_source(link),
                            "hash": "",
                        }
                    )

        collection.update_one({"_id": doc["_id"]}, {"$set": {"visited": True}})

        time.sleep(delay)

        if collection.count_documents({}) >= max_pages:
            break


if __name__ == "__main__":
    config_path = sys.argv[1]
    config = load_config(config_path)
    crawl(config)