import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

url = 'https://www.nflshop.com/'
nflshop_searchbox = 'typeahead-input'
nflshop_searchSubmit = 'typeahead-go'

driver_path = '/Users/bailey.finkelberg/Downloads/chromedriver'
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

query = ["Stefon Diggs", "Men's", "Blue"]

browser.get(url)

time.sleep(5)

# try:
#   popButton = browser.find_element_by_xpath('//*[@id="once-per-session___BV_modal_footer_"]/button').click()
# except:
#   pass

searchbox = browser.find_element(by=By.CLASS_NAME, value=nflshop_searchbox)
searchbox.clear()
searchbox.send_keys(query[0])

browser.find_element(by=By.CLASS_NAME, value=nflshop_searchSubmit).click()

# items = browser.find_elements(by=By.CLASS_NAME, value='product-card-title')
# for item in items:
#   title = item.get_attribute("title")
#   print("yeah", title)

# print("still on")

# try:
#   # items = browser.find_elements(by=By.CLASS_NAME, value='product-card-title')
#   # print(items)

#   elements = driver.find_elements(by=By.CSS_SELECTOR, value='product-card-title a')

#   print(elements)
#   # for element in elements:
#   #     print(element.get_attribute("title"))
# except:
#   print("COULD NOT FIND")
