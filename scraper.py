"""
Author:
    Amin Dziri
"""

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

        #Check if cookie pop up needs to be accepted
        try:
            driver.find_element(By.NAME, "agree").click()
        except:
            print("No Cookies to accept")

        driver.maximize_window()

        # Simulate continuous scrolling
        stop_scrolling = 0
        while True:
            stop_scrolling += 1
            driver.execute_script("window.scrollBy(0,40)")
            time.sleep(0.5)
            if stop_scrolling > 400:
                break

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, "html.parser")
        divs = soup.find_all("div")
        filtered_divs = [div for div in divs if div.h3 and len(div.h3.text) > 20]

        for div in filtered_divs:
            
            try:
                title = div.h3.text
            except:
                title = "/"
                print("The crawled entry doesn't have a title")
                continue

            try:
                link = div.a["href"]
            except:
                link = "/"
                print("The crawled entry doesn't have a link")

            self._save_to_db(title, link)

        driver.close()

    def _save_to_db(self, title: str, link: str) -> None:
        """
        Saves a datapoint consisting of article title and article link 
        to a MongoDB Database (NoSQL)

        Args:
            title (str): Title of the article
            link (str): Link of the article

        Returns:
            /
            
        Raises: 
            /
        """

        entry = {
            "title": title,
            "link": link,
            "date": datetime.datetime.now()
        }

        #Change this to your own Database & Collection
        client = MongoClient()
        yahoo_finance_db = client.YahooFinanceDB
        articles_collection = yahoo_finance_db.Articles

        #Check if the articles is already in the database
        if articles_collection.find_one({"title": entry["title"]}) == None:
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
        try:
            options.add_argument("--disable-search-engine-choice-screen")
            options.add_argument("--no-sandbox")
            options.add_argument("disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
        except:
            print("An Unknown error has occured")
        driver = webdriver.Chrome(options=options)

        return driver