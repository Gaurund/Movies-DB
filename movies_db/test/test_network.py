import movies_db.network as network
from unittest import TestCase

class TestNetwork(TestCase):

    def test_grab_page(self):
        url = "https://www.imdb.com/title/tt0111161/"
        response = network.grab_page(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("The Shawshank Redemption", response.text)

    def test_grab_page_invalid_url(self):
        url = "https://www.imdb.com/title/tt0000000/"
        with self.assertRaises(AssertionError):
            network.grab_page(url)