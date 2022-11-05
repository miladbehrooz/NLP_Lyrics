import requests
import re
import os
import time
import argparse
import numpy as np
from bs4 import BeautifulSoup



def make_lyrics_link(artist_name):
    """ Take name of the artis and return lyrics link as a list. """
    complete_url_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(f'https://www.azlyrics.com/{artist_name[0]}/{artist_name}.html',headers=headers)
    html_text = response.text
    pattern = '/lyrics/.+\.html'
    hyper_list = re.findall(pattern,html_text)
    
    prefix_url = 'https://www.azlyrics.com'

    for hyper_link in hyper_list:
        complete_url = prefix_url + hyper_link
        complete_url_list.append(complete_url)
    return complete_url_list

def save_lyrics(links,path):
    """ Take list of lyric links and path and save the lyrics in text files in folders which are named artis name. """
    for i , url in enumerate(links):
        #print(i,url)
        headers = {
                  'authority': 'scrapeme.live',
                  'dnt': '1',
                  'upgrade-insecure-requests': '1',
                  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'sec-fetch-site': 'none',
                  'sec-fetch-mode': 'navigate',
                  'sec-fetch-user': '?1',
                  'sec-fetch-dest': 'document',
                  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                  }
        t = np.random.randint(50)
        time.sleep(t)          
        response = requests.get(url,headers=headers)
        lyric_html = response.text 
        lyric_soup = BeautifulSoup(lyric_html,'html.parser')
        artist_name = lyric_soup.find('b').get_text()
        artist_name = artist_name.replace(' Lyrics','').replace(' ','_')
        
        song_name = lyric_soup.find_all('b')[1].get_text().replace(' ','_').replace('"','').lower()
        lyric_text = lyric_soup.find_all('div')[22].get_text()
        
        
        
        if not os.path.exists(f"{path}/{artist_name}"):
            os.mkdir(f"{path}/{artist_name}")
            
        if not os.path.exists(f"{path}/{artist_name}/{song_name}.txt"):
            file = open(file=f"{path}/{artist_name}/{song_name}.txt",mode='w')
            file.write(lyric_text)
            file.close()
            print(f'{song_name} from {artist_name} has been saved.')
        else:
            print(f'{song_name} from {artist_name} has already been saved.')

# Build parser with ArgumentParser: parse the command line
parser = argparse.ArgumentParser(description="""This script save the given artist lyrics in the given path """)

# Create arguments that the user can pass to the script
parser.add_argument("--artist", help="artist name ")
parser.add_argument("--path", help="path where you want to save the lyrics")

# map the user input values  with the possible arguments
arguments = parser.parse_args()

# extract the argument
path = arguments.path
artist_name = arguments.artist

print(f'Start to download {artist_name} lyrics in {path}/{artist_name} folder')

links = make_lyrics_link(artist_name)

# save lyrics into files
save_lyrics(links,path='../data/')
