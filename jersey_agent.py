import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless')
# browser = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

url = 'https://www.nflshop.com/'
nflshop_searchbox = 'typeahead-input'
nflshop_searchSubmit = 'typeahead-go'


browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("INSTALLING DRIVER")

query_terms = ["Stefon Diggs", "Men's", "Blue"]

def formulateQuery(query_terms):
  query = ''
  for q in query_terms:
    query = query + q

  query = query + "Jerseys"

  return query


query = formulateQuery(query_terms)

browser.get(url)
print("URL OPENED")

time.sleep(5)
print("WAITING FOR POPUP TO CLOSE")

# try:
#   popButton = browser.find_element_by_xpath('//*[@id="once-per-session___BV_modal_footer_"]/button').click()
# except:
#   pass

searchbox = browser.find_element(by=By.CLASS_NAME, value=nflshop_searchbox)
searchbox.clear()
searchbox.send_keys(query)
print("QUERY INPUTTED TO SEARCH BAR")

browser.find_element(by=By.CLASS_NAME, value=nflshop_searchSubmit).click()
print("SEARCHING")

items = browser.find_elements(by=By.CLASS_NAME, value='product-card-title a')
item1 = items[0]
itemHTML = item1.get_attribute('title')
print(itemHTML)

itemTitles = []
try:
  items = browser.find_elements(by=By.CLASS_NAME, value='product-card-title a')
  for item in items:
    itemTitle = item.get_attribute('title')
    itemTitles.append(itemTitle)
  print(itemTitles)
except:
  print("COULD NOT FIND")
