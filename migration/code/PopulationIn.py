import csv
import re
import numpy as np
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
population_file = dir_path + "/../data/World_Bank/population_total/Total_Population_Data.csv"

population = {}
countries_with_population = set()

with open(population_file, 'r') as population_input:
    population_reader = csv.reader(population_input)
    row_nr = 0
    index_year = {}
    for row in population_reader:
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
        pop_data = row[index_year[2000]]
        numeric_data = re.match(r'^\d', pop_data)
        if not numeric_data:
            continue
        population[country] = int(pop_data)
        countries_with_population.add(country)
        row_nr += 1

world_population = np.sum(population.values())