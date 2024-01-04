import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urlparse

# Function to get image URLs from HTML text using BeautifulSoup
def get_images_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img.get('src') for img in img_tags if img.get('src')]
    return img_urls

# Function to get image URLs from a URL
def get_images_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)
    if response.ok:
        return get_images_from_html(response.text)
    else:
        return []

def split_string_by_punctuation(text):
    words = re.split(r'[^\w\s_]', text)
    words = [word for word in words if word]
    return words

def is_match(url, firstname, lastname):
    url = split_string_by_punctuation(url)
    firstname_found = False
    lastname_found = False
    if "aresmgmt" in website_url:
        search = firstname[0].lower()+lastname.lower()
        for c in url:
            if search in c.lower(): return True
    else:
        for c in url:
            char = c.lower()
            if firstname.lower() in char: firstname_found = True
            if lastname.lower() in char: lastname_found = True
            
    return firstname_found and lastname_found

def download_img(all_image_urls, first, last, file_name):
    for img_url in all_image_urls:
        if is_match(img_url, first, last):
            try:
                # special cases
                if "www.nb.com" in website_url:
                    img_url = "https://www.nb.com/" + img_url
                if "dakotaventuregroup" in website_url:
                    img_url = "https://dakotaventuregroup.com" + img_url
                if "lonestarfunds" in website_url:
                    img_url = "https://www.lonestarfunds.com" + img_url
                if "mckinsey" in website_url:
                    img_url = "https://www.mckinsey.com" + img_url
                if "stifel" in website_url:
                    img_url = "https://www.stifel.com" + img_url
                if "hpspartners" in website_url:
                    img_url = "https://www.hpspartners.com" + img_url
                if "www.kkr.com" in website_url:
                    img_url = "https://www.kkr.com" + img_url
                if "aresmgmt" in website_url:
                    img_url = "https://www.aresmgmt.com" + img_url
                if "carlyle" in website_url:
                    img_url = "https://www.carlyle.com" + img_url
                if "concordeco" in website_url:
                    img_url = "https://www.concordeco.com" + img_url
                if "american-securities" in website_url:
                    img_url = "https://www.american-securities.com" + img_url
                if "centrepartners.com" in website_url:
                    img_url = "https://www.centrepartners.com" + img_url
                if "kelso" in website_url:
                    img_url = "https://www.kelso.com" + img_url
                if "gulfstargroup" in website_url:
                    img_url = "https:" + img_url
                if "thehalifaxgroup" in website_url:
                    img_url = "https://thehalifaxgroup.com" + img_url
                if "comvest" in website_url:
                    img_url = "https://comvest.com" + img_url
                if "ppmamerica" in website_url:
                    img_url = "https://www.ppmamerica.com" + img_url
                if "bbh" in website_url:
                    img_url = "https://www.bbh.com" + img_url
                if "atalayacap" in website_url:
                    img_url = "https://www.atalayacap.com" + img_url
                if "stockbridge" in website_url:
                    img_url = "https://www.stockbridge.com" + img_url
                if "midoceanpartners" in website_url:
                    img_url = "https://www.midoceanpartners.com" + img_url
                if "odeoncap" in website_url:
                    img_url = "https://www.odeoncap.com/" + img_url
                if "https://www.chertoffgroup.com" in website_url:
                    img_url = "https://www.chertoffgroup.com" + img_url
                if "https://rpcp.com/" in website_url:
                    img_url = "https://rpcp.com/" + img_url
                if "https://www.tcw.com" in website_url:
                    img_url = "https://www.tcw.com" + img_url
                if "fflpartners" in website_url:
                    img_url = "https://www.fflpartners.com/" + img_url
                if "jasperridge" in website_url:
                    img_url = "https://www.jasperridge.com" + img_url
                if "https://www.horsleybridge.com" in website_url:
                    img_url = "https://www.horsleybridge.com" + img_url
                if "https://www.cadentenergy.com/" in website_url:
                    img_url = "https://www.cadentenergy.com/" + img_url
                if "https://fmicorp.com" in website_url:
                    img_url = "https://fmicorp.com" + img_url
                if "https://www.crescentcap.com" in website_url:
                    img_url = "https:" + img_url
                if "https://ballentinepartners.com" in website_url:
                    img_url = "https://ballentinepartners.com" + img_url
                if "https://private-wealth.us.cibc.com" in website_url:
                    img_url = "https://private-wealth.us.cibc.com" + img_url
                if "https://www.swatequitypartners.com/" in website_url:
                    img_url = "https://www.swatequitypartners.com/" + img_url
                if "https://firstmanhattan.com/" in website_url:
                    img_url = "https://firstmanhattan.com" + img_url
                if "https://www.perceptivelife.com" in website_url:
                    img_url = "https://www.perceptivelife.com" + img_url
                if "http://www.p4gcap.com" in website_url:
                    img_url = "http://www.p4gcap.com" + img_url
                if "wisemontcapital" in website_url:
                    img_url = "https:" + img_url
                if "globalpartnerships" in website_url:
                    img_url = "https://globalpartnerships.org" + img_url
                if "newspringcapital" in website_url:
                    img_url = "https://newspringcapital.com" + img_url
                if "https://www.bhmsinvestments.com" in website_url:
                    img_url = "https://www.bhmsinvestments.com" + img_url
                if "manhattanwest" in website_url:
                    img_url = "https://manhattanwest.com" + img_url
                if "https://longrangecapital.com" in website_url:
                    img_url = "https://longrangecapital.com" + img_url
                if "https://www.galaxy.com" in website_url and img_url == "//images.ctfassets.net/f2k4wquz44by/45AocLSXe78Qv8JxbeEWkb/b84cd54bf757777e08ac4439d0e2695e/Steve_Kurz_Headshot.jpg?w=750&q=60&fm=jpg":
                    img_url = "https:" + img_url
                if "https://www.gaugecapital.com" in website_url:
                    img_url = "https://www.gaugecapital.com" + img_url
                if "https://burlingtoncapital.com" in website_url:
                    img_url = "https://burlingtoncapital.com" + img_url
                if "https://accelmed.com" in website_url:
                    img_url = "https://accelmed.com" + img_url
                if "https://www.tenexcm.com" in website_url:
                    img_url = "https://www.tenexcm.com" + img_url
                if "https://media.nmfn.com" in website_url:
                    img_url = "https://media.nmfn.com" + img_url
                if "https://www.teleocapital.com" in website_url:
                    img_url = "https://www.teleocapital.com/" + img_url
                if "https://www.greenmontcapital.com" in website_url:
                    img_url = "https://www.greenmontcapital.com/" + img_url
                if "https://umsocialventure.com" in website_url:
                    img_url = "https://umsocialventure.com" + img_url

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
                }

                session = requests.Session()
                session.headers.update(headers)
                response = session.get(img_url, stream=True)
                if response.ok:
                    filename = file_name 
                    directory = 'missing_images'
                    os.makedirs(directory, exist_ok=True)

                    with open(os.path.join(directory, filename), 'wb') as image_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            image_file.write(chunk)
                    print(f"Image downloaded and saved: {filename}")
                else:
                    print(f"Failed to download image from {img_url}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image from {img_url}: {e}")

data = pd.read_csv('p8.csv')
web_urls = {}

for index, row in data.iterrows():
    first = str(row['firstname'])
    last = str(row['lastname'])
    person_name = first + " " + last
    website_url = row['Website']
    file_name = row['image_name_new']

    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url

    try:
        all_image_urls = web_urls.get(website_url) 

        if all_image_urls is None:
            all_image_urls = get_images_from_url(website_url)
            web_urls[website_url] = all_image_urls
        if any(is_match(img_url, first, last) for img_url in all_image_urls):
            data.at[index, 'found'] = 'yes'
            print(f"Image found for {person_name} on {website_url}.")

            # Download and save the image
            download_img(all_image_urls, first, last, file_name)
 
        else:
            data.at[index, 'found'] = 'no'
            print(f"No image found for {person_name} on {website_url}.")

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {website_url}: {e}")
        data.at[index, 'found'] = 'error'

data.to_csv('p8.csv', index=False)
