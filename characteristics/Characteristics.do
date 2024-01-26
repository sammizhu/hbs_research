********
**Inputs
********

*Experience file from LinkedIn Resumes ()
import delimited "/Users/sammizhu/Downloads/input/experience_small.csv", clear
drop unnamed0
drop if start_year == .
drop if start_year >=yearfounded // Looking at Resume information that predates company formation
drop if company_id == .
// See ClassifyDegreesTitles.ipynb to transform raw linkedin work titles into GP relevant titles 
keep cik cik_group employee std_url profile_url company_name company_id start_year end_year relevant_titles yearfounded
gen fulltitle = lower(relevant_titles)
gen founder = (strpos(fulltitle, "ounder")>0 |strpos(fulltitle, "wner")>0 |strpos(fulltitle, "ounding")>0)
gen partners = (fulltitle == "partner"| strpos(fulltitle, "managing director") >0| strpos(fulltitle, "general partner") >0| strpos(fulltitle, "managing partner")>0 ///
|strpos(fulltitle, "chief executive officer")>0| strpos(fulltitle, "senior partner")>0|strpos(fulltitle, "general director")>0 /// 
|strpos(fulltitle, "ceo ")>0)
drop relevant_titles
keep if founder|partner
save .\Output\data\stata\formd_experience, replace

*This is a match of all the companies on the founder's resume's to the file of VC-backed startups in PitchBook 
import delimited "/Users/sammizhu/Downloads/input/pb_startup_exp_Lk_verified.csv", clear
keep if match == "Yes"
keep linkedin_id
duplicates drop
ren linkedin_id company_id
merge 1:m company_id using .\Output\data\stata\formd_experience
drop if _m ==1
gen startup_experience = (_m ==3 & founder)
drop _m
br std_url start_year end_year yearfounded if startup_experience
gen startupexplength = end_year - start_year +1
replace startupexplength = yearfounded - start_year if end_year >yearfounded
replace startupexplength = 0 if startup_experience == 0
bys std_url: egen startup_exp_total = max(startupexplength)
save .\Output\data\stata\formd_experience, replace


**This is a match of all the companies on the founder's resume's to the file of venture capital investment firms in PitchBook 
import delimited "/Users/sammizhu/Downloads/input/pb_investor_exp_Lk_verified.csv", clear
keep if match == "Yes"
ren ïlinkedin_id linkedin_id
keep linkedin_id
duplicates drop
ren linkedin_id company_id
merge 1:m company_id using .\Output\data\stata\formd_experience
drop if _m ==1
gen vc_experience = (_m ==3) // Are you also classified as venture capital or private equity in pitchbook
drop _m
br std_url start_year end_year yearfounded if vc_experience
gen vcexplength = end_year - start_year +1
replace vcexplength = yearfounded - start_year if end_year >yearfounded
replace vcexplength = 0 if vc_experience == 0
bys std_url: egen vc_exp_total = max(vcexplength)
save .\Output\data\stata\formd_experience, replace


*I need the file with individual linkedin URLs in the Form D data to produce covariate tests at the founder level 
*Import match keys to count founders with masters and founders that attended top schools
import delimited "/Users/sammizhu/Downloads/input/experience_cik.csv", clear
drop v1
keep cik cik_group yearfounded
duplicates drop
destring cik, replace force
drop if cik == .
joinby cik using .\Output\data\stata\formd_regression_03_22
drop if yearfounded > start_year
keep cik cik_group
save .\Output\data\stata\firms_in_regression, replace


*For pairs of cik (or companyid in PitchBook) and people listed on Form D, how many of them have LinkedIn profiles?
import delimited "/Users/sammizhu/Downloads/input/experience_cik.csv", clear
destring cik, replace force
drop if cik == .
merge m:1 cik cik_group using .\Output\data\stata\firms_in_regression
keep if _m ==3
drop _m
keep cik cik_group std_url profile_url minorityowned minorityowned25 employee
compress
drop if employee == ""
bys cik cik_group: egen count_employees = nvals(employee)
bys cik cik_group: egen step = nvals(employee) if profile_url !=""
bys cik cik_group: egen count_employees_profile = max(step)
drop step
gen fraction_employees_lp = count_employees_profile/count_employees
drop if profile_url == ""
duplicates drop
gen str url = ""
replace url = std_url
drop std_url
ren url std_url
save .\Output\data\stata\supply_side_tests, replace


*Define an indicator for founders with bachelor's and graduate degrees, and founders that attended top schools 
*See ClassifyDegreesTitles.ipynb for degree classification
import delimited "/Users/sammizhu/Downloads/input/education_processed.csv", clear
gen has_grad_degree = (highest_degree == "Graduate") 
bys std_url: egen end_school_one = min(end_year_school) if  standardized_degree == "Bachelor"|standardized_degree == "Engineering"| ///
standardized_degree == "JD"| standardized_degree == "MD"
bys std_url: egen end_school = min(end_school_one)
keep std_url top_50 has_grad_degree end_school
duplicates drop 
merge 1:m std_url using .\Output\data\stata\supply_side_tests
keep if _m ==3
drop _m
bys cik cik_group: egen count_employees_grad = sum(has_grad_degree) 
bys cik cik_group: egen count_employees_top_50 = sum(top_50) 
bys cik cik_group: egen years_since_first_deg = mean(end_school) 
gen fraction_employees_grad = count_employees_grad/count_employees
gen fraction_employees_top_50 = count_employees_top_50/count_employees
save .\Output\data\stata\supply_side_tests, replace



********
**TODO!!!
********
python
*Input should be a standardized_url, yearfounded of the company, education characteristics from resume, company characteristics from resume.
*Output is education and experience before the year the company was founded

def characteristics(url, company_year, education, company):
	*For each person, create a job_history dictionary using the standardized_url as the key and the values as (start_year, end_year, company_id, position)
	*Likewise, also create a education_history dictionary using the standardized_url as the key and the values as (start_year, end_year, school, major, )
	
	return 


end
