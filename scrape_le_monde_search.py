#!/usr/bin/env python
# coding: utf-8

from newspaper import Article
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import glob
import requests

# Create an empty list to store article data
corpus = []

# Initialize a list to store URLs of rejected premium articles
rejected_urls = []

# Specify the path to the CSV file containing the URLs
csv_file_path = 'C:\\Users\\eugen\\Documents\\le_monde_urls.csv'

# Specify the directory to save the files
save_directory = 'C:\\Users\\eugen\\corpus_article_debt\\raw files\\raw files le monde'

# Check if the directory exists, if not, create it
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Initialize a counter for filenames
file_counter = 1

# Load the CSV file with URLs
df = pd.read_csv(csv_file_path)

# Iterate through the URLs in the second column
import requests

# Set a timeout value in seconds
timeout_seconds = 5  # Adjust this value as needed

for url in df['URL']:
    try:
        # Create an Article object
        article = Article(url)

        # Download the article with a timeout
        print(f"Downloading article from URL: {url}")
        response = requests.get(url, timeout=timeout_seconds)

        # Check the HTTP status code to ensure the request was successful
        if response.status_code == 200:
            article.set_html(response.text)

            # Parse the article's content and metadata
            print(f"Parsing article from URL: {url}")
            article.parse()

            # Check if the article contains the premium content indicator in the HTML
            premium_indicator = article.html.find('<p class="article__status article__status--opinion">')
            if premium_indicator == -1:
                # Article is not premium
                # Access the article's text and metadata
                article_title = article.title
                article_authors = article.authors
                article_publish_date = article.publish_date
                article_text = article.text

                # Format the publish date as YYYYMMDD
                formatted_date = article_publish_date.strftime("%Y%m%d")

                # Define the file name with date
                file_name = f"{formatted_date}_{str(file_counter).zfill(3)}.txt"
                full_file_path = os.path.join(save_directory, file_name)

                # Save the article as a text file with UTF-8 encoding
                print(f"Saving article to file: {full_file_path}")
                with open(full_file_path, "w", encoding="utf-8") as text_file:
                    text_file.write(article_text)

                # Append the article data to the corpus as a dictionary
                article_data = {
                    'Title': article_title,
                    'Authors': article_authors,
                    'Publish Date': article_publish_date,
                    'Text': article_text
                }
                corpus.append(article_data)

                # Increment the counter
                file_counter += 1

            else:
                print("Skipping premium article:", url)
                # Append the URL of the rejected premium article to the rejected_urls list
                rejected_urls.append(url)

            # Add a random pause between 2 and 5 seconds
            pause_time = random.uniform(2, 5)
            print(f"Pausing for {pause_time:.2f} seconds before the next article...")
            time.sleep(pause_time)

        else:
            print(f"Failed to download article from URL: {url}. Status code: {response.status_code}")

    except Exception as e:
        # Handle any errors that may occur during processing
        print("Error processing URL:", url)
        print(e)

# Initialize df for rejectes URLs
rejected_urls = []

# Set a timeout value in seconds
timeout_seconds = 5

for url in df['URL']:
    try:
        print(f"Checking URL: {url}")
        response = requests.get(url, timeout=timeout_seconds)

        if response.status_code == 200:
            html_content = response.text

            # Check if the article contains the premium content indicator in the HTML
            premium_indicator = '<p class="article__status article__status--opinion">'
            if premium_indicator in html_content:
                print("Premium article found:", url)
                rejected_urls.append(url)

        else:
            print(f"Failed to access URL: {url}. Status code: {response.status_code}")

    except Exception as e:
        print("Error processing URL:", url)
        print(e)


# Create a DataFrame from the list of rejected URLs
rejected_df = pd.DataFrame(rejected_urls, columns=['Rejected URLs'])

# Define the path for saving the Excel file
excel_file_path = 'rejected_urls.xlsx'

# Save the DataFrame as an Excel file
rejected_df.to_excel(excel_file_path, index=False)

print(f"Rejected URLs saved to Excel file: {excel_file_path}")
