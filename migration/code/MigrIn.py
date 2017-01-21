import xlrd
import re
import os
import csv
from threading import Thread

dir_path = os.path.dirname(os.path.realpath(__file__))
migration_pair_file = dir_path + "/../data/MigrationDRC/Global_Migrant_Origin_Database_Version_4.xls"
migration_OECD_file = dir_path + "/../data/OECD/DIOC__2010-11Rev4/DIOC_2010_11_File_A_quater_REV.csv"

migration_workbook = xlrd.open_workbook(migration_pair_file)
migration_sheet = migration_workbook.sheet_by_index(0)
col_idx = migration_sheet.row(0)

migration = {}
countries_with_migration = {}
year_list = [2000, 2010]
for year in year_list:
    migration[year] = {}
    countries_with_migration[year] = set()
migration_country_col_idx = {}
country_name = {}
country_code = {}
OECD_countries = set()
migration_sex = {}
migration_age = {}
for idx, cell_obj in enumerate(col_idx):
    if cell_obj.value == "State Code":
        country_idx = idx
        continue
    if cell_obj.value == "Origin Countries":
        country_name_idx = idx
        continue
    migration_country_col_value = re.search(r'[A-Z]{3}', cell_obj.value)
    if migration_country_col_value:
        migration_country_col_idx[migration_country_col_value.group()] = idx
    continue

for row_idx in range(migration_sheet.nrows):
    if row_idx == 0:
        continue
    row = migration_sheet.row(row_idx)
    emigrating_country_cell = migration_sheet.cell(row_idx, country_idx)
    emigrating_country_re = re.search(r'[A-Z]{3}', emigrating_country_cell.value)
    if emigrating_country_re:
        emigrating_country = emigrating_country_re.group()
    else:
        continue
    country_name_cell = migration_sheet.cell(row_idx, country_name_idx)
    name = country_name_cell.value
    if name.find(u"\u2018") != -1 or name.find(u"\u2019") != -1:
        name = name.replace(u"\u2018", "'").replace(u"\u2019", "'")
    country_name[emigrating_country] = name
    country_code[name] = emigrating_country
    migration[2000][emigrating_country] = {}
    countries_with_migration[2000].add(emigrating_country)
    for immigrating_country_cell,immigrating_idx in migration_country_col_idx.items():
        immigrating_country_re = re.search(r'[A-Z]{3}', immigrating_country_cell)
        if immigrating_country_re:
            immigrating_country = immigrating_country_re.group()
        else:
            continue
        migrant_nr = int(migration_sheet.cell(row_idx, immigrating_idx).value)
        migration[2000][emigrating_country][immigrating_country] = migrant_nr

def fill_entries(dictionary, countries):
    for country1 in countries:
        if country1 not in dictionary:
            dictionary[country1] = {}
        for country2 in countries:
            if country2 not in dictionary[country1]:
                dictionary[country1][country2] = 0


def parse_OECD_1():
    with open(migration_OECD_file, 'r') as migration_input:
        migration_reader = csv.reader(migration_input)
        count = 0
        for row in migration_reader:
            if count == 0:
                for index,entry in enumerate(row):
                    if entry == "country":
                        immigration_idx = index
                    if entry == "coub":
                        emigration_idx = index
                    if entry == 'oecd':
                        oecd_idx = index
                count += 1
                continue
            immigrating_country = row[immigration_idx]
            emigrating_country = row[emigration_idx]
            if immigrating_country not in countries_with_migration[2010]:
                countries_with_migration[2010].add(immigrating_country)
            if int(row[oecd_idx]) == 1:
                OECD_countries.add(immigrating_country)
            count += 1

# empty data
def parse_OECD_2():
    with open(migration_OECD_file, 'r') as migration_input:
        migration_reader = csv.reader(migration_input)
        count = 0
        for row in migration_reader:
            if count == 0:
                for index,entry in enumerate(row):
                    if entry == "country":
                        immigration_idx = index
                    if entry == "coub":
                        emigration_idx = index
                    if entry == "national":
                        national_idx = index
                    if entry == "sex":
                        sex_idx = index
                    if entry == "age":
                        age_idx = index
                    if entry == "birth":
                        birth_idx = index
                    if entry == "oecd":
                        oecd_idx = index
                    if entry == "regionb":
                        birth_region_idx = index
                    if entry == "fborn":
                        foreign_born_idx = index
                    if entry == "number":
                        number_idx = index
                count += 1
                continue
            # only consider foreigners
            if row[national_idx] != '0':
                count += 1
                continue
            immigrating_country = row[immigration_idx]
            # although inaccurate, assume country born is citizenship country
            emigrating_country = row[emigration_idx]
            if emigrating_country == immigrating_country:
                count += 1
                continue
            if emigrating_country not in migration[2010]:
                migration[2010][emigrating_country] = {}
            if immigrating_country not in migration[2010][emigrating_country]:
                migration[2010][emigrating_country][immigrating_country] = 0
            migration[2010][emigrating_country][immigrating_country] += int(row[number_idx])

            if emigrating_country in OECD_countries and immigrating_country in OECD_countries:
                if emigrating_country not in migration_sex:
                    migration_sex[emigrating_country] = {}
                if emigrating_country not in migration_age:
                    migration_age[emigrating_country] = {}
                if immigrating_country not in migration_sex[emigrating_country]:
                    migration_sex[emigrating_country][immigrating_country] = {}
                if immigrating_country not in migration_age[emigrating_country]:
                    migration_age[emigrating_country][immigrating_country] = {}
                if sex_idx not in migration_sex[emigrating_country][immigrating_country]:
                    migration_sex[emigrating_country][immigrating_country][sex_idx] = int(row[number_idx])
                else:
                    migration_sex[emigrating_country][immigrating_country][sex_idx] += int(row[number_idx])
                if age_idx not in migration_sex[emigrating_country][immigrating_country]:
                    migration_age[emigrating_country][immigrating_country][age_idx] = int(row[number_idx])
                else:
                    migration_age[emigrating_country][immigrating_country][age_idx] += int(row[number_idx])
            count += 1
        fill_entries(migration[2010], countries_with_migration[2010])
        fill_entries(migration_sex, countries_with_migration[2010])
        fill_entries(migration_age, countries_with_migration[2010])

t_OECD1 = Thread(target=parse_OECD_1)
t_OECD1.start()
t_OECD1.join()
t_OECD2 = Thread(target=parse_OECD_2)
t_OECD2.start()
t_OECD2.join()
