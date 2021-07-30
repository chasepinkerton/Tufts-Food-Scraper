from fuzzywuzzy import process, fuzz
import pandas as pd
import pprint
import os
import io
import s3fs
import boto3
from io import StringIO

# Connect to S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id="aws_access_key_id",
    aws_secret_access_key="aws_secret_access_key",
    aws_session_token="aws_session_token",
)

# Function to Search Data
def search(food):

    # Store s3 bucket data in dataframe
    bucket_name = 'tufts-scraped-menu'
    object_key = 'data/menu_daily.csv'
    csv_obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    
    # Get Unique list of all Dishes
    unique_dish = df['Dish'].unique().tolist()
    
    # Get Partial Ratio Matching tuples
    matched_dishes = (process.extract(food, unique_dish, scorer=fuzz.partial_ratio))
    
    # Create a dataframe from the tuples
    similarity_sort = pd.DataFrame(matched_dishes, columns=['dish','score_sort'])
    
    # Only get high matches
    high_score_sort = similarity_sort[(similarity_sort['score_sort'] >= 84)]
    
    # Convert to list
    matched_dishes_cutoff = list(high_score_sort.dish)
    
    # Find matching rows in Menu CSV
    results = df[df['Dish'].isin(matched_dishes_cutoff)]
    
    # Output resulting rows
    print(results)
    
# Lambda Handler, takes in event and food type searched for
def lambda_handler(event, context):
    food = '{}'.format(event['food'])
    print("Searching for " + food + "\n")
    search(food)
if __name__ == "__main__":   
    lambda_handler()