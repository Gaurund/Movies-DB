import json
from bs4 import BeautifulSoup
import requests


def grab_page(url: str) -> requests.Response:
    headers = {
        "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5",
        "priority": "i",
        "referer": "https://www.imdb.com/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "image",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "cross-site",
        "sec-fetch-storage-access": "active",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    return response


def strip_page_details(response_text: str) -> dict:
    soup = BeautifulSoup(response_text, features="html.parser")
    movie_tags = [
        span.get_text()
        for span in soup.select("div.ipc-chip-list__scroller > a > span")
    ]
    script_json = soup.find("script", type="application/ld+json")
    data = json.loads(script_json.text) if script_json else {}
    premiere_link = soup.select_one('a[href*="releaseinfo"]')

    directors = []
    for person in data["director"] if "director" in data else []:
        directors.append(
            {"name": person.get("name", "N/A"), "imdb_link": person.get("url", "N/A")}
        )

    actors = []
    for person in data["actor"] if "actor" in data else []:
        actors.append(
            {"name": person.get("name", "N/A"), "imdb_link": person.get("url", "N/A")}
        )

    movie = {
        "name_original": data.get("name"),
        "name_russian": data.get("alternateName"),
        "duration": data.get("duration", None),
        "premiere_date": premiere_link.get_text(strip=True) if premiere_link else None,
        "imdb_link": data.get("url"),
        "type": data.get("@type"),
        "genres": movie_tags,
        "directors": directors,
        "actors": actors,
    }
    return movie

def process_movie_page(url: str) -> dict:
    response = grab_page(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to grab page: {url} (status code: {response.status_code})")
    movie_details = strip_page_details(response.text)
    return movie_details

if __name__ == "__main__":

    def print_movie_details(movie: dict):
        print(f"Original Name: {movie['name_original']}")
        print(f"Russian Name: {movie['name_russian']}")
        print(f"Duration: {movie['duration']}")
        print(f"Premiere Date: {movie['premiere_date']}")
        print(f"IMDb Link: {movie['imdb_link']}")
        print(f"Type: {movie['type']}")
        print(f"Genres: {', '.join(movie['genres'])}")
        print("Directors:")
        for director in movie["directors"]:
            print(f"  - {director['name']} ({director['imdb_link']})")
        print("Actors:")
        for actor in movie["actors"]:
            print(f"  - {actor['name']} ({actor['imdb_link']})")

    def test_strip_page_details(filename: str):
        with open(f"movies_db/test/{filename}", "r", encoding="utf-8") as f:
            page = f.read()
            movie = strip_page_details(page)
            print_movie_details(movie)
            print("-" * 40)

    def save_grabbed_page(url: str, filename: str):
        response = grab_page(url)
        with open(f"movies_db/test/{filename}", "w", encoding="utf-8") as f:
            f.write(response.text)

    test_strip_page_details("test_page_shawshank.html")
    test_strip_page_details("test_page_cold_case.html")
    # save_grabbed_page("https://www.imdb.com/title/tt0368479/", "test_page_cold_case.html")
