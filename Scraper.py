import requests
from bs4 import BeautifulSoup
from pprint import pprint


month = '5'
day = '7'
year = '2021'
url_date = month + '%2f' + day + '%2f' + year
date = month + '/' + day + '/' + year
# Get data from menu
URL = 'http://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=TUFTS+DINING&locationNum=09&locationName=Carmichael+Dining+Center&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=' + url_date
page = requests.get(URL)

# Convert to parsed html in Soup format
soup = BeautifulSoup(page.content, 'html.parser')

# Filter by class name "shortmenurecipes" and "shortmenumeals" for item/meal
menu = soup.find_all("div", {"class":["shortmenurecipes", "shortmenumeals"]})
breakfast = []
lunch = []
dinner = []
meal = 0

# Loop through menu data and store in correct list
for item in menu:
    # print(item.text)
    if (item.text == "Breakfast"):
        meal = 1
        continue
    if (item.text == "Lunch"):
        meal = 2
        continue
    if (item.text == "Dinner"):
        meal = 3
        continue
    if (meal == 1):
        breakfast.append(item.text)
    if (meal == 2):
        lunch.append(item.text)
    if (meal == 3):
        dinner.append(item.text)
    
# Remove \xa0 from each string
breakfast = [el.replace('\xa0','') for el in breakfast]
lunch = [el.replace('\xa0','') for el in lunch]
dinner = [el.replace('\xa0','') for el in dinner]

print("breakfast " + date + " :")
pprint(breakfast)
print("lunch " + date + " :")
pprint(lunch)
print("dinner " + date + " :")
pprint(dinner)