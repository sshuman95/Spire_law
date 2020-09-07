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

bar_nums = data['Bar Number'][0:5]


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
cell_numbers = []
office_numbers = []
fax_numbers = []
addresses = []
languages = []
browser = webdriver.Chrome("/Users/Buster/chromedriver")
for num in bar_nums:
   browser.get(f"https://www.floridabar.org/directories/find-mbr/?barNum={str(num)}")
   WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "mProfile")))

   status = browser.find_element_by_class_name('member-status')
   member_status.append(status.text)
   eligibility = browser.find_elements_by_class_name('eligibility')
   fl_eligibility.append(eligibility[0].text)
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
   total_sections.append(len(att_dict.keys()))
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
       total_prac_areas.append(len(areas))
   except:
       total_prac_areas.append('N/A')
   try:
       raw_lang = att_dict['Languages']
       languages.append(raw_lang.replace('\n',", "))
   except:
       languages.append('N/A')

print(fax_numbers)

browser.close()


"""
detailed_data = pd.DataFrame()
detailed_data["Bar Number"] = bar_numbers
detailed_data["Membership Status"] = member_status
detailed_data["Eligibility"] = fl_eligibility


"""
