#scrape script for BAT galleries
import requests
from bs4 import BeautifulSoup
import json
import os
import re

special_id = 'data-gallery-items' #this is the DIV identifier for the gallery data we want to scrape

# The URLs of the page you want to scrape (list)
urls = ['http://www.example12345667.com/page1','http://www.example12345667.com/page2','http://etc']

for url in urls:
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f'Failed to get content of the URL with status code: {response.status_code}')
    else:
        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title from the HTML
        title = soup.title.string

        # Sanitize the title by removing any character not allowed in file/directory names
        title_sanitized = re.sub(r'[\\/*?:"<>|]', "", title)

        # Try to find the div and extract the data-gallery-items attribute
        try:
            data_gallery_items = soup.find('div', attrs={special_id: True})[special_id]

            # Load the JSON data
            data = json.loads(data_gallery_items)

            # Create a directory with the title's text as its name if it does not exist
            if not os.path.exists(title_sanitized):
                os.makedirs(title_sanitized)

            # Loop over each item and save the large image to disk
            for idx, item in enumerate(data):
                img_url = item['large']['url']
                img_response = requests.get(img_url)
                    
                # Check if the request is successful
                if img_response.status_code == 200:
                    # Open file in write and binary mode
                    with open(f'{title_sanitized}/image_large_{idx}.jpg', 'wb') as file:
                        # Write the image content to the file
                        file.write(img_response.content)
                        print("WROTE FILE: ", file)
                else:
                    print(f'Failed to get image from URL {img_url} with status code: {img_response.status_code}')
        except KeyError:
            print("Could not find div with attribute ", special_id)


    print("FINISHED with ", url)

print("FINISHED OVERALL.")