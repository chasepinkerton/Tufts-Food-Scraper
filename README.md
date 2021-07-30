# Tufts Food Scraper (Work in Progress)
- By Chase Pinkerton

# Summary

This repository contains two files: daily_scrape.py and search_menu.py. This allows the user to search for a food item and any matching food is returned. The data returned includes dish, meal type, and day. 

# daily_scrape.py
daily_scrape.py uses BeautifulSoup to parse data from the Tufts Dining website in order to populate a pandas dataframe with new menu items from the most recently uploaded menu. This dataframe is then appened on top of the old menu in an S3 bucket and reuploaded as a CSV. 

# search_menu.py
search_menu.py uses fuzzywuzzy matching in order to get all corresponding dishes based on the users input. This script pulls the csv from s3 and prints out the matching dishes. 

# Lambda Functionality
Both scripts were uploaded to AWS Lambda to allow for daily execution in order to keep the menu data up to date. I created a AWS CloudWatch rule in order to run the daily_scrape script every morning. 

# Future Functionality
I am working on creating a frontend using AWS Amplify and allowing any Tufts Student to run my search_menu lambda function. I then will add in a way for users to create notification alerts in order to never miss their favorite meals. After that I will create a user pool with AWS Cognito to allow users to save preferences. 