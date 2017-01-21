import os
from MigrIn import country_name, migration, countries_with_migration
from PopulationIn import countries_with_population, population, world_population
from GDPIn import countries_with_gdp, gdp_per_capita
import pandas as pd

# This file requires 2MB of storage space to run
# It generates migration data and stores in descending order to files
dir_path = os.path.dirname(os.path.realpath(__file__))
folder = "/../data"
if not os.path.exists(dir_path + folder):
    os.makedirs(dir_path + folder)
largest_migration_file = dir_path + folder + "/LargestMigrationRate.csv"
largest_bidirectional_file = dir_path + folder + "/LargestBidirectional.csv"
largest_net_migration_file = dir_path + folder + "/LargestNetMigration.csv"

year = 2000

columns_large = ['Emigrating country', 'Immigrating country', 'Number of migrants', 'Population (emigrating country)',
                 'Population (immigrating country)', 'Migration rate', 'GDP per capita (emigrating country)',
                 'GDP per capita (immigrating country)']
columns_bi = ['Country 1', 'Country 2', 'Total bidirectional number of migrants', 'Population (Country 1)',
              'Population (Country 2)']
columns_net = ['Immigrating country', 'Emigrating country', 'Net flow', 'Population (emigrating country)',
               'Population (immigrating country)']
df_bi = pd.DataFrame(columns=columns_bi)
df_net = pd.DataFrame(columns=columns_net)
df_large = pd.DataFrame(columns=columns_large)

countries_to_consider = countries_with_gdp[year] & countries_with_migration[year] & countries_with_population
for emigrating_country in countries_to_consider:
    for immigrating_country in countries_to_consider:
        if emigrating_country == immigrating_country:
            continue
        migrant_nr = migration[year][emigrating_country][immigrating_country]
        weight = population[emigrating_country] * population[immigrating_country]
        migration_rate = migrant_nr * world_population * 1.0 / weight
        if migrant_nr > 1e2:
            df = pd.DataFrame([ [ country_name[emigrating_country], country_name[immigrating_country],
                                  migrant_nr, population[emigrating_country], population[immigrating_country],
                                  migration_rate, gdp_per_capita[year][emigrating_country],
                                  gdp_per_capita[year][immigrating_country] ] ], columns=columns_large )
            df_large = df_large.append(df, ignore_index=True)
        if emigrating_country > immigrating_country:
            bidirectional_nr = migrant_nr + migration[year][immigrating_country][emigrating_country]
            if bidirectional_nr > 1e2:
                df = pd.DataFrame([ [country_name[emigrating_country], country_name[immigrating_country],
                                     bidirectional_nr, population[emigrating_country], population[immigrating_country] ]
                                    ], columns=columns_bi )
                df_bi = df_bi.append(df, ignore_index=True)
            net_nr = -migrant_nr + migration[year][immigrating_country][emigrating_country]
            if net_nr > 10:
                df = pd.DataFrame([ [country_name[emigrating_country], country_name[immigrating_country],
                                     net_nr, population[emigrating_country], population[immigrating_country] ] ],
                                  columns=columns_net )
                df_net = df_net.append(df, ignore_index=True)
            elif net_nr < -10:
                df = pd.DataFrame([ [country_name[immigrating_country], country_name[emigrating_country],
                                     -net_nr, population[immigrating_country], population[emigrating_country] ] ],
                                  columns=columns_net )
                df_net = df_net.append(df, ignore_index=True)

# Consider countries among the highest migration factor
with open(largest_migration_file, 'w') as migration_output:
    df_large = df_large.sort_values(by='Migration rate', ascending=False)
    df_large.to_csv(path_or_buf=migration_output)

with open(largest_bidirectional_file, 'w') as migration_output:
    df_bi = df_bi.sort_values(by='Total bidirectional number of migrants', ascending=False)
    df_bi.to_csv(path_or_buf=migration_output)

with open(largest_net_migration_file, 'w') as migration_output:
    df_net = df_net.sort_values(by='Net flow', ascending=False)
    df_net.to_csv(path_or_buf=migration_output)

print "Program exited successfully"