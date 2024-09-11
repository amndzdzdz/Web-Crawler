import re

class Parser:
    """
    The Parser handles parsing the page text and finding new URLs
    """
    def parse(page_text):
        urls = re.findall(r'href=["\']?(https?://[^\s"\'<>]+)', page_text)
        return urls