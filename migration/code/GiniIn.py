import csv
import re
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
inequality_file = dir_path + "/../data/World_Bank/Gini_coefficient/Gini_Data.csv"

gini = {}
countries_with_gini = set()

with open(inequality_file, 'r') as gini_input:
    gini_reader = csv.reader(gini_input)
    row_nr = 0
    index_year = {}
    for row in gini_reader:
        if row_nr == 0:
            for index,entry in enumerate(row):
                if entry == "Country Code":
                    country_col = index
                year = re.match(r'^\d{4}',entry)
                if year:
                    index_year[int(year.group())] = index
            row_nr += 1
            continue
        country = row[country_col]
        gini_index = row[index_year[2000]]
        numeric_data = re.match(r'^\d', gini_index)
        if not numeric_data:
            continue
        gini_index = float(gini_index)
        countries_with_gini.add(country)
        gini[country] = gini_index
        row_nr += 1