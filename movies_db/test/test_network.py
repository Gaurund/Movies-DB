from contextlib import AbstractContextManager
from typing import Any

import movies_db.network as network
from unittest import TestCase

class TestGrabPage(TestCase):

    def test_strip_page_details(self):
        with open("movies_db/test/test_page_shawshank.html", "r", encoding="utf-8") as f:
            page = f.read()
        movie = network.strip_page_details(page)
        self.assertEqual(movie["name_original"], "The Shawshank Redemption")
        self.assertEqual(movie["name_russian"], "Побег из Шоушенка")

    def test_grab_page(self):
        url = "https://www.imdb.com/title/tt0111161/"
        response = network.grab_page(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("The Shawshank Redemption", response.text)

    def test_grab_page_invalid_url(self):
        url = "https://www.imdb.com/title/tt0000000/"
        with self.assertRaises(AssertionError):
            network.grab_page(url)
    
class TestStripPageDetails(TestCase):

    def test_strip_page_details(self):
        with open("movies_db/test/test_page_shawshank.html", "r", encoding="utf-8") as f:
            page = f.read()
        movie = network.strip_page_details(page)
        self.assertEqual(movie["name_original"], "The Shawshank Redemption")
        self.assertEqual(movie["name_russian"], "Побег из Шоушенка")
        self.assertEqual(movie["duration"], "PT2H22M")
        self.assertEqual(movie["premiere_date"], "1994")
        self.assertEqual(movie["imdb_link"], "https://www.imdb.com/title/tt0111161/")
        self.assertEqual(movie["type"], "Movie")
        self.assertIn("Drama", movie["genres"])
        self.assertIn("Prison Drama", movie["genres"])
        self.assertIn("Frank Darabont", movie["directors"][0]["name"])
        self.assertIn("Tim Robbins", movie["actors"][0]["name"])
        self.assertIn("Morgan Freeman", movie["actors"][1]["name"])
        self.assertIn("Bob Gunton", movie["actors"][2]["name"])
