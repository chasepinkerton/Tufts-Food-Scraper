import requests
from bs4 import BeautifulSoup

# Get data from menu
URL = 'http://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=TUFTS+DINING&locationNum=09&locationName=Carmichael+Dining+Center&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=5%2f7%2f2021'
page = requests.get(URL)

# Convert to parsed html in Soup format
soup = BeautifulSoup(page.content, 'html.parser')

# Filter by class name "shortmenurecipes"
menu = soup.find_all("div", {"class":["shortmenurecipes", "shortmenumeals"]})

# Loop through menu data and print each item
for item in menu:
    print(item.text)
