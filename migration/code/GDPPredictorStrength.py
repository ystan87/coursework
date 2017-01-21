from GDPIn import countries_with_gdp, log_gdp_per_capita, world_gdp_per_capita
from MigrIn import countries_with_migration, country_name, migration
from PopulationIn import population, countries_with_population, world_population
import operator
import numpy as np
import csv
import os
import math

dir_path = os.path.dirname(os.path.realpath(__file__))
folder = "/../display"
if not os.path.exists(dir_path + folder):
    os.makedirs(dir_path + folder)

year = 2000

# only consider countries that have both GDP, population_cell and migration data
countries_to_consider = countries_with_gdp[year] & countries_with_migration[year] & countries_with_population

# Assess strength of GDP as predictor of migration direction
GDP_predictor_immigration = {}
GDP_predictor_emigration = {}

for base_country in countries_to_consider:
    convolution = 0
    convolution_abs = 0
    immigration_nr = []
    emigration_nr = []
    relative_log_GDP = []
    neg_relative_log_GDP = []
    other_population = []

    for other_country in countries_to_consider:
        if other_country == base_country:
            continue

        if migration[year][other_country][base_country] == 0:
            continue

        other_population.append(population[other_country])
        relative_log_GDP.append(log_gdp_per_capita[year][other_country])
        neg_relative_log_GDP.append(-log_gdp_per_capita[year][other_country])
        immigration_nr.append(migration[year][other_country][base_country])
        emigration_nr.append(migration[year][base_country][other_country])

    if len(other_population) <= 1:
        continue

    immigration_nr = np.asarray(immigration_nr)
    emigration_nr = np.asarray(emigration_nr)
    relative_log_GDP = np.asfarray(relative_log_GDP)
    neg_relative_log_GDP = np.asfarray(neg_relative_log_GDP)
    cov_array_immi = np.asfarray([immigration_nr, neg_relative_log_GDP])
    cov_array_emi = np.asfarray([emigration_nr, relative_log_GDP])
    covariance_immi = np.cov(cov_array_immi, aweights=immigration_nr)
    covariance_emi = np.cov(cov_array_emi, aweights=emigration_nr)
    GDP_predictor_immigration[base_country] = covariance_immi[0][1]/\
                                              math.sqrt(covariance_immi[0][0]*covariance_immi[1][1])
    GDP_predictor_emigration[base_country] = covariance_emi[0][1]/\
                                             math.sqrt(covariance_emi[0][0]*covariance_emi[1][1])

special_char = u'\u00F4'
special_char = special_char.encode('utf8')
to_rename = {
    "United States of America": "United States",
    "Bolivia": "Bolivia, Plurinational State of",
    "Iran, Islamic Republic of": "Iran",
    "Cote d'Ivoire": "C"+special_char+"te d'Ivoire",
    "Korea, Democratic People's Republic of": "North Korea",
    "Korea, Republic of": "South Korea",
    "Libyan Arab Jamahiriya": "Libya",
    "Tanzania, United Republic of": "Tanzania",
    "Moldova, Republic of": "Moldova",
    "Macedonia, the former Yugoslav Republic of": "Macedonia"
}

sorted_predictor_strength = sorted(GDP_predictor_immigration.items(), key=operator.itemgetter(1), reverse=True)

with open("./../display/GDP_predictor_immigration.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "country", "value"])
    displayed = False
    for i in range(len(sorted_predictor_strength)):
        country = country_name[sorted_predictor_strength[i][0]]
        if country in to_rename:
            country = to_rename[country]
        writer.writerow([i+1, country, sorted_predictor_strength[i][1]])
        if not displayed and sorted_predictor_strength[i][1] < 0:
            displayed = True
            print "The number of positive correlation countries for immigration is", i, \
                "out of", len(sorted_predictor_strength)

sorted_predictor_strength = sorted(GDP_predictor_emigration.items(), key=operator.itemgetter(1), reverse=True)

with open("./../display/GDP_predictor_emigration.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "country", "value"])
    displayed = False
    for i in range(len(sorted_predictor_strength)):
        country = country_name[sorted_predictor_strength[i][0]]
        if country in to_rename:
            country = to_rename[country]
        writer.writerow([i+1, country, sorted_predictor_strength[i][1]])
        if not displayed and sorted_predictor_strength[i][1] < 0:
            displayed = True
            print "The number of positive correlation countries for emigration is", i, \
                "out of", len(sorted_predictor_strength)

print "Program exited successfully"
