import pandas as pd
import requests
from selenium import webdriver
import time
import os
import pickle
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def get_linkedin_pfp(profile_data):
    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com/login')

    email = ""  # Replace with your email
    password = ""  # Replace with your password

    wait = WebDriverWait(driver, 10)

    email_element = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    email_element.send_keys(email)

    password_element = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_element.send_keys(password)

    time.sleep(3)  # A small pause before hitting 'Enter' (just for example)
    password_element.send_keys(Keys.RETURN)
    time.sleep(5)

    for data in profile_data:
        profile_url, first, last, person_name, found, file_name = data

        try:
            driver.get(profile_url)

            all_image_urls = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
            )

            for img in all_image_urls:
                alt_text = img.get_attribute('alt')
                if first in alt_text and last in alt_text:
                    image_url = img.get_attribute('src')
                    response = requests.get(image_url)
                    directory = 'missing_images'
                    os.makedirs(directory, exist_ok=True)
                    filename = os.path.join(directory, file_name)
                    with open(filename, 'wb') as image_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            image_file.write(chunk)
                    print(f"Image downloaded and saved: {filename}")
                    break  # Break after finding the image
                else:
                    print(f"No profile picture found for {person_name}")
        except Exception as e:
            print(f"Error occurred for {person_name}: {e}")
        time.sleep(4)
    driver.quit()

data = pd.read_csv('p1-a.csv')
profile_data_list = []
for index, row in data.iterrows():
    profile_url = row['linkedinprofileurl']
    first = str(row['firstname'])
    last = str(row['lastname'])
    person_name = first + " " + last
    found = row['found']
    file_name = row['image_name_new']

    if found != "yes" and profile_url:
        profile_data_list.append([profile_url, first, last, person_name, found, file_name])

get_linkedin_pfp(profile_data_list)

data.to_csv('p1-a.csv', index=False)
