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
import boto3
import s3fs
from io import StringIO


# Connect to S3
s3_client = boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id='AKIAVL4ZJ7NGDICR65VG',
    aws_secret_access_key='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'
)

# Function to Scrape Data
def scrape():
    
    # Get day 19 days from now (Newest menu released by Tufts)
    date_1 = datetime.strptime(datetime.today().strftime("%m/%d/%Y"), "%m/%d/%Y")
    end_date = date_1 + timedelta(days=19)

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
    breakfast = []
    brunch = []
    lunch = []
    dinner = []
    meal = 0
    valid_menu = False

    # Loop through menu data and store in correct list
    for item in menu:
        valid_menu = True
        # Data cleaning
        dish = item.text.replace('\xa0','')

        # Sorting to correct meal type
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
    if (valid_menu == False):
        print("Website Down")
        quit()
    # Create dataframes for each meal type

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
    
    # Retrieve data from bucket and rewrite it
    with io.StringIO() as csv_buffer:
        
        bucket_name = 'tufts-scraped-menu'
        object_key = 'data/menu_daily.csv'
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        
        # Read old menu data 
        df = pd.read_csv(StringIO(csv_string))
        
        # Add new menu data
        df3 = df.append(df3, ignore_index=True)

        # Write to local csv
        df3.to_csv("local_menu", index=False)
    

def lambda_handler():   
    print("Running Main\n")
    scrape()
if __name__ == "__main__":   
    lambda_handler()