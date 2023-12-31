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
    # Set a custom user-agent to mimic a browser (e.g., Chrome)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    # Create a session to handle cookies across requests
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)
    if response.ok:
        return get_images_from_html(response.text)
    else:
        return []

def split_string_by_punctuation(text):
    # Split the string based on punctuation characters using regular expressions
    words = re.split(r'[^\w\s_]', text)
    words = [word for word in words if word]  # Remove empty strings from the result
    return words

def is_match(url, firstname, lastname):
    url = split_string_by_punctuation(url)
    firstname_found = False
    lastname_found = False
    for c in url:
        char = c.lower()
        if firstname.lower() in char: firstname_found = True
        if lastname.lower() in char: lastname_found = True
            
    return firstname_found and lastname_found

# Read the CSV file
data = pd.read_csv('missingimages_12_27_2023.csv')
web_urls = {}

for index, row in data.iterrows():
    first = str(row['firstname'])
    last = str(row['lastname'])
    person_name = first + " " + last
    website_url = row['Website']
    file_name = row['image_name_new']

    # Check if the URL contains a scheme, if not, prepend "https://"
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url

    try:
        # Get images URLs from the website URL
        all_image_urls = web_urls.get(website_url) 

        # Check if the image URL for the person matches the defined criteria
        if all_image_urls is None:
            all_image_urls = get_images_from_url(website_url)
            web_urls[website_url] = all_image_urls

        # Check if the image URL for the person matches the defined criteria
        if any(is_match(img_url, first, last) for img_url in all_image_urls):
            data.at[index, 'found'] = 'yes'
            print(f"Image found for {person_name} on {website_url}.")
        else:
            data.at[index, 'found'] = 'no'
            print(f"No image found for {person_name} on {website_url}.")

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {website_url}: {e}")
        data.at[index, 'found'] = 'error'

# Save the updated DataFrame back to the CSV file
data.to_csv('missingimages_12_27_2023.csv', index=False)
