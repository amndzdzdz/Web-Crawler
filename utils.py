def read_initial_urls(path:str) -> list:
    """
    Reads the initial URLs from the initial_urls.txt file

    Args:
        path (str): relative path to the file

    Returns:
        initial_urls (list): The initial URLs from the file
        
    Raises: 
        /
    """
    with open(path, 'r') as urls_file:
        initial_urls = [file.replace("\n", "") for file in urls_file]
    
    return initial_urls

def filter_urls(urls: list, target_site: str) -> list:
    """
    Filters the URLs-List to only contain URLs to webpages with textual information and stay on the target webpage 
    
    Args:
        url (list): List of all crawled URLs
        target_site (str): Site on which the crawler should focus

    Returns:
        filtered_urls (list): All the filtered URLs that are on the same page and  
        
    Raises: 
        /
    """
    filtered_urls = []
    file_endings = ['png', 'js', 'jpg', 'jpeg', 'gif', 'css', 'php', 'mp3']
    for url in urls:
        url_ending = url.split('.')[-1]
        if (url_ending not in file_endings) and (target_site in url):
            filtered_urls.append(url)
        
    return filtered_urls


if __name__ == '__main__':
    urls = ["https://s.yimg.com/uc/finance/webcore","https://www.yahoo.com/news/politics/", "https://s.yimg.com/uc/finance/webcore/js/_staticFinProtobuf.4b1559b8e4645fd93a12.js"]

    filter_urls(urls, "https://www.yahoo.com")
