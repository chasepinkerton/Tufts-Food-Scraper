import requests
import os
from bs4 import BeautifulSoup
from pprint import pprint
from fuzzywuzzy import process, fuzz
import numpy as np
import pandas as pd

i = 0

month = 7
month = str(month)
day = 22
year = 2021
year = str(year)
column_names = ["Dish", "Meal", "Day"]
df3 = pd.DataFrame(columns = column_names)

while day < 23:
    url_date = month + '%2f' + str(day) + '%2f' + year
    date = month + '/' + str(day) + '/' + year

    # Get data from menu
    URL = 'https://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=TUFTS+DINING&locationNum=11&locationName=Dewick2GO&naFlag=1' + url_date
    page = requests.get(URL)

    # Convert to parsed html in Soup format
    soup = BeautifulSoup(page.content, 'html.parser')

    # Filter by class name "shortmenurecipes" and "shortmenumeals" for item/meal
    menu = soup.find_all("div", {"class":["shortmenurecipes", "shortmenumeals"]})
    breakfast = []
    brunch = []
    lunch = []
    dinner = []
    meal = 0

    # Loop through menu data and store in correct list
    for item in menu:
        # print(item.text)
        dish = item.text.replace('\xa0','')
        # print(dish)
        if (dish == "Breakfast"):
            meal = 1
            continue
        if (dish == "Brunch"):
            meal = 4
            continue
        if (dish == "Lunch"):
            meal = 2
            continue
        if (dish == "Dinner"):
            meal = 3
            continue
        if (meal == 1):
            breakfast.append(dish)
        if (meal == 2):
            lunch.append(dish)
        if (meal == 3):
            dinner.append(dish)
        if (meal == 4):
            brunch.append(dish)

    df_breakfast = pd.DataFrame()
    df_breakfast['Dish']  = breakfast
    df_breakfast = df_breakfast.assign(Meal='Breakfast')

    df_lunch = pd.DataFrame()
    df_lunch['Dish']  = lunch
    df_lunch = df_lunch.assign(Meal='Lunch')

    df_dinner = pd.DataFrame()
    df_dinner['Dish']  = dinner
    df_dinner = df_dinner.assign(Meal='Dinner')
    
    df_brunch = pd.DataFrame()
    df_brunch['Dish']  = brunch
    df_brunch = df_brunch.assign(Meal='Brunch')
    
    day = day + 1
    if (day != 1):
        df2 = pd.concat([df_breakfast, df_brunch, df_lunch, df_dinner])
        df2 = df2.assign(Day=date)
        df3 = pd.concat([df2, df3])
    else:
        df3 = pd.concat([df_breakfast, df_brunch, df_lunch, df_dinner])
        df3 = df1.assign(Day=date)    


cwd = os.getcwd()
path = cwd + "/menu.csv"
df3.to_csv(path)

