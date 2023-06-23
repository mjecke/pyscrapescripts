#Script downloads images named sequentially between start_number and stop_number
#with numbers inserted between url_base and urL_end

import requests
import os
import shutil
import time


#-------------------------------------------------------------------------------

url_base = "https://www.blahblahblahblahb.blahcom/images/img-" #url to target

url_end = ".jpg" #files will all end in the same extension

start_number = 1
stop_number = 200

save_directory = './saved/'

#-------------------------------------------------------------------------------

def download_image(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Get the response from the URL
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the filename from the URL
        filename = os.path.join(folder, url.split("/")[-1])

        # Open the output file and save the image into it
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            print("Saved: ", filename)

    else:
        print('Unable to download image:', url)


for i in range (start_number,stop_number+1):

    image_url = url_base+str(i)+url_end
    download_image(image_url, save_directory)

    #time.sleep(0.1) #optional delay

