# To run this crawler, save the script as crawler.py and use the following command in the terminal:
# scrapy runspider crawler.py

# Author: Sabina Sokol
# Course: CS 4675
# Homework: 1.2

import scrapy
from bs4 import BeautifulSoup
import time
import csv
from threading import Thread
import matplotlib.pyplot as plt

class ComputingCrawler(scrapy.Spider):
    name = "computing_crawler"
    start_urls = ["https://cc.gatech.edu"]

    custom_settings = {
        'DOWNLOAD_DELAY': 1  # Politeness delay
    }

    total_pages_crawled = 0
    start_time = time.time()
    url_queue = set()
    stats = []  # To store crawl statistics

    def __init__(self):
        # Open CSV files for writing
        self.pages_file = open("crawled_pages_keywords.csv", "w", newline="", encoding="utf-8")
        self.stats_file = open("crawler_statistics.csv", "w", newline="", encoding="utf-8")

        # Initialize CSV writers
        self.pages_writer = csv.writer(self.pages_file)
        self.stats_writer = csv.writer(self.stats_file)

        # Write headers for both CSV files
        self.pages_writer.writerow(["URL", "Keywords", "Timestamp"])
        self.stats_writer.writerow(["Timestamp", "Pages Crawled", "Speed (pages/min)", "Crawled/Queued Ratio"])

        # Start the statistics logger in a separate thread
        Thread(target=self.log_statistics, daemon=True).start()

    def log_statistics(self):
        while True:
            time.sleep(60)  # Log every minute
            elapsed_minutes = (time.time() - self.start_time) / 60
            speed = self.total_pages_crawled / elapsed_minutes if elapsed_minutes > 0 else 0
            ratio = self.total_pages_crawled / (len(self.url_queue) + self.total_pages_crawled) if (len(self.url_queue) + self.total_pages_crawled) > 0 else 0
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Write statistics to CSV
            self.stats_writer.writerow([timestamp, self.total_pages_crawled, speed, ratio])

            # Save stats for plotting
            self.stats.append((self.total_pages_crawled, speed, ratio))

            print(f"[Statistics] Pages Crawled: {self.total_pages_crawled} | Speed: {speed:.2f} pages/min | Crawled/Queued Ratio: {ratio:.2f}")

    def parse(self, response):
        # Increment the page counter
        self.total_pages_crawled += 1

        # Extract visible text using BeautifulSoup
        soup = BeautifulSoup(response.body, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()

        # Split text into words and count keyword frequencies
        words = [word.lower() for word in text.split() if word.isalnum()]
        word_frequencies = {}
        for word in words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

        # Save URL and word frequencies to CSV
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.pages_writer.writerow([response.url, word_frequencies, timestamp])

        # Extract new links and add them to the crawl queue
        for link in response.css("a::attr(href)").getall():
            if link.startswith("/") or link.startswith("https://cc.gatech.edu"):
                absolute_url = response.urljoin(link)
                if absolute_url not in self.url_queue:
                    self.url_queue.add(absolute_url)
                    yield scrapy.Request(absolute_url, callback=self.parse)

        # Plot statistics after 2000 pages
        if self.total_pages_crawled == 2000:
            self.plot_statistics()

    def plot_statistics(self):
        pages, speeds, ratios = zip(*self.stats)

        plt.figure(figsize=(10, 5))

        # Plot crawl speed
        plt.subplot(1, 2, 1)
        plt.plot(pages, speeds, label="Crawl Speed (pages/min)")
        plt.xlabel("Pages Crawled")
        plt.ylabel("Pages/Minute")
        plt.title("Crawl Speed Over Time")
        plt.legend()

        # Plot crawl ratio
        plt.subplot(1, 2, 2)
        plt.plot(pages, ratios, label="Crawled/Queued Ratio")
        plt.xlabel("Pages Crawled")
        plt.ylabel("Crawled/Queued Ratio")
        plt.title("Crawled/Queued Ratio Over Time")
        plt.legend()

        plt.tight_layout()
        plt.savefig("crawl_statistics.png")
        plt.show()

    def closed(self, reason):
        # Close CSV files on spider close
        self.pages_file.close()
        self.stats_file.close()
