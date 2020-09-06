import time
import datetime
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

data = pd.read_csv('spire_law.csv')

urls = data['URL'][0:4]


member_status = []
fl_eligibility = []
browser = webdriver.Chrome("/Users/Buster/chromedriver")
for url in urls:
   browser.get(url)
   WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "mProfile")))
   #getting member status
   time.sleep(2)
   status = browser.find_element_by_class_name('member-status')
   member_status.append(status.text)
   #eligibility = browser.find_elements_by_class_name('eligibility-status')
   #fl_eligibility.append(eligibility[0].text)

browser.close()



print(member_status)

