import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

options = Options()
# options.headless = True
options.headless = False
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


name = input("Enter player name: ")
name = name.lower().title()
print(name)
while True:
  size = input("Men, Women, or Youth Jersey?: ")
  size = size.lower().title()
  print(size == 'Youth')
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

    print(item_dict)
  except Exception as e:
      print(e, url)

sorted_dict = sorted(item_dict.items(), key=lambda x: x[1])
lowestKey = list(sorted_dict)[0][0]

browser.close()
browser.quit()

options.headless = False
browser2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
browser2.get(item_dict.get(lowestKey)[0])

browser2.close()
browser2.quit()

end = time.time()

print("Time: ", end - start)
