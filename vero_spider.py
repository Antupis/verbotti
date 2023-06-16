import scrapy
from bs4 import BeautifulSoup

class VeroSpider(scrapy.Spider):
    name = "vero"
    allowed_domains = ["vero.fi"]
    start_urls = [
        'http://vero.fi/',
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 3, # delay between requests
    }

    def parse(self, response):
        # Create a BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Get the text from the soup
        text = soup.get_text()

        # Save the text to a file
        with open('og_data/vero_text.txt', 'a') as f:
            f.write(text)

        # Look for links to follow, ignoring javascript: and mailto: links
        for href in response.css('a::attr(href)').getall():
            if not (href.startswith('javascript:') or href.startswith('mailto:')):
                yield response.follow(href, self.parse)