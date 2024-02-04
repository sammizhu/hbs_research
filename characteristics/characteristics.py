import pandas as pd
import subprocess
import csv
import math 
import re


file1_path = "/Users/sammizhu/Downloads/input/experience_cik.csv"
experience_cik = pd.read_csv(file1_path)

file2_path = "/Users/sammizhu/Downloads/input/education_processed.csv"
education_processed = pd.read_csv(file2_path)

job_history_dict = []
edu_history_dict = []

"""
Generates an experience file from LinkedIn Resumes given 
"""
def prior_experience(stdized_url, founding_year):
    for index, row in education_processed.iterrows():
        std_url = row['std_url']
        if stdized_url == std_url:
            top50 = row["Top_50"]
            has_grad_degree = ""
            end_year = row["end_year_school"]
            profile_url = row["profile_url"]
            highest_degree = row["highest_degree"]

            # We only want to keep the data if the education was completed before the founding year
            if end_year < founding_year or not math.isnan(end_year):
                data = (std_url, end_year, top50, highest_degree)
                # Idea is to store each person's relevant education history in a dictionary to make 
                # comparison with for individual job experiences later
                if data not in edu_history_dict:
                    edu_history_dict.append(data)

    for index, row in experience_cik.iterrows():
        std_url = row['std_url']
        if stdized_url == std_url:
            cik = row['cik']
            cik_group = row['cik_group']
            employee = row['employee']
            std_url = row['std_url']
            profile_url = row['profile_url']
            company_name = row['company_name']
            company_id = row['company_id']
            start_year = row['start_year']
            end_year = row['end_year']
            relevant_titles = row['title_y']
            yearfounded = row['year founded']
            try:
                fulltitle = relevant_titles.lower()
            except:
                fulltitle = ""
            founder = any(substring in fulltitle for substring in ["ounder", "wner", "ounding"]) # translated from Stata function
            partners = any(substring in fulltitle for substring in ["partner", "managing director", "general partner", 
                            "managing partner", "chief executive officer", "senior partner", "general director", "ceo"]) # translated from Stata function
            
            # Only want to collect data is the person's role was a founder or partner,
            # if the start year is before the founding_year, and there is a valid company_id
            if founder or partners:
                if math.isnan(start_year) or start_year < founding_year:
                    if not math.isnan(company_id):
                        end_school_year = 0
                        top50_var = 0
                        # For each of these experiences, we'll go through the edu_history_dict that was previously populated in order to find
                        # whether or not by the point of *this* job experience, the person has had attended a top 50 school or gotten their grad degree
                        for (std_url, end, top50, highest_degree) in edu_history_dict:
                            # Only count data if person ended their schooling before their company was founded
                            if end < yearfounded:
                                top50_var = (top50 == 1)
                                has_grad_degree = (highest_degree == "Graduate")
                                end_school_year = max(end, end_school_year)
                        data = (cik, cik_group, employee, std_url, profile_url, company_name, int(company_id), start_year, end_year, yearfounded, "", "", fulltitle, top50_var, has_grad_degree, end_school_year)
                        if data not in job_history_dict:
                            job_history_dict.append(data)

"""
Tag experineces from Experience File as Start-Up
    --> Translated from Stata function
"""
def start_up_tagging(experience_file_path):
    # Load the startup experience data and filter for rows with a match
    df_startup_exp = pd.read_csv("/Users/sammizhu/Downloads/input/pb_startup_exp_Lk_verified.csv")
    df_startup_exp = df_startup_exp[df_startup_exp['Match?'] == "Yes"]
    df_startup_exp = df_startup_exp[['LinkedIn_ID']]
    df_startup_exp = df_startup_exp.drop_duplicates()
    df_startup_exp = df_startup_exp.rename(columns={'LinkedIn_ID': 'company_id'})
    start_up_ids = list(df_startup_exp['company_id'])
    
    experience_file = pd.read_csv(experience_file_path)
    
    # Iterate over rows and update columns
    for index, row in experience_file.iterrows():
        company_id = row['company_id']
        
        if company_id in start_up_ids and 'founder' in row['fulltitle']:
            experience_file.loc[index, 'experience_type'] = 'Start-Up'
            
            # If there is no end_year, then temporarily mark is current_year for calculation purposes
            end_year = row['end_year']
            if math.isnan(end_year):
                end_year = 2024
            
            # Calculate experience length
            experience_file.loc[index, 'exp_length'] = end_year - row['start_year'] + 1
            if end_year > row['yearfounded'] and row['yearfounded'] - row['start_year'] > 0:
                experience_file.loc[index, 'exp_length'] = row['yearfounded'] - row['start_year'] 
    
    experience_file.to_csv(experience_file_path, index=False)


"""
Tag experineces from Experience File as Venture Captial 
    --> Translated from Stata function
"""
def VC_tagging(experience_file_path):
    # Load the venture capital experience data and filter for rows with a match
    df_vc_exp = pd.read_csv("/Users/sammizhu/Downloads/input/pb_investor_exp_Lk_verified.csv")
    df_vcp_exp = df_vc_exp[df_vc_exp['Match?'] == "Yes"]
    df_vcp_exp = df_vcp_exp[['LinkedIn_ID']]
    df_vcp_exp = df_vcp_exp.drop_duplicates()
    df_vcp_exp = df_vcp_exp.rename(columns={'LinkedIn_ID': 'company_id'})
    vc_ids = list(df_vcp_exp['company_id'])

    experience_file = pd.read_csv(experience_file_path)
    
    # Iterate over rows and update columns
    for index, row in experience_file.iterrows():
        company_id = row['company_id']
        
        if company_id in vc_ids:
            experience_file.loc[index, 'experience_type'] = 'VC'
            
            # If there is no end_year, then temporarily mark is current_year for calculation purposes
            end_year = row['end_year']
            if math.isnan(end_year):
                end_year = 2024
            
            # Calculate experience length
            experience_file.loc[index, 'exp_length'] = end_year - row['start_year'] + 1
            if end_year > row['yearfounded'] and row['yearfounded'] - row['start_year'] > 0:
                experience_file.loc[index, 'exp_length'] = row['yearfounded'] - row['start_year'] 

    experience_file.to_csv(experience_file_path, index=False)

##################################
## REPLACE WITH DESIRED STD_URL ##
## NOTE: not all std_url will   ##
## produce results because of   ##
## the year constraints. Some   ##
## examples to use are listed   ##
## below.                       ##
##################################
# https://www.linkedin.com/in/adelson
# https://www.linkedin.com/in/jtlonsdale
# https://www.linkedin.com/in/pengtong
# https://www.linkedin.com/in/limky
# https://www.linkedin.com/in/meyermalka
# https://www.linkedin.com/in/will-griffith-a51a9237

prior_experience("https://www.linkedin.com/in/jtlonsdale", 2014)
columns = ['cik', 'cik_group', 'employee', 'std_url', 'profile_url', 'company_name', 'company_id', 'start_year', 
'end_year', 'yearfounded', 'experience_type', 'exp_length', 'fulltitle', "Top_50", "has_grad_degree", "end_school"]

with open('/Users/sammizhu/research/hbs_research/characteristics/data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(job_history_dict)

start_up_tagging('/Users/sammizhu/research/hbs_research/characteristics/data.csv')
VC_tagging('/Users/sammizhu/research/hbs_research/characteristics/data.csv')
