import math
from sklearn import linear_model
import matplotlib.pyplot as plt
from MigrIn import countries_with_migration, migration, country_name
from GDPIn import countries_with_gdp, log_gdp_per_capita
from PopulationIn import countries_with_population, population, world_population
from GiniIn import countries_with_gini, gini
import sys

if len(sys.argv) < 2:
    print "Invalid input."
    print "Format: python WealthEquality.py [year]"
    exit()
year = int(sys.argv[1])

# only consider countries that have both GDP, population_cell and migration data
countries_to_consider = countries_with_gdp[year] & countries_with_migration[year] & countries_with_population
countries_to_consider_gini = countries_to_consider & countries_with_gini
has_gini = False

gdp_regr = linear_model.LinearRegression()
gini_regr = linear_model.LinearRegression()
migration_rate_data = []
log_gdp_per_capita_data = []
weight_of_data = []
gini_data = []
migrant_nr_gini = []
weight_gini = []
gdp_gini = []
max_migration_factor=0
for emigrating_country in countries_to_consider:
    for immigrating_country in countries_to_consider:
        if emigrating_country == immigrating_country:
            continue
        migrant_nr = migration[year][emigrating_country][immigrating_country]
        if migrant_nr == 0:
            continue
        weight = population[emigrating_country] * population[immigrating_country]
        migration_rate = migrant_nr * world_population * 1.0 / weight
        if emigrating_country in countries_to_consider_gini and immigrating_country in countries_to_consider_gini:
            has_gini = True
            migrant_nr_gini.append(migration_rate)
            weight_gini.append(weight)
            gini_data.append(gini[immigrating_country] - gini[emigrating_country])
            gdp_gini.append(log_gdp_per_capita[year][immigrating_country]-log_gdp_per_capita[year][emigrating_country])
        # only consider countries with significant migration data
        #if math.fabs(migration_rate) < 1*10**(-9) or migrant_nr < 5000:
        #    continue
        if migration_rate > max_migration_factor:
            max_migration_factor = migration_rate
            max_country_pair = (country_name[emigrating_country], country_name[immigrating_country])
            max_population_pair = (population[emigrating_country], population[immigrating_country])
            max_migration = migrant_nr
            max_index = len(migration_rate_data)
        migration_rate_data.append([migration_rate])
        log_gdp_per_capita_data.append([log_gdp_per_capita[year][immigrating_country]-
                                        log_gdp_per_capita[year][emigrating_country]])
        weight_of_data.append(weight)
num_entries = len(migration_rate_data)
gdp_regr.fit(log_gdp_per_capita_data, migration_rate_data, weight_of_data)

if has_gini:
    gini_scale = (max(gini_data)-min(gini_data))/(max(gdp_gini)-min(gdp_gini))
    gdp_gini = [gdp/gini_scale for gdp in gdp_gini]
    gini_regr.fit([[gdp, gini]for gdp, gini in zip(gdp_gini, gini_data)], migrant_nr_gini, weight_gini)

    print "There is observed a slight negative correlation between migration numbers and Gini coefficient"
    print "Ratio of effect of GDP to Gini coefficient on migration ", math.fabs(gini_regr.coef_[0]/gini_regr.coef_[1])

# Datum highest on the migration rate score, this rate is more than 3 times that of the second
print 'The maximal migration rate is observed from %s to %s' % max_country_pair
print 'Their respective populations are %d and %d' % max_population_pair
print 'The number of migrants is %d' % max_migration

fig = plt.figure()
weight_scale = math.sqrt(max(weight_of_data))/100
plt.subplot(121)
plt.scatter(log_gdp_per_capita_data, migration_rate_data,
            [math.sqrt(weight)/weight_scale for weight in weight_of_data], color='purple')
plt.plot(log_gdp_per_capita_data, gdp_regr.predict(log_gdp_per_capita_data), color='green',linewidth=3)
plt.axvline(x=0, color='yellow', linewidth=1)

plt.ylim((0, max(migration_rate_data)[0]))
plt.ylabel('Migration rate')
plt.xlabel('Log-scale GDP per capita difference')
plt.title("International Migration Rate")

plt.subplot(122)
plt.scatter(log_gdp_per_capita_data, migration_rate_data,
            [math.sqrt(weight)/weight_scale for weight in weight_of_data], color='purple')
plt.plot(log_gdp_per_capita_data, gdp_regr.predict(log_gdp_per_capita_data), color='green',linewidth=3)
plt.axvline(x=0, color='yellow', linewidth=1)

plt.ylim((0, max(migration_rate_data)[0]/100))
#plt.ylabel('Migration rate (zoom-in factor of 100)')
plt.xlabel('Log-scale GDP per capita difference')
plt.title("Zoom-in factor of 100")

if year == 2000:
    fig.savefig('./../report/GDP_regression_2000.png')
else:
    fig.savefig('./../report/GDP_regression_2010.png')

#plt.show()
plt.clf()

num_deleted = 0
migration_rate_data_trunc=[]
log_gdp_per_capita_data_trunc=[]
weight_of_data_trunc=[]

if year == 2010:
    print "Program exited successfully"
    exit()

for idx,rate_data in enumerate(migration_rate_data):
    rate = rate_data[0]
    if rate > 0.15:
        num_deleted += 1
    else:
        migration_rate_data_trunc.append(rate)
        log_gdp_per_capita_data_trunc.append(log_gdp_per_capita_data[idx])
        weight_of_data_trunc.append(weight_of_data[idx])

print "Number of entries removed in the truncated figure (factor of 20,000) ", num_deleted, \
    " out of ", len(migration_rate_data)
weight_scale *= max(weight_of_data)*2e-10
# zoom in
plt.scatter(log_gdp_per_capita_data_trunc, migration_rate_data_trunc,
            [weight/weight_scale for weight in weight_of_data_trunc], color='purple')
line_reg, = plt.plot(log_gdp_per_capita_data, gdp_regr.predict(log_gdp_per_capita_data), color='green',lw=3,
                    label='regression line')
plt.axvline(x=0, color='yellow', linewidth=1)

plt.ylim((0, max(migration_rate_data_trunc)))
plt.title("Zoomed-in View of Migration Sizes")
plt.ylabel('Migration rate (zoom-in factor of 20,000)')
plt.xlabel('Log-scale GDP per capita difference')
plt.legend(handles=[line_reg], loc=0)

fig.savefig('./../report/GDP_regression_zoom_2000.png')

print "Program exited successfully"