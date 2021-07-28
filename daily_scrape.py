import requests
import os
import sys
import io
from bs4 import BeautifulSoup
from pprint import pprint
from fuzzywuzzy import process, fuzz
# import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import boto3
import s3fs

s3_client = boto3.client(
    "s3",
    aws_access_key_id="ASIAVL4ZJ7NGEPO7GWDO",
    aws_secret_access_key="2UOVRxFGDBvbijQzvIgfkk92U4FThh8xcFDlCFMr",
    aws_session_token="IQoJb3JpZ2luX2VjEHUaCXVzLWVhc3QtMSJHMEUCIBcUcl5+KNUryiIJJhUGG/SFripEk/u2oz/E3YwvXNoYAiEA7g1LiNuoQ/SW6Nfun452nbqqwixriKb92a1kZiUwa0Mq6wEIfhAAGgwzNjkxNTE4MzQ5NTYiDPZmo+dYt8q7gIm2ASrIAWwXLBTVM6bSIqMm1MPAIl1S7PfoS/0B6L6AGc/DD2DjWwpbjWh8qVXtn8tEKYEO/iGsRQuAbWitjK9wF5M7JGcBbjc0rKG38lGBIIGuRmvClm9y7/j3bq2Xei4iU+GOOG/hHghDpFtXJrqsKndL695Xh7rne7yXLMGl9RPNUt+qX065A+2DHoB1TSeXw1Ip6ot8qfMuShlOrdSXtMLruSQu3HN6JmTmWEdFDvs2k0oS1N4yu6pEwQOsS/K98vZusGXwhw65Hv3BMO6Kh4gGOpgBrTa8C2ay8jkl3qg+nrAZvi12eG3gW3yPWxRj2SR4gQbcbD61ZH+YMxF3Qh+xp5yyDWP3uSYBli+INyxbIeKrECK9szH0Zh9c9VmdOTxfz+GIce1SyPg8rfWCKSO34sYTuxk+vZ5GxiudajyF9GedjylkM1b6nrHEmXcHzhOgXE1C1mVZbg9/T1ZaIM4SDmKjGebqNAveqI0=",
)

def scrape():
    date_1 = datetime.strptime(datetime.today().strftime("%m/%d/%Y"), "%m/%d/%Y")
    end_date = date_1 + timedelta(days=19)
    # print(end_date)

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


    with io.StringIO() as csv_buffer:
        df3.to_csv(csv_buffer, index=False)

        response = s3_client.put_object(
            Bucket="tufts-scraped-menu", Key="data/test.csv", Body=csv_buffer.getvalue()
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 put_object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 put_object response. Status - {status}")


    # cwd = os.getcwd()
    # path = cwd + "/menu_daily.csv"
    # df3.to_csv(path, mode='a', header=False)
    
def lambda_function():   
    print("Running Main\n")
    scrape()
if __name__ == "__main__":   
    lambda_function()