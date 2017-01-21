import community
import networkx as nx
from MigrIn import migration, countries_with_migration, country_name
import os
import math
import operator
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))
folder = "/../report"
if not os.path.exists(dir_path + folder):
    os.makedirs(dir_path + folder)
partition_file = dir_path + folder + "/supplementary_material.txt"
folder = "/../display"
if not os.path.exists(dir_path + folder):
    os.makedirs(dir_path + folder)
display_file = dir_path + folder + "/community.csv"


year = 2000
migration_graph = nx.Graph()
total_migration_2000 = {}
print "number of countries for partition analysis",  len(countries_with_migration[year])
for country in countries_with_migration[year]:
    migration_graph.add_node(country)
    total_migration_2000[country] = 0
    for other_country in countries_with_migration[year]:
        total_migration_2000[country] = total_migration_2000[country] + \
                                        migration[year][country][other_country] + \
                                        migration[year][other_country][country]

total_weight = 0
threshold = 0.5
for country1 in countries_with_migration[year]:
    for country2 in countries_with_migration[year]:
        if country2 <= country1:
            continue

        weight = float( migration[year][country1][country2] + migration[year][country2][country1] ) / \
                 (total_migration_2000[country1] + total_migration_2000[country2]) *len(countries_with_migration[year])
        if weight < threshold:
            continue
        migration_graph.add_edge(country1, country2, weight=weight)
        total_weight += weight

print "total weight", total_weight
print "number of edges", len(migration_graph.edges())
resolution_limit = math.sqrt(total_weight/2)
print "resolution limit is", resolution_limit

partition = community.best_partition(migration_graph)
partition_num = list(set(list(partition.values())))
partition_reverse = {}
for part in partition_num:
    part_set = set()
    for country in partition:
        if partition[country] == part:
            part_set.add(country)
    partition_reverse[part] = part_set

print "The modularity of this partition is", community.modularity(partition, migration_graph)

community_names = {
    0 : "Much of Europe, North Africa, Turkey and Northern corner of South America",
    12: "Northern Europe and Eastern Africa",
    17: "Central Europe",
    14: 'Central Asia and Eastern Europe',
    1 : 'Middle East and South Asia',
    2 : 'Central, East and South Africa',
    4 : 'Western Africa',
    3 : 'South America',
    13: 'Central America',
    9 : 'The Caribbean',
    6 : 'North America, East Asia, UK & Ireland, Australia & New Zealand and Southeast Asia',
    5 : 'Archipelagic Oceania'}
community_weight = {}
above_resolution_limit = set()

for part in partition_reverse:
    part_list = list(partition_reverse[part])
    sub_graph = migration_graph.subgraph(part_list)
    community_weight[part] = sub_graph.size(weight='weight')
    if sub_graph.size(weight='weight') > resolution_limit:
        above_resolution_limit.add(part)

with open(partition_file, 'w') as f:
    for part in sorted(community_weight.items(), key=operator.itemgetter(1), reverse=True):
        if part[0] not in above_resolution_limit:
            break
        f.write("Community: " + community_names[part[0]] + '\n')
        f.write("Member countries:" + '\n')
        for country in partition_reverse[part[0]]:
            f.write(country_name[country] + '\n')
        f.write('\n')

special_char = u'\u00F4'
special_char = special_char.encode('utf8')
to_rename = {
    "United States of America": "United States",
    "Bolivia": "Bolivia, Plurinational State of",
    "Iran, Islamic Republic of": "Iran",
    "Cote d'Ivoire": "C"+special_char+"te d'Ivoire",
    "Congo, the Democratic Republic of the": "Democratic Republic of Congo",
    "Korea, Democratic People's Republic of": "North Korea",
    "Korea, Republic of": "South Korea",
    "Libyan Arab Jamahiriya": "Libya",
    "Tanzania, United Republic of": "Tanzania",
    "Moldova, Republic of": "Moldova",
    "Macedonia, the former Yugoslav Republic of": "Macedonia"
}
color_list = [1, 11, 7, 3, 10, 9, 6, 4, 0, 2, 5, 8]
with open(display_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["community", "country", "community name"])
    for idx,part in enumerate(sorted(community_weight.items(), key=operator.itemgetter(1), reverse=True)):
        if part[0] not in above_resolution_limit:
            break
        color = color_list.pop(0)
        for country in partition_reverse[part[0]]:
            country2 = country_name[country]
            if country2 in to_rename:
                country2 = to_rename[country2]
            writer.writerow([color+1, country2, idx+1])


print "Program exited successfully"