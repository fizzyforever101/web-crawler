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
- **Natural Language Toolkit**: For identifying stopwords and word classification for the post-processing keyword analysis.

---

## Installation
### Prerequisites
Ensure the following are installed on your system:
1. **Python (>=3.8)**
2. **pip** (Python package manager)

### Install Dependencies
Run the following command to install the required Python libraries:
```bash
pip3 install scrapy beautifulsoup4 matplotlib nltk
```

---

## Project Structure
- **`crawler.py`**: The main script containing the web crawler implementation.
- **`crawled_pages_keywords.csv`**: The output CSV file that stores crawled URLs and their keyword frequencies.
- **`keyword_post_processing.py`**: A script for performing post-crawl keyword analysis.

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
python3 keyword_post_processing.py
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

## Example Output
### General Scrapy (Open Source Crawler Used) Statistics
![image](https://github.com/user-attachments/assets/a0b882bb-e51c-47da-b4a1-877f35a4dd2c)

### Crawled Pages (CSV File)
`crawled_pages_keywords.csv`:
![image](https://github.com/user-attachments/assets/9cfe1f0c-c7a0-42d5-b710-f578305efa25)

### Crawl Ratio and Crawl Speed Plots (2000 Pages)
![image](https://github.com/user-attachments/assets/de78a21c-b8c5-4e8e-a0b7-1d7db2d3dce9)

### Keyword Analysis Output
![image](https://github.com/user-attachments/assets/0235a5e2-9a0b-4ad3-9784-7a24d175e0d5)

---

## Results and Lessons Learned
1. **Process**: After conducting thorough research on Scrapy and existing open-source web crawlers, I began my project by exploring efficient ways to store and process the crawled data. Initially, I considered using an SQLite database, but after evaluating the requirements and complexity, I opted for CSV files as a simpler, more practical solution. As I progressed, I encountered an issue with my initial keyword analysis, where basic word counts resulted in common, uninformative words like "your" and "the." To address this, I implemented basic natural language processing (NLP) techniques to filter out stopwords and focus on more meaningful keywords. This approach significantly improved the relevance of my analysis and allowed me to better capture the essential terms from the crawled pages.
2. **Conclusions Based on Plots**: The crawl speed over time graph was linear and increasing due to several factors. Initially, there may be more setup overhead, like connection handling or parsing delays, but as the crawl progresses, these reduce, allowing for faster processing. Additionally, caching, network optimizations (e.g., persistent connections), and better resource management can lead to increased efficiency. Over time, the crawler may encounter fewer bottlenecks, and websites might respond more quickly. Moreover, as the crawler adapts to the site's structure and handles requests more effectively, it can reduce time between requests, resulting in an overall increase in crawl speed. The crawled/queued ratio being linear and decreasing suggests that the crawler is efficiently processing the queued pages at a steady rate. As the crawl progresses, the queue may become smaller, meaning there are fewer pages left to process, and the crawler is clearing them at a consistent pace. This could be a result of the crawler initially encountering a larger pool of pages to process, and as more pages are crawled and removed from the queue, the ratio naturally decreases. Additionally, it could indicate that the crawler is handling the requests in a predictable manner, with each queued page getting processed efficiently without delays. The ratio's decrease over time might reflect fewer remaining tasks, indicating progress toward completing the crawl. Based on the plots and average crawl speed (calculated by dividing total pages/total time as shown on the Scrapy statistics), it would take approximately 11,092 minute (or about 7.7 days) to crawl 10 million pages and 1,109,234 minutes (or about 2.1 years) to crawl 1 billion pages. 
3. **Keyword Filtering**: The current keyword analysis method tends to identify broad, general words that may not be meaningful in the context of the dataset. By focusing only on nouns and filtering out stopwords, it overlooks the subtleties and more specific terms that could provide valuable insights. This results in common terms like "the," "and," or "data," which appear frequently but don't contribute to a deeper understanding of the content. The analysis also doesn't account for multi-word phrases or domain-specific terms that may be more relevant. To improve the analysis, incorporating more sophisticated techniques like keyword extraction algorithms or utilizing contextual word embeddings could help identify more specific and meaningful keywords. Additionally, considering word collocations and domain-specific language would allow for a richer, more accurate analysis, capturing the true essence of the content.
4. **Performance**: Crawling speed is influenced by server response times and the size of pages. In addition, the `DOWNLOAD_DELAY` setting introduces a 1-second pause between requests, which can be reduced for faster crawling, while still respecting server limits. Maintaining a custom `url_queue` for deduplication slows down the process, as Scrapy already handles URL uniqueness. Writing to CSV on every page crawl introduces I/O overhead, which can be improved by batching writes. The use of BeautifulSoup for parsing adds extra processing time, and switching to Scrapy's native selectors would speed things up. Additionally, the separate thread for logging statistics and the plotting after 2000 pages can introduce delays, and optimizing or removing these could improve performance. Adjusting these factors will likely lead to a significant increase in crawl speed.
