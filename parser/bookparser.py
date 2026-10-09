from scraper import Scraper
from urllib.parse import urljoin
import re
import csv
import os

DETAILS_DIR = "Books_details"     # Name prefix for the directory name of the CSV files

class BookParser:
    """Book data extraction"""

    def __init__(self, html):
        self.html = html

    def parse_book(self):
        """Parse the data of a book"""

        scraper = Scraper(self.html)
        html_url_access_test = scraper.url_access_test()
        if html_url_access_test is None:
            print(f"No data for : {self.html}")
            return None
        else:
            self.soup = scraper.get_page(html_url_access_test)

        dico_infos = {}
        currency = "£"
        title = self.soup.find("div", class_="col-sm-6 product_main").find("h1").text
        dico_infos["title"] = title

        table = self.soup.find("table", class_="table table-striped")
        for tr in table.find_all("tr"):
            for th in tr.find_all("th"):
                if th.text.lower() == "upc":
                    dico_infos[th.text] = tr.find("td").get_text(strip=True)
                if th.text.lower() == "price (incl. tax)":
                    raw_taxed_price = tr.find("td").get_text(strip=True)
                    taxed_price = raw_taxed_price.split(currency)[1] + currency
                    dico_infos[th.text] = taxed_price
                if th.text.lower() == "price (excl. tax)":
                    raw_free_price = tr.find("td").get_text(strip=True)
                    free_price = raw_free_price.split(currency)[1] + currency
                    dico_infos[th.text] = free_price
                if th.text.lower() == "tax":
                    raw_tax = tr.find("td").get_text(strip=True)
                    tax = raw_tax.split(currency)[1] + currency
                    dico_infos[th.text] = tax
                if th.text.lower() == "availability":
                    raw_availibility = tr.find("td").get_text(strip=True)
                    availibility = (raw_availibility.split("(")[1]).split(" ")[0]
                    dico_infos[th.text] = availibility
        
        # Description
        h2_product_description = self.soup.find("h2", string="Product Description")
        if h2_product_description:
            product_description = h2_product_description.find_next("p")
            dico_infos["product_description"] = product_description.get_text(strip=True)
        else:
            dico_infos["product_description"] = "No description found !!"

        # Category
        ul_breadcrumb = self.soup.find("ul", class_="breadcrumb")
        for li in ul_breadcrumb.find_all("li"):
            a_category = li.find("a")
            if a_category:
                if a_category.string.lower() == "home" or a_category.string.lower() == "books":
                    continue
                else:
                    book_category = li.find("a").text
                    dico_infos["category"] = book_category

        # Book rating
        star_rating = self.soup.find("i", class_="icon-star").find_parent("p")
        review_rating = star_rating.get("class")
        nb_stars_en = review_rating[-1].lower()
        nb_stars = {"one":1, "two": 2, "three": 3, "four": 4, "five": 5}
        nb_stars_fr = nb_stars[nb_stars_en]
        dico_infos["review_rating"] = nb_stars_fr

        # Book image absolute url
        image_url = self.soup.find(id="product_gallery").find("img").get("src")
        src_image = image_url.split('../')[-1]
        image_url_absolute = urljoin('https://books.toscrape.com/', src_image)
        dico_infos["image_url"] = image_url_absolute

        # Save CSV
        safe_title = re.sub(r"[^a-zA-Z0-9]+", "_", title).strip("_")
        filename = "details_" + (safe_title)[:25] + "_"     # 25 premiers caracteres du titre seulement
        self.save_book_data_to_csv(filename, dico_infos, "a")

        # Fetch image and save it in the same folder as the 'csv' file
        image_scraper = Scraper(image_url_absolute)
        image_url_access_test = image_scraper.url_access_test()
        if image_url_access_test is None:
            print(f"No data for : {image_url_absolute}")
            return dico_infos
        path_jpg_filename = DETAILS_DIR + "/" + filename + '.jpg'
        jpg_file_exists = os.path.isfile(path_jpg_filename)
        if jpg_file_exists:
            return dico_infos
        with open(path_jpg_filename, "wb") as image_file:
            image_file.write(image_url_access_test.content)

        return dico_infos

    def save_book_data_to_csv(self, filename, dico_infos, mode):   
        self.filename = filename
        self.dico_infos = dico_infos
        self.mode = mode

        os.makedirs(DETAILS_DIR, exist_ok=True)
        path_output_filename = os.path.join(DETAILS_DIR, self.filename + ".csv")
        
        file_exists = os.path.isfile(path_output_filename)

        with open(path_output_filename, self.mode, newline="", encoding="utf-8") as output_csv:
            fieldnames = dico_infos.keys()
            writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(self.dico_infos)


if __name__ == "__main__":
    book = BookParser("https://books.toscrape.com/catalogue/the-argonauts_837/index.html")
    book.parse_book()
