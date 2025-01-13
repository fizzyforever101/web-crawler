# To run this keyword analysis, edit "CSV_FILE" and use the following command in the terminal:
# python analyze_keywords.py

# Author: Sabina Sokol
# Course: CS 4675
# Homework: 1.2

import csv
from collections import Counter
CSV_FILE = 'crawled_pages_keywords.csv'

def analyze_keywords(csv_file):
    total_keywords = Counter()
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Keywords']:
                # Parse the keyword counts
                keywords = dict(kv.split(':') for kv in row['Keywords'].split(';'))
                total_keywords.update({k: int(v) for k, v in keywords.items()})
    return total_keywords.most_common(10)  # Top 10 keywords

top_keywords = analyze_keywords(CSV_FILE)
print("Top Keywords:", top_keywords)
