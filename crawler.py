from utils import read_initial_urls, filter_urls
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
from urllib.error import URLError
import urllib
import re
import requests

class Crawler:
    def __init__(self, initial_urls: str): 
        self.url_queue = read_initial_urls(initial_urls)
        self.visited_urls = set()
        
    def _get_page_text(self, url:str) -> str:
        """
        Makes a get request to an URL and fetches the page text
        
        Args:
            url (str): The URL of the webpage
            
        Returns:
            page_text (str): all the Text on the webpage
            page_status_code (str): status code of the get request
            
        Raises: 
            /
        """
        page_info = requests.get(url, timeout=2.50)
        page_status_code = page_info.status_code
        page_text = page_info.text

        return page_text, page_status_code
    
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

    def _parse_page_text(self, page_text: str) -> list:
        """
        Retrieves for a given String all the occurences of URLs
        
        Args:
            page_text (str): A String with all the text of a webpage
            
        Returns:
            urls (list): A List with all the URLs within the page_text 
            
        Raises: 
            /
        """
        urls = re.findall(r'href=["\']?(https?://[^\s"\'<>]+)', page_text)
        urls = filter_urls(urls, "https://finance.yahoo.com/")
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

        for url in self.url_queue:
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
            page_text, _ = self._get_page_text(url)
            crawled_urls = self._parse_page_text(page_text)
            self.url_queue.extend(crawled_urls)

if __name__ == '__main__':
    crawler = Crawler("initial_urls.txt")
    crawler.crawl_urls()
    


        