from fuzzywuzzy import process, fuzz
import pandas as pd
import pprint
import os

df = pd.read_csv(('menu.csv'), index_col=0)  

# Get Unique list of all Dishes
unique_dish = df['Dish'].unique().tolist()

food = input("What food are you looking for?\n")

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
