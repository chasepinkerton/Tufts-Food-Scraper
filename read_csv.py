from pprint import pprint
from fuzzywuzzy import process, fuzz
import numpy as np
import pandas as pd
import os


df = pd.read_csv('menu.csv')  

unique_dish = df['Dish'].unique().tolist()

inp = input("What food are you looking for?\n")

matched_dishes = (process.extract(inp, unique_dish, scorer=fuzz.partial_ratio))

#Create a dataframe from the tuples
similarity_sort = pd.DataFrame(matched_dishes, columns=['dish','score_sort'])

high_score_sort = similarity_sort[(similarity_sort['score_sort'] >= 84)]['score_sort'], ascending=False)


matched_dishes_cutoff = list(high_score_sort.dish)

for dish in matched_dishes_cutoff:
    # print(df.loc[df['dish'] == dish.text])
    print(dish)
