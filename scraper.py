import requests
from bs4 import BeautifulSoup

class Scraper:
    """HTML page extraction"""
    def __init__(self, url):
        self.url = url

    def url_access_test(self):
        response = requests.get(self.url)
        print(f"{self.url} --> {response.status_code}")

        if response.status_code == 200:
            return response
        print(f"ERROR : access to '{self.url}' is not possible ")
        return None

    def get_page(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/the-argonauts_837/index.html"
    scraper = Scraper(url)
    test_book_page_access = scraper.url_access_test()
    if test_book_page_access is None:
        print(f"No data for : {url}")
    else:
        soup = scraper.get_page(test_book_page_access)

