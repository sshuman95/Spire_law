from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.Chrome("/Users/Buster/chromedriver")
urls=[]
final = []
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
output = browser.find_elements_by_class_name('profile-compact')
bar_numbers = []

for profile in output:
   bar_number = profile.find_elements_by_class_name('profile-bar-number')[0].text
   bar_numbers.append(bar_number)

print(bar_numbers)
browser.close()



#vehicle_overviews = soup.select('.vehicle-overview')
#soup = BeautifulSoup(browser.page_source,"html.parser")