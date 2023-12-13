import pandas as pd
import some_cleaning_functions as clean
from fuzzywuzzy import fuzz
import csv
import json

def fuzzy_check(target, arr, threshold, check):
    for y in arr:
        if fuzz.ratio(str(target), str(y)) >= threshold and clean_entityname[str(y)] not in check:
            return [target,y]
    return None

def fuzzy_check_lastnames(arr1, arr2, threshold):
    lastnames = []
    for x in arr1:
        for y in arr2:
            if fuzz.ratio(str(x), str(y)) >= threshold:
                lastnames.append(x)
    if len(lastnames) > 0: return lastnames
    else: return []

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


lastname_fundid_personid = {}
with open('pitchbook_investmentfunds.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        key = row['lastname']
        value = [row['fundid'], row['personid']]
        if key not in lastname_fundid_personid:
            lastname_fundid_personid[key] = [value]
        else:
            lastname_fundid_personid[key].append(value)

data = []
matched_entitynames = set()
unmatched = {}

for key_p, item_p in pitchbook_lastnames.items():
    key_p_clean = clean.clean_up_company_names(key_p) 
    # DIRECT MATCHING
    if key_p_clean in clean_entityname_lastname.keys(): 
        item_f = clean_entityname_lastname.get(key_p_clean)
        lastnames = fuzzy_check_lastnames(item_p, item_f, 90)
        if len(lastnames) > 0 and clean_entityname[str(key_p_clean)] not in matched_entitynames:
            fundid = clean_fundname_fundid[str(key_p_clean)][0]
            for name in lastnames:
                values = lastname_fundid_personid.get(name)
                for fdid, personid in values:
                    if fdid == fundid:
                        entry = [clean_entityname_cik[str(key_p_clean)][0], clean_entityname[str(key_p_clean)], personid]
                        data.append(entry)
            matched_entitynames.add(clean_entityname[str(key_p_clean)])
    else:
        unmatched[key_p] = item_p
        
# FUZZY MATCHING FOR NAMES W/ NO DIRECT MATCHINGS    
for key_p, item_p in unmatched.items():
    key_p_clean = clean.clean_up_company_names(key_p) 
    check = fuzzy_check(key_p_clean, clean_entityname_lastname.keys(), 90, matched_entitynames)
    if check:
        p, f = check[0], check[1]
        lastnames = fuzzy_check_lastnames(item_p, item_f, 90)
        if len(lastnames) > 0 and clean_entityname[str(f)] not in matched_entitynames:
            fundid = clean_fundname_fundid[str(p)][0]
            for name in lastnames:
                values = lastname_fundid_personid[name]
                for fdid, personid in values:
                    if fdid == fundid:
                        entry = [clean_entityname_cik[str(f)][0], clean_entityname[str(f)], personid]
                        data.append(entry)
            matched_entitynames.add(clean_entityname[str(f)])


# WRITE DATA TO FILE
columns = ["cik", "entityname", "personid"]
file_path = 'lastname_match.csv'
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(data)