import requests

class RequestHandler:
    """
    The RequestHandler class handles the get requests and retrieves new urls
    """
    def get_page_text(self, url):
        page_info = requests.get(url, timeout=2.50)
        page_status_code = page_info.status_code
        page_text = page_info.text

        return page_text, page_status_code

    def crawl_urls(url):
        new_urls = []

        return new_urls