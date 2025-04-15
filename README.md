# Web Crawler

A Python CLI-based web crawler that extracts and navigates links from web pages recursively.

## Features

- Takes a target URL as input (starting point)
- Accepts a depth level parameter to control how deep to crawl from the starting page
- Uses requests and BeautifulSoup to extract all `<a href>` links
- Recursively visits the links up to the defined depth
- Normalizes relative and absolute URLs
- Ignores external domains (crawls only within the same domain)
- Can save all discovered URLs to a file
- Avoids crawling the same URL twice by tracking visited URLs
- Clean CLI output with progress information and summary

## Requirements

- Python 3.6+
- Required packages:
  - requests
  - beautifulsoup4

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd Web-Crawler
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Basic usage:
```
./web_crawler.py https://example.com
```

Advanced usage:
```
./web_crawler.py https://example.com -d 2 -o results.txt
```

### Command-line Arguments

- `url`: The starting URL to crawl (required)
- `-d, --depth`: Maximum depth to crawl (default: 3)
- `-o, --output`: File to save discovered URLs (optional)

## Example

```
$ ./web_crawler.py https://example.com -d 2 -o results.txt
Starting web crawler at https://example.com with max depth 2
[Depth 0] Crawling: https://example.com
[Depth 1] Crawling: https://example.com/about
[Depth 1] Crawling: https://example.com/contact
[Depth 2] Crawling: https://example.com/about/team
[Depth 2] Crawling: https://example.com/about/history
[Depth 2] Crawling: https://example.com/contact/locations
...

==================================================
Crawl Summary:
Base URL: https://example.com
Maximum Depth: 2
Total URLs discovered: 35
Total pages crawled: 12
==================================================

Saved 35 URLs to results.txt
```

## Limitations

- The crawler implements a simple rate limiting (0.1-second delay between requests)
- Only follows links within the same domain as the starting URL
- May not handle all edge cases with URL formats

## License

MIT

## Last Updated

April 15, 2025