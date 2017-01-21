import os
import re
from MigrIn import country_code, country_name
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
europe_population_center_file = dir_path + "/../data/Hamerly/europe_population_weighted_centers.txt"

special_case = {'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
                'Faeroe Islands': 'Faroe Islands',
                'Macedonia': 'Macedonia, the former Yugoslav Republic of',
                'Republic of Moldova': 'Moldova, Republic of',
                'Russia': 'Russian Federation'}

population = {}
european_countries_with_pop_cent = set()

with open(europe_population_center_file, 'r') as population_center_input:
    num_line = 0
    pop_cent_line = population_center_input.readline()
    pop_cent = {}
    while pop_cent_line:
        if num_line == 0:
            pop_cent_re = re.search(r'[12][0-9]{3}', pop_cent_line)
            if pop_cent_re:
                year = int(pop_cent_re.group())
                pop_cent[year] = {}
                population[year] = {}
                num_line += 1
                pop_cent_line = population_center_input.readline()
            else:
                print "Invalid data format for population_cell centers"
                exit()
        if num_line == 1:
            pop_cent_line = pop_cent_line.strip()
            col_idx = []
            for i in pop_cent_line.split(' '):
                if len(i) > 0:
                    col_idx.append(i)
            num_line += 1
            pop_cent_line = population_center_input.readline()
            continue

        pop_cent_line = pop_cent_line.strip()
        if len(pop_cent_line) == 0:
            num_line = 0
            pop_cent_line = population_center_input.readline()
            if pop_cent_line == "":
                break
            continue
        pop_cent_col = []
        for i in pop_cent_line.split(' '):
            if len(i) > 0:
                pop_cent_col.append(i)
        population_cell = int(pop_cent_col.pop())
        lon = float(pop_cent_col.pop())
        lat = float(pop_cent_col.pop())
        country = " ".join(pop_cent_col)
        if country in special_case:
            country = special_case[country]
        elif country not in country_code:
            num_line += 1
            pop_cent_line = population_center_input.readline()
            continue
        country = country_code[country]
        european_countries_with_pop_cent.add(country)
        pop_cent[year][country] = (lat, lon)
        population[year][country] = population_cell
        num_line += 1
        pop_cent_line = population_center_input.readline()

europe_population = {}
for year in population:
    europe_population[year] = np.sum(population[year].values())