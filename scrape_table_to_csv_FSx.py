# Table scraping script for a specifc website; not general purpose

import time
import requests 
import urllib.request
from bs4 import BeautifulSoup
import re
import random
import pandas as pd

toplevel = "http://*******URL*REMOVED*********"
subfolder = "/************/"
mainurl = toplevel + subfolder

magicword = "**key**" #keyword in links to validate 

delay = 860 #microseconds

def getlinks(url_in): #get all links off page that have the magic word
    links_scraped = []
    parser = 'html.parser'  
    resp = urllib.request.urlopen(url_in)
    soup = BeautifulSoup(resp, parser, 
        from_encoding=resp.info().get_param('charset'))

    for link in soup.find_all('a', href=True):
        # get links that are children of main url only:
        if re.search(toplevel, link['href']): 
            links_scraped.append(link['href'])

    links_ret = []
    for _ in links_scraped:
         if re.search(magicword, _): 

            links_ret.append(_)
    return links_ret

def save_table_to_csv(url): #saves table on page to csv

    html = requests.get(url).content
    df_list = pd.read_html(html)
    

    df = df_list[-1]
    
    subname = re.search(r"/([^/]*)/[^/]*$", url).group(1)
    filename = subname + ".csv"
    df.to_csv(filename, index=None, header=False)

    print("Saved table: ", subname)


all_links = getlinks(mainurl)

for link in all_links:
    save_table_to_csv(link)

    #uncomment if needed to do a bit of random rate limit:
    #time.sleep(random.randint(160, delay)/1000) 

print("FINISHED.")