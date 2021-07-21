from pprint import pprint
from fuzzywuzzy import process, fuzz
import numpy as np
import pandas as pd
import os

# Convert Menu into Dataframe
df = pd.read_csv(('menu.csv'), index_col=0)  

# Get Unique list of all Dishes
unique_dish = df['Dish'].unique().tolist()

inp = input("What food are you looking for?\n")

matched_dishes = (process.extract(inp, unique_dish, scorer=fuzz.partial_ratio))
# pprint(matched_dishes)

# Create a dataframe from the tuples
similarity_sort = pd.DataFrame(matched_dishes, columns=['dish','score_sort'])

# Only get high matches
high_score_sort = similarity_sort[(similarity_sort['score_sort'] >= 84)]

# Convert to list
matched_dishes_cutoff = list(high_score_sort.dish)

# Find matching rows in Menu CSV
results = df[df['Dish'].isin(matched_dishes_cutoff)]

pprint(results)


