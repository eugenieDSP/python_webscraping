import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import random
import time

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

# define the folder to save the press releases
folder_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Dutch Political Parties PRs')

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
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
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
                filename = f'{order_number:03d}_{date_str}_{title[:50]}.txt'
                filename = filename.replace('/', '-')
                
                # create the year folder and move the file
                year_dir = os.path.join(party_dir, str(date.year))
                if not os.path.exists(year_dir):
                    os.makedirs(year_dir)
                filepath = os.path.join(year_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                order_number += 1
        
        # check if there are more pages
        next_link = soup.find('a', {'class': 'next'})
        if not next_link:
            break
        page += 1
        
        # add a random timeout between 5 and 30 seconds
        timeout = random.randint(5, 30)
        time.sleep(timeout)
