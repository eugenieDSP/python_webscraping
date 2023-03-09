import os
import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# define the parties and their websites
parties = {
    'VVD': 'https://www.vvd.nl/nieuws/',
    'CDA': 'https://www.cda.nl/nieuws/',
    'PVV': 'https://www.pvv.nl/nieuws/',
    'D66': 'https://d66.nl/nieuws/',
    'SP': 'https://www.sp.nl/nieuws/',
    'GL': 'https://groenlinks.nl/nieuws',
    'PvdA': 'https://www.pvda.nl/nieuws/',
    'CU': 'https://www.christenunie.nl/nieuws',
    'PvdD': 'https://www.partijvoordedieren.nl/nieuws/',
    '50PLUS': 'https://50pluspartij.nl/nieuws/',
    'SGP': 'https://www.sgp.nl/actueel/nieuws',
    'FvD': 'https://www.fvd.nl/nieuws'
}

# define the date range
start_date = datetime(2011, 6, 1)
end_date = datetime.now()

# define the folder to save the articles
folder_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Dutch Political Parties Articles')

# define the web driver options
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
options.add_argument('disable-gpu')
options.add_argument('no-sandbox')
options.add_argument('disable-dev-shm-usage')

# start the web driver
driver = webdriver.Chrome(options=options)

# loop through the parties and their websites
for party, website in parties.items():
    order_number = 1
    party_dir = os.path.join(folder_path, party)
    if not os.path.exists(party_dir):
        os.makedirs(party_dir)
    
    # loop through the pages of the website
    page = 1
    while True:
        url = f'{website}?page={page}'
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # loop through the articles on the page
        for article in soup.find_all('article'):
            # extract the title, date and content of the article
            title = article.find('h3').text.strip()
            try:
                date_str = article.find('time')['datetime'][:10]
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                continue
            content = article.find('div', {'class': 'content'}).text.strip()
            
            # filter articles by date
            if start_date <= date <= end_date:
                # create the filename
                filename = f'{order_number:03d}_{party}_{date_str}.txt'
                
                # create the year folder and move the file
                year_dir = os.path.join(party_dir, str(date.year))
                if not os.path.exists(year_dir):
                    os.makedirs(year_dir)
                filepath = os.path.join(year_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f'{title}\n\n{content}')
                
                # increment the order number
                order_number += 1
            
            # check if the article is outside the date range
            elif date < start_date:
                break
        
        # check if there are no more pages
        if soup.find('a', {'class': 'next-page'}) is None:
            break
        
        # increment the page number and wait for a random time
        page += 1
        time.sleep(random.randint(5, 30))
    
    # sort the files in the "party" subfolder by year
    for year_dir in os.listdir(party_dir):
        if not year_dir.isdigit():
            continue
        year_path = os.path.join(party_dir, year_dir)
        if not os.path.isdir(year_path):
            continue
        for filename in os.listdir(year_path):
            filepath = os.path.join(year_path, filename)
            if not os.path.isfile(filepath):
                continue
            new_filename = f'{filename.split("_")[1]}_{filename.split("_")[2]}_{filename.split("_")[3]}'
            new_filepath = os.path.join(year_path, new_filename)
            os.rename(filepath, new_filepath)
    
# close the web driver
driver.quit()


