#!/usr/bin/env python3
"""
Web Crawler - A CLI tool to crawl websites recursively
"""
import argparse
import collections
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import sys
import time


class WebCrawler:
    """Web crawler that extracts links from web pages up to a specified depth"""
    
    def __init__(self, base_url, max_depth=3, output_file=None):
        """Initialize the crawler with base URL and maximum depth"""
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.output_file = output_file
        self.visited_urls = set()
        self.found_urls = set()
        self.queue = collections.deque()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; PythonWebCrawler/1.0)'
        }

    def is_valid_url(self, url):
        """Check if URL belongs to the same domain and has not been visited"""
        parsed_url = urlparse(url)
        return (parsed_url.netloc == self.base_domain or not parsed_url.netloc) and url not in self.visited_urls

    def normalize_url(self, url):
        """Convert relative URLs to absolute URLs"""
        return urljoin(self.base_url, url)

    def extract_links(self, url):
        """Extract all links from a webpage"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to retrieve {url}: HTTP {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']
                absolute_url = self.normalize_url(href)
                if self.is_valid_url(absolute_url):
                    links.append(absolute_url)
            
            return links
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return []

    def crawl(self):
        """Start crawling from the base URL up to max_depth"""
        # Add the base URL to the queue with depth 0
        self.queue.append((self.base_url, 0))
        
        while self.queue:
            url, depth = self.queue.popleft()
            
            # Skip if already visited or exceeds max depth
            if url in self.visited_urls or depth > self.max_depth:
                continue
            
            print(f"[Depth {depth}] Crawling: {url}")
            self.visited_urls.add(url)
            self.found_urls.add(url)
            
            # If we're at max depth, don't extract more links
            if depth == self.max_depth:
                continue
            
            # Extract links and add to queue
            links = self.extract_links(url)
            for link in links:
                if link not in self.visited_urls:
                    self.queue.append((link, depth + 1))
                    
            # Brief pause to be considerate to the server
            time.sleep(0.1)
    
    def save_results(self):
        """Save the discovered URLs to a file if specified"""
        if self.output_file:
            try:
                with open(self.output_file, 'w') as f:
                    for url in sorted(self.found_urls):
                        f.write(f"{url}\n")
                print(f"\nSaved {len(self.found_urls)} URLs to {self.output_file}")
            except Exception as e:
                print(f"Error saving results to file: {e}")
    
    def print_summary(self):
        """Print a summary of the crawl results"""
        print("\n" + "=" * 50)
        print(f"Crawl Summary:")
        print(f"Base URL: {self.base_url}")
        print(f"Maximum Depth: {self.max_depth}")
        print(f"Total URLs discovered: {len(self.found_urls)}")
        print(f"Total pages crawled: {len(self.visited_urls)}")
        print("=" * 50)


def main():
    """Parse arguments and run the crawler"""
    parser = argparse.ArgumentParser(description='Web Crawler - Crawl websites recursively')
    parser.add_argument('url', help='Starting URL to crawl')
    parser.add_argument('-d', '--depth', type=int, default=3, 
                        help='Maximum depth to crawl (default: 3)')
    parser.add_argument('-o', '--output', help='File to save discovered URLs')
    
    args = parser.parse_args()
    
    print(f"Starting web crawler at {args.url} with max depth {args.depth}")
    crawler = WebCrawler(args.url, args.depth, args.output)
    
    try:
        crawler.crawl()
        crawler.print_summary()
        crawler.save_results()
    except KeyboardInterrupt:
        print("\nCrawling interrupted by user.")
        crawler.print_summary()
        crawler.save_results()
        sys.exit(1)


if __name__ == '__main__':
    main()