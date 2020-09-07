import time
import datetime
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
data = pd.read_csv('spire_law.csv')

bar_nums = data['Bar Number'][0:30]


member_status = []
fl_eligibility = []
bar_numbers = []
company_url = []
firms = []
ten_year = []
admitted_date = []
circuit = []
firm_size = []
firm_position = []
county = []
law_school = []
total_sections = []
total_prac_areas = []
practice_areas = []
cell_numbers = []
office_numbers = []
fax_numbers = []
addresses = []
languages = []
sections = []
fed_courts = []
state_courts = []
browser = webdriver.Chrome("/Users/Buster/chromedriver")
for num in bar_nums:
   time.sleep(3)
   browser.get(f"https://www.floridabar.org/directories/find-mbr/?barNum={str(num)}")
   WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "mProfile")))

   try:
       status = browser.find_element_by_class_name('member-status')
       member_status.append(status.text)
   except:
       member_status.append("N/A")
   try:
       eligibility = browser.find_elements_by_class_name('eligibility')
       fl_eligibility.append(eligibility[0].text)
   except:
       member_status.append("N/A")
   bar_numbers.append(num)
   labels = browser.find_elements_by_class_name('col-sm-3')
   label_data = browser.find_elements_by_class_name('col-sm-9')
   section_labels = []
   section_data = []
   for label in labels:
       section_labels.append(label.text.replace(':',''))
   for s_data in label_data:
       section_data.append(s_data.text)
   att_zip = zip(section_labels,section_data)
   att_dict = {}
   for (x,y) in att_zip:
       att_dict[str(x)] = y
   try:
       office_number = re.findall(r'Office: ([^\s]+)', att_dict['Mail Address'])[0]
       office_numbers.append(office_number)
   except:
       office_numbers.append("N/A")
   try:
       cell_number = re.findall(r'Cell: ([^\s]+)', att_dict['Mail Address'])[0]
       cell_numbers.append(cell_number)
   except:
       cell_numbers.append("N/A")
   try:
       fax_number = re.findall(r'Fax: ([^\s]+)', att_dict['Mail Address'])[0]
       fax_numbers.append(fax_number)
   except:
       fax_numbers.append("N/A")
   try:
       company_url.append(att_dict['Firm Website'])
   except:
       company_url.append('N/A')
   try:
       firms.append(att_dict['Firm'])
   except:
       firms.append('N/A')
   try:
       ten_year.append(att_dict['10-Year Discipline History'])
   except:
       ten_year.append('N/A')
   try:
       admitted_date.append(att_dict['Admitted'])
   except:
       admitted_date.append('N/A')
   try:
       circuit.append(att_dict['Circuit'])
   except:
       circuit.append('N/A')
   try:
       firm_size.append(att_dict['Firm Size'])
   except:
       firm_size.append('N/A')
   try:
       firm_position.append(att_dict['Firm Position'])
   except:
       firm_position.append('N/A')
   try:
       county.append(att_dict['County'])
   except:
       county.append('N/A')
   try:
       law_school.append(att_dict['Law School'])
   except:
       law_school.append('N/A')
   try:
       areas = (att_dict['Practice Areas']).split('\n')
       text_areas = (att_dict['Practice Areas']).replace('\n',", ")
       total_prac_areas.append(len(areas))
       practice_areas.append(text_areas)
   except:
       total_prac_areas.append('N/A')
       practice_areas.append("N/A")
   try:
       raw_lang = att_dict['Languages']
       languages.append(raw_lang.replace('\n',", "))
   except:
       languages.append('N/A')
   try:
       raw_sections = att_dict['Sections'].split("\n")
       text_sections = att_dict['Sections'].replace('\n',", ")
       total_sections.append(len(raw_sections))
       sections.append(text_sections)
   except:
       total_sections.append(0)
       sections.append("N/A")
   try:
       raw_court = att_dict['Federal Courts']
       fed_courts.append(raw_court.replace('\n',", "))
   except:
       fed_courts.append('N/A')
   try:
       raw_court = att_dict['State Courts']
       state_courts.append(raw_court.replace('\n',", "))
   except:
       state_courts.append('N/A')

print(state_courts)
browser.close()



detailed_data = pd.DataFrame()
detailed_data["Membership Status"]=member_status
detailed_data["Eligibility"]=fl_eligibility
detailed_data["Bar Number"]=bar_numbers
detailed_data["Firm URL"]=company_url
detailed_data["Firm"]=firms
detailed_data["Firm Position"]=firm_position
detailed_data["Firm Size"]=firm_size
detailed_data["10-Year Discipline"]=ten_year
detailed_data["Admitted Date"]=admitted_date
detailed_data["Circuit"]=circuit
detailed_data["County"]=county
detailed_data["Law School"]=law_school
detailed_data["Total # of Sections"]=total_sections
detailed_data["Total # of Practice Area"]=total_prac_areas
detailed_data["Sections"]=sections
detailed_data["Practice Areas"]=practice_areas
detailed_data["Cell Number"]=cell_numbers
detailed_data["Cell Number"]=office_numbers
detailed_data["Cell Number"]=fax_numbers
detailed_data["Languages"]=languages
detailed_data["Federal Courts"]=fed_courts
detailed_data["State Courts"]=state_courts



detailed_data.to_csv('spire_detailed_law.csv', sep=',')