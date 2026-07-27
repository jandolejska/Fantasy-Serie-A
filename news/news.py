import json
from pathlib import Path

DATA_FILE = Path("data/current_news.json")


def load_news():

    if not DATA_FILE.exists():
        return []

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_news(news):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            news,
            f,
            ensure_ascii=False,
            indent=4
        )


def add_news(item):

    news = load_news()

    news.append(item)

    save_news(news)


def clear_news():

    save_news([])