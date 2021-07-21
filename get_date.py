import pandas as pd
from pprint import pprint
import csv

with open('matches.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

print(data)
# matches = pd.read_csv('matches.csv')
menu = pd.read_csv('menu.csv')



