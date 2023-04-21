# Image scraping script for a specifc website config; not general purpose

import time
import os
import requests 
import urllib.request
from bs4 import BeautifulSoup
import re
import random


toplevel = "http://www.google.com". #top level domain to scrape
subfolder = ""  #empty, subfolder can go here
mainurl = toplevel + subfolder

magicword = "" #empty, magic word to sort for goes here

delay = 500 #microseconds delay for rate limiter

def getlinks(url_in): 
    links_scraped = []
    parser = 'html.parser'  
    resp = urllib.request.urlopen(url_in)
    soup = BeautifulSoup(resp, parser, 
        from_encoding=resp.info().get_param('charset'))

    for link in soup.find_all('a', href=True):
        # get links that are children of main url only:
        if re.search(mainurl, link['href']): 
            links_scraped.append(link['href'])
    return links_scraped

def getdata(url): 
    r = requests.get(url) 
    return r.text 

def getimageurls(url):
    img_list = []
    htmldata = getdata(url) 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    for item in soup.find_all('img'):
        img_list.append(item['src'])
    return img_list

def savedata(url):
    response = requests.get(url)
    filename = os.path.basename(url)
    with open(filename, "wb") as f:
        f.write(response.content)

all_links = getlinks(mainurl)
cached_links = []

for i in range(len(all_links)):
    images_on_page = getimageurls(all_links[i])

    for item in images_on_page:
        if re.search(magicword, item):
            
            full_link = (toplevel + item)
            if full_link not in cached_links:
                cached_links.append(full_link)
                savedata(full_link)
                print("Saved: ", full_link)

    #small randomized delay to keep from getting IP flagged / rate limited
    time.sleep(random.randint(160, delay)/1000) 

print("FINISHED.")
