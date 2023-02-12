#Script for scraping text off of a specfic website config, not general purpose
#saves to a text file

import time
import urllib.request
from bs4 import BeautifulSoup, Comment
import re
import random


toplevel = "http://*******URL REMOVED*********"
subfolder = "/************/"
mainurl = toplevel + subfolder

savefile = "data.txt"

# start and end words on page to scrape between
start = "************ "
end = "********"

delay = 2000 #microseconds

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

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)


all_links = getlinks(mainurl)

#open file to start writing data
f = open(savefile, "a")

#get data
for i in range(len(all_links)):
    url = all_links[i]

    html = urllib.request.urlopen(url).read()

    full_text = (text_from_html(html))

    result = ''.join((re.findall(f'{start}(.*?){end}', full_text))) + end

    f.writelines([("ENTRY: " + url + "\n"), (result + "\n") , "\n\n"])
    
    print("Wrote entry for: ", url)

    time.sleep(random.randint(500, delay)/1000) 

f.close()


