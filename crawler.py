from utils import read_initial_urls, filter_urls
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
from urllib.error import URLError
from lxml import html
from scraper import Scraper
import urllib
import re
import requests

class YahooCrawler:
    def __init__(self, n_urls, initial_urls: str, base_page: str): 
        """
        Initialzes some Arguments
        
        Args:
            n_urls (str): Amount of URLs that should be parsed
            initial_urls (str): Path to the inital_urls.txt file
            base_page (str): URL on which the crawler should stay

        """
        self.url_queue = read_initial_urls(initial_urls)
        self.visited_urls = set()
        self.scraper = Scraper()
        self.base_page = base_page
        self.n_urls = n_urls
    
    def _check_allowance(self, url: str) -> bool:
        """
        Checks for a given webpage-url whether its crawlable. The function checks the robots.txt of the
        webpage.
        
        Args:
            url (str): The URL of the webpage
            
        Returns:
            bool: True if url is crawlable, False if otherwise 
            
        Raises: 
            /
        """
        robots_txt_url = self._get_robots_txt_url(url)
        robotParser = RobotFileParser()
        robotParser.set_url(robots_txt_url)
        robotParser.read()

        return robotParser.can_fetch("*", url)
    
    def _get_robots_txt_url(self, url: str) -> str:
        """
        Returns for an URL the URL to the robots.txt file of this website
        
        Args:
            url (str): The URL of the webpage
            
        Returns:
            robot_txt_url (str): The URL to the robots.txt file of the page 
            
        Raises: 
            /
        """
        split_url = urlsplit(url)

        #robots.txt url is base_url + /robots.txt
        base_url = split_url.scheme + '://' + split_url.netloc
        robot_txt_url = base_url + '/' + "robots.txt"
        return robot_txt_url

    def _get_page_urls(self, url: str) -> list:
        """
        Retrieves for a given String all the occurences of URLs
        
        Args:
            page_text (str): A String with all the text of a webpage
            
        Returns:
            urls (list): A List with all the URLs within the page_text 
            
        Raises: 
            /
        """
        page_info = requests.get(url, timeout=2.50)
        page_text = page_info.text
        urls = re.findall(r'href=["\']?(https?://[^\s"\'<>]+)', page_text)
        urls = filter_urls(urls, self.base_page)
        return urls

    def crawl_urls(self) -> None:
        """
        Main Crawling loop
        
        Args:
            /
        Returns:
            /
        Raises: 
            URLError, if the URL is not a real URL
        """
        i = 1
        for url in self.url_queue:
            print(f"Currently Scraping URL Nr.{i}")
            i += 1
            
            try:
                self.url_queue.remove(url)
            except URLError:
                print(f"The URL {url} is not correct")
            
            #Check if the current webpage was already visited
            if url in self.visited_urls:
                continue

            #Check if webpage allows crawling
            if not self._check_allowance(url):
                continue

            self.visited_urls.add(url)
            crawled_urls = self._get_page_urls(url)
            self.scraper.scrape(url)
            self.url_queue.extend(crawled_urls)

            if i > self.n_urls:
                break


if __name__ == '__main__':
    crawler = YahooCrawler(n_urls=50, "initial_urls.txt", "https://finance.yahoo.com/")
    crawler.crawl_urls()
    


        