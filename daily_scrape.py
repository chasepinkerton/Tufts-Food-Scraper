#
#   daily_scrape.py
#   by Chase Pinkerton
#
import requests
import os
import sys
import io
from bs4 import BeautifulSoup
from pprint import pprint
from fuzzywuzzy import process, fuzz
import pandas as pd
from datetime import datetime, timedelta

def get_meal_type(dish):
    if (dish == "Breakfast"):
        return 1
    if (dish == "Brunch"):
        return 4
    if (dish == "Lunch"):
        return 2
    if (dish == "Dinner"):
        return 3
    return 10

def create_df(breakfast, brunch, lunch, dinner, end_date):
    
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

    # Combine Dataframes and append correct date
    df3 = pd.concat([df_breakfast, df_brunch, df_lunch, df_dinner])
    df3 = df3.assign(Day=end_date.strftime('%Y-%m-%d'))    
    return df3

# Function to Scrape Data
def scrape():
    
    # Get day 19 days from now (Newest menu released by Tufts)
    date_1 = datetime.strptime(datetime.today().strftime("%m/%d/%Y"), "%m/%d/%Y")
    end_date = date_1 + timedelta(days=4)

    # Convert to correct format for URL
    url_date = end_date.strftime('%m%%2f%d%%2f%Y')

    print("\tGetting Menu Data from " + str(end_date), flush=True)

    # Get data from menu
    URL = 'https://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=TUFTS+DINING&locationNum=11&locationName=Dewick2GO&naFlag=1' + url_date
    page = requests.get(URL)

    # Convert to parsed html in Soup format
    soup = BeautifulSoup(page.content, 'html.parser')

    # Filter by class name "shortmenurecipes" and "shortmenumeals" for item/meal
    menu = soup.find_all("div", {"class":["shortmenurecipes", "shortmenumeals"]})
    breakfast, brunch, lunch, dinner = ([] for i in range(4))

    valid_menu = False

    # Loop through menu data and store in correct list
    for item in menu:
        valid_menu = True
        # Data cleaning
        dish = item.text.replace('\xa0','')

        # Sorting to correct meal type
        if (get_meal_type(dish) != 10):
            meal = get_meal_type(dish)


        if (meal == 1):
            breakfast.append(dish)
        if (meal == 2):
            lunch.append(dish)
        if (meal == 3):
            dinner.append(dish)
        if (meal == 4):
            brunch.append(dish)

    if (valid_menu == False):
        print("Website Down")
        quit()
    # Create dataframe from lists
    df3 = create_df(breakfast, brunch, lunch, dinner, end_date)

    cwd = os.getcwd()
    path = cwd + "/menu.csv"
    df3.to_csv(path, mode='a', header=False)
    

def main():     
    scrape()
if __name__ == "__main__":
    main()