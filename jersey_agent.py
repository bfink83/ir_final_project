import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

options = Options()
options.headless = True
options.add_argument('window-size=1100,700')

# url_list = ['https://www.nflshop.com/', 'https://www.fanatics.com/', 'https://www.lids.com/']
url_list = ['https://www.nflshop.com/']
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

start = time.time()

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("INSTALLING DRIVER")

for url in url_list:
  browser.get(url)
  print("URL OPENED")

  time.sleep(5)
  print("WAITING FOR POPUP TO CLOSE")

  if 'nflshop' in url:
    search(nflshop_searchbox, nflshop_searchSubmit, name, browser)
    nflShopFilter(size, team, name, browser)
  elif 'fanatics' in url or 'lids' in url:
    search(fanatics_searchbox, fanatics_searchSubmit, name, browser)
    fanaticsLidsFilter(size, team, name, browser)

  item_dict = {}

  try:
    items = browser.find_elements(by=By.CLASS_NAME, value='product-card')
    for item in items:
      itemLink = item.find_element(by=By.CLASS_NAME, value='product-card-title a')
      itemTitle = itemLink.get_attribute('title')
      if "Custom" not in itemTitle:
        itemURL = itemLink.get_attribute('href')
        price_div = item.find_element(by=By.CSS_SELECTOR, value="span[class='sr-only']")
        price = price_div.get_attribute('innerText')
        item_dict[itemTitle] = [itemURL, price]

    # print(item_dict)
  except Exception as e:
      print(e, url)

sorted_dict = sorted(item_dict.items(), key=lambda x: x[1])
lowestKey = list(sorted_dict)[0][0]
# print(item_dict.get(lowestKey)[1])
lowestJerseys = [k for k,v in item_dict.items() if v[1] == item_dict.get(lowestKey)[1]]
lowJlen = len(lowestJerseys)
print("These jerseys were found at the same price of", item_dict.get(lowestKey)[1])
print(lowestJerseys)

if lowJlen > 1:
    # print(lowestJerseys)
    print("Please select a jersey as # 1 -", (lowJlen + 1), end='')
    selectedJersey = int(input(": "))


browser.close()
browser.quit()

proceed = input("Would you like to continue to purchase?(y/n) " )
if proceed == "y":
    jerseySize = input("Enter jersey size: ")
    color = input("Enter jersey color: ")


    options.headless = False
    print(item_dict.get(lowestJerseys[selectedJersey - 1])[0])
    browser2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    if lowJlen > 1:
        browser2.get(item_dict.get(lowestJerseys[selectedJersey - 1])[0])
    else:
        browser2.get(item_dict.get(lowestJerseys[0])[0])

    browser2.close()
    browser2.quit()

end = time.time()

print("Time: ", end - start)
