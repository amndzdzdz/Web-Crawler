from utils import read_initial_urls
import requests
from parser import Parser
from RequestHandler import RequestHandler

class Crawler:
    def __init__(self, initial_urls):
        self.urls = read_initial_urls(initial_urls)
        self.RequestHandler = RequestHandler()
        self.Parser = Parser()

    def crawl_urls(self):
        for url in self.urls:
            page_text, page_status_code = self.RequestHandler.get_page_text(url)
            crawled_urls = Parser.parse(page_text)
            self.urls.append(crawled_urls)
            

if __name__ == '__main__':
    crawler = Crawler("initial_urls.txt")
    crawler.crawl_urls()
    


        