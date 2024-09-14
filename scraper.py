import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from typing import Type
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime

class Scraper():
    """
    Scrapes titles, text and links from articles on the given url webpage and saves them to a NoSQL DB

    Args:
        url (str): URL to a webpage

    Returns:
        /
        
    Raises: 
        /
    """

    def scrape(self, url: str) -> list:
        """
        Scrapes titles, text and links from articles on the given url webpage and saves them to a NoSQL DB

        Args:
            url (str): URL to a webpage

        Returns:
            /
            
        Raises: 
            /
        """
        driver = self.__initialize_driver()
        driver.get(url)
        time.sleep(3)
        driver.find_element(By.NAME, "agree").click()
        driver.maximize_window()

        # Simulate continuous scrolling
        stopScrolling = 0
        while True:
            stopScrolling += 1
            driver.execute_script("window.scrollBy(0,40)")
            time.sleep(0.5)
            if stopScrolling > 100:
                break

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, "html.parser")
        divs = soup.find_all("div")
        filtered_divs = [div for div in divs if div.h3 and len(div.h3.text) > 20]

        for div in filtered_divs:
            text = ""
            
            try:
                title = div.h3.text

            except:
                print("The crawled entry doesn't have a title")
                continue

            try:
                link = div.a["href"]
            except:
                link = "/"
                print("The crawled entry doesn't have a link")

            self._save_to_db(title, text, link)

        driver.close()

    def _save_to_db(self, title: str, text: str, link: str) -> None:
        """
        Saves a datapoint consisting of article title, article text (so far empty) and link to the article
        to a MongoDB Database (NoSQL)

        Args:
            title (str): Title of the article
            text (str): Text of the article
            link (str): Link of the article

        Returns:
            /
            
        Raises: 
            /
        """

        entry = {
            "title": title,
            "text": text,
            "link": link,
            "date": datetime.datetime.now()
        }

        client = MongoClient()
        yahoo_finance_db = client.YahooFinanceDB
        articles_collection = yahoo_finance_db.Articles
        articles_collection.insert_one(entry).inserted_id

    def __initialize_driver(self) -> webdriver:
        """
        initializes the chrome webdriver for selenium

        Args:
            /

        Returns:
            driver (WebDriver): The initialised webdriver
            
        Raises: 
            /
        """
        options = Options()
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument("--no-sandbox")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        return driver


if __name__ == '__main__':
    scraper = Scraper()
    scraper.scrape("https://finance.yahoo.com/news/")