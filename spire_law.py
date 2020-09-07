import time
import datetime
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome("/Users/Buster/chromedriver")
browser.get("https://www.floridabar.org/directories/find-mbr/")
time.sleep(1)
fname_input = browser.find_element_by_id('sFirstname')
fname_input.send_keys("*")
btn_array = browser.find_elements_by_class_name("form-btn")
submit = None

for btn in btn_array:
    if(btn.get_attribute('value') == "Search"):
        submit = btn
    else:
        print("No")

submit.click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "size50")))
scrape_size = browser.find_element_by_id('size50')

time.sleep(3)
scrape_size.click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "output")))
bar_numbers = []
attorney_names = []
urls = []
eligibility_status = []
profile_images = []
emails = []
original_search = []
recent_search = []
mailing_address = []
office_numbers = []
fax_numbers = []
cell_numbers = []
for i in range(1,21):
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "output")))
    output = browser.find_elements_by_class_name('profile-compact')
    for profile in output:
        #Getting name
        attorney_name = profile.find_elements_by_class_name('profile-name')
        attorney_names.append(attorney_name[0].text)
        url = attorney_name[0].find_element_by_tag_name("a")
        urls.append(url.get_attribute("href"))
        #Getting bar number
        bar_number = profile.find_elements_by_class_name('profile-bar-number')[0].text
        stripped_num = re.findall(r'\d+',bar_number)
        bar_numbers.append(stripped_num[0])
        #Getting eligibility
        eligibility = profile.find_elements_by_class_name('eligibility')[0].text
        eligibility_status.append(eligibility)
        #getting profile picture
        image_div = profile.find_elements_by_class_name('profile-image')
        image = image_div[0].find_element_by_tag_name("img")
        image_source = image.get_attribute("src")
        profile_images.append(image_source)
        #getting emails
        email = profile.find_elements_by_class_name('icon-email')
        if(len(email)>0):
            emails.append(email[0].text)
        else:
            emails.append("N/A")
        #getting first search date
        today = datetime.datetime.now()
        original_search.append(today)
        recent_search.append(today)
        #getting addresses
        address_arr = profile.find_elements_by_class_name('profile-contact')
        for a in address_arr:
            try:
                mailing_address.append(a.find_element_by_tag_name('p').text.replace('\n'," "))
            except:
                mailing_address.append('N/A')
        #getting phone numbers
        try:
             phone_arr = profile.find_elements_by_class_name("profile-contact")
             raw_phone = phone_arr[0].text.replace('\n', " ")
             office_number = re.findall(r'Office: ([^\s]+)', raw_phone)
             if(office_number):
                office_numbers.append(office_number[0])
             else:
                office_numbers.append("N/A")

             cell_number = re.findall(r'Cell: ([^\s]+)', raw_phone)
             if(cell_number):
                cell_numbers.append(cell_number[0])
             else:
                cell_numbers.append("N/A")
             fax_number = re.findall(r'Fax: ([^\s]+)', raw_phone)
             if(fax_number):
                fax_numbers.append(fax_number[0])
             else:
                fax_numbers.append("N/A")
        except:
             office_numbers.append("N/A")
             fax_numbers.append("N/A")
             cell_numbers.append("N/A")
    next_page = browser.find_element_by_xpath('//*[@title="next page"]')
    next_page.click()

browser.close()

big_data = pd.DataFrame()
big_data["Attorney Name"] = attorney_names
big_data["Bar Number"] = bar_numbers
big_data["Eligibility"] = eligibility_status
big_data["Profile Picture"] = profile_images
big_data["Email"] = emails
big_data["URL"] = urls
big_data["Original Search"] = original_search
big_data["Recent Search"] = recent_search
big_data["Address"] = mailing_address
big_data["Office Number"] = office_numbers
big_data["Cell Number"] = cell_numbers
big_data["Fax Number"] = fax_numbers

#Starting second scrape right after this one
bar_nums = big_data["Bar Number"]

member_status = []
fl_eligibility = []
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
       fl_eligibility.append("N/A")
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

browser.close()

big_data["Membership Status"]=member_status
big_data["Eligibility"]=fl_eligibility
big_data["Firm URL"]=company_url
big_data["Firm"]=firms
big_data["Firm Position"]=firm_position
big_data["Firm Size"]=firm_size
big_data["10-Year Discipline"]=ten_year
big_data["Admitted Date"]=admitted_date
big_data["Circuit"]=circuit
big_data["County"]=county
big_data["Law School"]=law_school
big_data["Total # of Sections"]=total_sections
big_data["Total # of Practice Area"]=total_prac_areas
big_data["Sections"]=sections
big_data["Practice Areas"]=practice_areas
big_data["Languages"]=languages
big_data["Federal Courts"]=fed_courts
big_data["State Courts"]=state_courts


old_data = pd.read_csv('spire_law.csv',sep='|')
big_data['Original Search'] = old_data['Original Search']

big_data.to_csv('spire_law.csv', sep='|')