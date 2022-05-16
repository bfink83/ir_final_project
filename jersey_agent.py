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
from urllib import parse, request

options = Options()
# options.add_argument('--headless')

# url = 'https://www.nflshop.com/'
url = 'https://www.fanatics.com/'
nflshop_searchbox = 'typeahead-input'
nflshop_searchSubmit = 'typeahead-go'

# name = input("Enter player name: ")
# size = input("Men, Women, or Youth Jersey?: ")
# color = input("Enter jersey color: ")
# team = input("Enter desired player team: ")

name = "Diggs"
size = "Men"
color = "Blue"
team = "Bills"


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

# browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(team)).click()
browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(size)).click()
browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("Jerseys")).click()
# browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("NFL")).click()
elements = browser.find_elements(by=By.PARTIAL_LINK_TEXT, value = ("NFL"))
elements[1].click()

browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(team)).click()
browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("View all players")).click()
browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(name)).click()
print("NARROWING SEARCH")



# items = browser.find_elements(by=By.CLASS_NAME, value='product-card-title a')
# item1 = items[0]
# itemHTML = item1.get_attribute('title')
# print(itemHTML)

item_dict = {}

try:
  items = browser.find_elements(by=By.CLASS_NAME, value='product-card-title a')
  for item in items:
    itemTitle = item.get_attribute('title')
    if "Custom" not in itemTitle:
      itemLink = item.get_attribute('href')
      item_dict[itemTitle] = [itemLink]

  print(item_dict)
  print(len(item_dict))

  for k,v in item_dict.items():
    browser.get(v[0])
    price_div = browser.find_element(By.CSS_SELECTOR, value = "span[class='sr-only']")
    # find_element_by_css_selector("span[class='sr-only']")
    price = price_div.get_attribute('innerText')
    item_dict[k] += str(price)
    # print(price)
  
  print(item_dict)


  browser.close()
  browser.quit()


except:
  print("COULD NOT FIND")
