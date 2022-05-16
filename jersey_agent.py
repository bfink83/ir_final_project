import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')
options.add_argument('window-size=1100,700')

url_list = ['https://www.nflshop.com/', 'https://www.fanatics.com/']
nflshop_searchbox = fanatics_searchbox = 'typeahead-input'
nflshop_searchSubmit = fanatics_searchSubmit = 'typeahead-go'

def search(search_class, submit_class, name, browser):
  print("INPUTTING QUERY TO SEARCH BAR")
  searchbox = browser.find_element(by=By.CLASS_NAME, value=search_class)
  searchbox.clear()
  searchbox.send_keys(name)

  print("SEARCHING")
  browser.find_element(by=By.CLASS_NAME, value=submit_class).click()

def nflShopFilter(size, team, name, browser):
  print("NARROWING SEARCH")
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(team)).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(size)).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("Jerseys")).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("View all players")).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(name)).click()

def fanaticsLidsFilter(size, team, name, browser):
  print("NARROWING SEARCH")
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(size)).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("Jerseys")).click()
  elements = browser.find_elements(by=By.PARTIAL_LINK_TEXT, value = ("NFL"))
  elements[1].click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(team)).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("View all players")).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(name)).click()

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

for url in url_list:
  browser.get(url)
  print("URL OPENED")

  time.sleep(5)
  print("WAITING FOR POPUP TO CLOSE")

  # searchbox = browser.find_element(by=By.CLASS_NAME, value=nflshop_searchbox)
  # searchbox.clear()
  # searchbox.send_keys(name)
  # print("QUERY INPUTTED TO SEARCH BAR")

  # browser.find_element(by=By.CLASS_NAME, value=nflshop_searchSubmit).click()
  # print("SEARCHING")

  if 'nflshop' in url:
    search(nflshop_searchbox, nflshop_searchSubmit, name, browser)
    nflShopFilter(size, team, name, browser)
  elif 'fanatics' in url or 'lids' in url:
    search(fanatics_searchbox, fanatics_searchSubmit, name, browser)
    fanaticsLidsFilter(size, team, name, browser)

  item_dict = {}

  try:
    items = browser.find_elements(by=By.CLASS_NAME, value='product-card-title a')
    for item in items:
      itemTitle = item.get_attribute('title')
      if "Custom" not in itemTitle:
        itemLink = item.get_attribute('href')
        item_dict[itemTitle] = [itemLink]

    for k,v in item_dict.items():
      browser.get(v[0])
      price_div = browser.find_element(By.CSS_SELECTOR, value = "span[class='sr-only']")
      price = price_div.get_attribute('innerText')
      item_dict[k].append(price)

    browser.close()
    browser.quit()
  except Exception as e:
      print(e, url)
