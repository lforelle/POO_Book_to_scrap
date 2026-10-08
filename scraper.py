import requests
from bs4 import BeautifulSoup

class Scraper:
    """Récupération page HTML"""
    def __init__(self, url):
        self.url = url

    def test_page_access(self):
        response = requests.get(self.url)
        print(f"{self.url} --> {response.status_code}")

        if response.status_code == 200:
            return response
        print(f"ERREUR : impossible d'accéder à {self.url}")
        return None

    def get_page(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/the-argonauts_837/index.html"
    scraper = Scraper(url)
    test_acces_page_html = scraper.test_page_access()
    if test_acces_page_html is None:
        print(f"Pas de données pour : {url}")
    else:
        soup = scraper.get_page(test_acces_page_html)

