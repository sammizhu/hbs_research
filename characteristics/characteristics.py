import pandas as pd
import subprocess
import csv
import math 
import re


file1_path = "/Users/sammizhu/Downloads/input/experience_cik.csv"
experience_small = pd.read_csv(file1_path)

job_history_dict = []

"""
Generates an experience file from LinkedIn Resumes given 
"""
def characteristics(stdized_url):
    for index, row in experience_small.iterrows():
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
            founder = any(substring in fulltitle for substring in ["ounder", "wner", "ounding"])
            partners = any(substring in fulltitle for substring in ["partner", "managing director", "general partner", "managing partner", "chief executive officer", "senior partner", "general director", "ceo"])
            
            if founder or partners:
                if math.isnan(start_year) or start_year < yearfounded:
                    if not math.isnan(company_id):
                        data = (cik, cik_group, employee, std_url, profile_url, company_name, int(company_id), start_year, end_year, yearfounded, "", "", fulltitle)
                        if data not in job_history_dict:
                            job_history_dict.append(data)

"""
Tag experineces from Experience File as Start-Up
"""
def start_up_tagging(experience_file_path):
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
            if row['end_year'] > row['yearfounded']:
                experience_file.loc[index, 'exp_length'] = row['yearfounded'] - row['start_year'] 
            else: experience_file.loc[index, 'exp_length'] = row['end_year'] - row['start_year'] + 1
    experience_file.to_csv(experience_file_path, index=False)


"""
Tag experineces from Experience File as Venture Captial 
"""
def VC_tagging(experience_file_path):
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
            if row['end_year'] > row['yearfounded']:
                experience_file.loc[index, 'exp_length'] = row['yearfounded'] - row['start_year'] 
            else: experience_file.loc[index, 'exp_length'] = row['end_year'] - row['start_year'] + 1
    experience_file.to_csv(experience_file_path, index=False)


characteristics("https://www.linkedin.com/in/jtlonsdale")
columns = ['cik', 'cik_group', 'employee', 'std_url', 'profile_url', 'company_name', 'company_id', 'start_year', 
'end_year', 'yearfounded', 'experience_type', 'exp_length', 'fulltitle']

with open('/Users/sammizhu/research/hbs_research/characteristics/job.txt', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(job_history_dict)

start_up_tagging('/Users/sammizhu/research/hbs_research/characteristics/job.txt')
VC_tagging('/Users/sammizhu/research/hbs_research/characteristics/job.txt')
