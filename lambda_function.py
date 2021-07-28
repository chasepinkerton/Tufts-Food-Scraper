import requests
import os
import sys
from bs4 import BeautifulSoup
from pprint import pprint
from fuzzywuzzy import process, fuzz
# import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def scrape():
    date_1 = datetime.strptime(datetime.today().strftime("%m/%d/%Y"), "%m/%d/%Y")
    end_date = date_1 + timedelta(days=19)
    # print(end_date)

    url_date = end_date.strftime('%m%%2f%d%%2f%Y')

    # month = datetime.today().strftime('%m')
    # day = datetime.today().strftime('%d')
    # year = datetime.today().strftime('%Y')
    # month = str(8)
    # day = str(10)
    # year = str(2021)
    # url_date = month + '%2f' + day + '%2f' + year 
    # print(url_date)
    # date = month + '/' + str(day) + '/' + year

    print("\tGetting Menu Data from " + str(end_date), flush=True)

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

    df3 = pd.concat([df_breakfast, df_brunch, df_lunch, df_dinner])
    df3 = df3.assign(Day=end_date.strftime('%Y-%m-%d'))    
    # df3.columns = ["Dish", "Meal", "Date"]

    cwd = os.getcwd()
    path = cwd + "/menu_daily.csv"
    df3.to_csv(path, mode='a', header=False)
    
def lambda_function():   
    print("Running Main\n")
    scrape()
if __name__ == "__main__":   
    lambda_function()