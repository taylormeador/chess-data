import requests
import logging
import sys
import shutil
import os

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
logger = logging.getLogger()

# lichess provides a txt file that has all the download links
response = requests.get('https://database.lichess.org/standard/list.txt')
if response.status_code != 200:
    logger.error('Error getting download links. Exiting...')
    sys.exit()
else:
    logger.info('Retrieved download links')

# extract links and loop through each, downloading the file if it doesn't already exist locally
links = response.text.split('\n')
for link in links:
    file_name = link.split('/')[4]
    if os.path.isfile('./lichess_pgn/' + file_name):
        logger.info('File already exists, trying next link...')
        continue
    with requests.get(link, stream=True) as r:
        with open('./lichess_pgn/' + file_name, 'wb') as f:
            logger.info('Downloading ' + file_name)
            shutil.copyfileobj(r.raw, f)
