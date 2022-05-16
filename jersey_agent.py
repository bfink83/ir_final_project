import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

options = Options()
# options.add_argument('--headless')

url = 'https://www.nflshop.com/'
nflshop_searchbox = 'typeahead-input'
nflshop_searchSubmit = 'typeahead-go'

name = input("Enter player name: ")
size = input("Men, Women, or Youth Jersey?: ")
color = input("Enter jersey color: ")
team = input("Enter desired player team: ")


browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("INSTALLING DRIVER")

browser.get(url)
print("URL OPENED")

time.sleep(5)
print("WAITING FOR POPUP TO CLOSE")

searchbox = browser.find_element(by=By.CLASS_NAME, value=nflshop_searchbox)
searchbox.clear()
searchbox.send_keys(name)
print("QUERY INPUTTED TO SEARCH BAR")

browser.find_element(by=By.CLASS_NAME, value=nflshop_searchSubmit).click()
print("SEARCHING")

browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(team)).click()
browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(size)).click()
browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("Jerseys")).click()
browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("View all players")).click()
browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(name)).click()
print("NARROWING SEARCH")

items = browser.find_elements(by=By.CLASS_NAME, value='product-card-title a')
item1 = items[0]
itemHTML = item1.get_attribute('title')
print(itemHTML)

item_dict = {}
try:
  items = browser.find_elements(by=By.CLASS_NAME, value='product-card-title a')
  for item in items:
    itemTitle = item.get_attribute('title')
    if "Custom" not in itemTitle:
      itemLink = item.get_attribute('href')
      item_dict[itemTitle] = itemLink

  print(item_dict)
  print(len(item_dict))
except:
  print("COULD NOT FIND")
