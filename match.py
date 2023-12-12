import pandas as pd
import some_cleaning_functions as clean
from fuzzywuzzy import fuzz
import csv
import json

def fuzzy_check(target, arr, threshold):
    for y in arr:
        if fuzz.ratio(str(target), str(y)) >= threshold:
            return [target,y]
    return None

def fuzzy_check_lastnames(arr1, arr2, threshold):
    for x in arr1:
        for y in arr2:
            if fuzz.ratio(str(x), str(y)) >= threshold:
                return True
    return False

pitchbook = pd.read_csv('pitchbook_investmentfunds.csv')
formd = pd.read_csv('formd_investmentfunds.csv')

# FUNDNAME - LASTNAME Dictionary
pitchbook_lastnames = dict(pitchbook.groupby('fundname')['lastname'].agg(list))

# CLEAN ENTITYNAME - LASTNAME Dictionary
formd_lastnames = dict(formd.groupby('entityname')['lastname'].agg(list))
clean_entityname_lastname = {clean.clean_up_company_names(str(k)): v for k, v in formd_lastnames.items()}

# CLEAN ENTITYNAME - ENTITYNAME
clean_entityname = {}
for k in formd["entityname"].unique():
    cleaned_name = clean.clean_up_company_names(str(k))
    clean_entityname[cleaned_name] = k

# CLEAN FUNDNAME - FUNDID
pitchbook_fundid = dict(pitchbook.groupby('fundname')['fundid'].unique())  # this is assuming that each fundname has a unique fundid
clean_fundname_fundid = {clean.clean_up_company_names(str(k)): v for k, v in pitchbook_fundid.items()}

# CLEAN ENTITYNAME - CIK
formd_cik = dict(formd.groupby('entityname')['cik'].unique()) # likewise assumption
clean_entityname_cik = {clean.clean_up_company_names(str(k)): v for k, v in formd_cik.items()}

""" 
Given unique rows in pitchbook.csv grouped by fundname, 
    1) clean the fundname to try and find direct clean entityname match
    2) otherwise, try to implement a fuzzy match on between entityname and fundname
In both cases if a match condition is met, perform the following:
    a) if there exists a match, perform a fuzzy check on the lastnames across the associated fundname and entityname
    b) if the threshold for fuzzy match on lastnames is met, retrieve [fundname, fundid, entityname, cik]
"""
data = []
for key_p, item_p in pitchbook_lastnames.items():
    key_p_clean = clean.clean_up_company_names(key_p) 
    # DIRECT MATCHING
    if key_p_clean in clean_entityname_lastname.keys(): 
        item_f = clean_entityname_lastname.get(key_p_clean)
        if fuzzy_check_lastnames(item_p, item_f, 90): 
            entry = [key_p, clean_fundname_fundid[str(key_p_clean)][0], clean_entityname[str(key_p_clean)], clean_entityname_cik[str(key_p_clean)][0]]
            data.append(entry)
    else: # FUZZY MATCHING
        check = fuzzy_check(key_p_clean, clean_entityname_lastname.keys(), 90)
        if check:
            p, f = check[0], check[1]
            if fuzzy_check_lastnames(item_p, clean_entityname_lastname[f], 90):
                entry = [key_p, clean_fundname_fundid[str(p)][0], clean_entityname[str(f)], clean_entityname_cik[str(f)][0]]
                data.append(entry)

# WRITE DATA TO FILE
columns = ['fundname', 'fundid', 'entityname', 'cik']
file_path = 'match.csv'
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(data)