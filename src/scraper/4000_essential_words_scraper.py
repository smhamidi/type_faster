import os
from pathlib import Path
import sys

import requests
from bs4 import BeautifulSoup


path = Path(__file__).resolve()
parent_dir = path.parents[2]
if not parent_dir in sys.path:
    sys.path.insert(0, str(parent_dir))

from config.path import ROOT_DIR


def get_book_links():
    url = "https://lang.b-amooz.com/en/vocabulary/book-collection/29/4000-essential-english-words"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    book_links = [
        link.get("href")
        for link in soup.find_all(
            "a", class_="btn bg-gradient-color btn-rounded text-white"
        )
    ]

    return book_links


def get_lesson_links(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    lesson_links = [
        link.get("href")
        for link in soup.find_all(
            "a", class_="btn bg-gradient-color btn-rounded text-white mb-3"
        )
    ]

    return lesson_links


def get_words_from_lesson(lesson_url):
    try:
        response = requests.get(lesson_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        divs = soup.find_all("div", class_="ltr d-inline-block")

        words = []
        for div in divs:
            span = div.find("span", class_="font-weight-bold")
            if span:
                words.append(
                    span.text.strip()
                )  # Get the text and remove leading/trailing whitespace

        return words

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []


if __name__ == "__main__":
    books = get_book_links()

    lessons = []
    for book in books:
        lessons += get_lesson_links(book)

    words = []
    for lesson in lessons:
        words += get_words_from_lesson(lesson)

    with open(
        os.path.join(ROOT_DIR, "static", "word", "4000_essential_words.txt"), "w"
    ) as file:
        for word in words:
            file.write(str(word) + "\n")
