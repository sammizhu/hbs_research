import requests
import csv
import pandas as pd

df = pd.read_csv('pitchbook_investmentfunds.csv')

# Filter unique values based on 'personid'
unique_ids = df.drop_duplicates(subset='personid')

# Create a list of dictionaries with required information
personal_names = []
for index, row in unique_ids.iterrows():
    name_info = {
        "id": row['personid'],
        "firstName": row['firstname'],
        "lastName": row['lastname'],
        "countryIso2": "US"
    }
    print(name_info)
    personal_names.append(name_info)

print(len(personal_names)) # for pitchbook the expected unique names should be 154,087 names

cont = input("Continue?")

if cont == "yes":
    url = "https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicityBatch"

    payload = {
        "personalNames": personal_names
    }

    headers = {
        "X-API-KEY": "",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    # Debug for why reponse is not working 
    if response.status_code == 200:
        try:
            data = response.json()['personalNames']
        except json.decoder.JSONDecodeError:
            print("Response is not in JSON format")
    else:
        print("Request failed with status code:", response.status_code)

    # Extract data from the response
    data = response.json()['personalNames']

    # Define headers for the CSV file based on the keys in the extracted data
    headers = [
        'id',
        'firstName',
        'lastName',
        'raceEthnicityAlt',
        'raceEthnicity',
        'score',
        'raceEthnicitiesTop',
        'probabilityCalibrated',
        'probabilityAltCalibrated'
    ]

    # Write extracted data to a new CSV file
    with open('extracted_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for entry in data:
            writer.writerow({
                'id': entry.get('id', ''),
                'firstName': entry.get('firstName', ''),
                'lastName': entry.get('lastName', ''),
                'raceEthnicityAlt': entry.get('raceEthnicityAlt', ''),
                'raceEthnicity': entry.get('raceEthnicity', ''),
                'score': entry.get('score', ''),
                'raceEthnicitiesTop': ','.join(entry.get('raceEthnicitiesTop', '')),
                'probabilityCalibrated': entry.get('probabilityCalibrated', ''),
                'probabilityAltCalibrated': entry.get('probabilityAltCalibrated', '')
            })

    print("Data has been written to extracted_data.csv")