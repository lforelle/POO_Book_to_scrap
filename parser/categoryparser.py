from bs4 import BeautifulSoup
from scraper import Scraper
from urllib.parse import urljoin
from .bookparser import BookParser, DETAILS_DIR
import csv
import os

# Project directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class CategoryParser:
    """Parse data from books in a category"""
  
    def __init__(self, category_url):
        self.category_url = category_url        
        self.soup = BeautifulSoup
        self.books_url_list = []

    def parse_category(self):
        """Parse data from the category"""
        
        # Access test to category url
        scraper_category_url = Scraper(self.category_url)
        category_url_access_test = scraper_category_url.url_access_test()
        if category_url_access_test is None:
            print(f"No data for : {self.category_url}")
        else:
            self.soup = scraper_category_url.get_page(category_url_access_test)
        
        self.category_name = self.soup.find("head").find("title").string
        self.category_name = self.category_name.split('|')[0].strip()
        category_slug = self.category_name.replace(" ", "_")
        category_dir = os.path.join("Extracts", category_slug)
        os.makedirs(category_dir, exist_ok=True)
        os.chdir(category_dir)
     
        next_page_url = False

        # Extract url from books of the category and store them in a list
        self.books_url_extract()
        
        # Check if several html pages are used  
        next_page_url = self.find_next_page_url()

        while next_page_url:
            scraper_next_url = Scraper(next_page_url)
            next_url_access_test = scraper_next_url.url_access_test()
            if next_url_access_test is None:
                print(f"No data for : {next_page_url}")
            else:
                self.soup = scraper_next_url.get_page(next_url_access_test)
            self.books_url_extract()
            self.category_url = next_page_url
            next_page_url = self.find_next_page_url()

        print(f"####### Book(s) in the category '{self.category_name}' ########") 
        # Parse data of each book
        for book_url in self.books_url_list:
            book_parser = BookParser(book_url)
            book_data = book_parser.parse_book()
            if book_data is not None:
                self.category_name = book_data.get("category", self.category_name)

        category_filename = "books_by_category_" + category_slug + "_"

        # Save the url list of the category
        self.save_category_url(category_filename, "w")
        os.chdir("./../..")

    def books_url_extract(self):
        ol_books = self.soup.find("ol", class_="row")
        for li_book in ol_books.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
            div_image_container_href = li_book.find("div", class_="image_container").find("a").get("href")
            div_image_container_href = div_image_container_href.split('../')[-1]
            book_url_absolue = urljoin('https://books.toscrape.com/catalogue/', div_image_container_href)
            self.books_url_list.append(book_url_absolue)

    def find_next_page_url(self):
        ul_pager = self.soup.find("ul", class_="pager")
        if ul_pager == None:
            return False

        li_next = ul_pager.find("li", class_="next")
        if li_next:
            href_page = li_next.find("a").get("href")
            return urljoin(self.category_url, href_page)
        return False

    def save_category_url(self, category_filename, mode):   
        os.makedirs(DETAILS_DIR, exist_ok=True)
        path_output_filename = os.path.join(DETAILS_DIR, category_filename + ".csv")

        with open(path_output_filename, mode, newline="", encoding="utf-8") as output_csv:
            writer = csv.writer(output_csv, delimiter=",")
            writer.writerow(self.books_url_list)

if __name__ == "__main__":
    categoryBook = CategoryParser("https://books.toscrape.com/catalogue/category/books/mystery_3/index.html")
    categoryBook.parse_category()
