import csv
import re
import math
import os
from PopulationIn import world_population, population

dir_path = os.path.dirname(os.path.realpath(__file__))
gdp_per_capita_file = dir_path + "/../data/World_Bank/GDP_per_capita/GDP_per_capita_Data.csv"

gdp_per_capita = {}
# it is more natural to measure GDP with log scale
log_gdp_per_capita = {}
countries_with_gdp = {}

with open(gdp_per_capita_file, 'r') as gdp_per_capita_input:
    gdp_reader = csv.reader(gdp_per_capita_input)
    row_nr = 0
    index_year = {}
    for row in gdp_reader:
        if row_nr == 0:
            for index,entry in enumerate(row):
                if entry == "Country Code":
                    country_col = index
                year = re.match(r'^\d{4}',entry)
                if year:
                    index_year[int(year.group())] = index
            for year in index_year:
                countries_with_gdp[year] = set()
                gdp_per_capita[year] = {}
                log_gdp_per_capita[year] = {}
            row_nr += 1
            continue
        country = row[country_col]
        for year in index_year:
            gdp = row[index_year[year]]
            numeric_data = re.match(r'^\d', gdp)
            if not numeric_data:
                continue
            gdp = float(gdp)
            gdp_per_capita[year][country] = gdp
            log_gdp_per_capita[year][country] = math.log(gdp)
            countries_with_gdp[year].add(country)
            row_nr += 1
world_gdp_per_capita = 0
for country in countries_with_gdp[2000]:
    world_gdp_per_capita += gdp_per_capita[2000][country] * population[country]
world_gdp_per_capita /= world_population