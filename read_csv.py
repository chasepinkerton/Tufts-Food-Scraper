from pprint import pprint
from fuzzywuzzy import process, fuzz
import numpy as np
import pandas as pd
import os


df = pd.read_csv('menu.csv')  

unique_dish = df['Dish'].unique().tolist()

inp = input("What food are you looking for?\n")

matched_dishes = (process.extract(inp, unique_dish, scorer=fuzz.partial_ratio))

# pprint(matched_dishes)

#Create tuples of brand names, matched brand names, and the score
# score_sort = [(x,) + i
#              for x in unique_dish 
#              for i in process.extract(inp, unique_dish, scorer=fuzz.partial_ratio)]

#Create a dataframe from the tuples
similarity_sort = pd.DataFrame(matched_dishes, columns=['dish','score_sort'])
# similarity_sort.head()

high_score_sort = similarity_sort[(similarity_sort['score_sort'] >= 84)]
# high_score_sort = high_score_sort.drop('sorted_brand_sort',axis=1).copy()

# high_score_sort.groupby(['brand_sort','score_sort']).agg(
#                         {'match_sort': ', '.join}).sort_values(
#                         ['score_sort'], ascending=False)

pprint(high_score_sort)

# cwd = os.getcwd()
# path = cwd + "/menu2.csv"
# high_score_sort.to_csv(path)