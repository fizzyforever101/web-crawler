# To run this keyword analysis, use the following command in the terminal:
# python3 keyword_post_processing.py

# Author: Sabina Sokol
# Course: CS 4675
# Homework: 1.2

import csv
import ast
import nltk
from collections import Counter

# Make sure to download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords

# Define a function to analyze keywords from CSV file
def analyze_keywords(csv_file):
    top_keywords = Counter()  # Use Counter to automatically count frequency

    # Define a set of stop words
    stop_words = set(stopwords.words('english'))

    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Safely evaluate the string representation of a dictionary
            keywords = ast.literal_eval(row['Keywords'])

            for key, value in keywords.items():
                # Tokenize the keyword and perform part-of-speech tagging
                tokens = word_tokenize(key)
                tagged_tokens = pos_tag(tokens)

                # Filter out stopwords and focus on nouns (singular/plural/proper nouns)
                for word, tag in tagged_tokens:
                    if tag in ['NN', 'NNS', 'NNP', 'NNPS'] and word.lower() not in stop_words:
                        top_keywords[word.lower()] += value

    # Get top 10 most common keywords
    top_10_keywords = top_keywords.most_common(10)

    return top_10_keywords

CSV_FILE = 'crawled_pages_keywords.csv'
top_10_keywords = analyze_keywords(CSV_FILE)

# Print top 10 keywords
print(f"Top Keywords: {top_10_keywords}")

