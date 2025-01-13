# Focused Web Crawler with Keyword Analysis and Statistics Plots

## Overview
This project is a focused web crawler that extracts and analyzes the most frequently used keywords from pages within the `cc.gatech.edu` domain. It uses Scrapy for crawling, BeautifulSoup for text extraction, and Python's `collections.Counter` for keyword frequency analysis. The results are stored in a CSV file for post-crawl analysis. Crawler statistics such as crawl speed and crawl ratio are captured and displayed with `matplotlib` 

---

## Technologies Used
- **Python**: The main programming language.
- **Scrapy**: A powerful web crawling framework.
- **BeautifulSoup**: For extracting visible text from HTML.
- **collections.Counter**: For counting keyword frequencies.
- **CSV Module**: For storing crawled data in a CSV file.
- **Matplotlib**: For plotting crawler statistics.

---

## Installation
### Prerequisites
Ensure the following are installed on your system:
1. **Python (>=3.8)**
2. **pip** (Python package manager)

### Install Dependencies
Run the following command to install the required Python libraries:
```bash
pip3 install scrapy beautifulsoup4 matplotlib
```

---

## Project Structure
- **`crawler.py`**: The main script containing the web crawler implementation.
- **`crawled_pages_keywords.csv`**: The output CSV file that stores crawled URLs and their keyword frequencies.
- **`analyze_keywords.py`**: A script for performing post-crawl keyword analysis.

---

## How to Run

### Step 1: Initialize the Environment
Ensure you have Python installed and dependencies installed as per the "Installation" section.

### Step 2: Run the Web Crawler
Execute the crawler script to start crawling the `cc.gatech.edu` domain:
```bash
python3 -m scrapy runspider crawler.py
```
The script will:
1. Crawl pages under `https://cc.gatech.edu`.
2. Extract visible text from each page.
3. Calculate the frequency of each word.
4. Save the URL and keyword frequencies to `crawled_pages_keywords.csv`.

### Step 3: Analyze the Keywords
Once the crawl is complete, run the analysis script to determine the most frequent keywords:
```bash
python3 analyze_keywords.py
```
The script will:
1. Read the `crawled_pages_keywords.csv` file.
2. Aggregate keyword frequencies across all pages.
3. Display the top 10 most common keywords.

---

## Gathering Crawl Statistics
To monitor the performance and progress of the crawler during runtime, the following statistics are tracked and logged:
1. **Crawl Speed**: Number of pages crawled per minute.
2. **Crawl Ratio**: Ratio of URLs crawled to URLs queued.

### Implementation
The `crawler.py` script includes logging functionality to track these statistics. Key updates:
- **Start Time**: Recorded at the start of the crawl.
- **Page Count**: Incremented for each successfully crawled page.
- **Logging**: Logs the total pages crawled, pages per minute, and URL ratio every minute.

Example of running output:
![image](https://github.com/user-attachments/assets/8cd59eff-d6bc-4b53-8ab3-240685d1d048)


Example of logging output:
```plaintext
[2025-01-13 12:10:00] Pages Crawled: 50 | Speed: 10 pages/min | Crawled/Queued: 50/100
[2025-01-13 12:11:00] Pages Crawled: 60 | Speed: 10 pages/min | Crawled/Queued: 60/90
```
## Example Output
### Crawled Pages (CSV File)
`crawled_pages_keywords.csv`:
```csv
URL,Keywords,Timestamp
https://cc.gatech.edu,"computing:20;science:15;research:10",2025-01-13 12:00:00
https://cc.gatech.edu/research,"ai:25;data:20;learning:15",2025-01-13 12:05:00
```

### Keyword Analysis Output
```bash
Top Keywords: [('ai', 25), ('computing', 20), ('data', 20), ('science', 15), ('research', 10), ('learning', 15)]
```

---

## Notes
- **Politeness Policy**: The crawler respects polite crawling practices with a delay between requests (`DOWNLOAD_DELAY=1`).
- **Restartable**: Previously crawled URLs are skipped by checking the `crawled_pages_keywords.csv` file.
- **Extensible**: The keyword extraction and analysis logic can be modified to include more sophisticated techniques, such as stemming or stopword removal.

---

## Lessons Learned
1. **Scalability**: Storing data in CSV is sufficient for small-scale projects but may require a database for larger crawls.
2. **Keyword Filtering**: More advanced techniques (e.g., NLP) could improve the quality of keyword extraction.
3. **Performance**: Crawling speed is influenced by server response times and the size of pages. In addition,tThe `DOWNLOAD_DELAY` setting introduces a 1-second pause between requests, which can be reduced for faster crawling, while still respecting server limits. Maintaining a custom `url_queue` for deduplication slows down the process, as Scrapy already handles URL uniqueness. Writing to CSV on every page crawl introduces I/O overhead, which can be improved by batching writes. The use of BeautifulSoup for parsing adds extra processing time, and switching to Scrapy's native selectors would speed things up. Additionally, the separate thread for logging statistics and the plotting after 2000 pages can introduce delays, and optimizing or removing these could improve performance. Adjusting these factors will likely lead to a significant increase in crawl speed.
