import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(list)
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    # fixed logic 1: check if href is absolute or relative
                    if not urlparse(href).netloc:  # relative link
                        href = urljoin(base_url or url, href)
                    if href.startswith(base_url or url):
                        self.crawl(href, base_url=base_url or url)  
                        # fixed 2: only crawl inside same domain
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            if keyword.lower() in text.lower():  # fixed 3: was "not in"
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")  # fixed 4: replaced undefined_variable with result
        else:
            print("No results found.")

def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.crawl(start_url)  # fixed 5: typo `craw` → `crawl`

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)

# ------------------ Unit Tests ------------------

import unittest
from unittest.mock import patch, MagicMock

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Assert that 'about' was added to visited URLs
        self.assertIn("https://example.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")

        crawler = WebCrawler()
        crawler.crawl("https://example.com")
        # no exception should be raised → just logged

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No key here"

        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])  # fixed 1: should return page1

    @patch('sys.stdout')
    def test_print_results(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])
        # check output written (simplified)

if __name__ == "__main__":
    unittest.main(exit=False)  # fixed: allow running both tests and main()
    main()
