import json
import re
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
    def href_releaseinfo(href):
        return href and re.compile("releaseinfo").search(href)

    soup = BeautifulSoup(response_text, features="html.parser")
    movie_tags = [
        span.text for span in soup.select("div.ipc-chip-list__scroller > a > span")
    ]
    script_json = soup.find_all(type="application/ld+json")
    json_dict = json.loads(script_json[0].text)
    premiere_link = soup.find(href=href_releaseinfo)

    if "duration" in json_dict.keys():
        duration = json_dict["duration"]
    else:
        duration = None

    movie = {
        "name_original": json_dict["name"],
        "name_russian": json_dict["alternateName"],
        "duration": duration,
        "premiere_date": premiere_link.text,
        "imdb_link": json_dict["url"],
        "type": json_dict["@type"],
        "genres": movie_tags,
    }
    return movie

if __name__ == "__main__":
    def test_strip_page_details(filename: str):
        with open(f"movies_db/test/{filename}", "r", encoding="utf-8") as f:
            page = f.read()
            movie = strip_page_details(page)
            print(movie)

    def save_grabbed_page(url: str, filename: str):
        response = grab_page(url)
        with open(f"movies_db/test/{filename}", "w", encoding="utf-8") as f:
            f.write(response.text)

    test_strip_page_details('test_page_cold_case.html')
    # save_grabbed_page("https://www.imdb.com/title/tt0368479/", "test_page_cold_case.html")
    