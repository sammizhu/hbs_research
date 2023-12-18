import pandas as pd
import some_cleaning_functions as clean
from fuzzywuzzy import fuzz
import csv
import json

# GOAL: get cik, entityname, and personID 
# cik comes from formd
# entityname comes from formd
# personid comes from pitchbook

# for each match in entityname_fundname (merge that we did last time)
    # find list of first and last name based on cik and entityname
    # see if there is a match on the first and last name
    # if so append the data

def getnames(file, matchon, nameAsKey=False):
    names = {}
    with open(file, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            match = row[matchon]
            first_name = row['firstname']
            last_name = row['lastname']
            
            name = str(first_name) + " " + str(last_name)

            if nameAsKey:
                if name in names:
                    names[name].append(match)
                else:
                    names[name] = [match]
            else:
                if match in names and name not in names[match]:
                    names[match].append(name)
                else:
                    names[match] = [name]
    return names

# every CIK and its FIRST AND LAST NAME 
cik_names = getnames("formd_investmentfunds.csv", "cik")
fundname_names = getnames("pitchbook_investmentfunds.csv", "fundid")
personid_names = getnames("pitchbook_investmentfunds.csv", "personid", True)

# [print(x) for x in personid_names.items()]

data = []
with open("csv/entityname_fundname.csv", mode='r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        cik = row["cik"].strip()
        entityname = row["entityname"].strip()
        fundid = row["fundid"].strip()
        
        formd_names = cik_names[cik]
        pitchbook_names = fundname_names[fundid]

        for x in formd_names:
            for y in pitchbook_names:
                if fuzz.ratio(x,y) >= 80:
                    personid = personid_names[y][0]
                    entry = [cik, entityname, personid]
                    data.append(entry)


# # WRITE DATA TO FILE
columns = ["cik", "entityname", "personid"]
file_path = 'lastname_match.csv'
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(data)