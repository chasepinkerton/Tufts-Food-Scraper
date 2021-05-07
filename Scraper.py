import requests
from bs4 import BeautifulSoup

URL = 'http://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=TUFTS+DINING&locationNum=09&locationName=Carmichael+Dining+Center&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=5%2f7%2f2021'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

# spans = soup.findAll('span')
# for span in spans:
#     print(span.text)

menu = soup.find_all("div", class_="shortmenurecipes")


for item in menu:
    print(item.text)

# print(soup.select_one("span").text)

# print(filtered_menu)

# print(items)

# print(soup.get_text())



# print(page.content