from distutils.spawn import find_executable
import sys
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
# options.headless = False
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('window-size=1100,700')

nfl_teams = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens',
  'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals',
  'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 
  'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars',
  'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams',
  'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 
  'New York Giants', 'New York Jets', 'Philadelphia Eagles', 'Pittsburgh Steelers',
  'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers', 'Tennessee Titans',
  'Washington Commanders']

url_list = ['https://www.nflshop.com/', 'https://www.fanatics.com/', 'https://www.lids.com/']
# url_list = ['https://www.nflshop.com/']
# url_list = ['https://www.lids.com/']
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

def fanaticsFilter(size, team, name, browser):
  print("NARROWING SEARCH")
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(size)).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("Jerseys")).click()
  elements = browser.find_elements(by=By.PARTIAL_LINK_TEXT, value = ("NFL"))
  elements[1].click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(team)).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("View all players")).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(name)).click()

def lidsFilter(size, team, name, browser):
  print("NARROWING SEARCH")
  elements = browser.find_elements(by=By.PARTIAL_LINK_TEXT, value = ("NFL"))
  elements[1].click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(size)).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("Jerseys")).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(team)).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=("View all players")).click()
  browser.find_element(by=By.PARTIAL_LINK_TEXT, value=(name)).click()


name = input("Enter player name: ")
name = name.lower().title()
print(name)
while True:
  size = input("Men, Women, or Youth Jersey?: ")
  size = size.lower().title()
  if size != 'Men' and size != 'Women' and size != 'Youth':
    print("Please input one of the size options above.")
    continue
  else:
    break

while True:
  team = input("Enter desired player team: ")
  team = team.lower().title()
  team = [t for t in nfl_teams if team in t][0]
  if team not in nfl_teams:
    print("Please input an NFL team.")
    continue
  else:
    break

start = time.time()

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("INSTALLING DRIVER")

item_dict = {}

for url in url_list:
  browser.get(url)
  print("URL OPENED")

  time.sleep(5)
  print("WAITING FOR POPUP TO CLOSE")

  if 'nflshop' in url:
    search(nflshop_searchbox, nflshop_searchSubmit, name, browser)
    nflShopFilter(size, team, name, browser)
  elif 'fanatics' in url:
    search(fanatics_searchbox, fanatics_searchSubmit, name, browser)
    fanaticsFilter(size, team, name, browser)
  elif 'lids' in url:
    search(fanatics_searchbox, fanatics_searchSubmit, name, browser)
    lidsFilter(size, team, name, browser)

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
  except Exception as e:
      print(e, url)

sorted_dict = sorted(item_dict.items(), key=lambda x: x[1])
lowestKey = list(sorted_dict)[0][0]
lowestJerseys = [k for k,v in item_dict.items() if v[1] == item_dict.get(lowestKey)[1]]
lowestUrls = []
for a in lowestJerseys:
    string1 = item_dict.get(a)[0]
    lowestUrls.append(string1.rpartition('.com')[0])

titlesAndUrls = []
i = 0
for title in lowestJerseys:
    titlesAndUrls.append([title, lowestUrls[i]])
    i += 1
lowJlen = len(lowestJerseys)

print("These jerseys were found at the same price of", item_dict.get(lowestKey)[1])
print(titlesAndUrls)
color = input("Please select desired color from the list: ")
coloredJerseys = []
for j in titlesAndUrls:
    if color in j[0]:
        coloredJerseys.append([j[0], j[1]])
colJlen = len(coloredJerseys)
print(coloredJerseys)


if colJlen > 1:
    print("Please select a jersey as # 1 -", colJlen, end='')
    selectedJersey = int(input(": "))


browser.close()
browser.quit()

proceed = input("Would you like to continue to purchase?(y/n) " )
if proceed == "y":
    jerseySize = input("Enter jersey size (ex. '2XL'): ")

    options.headless = False
    options.add_experimental_option("detach", True)
    browser2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    if colJlen > 1:
        browser2.get(item_dict.get(coloredJerseys[selectedJersey - 1][0])[0])
    else:
        print(item_dict.get(coloredJerseys[0][0])[0])
        browser2.get(item_dict.get(coloredJerseys[0][0])[0])
    
    time.sleep(5)

    while True:
      size_in_stock = browser2.find_element(by=By.LINK_TEXT, value=(jerseySize))
      if "unavailable" in size_in_stock.get_attribute("class"):
        jerseySize = input("Size out of stock. Please Select Another: ")
        continue
      else:
        size_in_stock.click()
        break

    #For implementing full functonality in purchasing the product
    # browser2.find_element(by=By.CLASS_NAME, value=("button large team-primary-colors primary")).click()
    # time.sleep(3)
    # browser2.find_element(by=By.XPATH, value=('//button[@data-talos="buttonAddToCart"]')).click()
    # print("ADDED TO CART.")

end = time.time()

print("Time: ", end - start)
