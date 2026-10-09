from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scraper import Scraper
from .categoryparser import CategoryParser

class CategoriesParser:
    """Parse the data from all the books in all categories of the website"""
    
    def __init__(self, website_url):
        self.website_url = website_url        
        self.soup = BeautifulSoup
        self.categories_url_list = []

    def parse_categories(self):
        """Parse the data from categories"""

        # Website url access test
        scraper_website_url = Scraper(self.website_url)
        website_url_access_test = scraper_website_url.url_access_test()
        if website_url_access_test is None:
            print(f"Website : {self.website_url} not accessible !")
        else:
            self.soup = scraper_website_url.get_page(website_url_access_test)

        ul_categories_list = self.soup.find("ul", class_="nav nav-list").find("li").find("ul")
        for li_category in ul_categories_list.find_all("li"):
            category_url = li_category.find("a").get("href")
            category_absolute_url = urljoin('https://books.toscrape.com/', category_url)
            self.categories_url_list.append(category_absolute_url)

        for url in self.categories_url_list:
            category_parser = CategoryParser(url)
            category_parser.parse_category()
        

if __name__ == "__main__":
    categories = CategoriesParser("https://books.toscrape.com/")
    categories.parse_categories()