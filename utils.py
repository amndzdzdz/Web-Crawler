def read_initial_urls(path):
    with open(path, 'r') as urls_file:
        initial_urls = [file for file in urls_file]
    
    return initial_urls


if __name__ == '__main__':
    read_initial_urls("initial_urls.txt")
