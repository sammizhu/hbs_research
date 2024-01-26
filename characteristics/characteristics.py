import pandas as pd
import subprocess

""" 
POPULATING AND SAVING THE DICTIONARIES TO IMPROVE RUNTIME 
-can comment out after the files are populated!!!
"""

file1_path = "/Users/sammizhu/Downloads/input/experience_small.csv"
experience_small = pd.read_csv(file1_path)

file2_path = "/Users/sammizhu/Downloads/input/education_processed.csv"
education_processed = pd.read_csv(file2_path)

# For each person, create a job_history dictionary using the standardized_url 
# as the key and the values as (start_year, end_year, company_id, position)
job_history_dict = []

for index, row in experience_small.iterrows():
    cik = row['cik']
    cik_group = row['cik_group']
    employee = row['employee']
    std_url = row['std_url']
    profile_url = row['profile_url']
    company_name = row['company_name']
    company_id = row['company_id']
    start_year = row['start_year']
    end_year = row['end_year']
    relevant_titles = row['relevant_titles']
    yearfounded = row['yearfounded']

def characteristics(cik, cik_group, employee, std_url, profile_url, company_name, company_id, start_year, end_year, relevant_titles, yearfounded):

    data = (cik, cik_group, employee, std_url, profile_url, company_name, company_id, start_year, end_year, relevant_titles, yearfounded)

    if start_year < yearfounded and data not in job_history_dict:
        job_history_dict.append(data)

job = pd.DataFrame(list(job_history_dict.items()), columns=['std_url', 'description'])
job.to_csv('job_history.csv', index=False)

# Create a education_history dictionary using the std_url as the key and 
# the values as (start_year, end_year, school, major, standardized_degree)
education_history_dict = {}

for index, row in education_processed.iterrows():
    std_url = row['std_url']
    start_year = row['start_year_school']
    end_year = row['end_year_school']
    school = row['school_name']
    major = row['field_of_study']
    degree = row['standardized_degree']

    if std_url in education_history_dict:
        education_history_dict[std_url].append((start_year, end_year, school, major, degree))
    else:
        education_history_dict[std_url] = [(start_year, end_year, school, major, degree)]

edu = pd.DataFrame(list(education_history_dict.items()), columns=['std_url', 'description'])
edu.to_csv('edu_history.csv', index=False)

"""
-Input = std_url, year founded of the company, education characteristics from resume, company characteristics from resume.
-Output = education and experience before the year the company was founded
"""
# job_history = pd.read_csv('job_history.csv')
# education_history = pd.read_csv('edu_history.csv')

def find_prior(dict, year, std_url, result):
    data = dict[std_url]
    if data:
        for value in data:
            
            start_year = value[0]
            if start_year < year:
                result.add(value)
    return result

def characteristics(std_url, company_founding_year, education, company):
    output = set()
    data = job_history_dict[std_url]
    output = find_prior(job_history_dict, company_founding_year, std_url, output)
    output = find_prior(education_history_dict, company_founding_year, std_url, output)
    return output


# EXAMPLE USAGE
result = characteristics("https://www.linkedin.com/in/rob-brydges-650aa4", 2022, 2, 2)
print(result)

## NOTE: for some reason there are duplicates being printed with the jobs, but can fix later

subprocess.run(["stata", "do", "/path/to/your/do_file.do"])
