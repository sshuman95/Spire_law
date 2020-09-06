from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome("/Users/Buster/chromedriver")
browser.get("https://www.floridabar.org/directories/find-mbr/")
time.sleep(3)
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
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "output")))
bar_numbers = []
attorney_names = []
for i in range(1,5):
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "output")))
    output = browser.find_elements_by_class_name('profile-compact')
    for profile in output:
        attorney_name = profile.find_elements_by_class_name('profile-name')[0].text
        attorney_names.append(attorney_name)
        bar_number = profile.find_elements_by_class_name('profile-bar-number')[0].text
        bar_numbers.append(bar_number)
    next_page = browser.find_element_by_xpath('//*[@title="next page"]')
    next_page.click()

browser.close()

big_data = pd.DataFrame()
big_data["Attorney Name"] = attorney_names
big_data["Bar Number"] = bar_numbers

big_data.to_csv('spire_law.csv', sep='\t')