import requests
from bs4 import BeautifulSoup

# Get data from menu
URL = 'http://menus.tufts.edu/FoodPro%203.1.NET/longmenu.aspx?sName=TUFTS+DINING&locationNum=09&locationName=Carmichael+Dining+Center&naFlag=1&WeeksMenus=This+Week%27s+Menus&dtdate=05%2f08%2f2021&mealName=Lunch'
page = requests.get(URL)

# Convert to parsed html in Soup format
soup = BeautifulSoup(page.content, 'html.parser')

# Filter by class name "shortmenurecipes" and "shortmenumeals" for item/meal
menu = soup.find_all("div", {"class":["longmenucoldispname"]})

# Loop through menu data and print each item
for item in menu:
    print(item.text)
