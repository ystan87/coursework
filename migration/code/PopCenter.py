import math
from sklearn import linear_model
from haversine import haversine
import matplotlib.pyplot as plt
import numpy as np
from GDPIn import countries_with_gdp, log_gdp_per_capita
from MigrIn import country_name, countries_with_migration, migration
from EuPopCentIn import european_countries_with_pop_cent, europe_population, population, pop_cent
#import powerlaw
from scipy import misc

year = 2000

# only consider countries that have both GDP, population_cell, migration and distance data
countries_to_consider = countries_with_gdp[year] & countries_with_migration[year] & european_countries_with_pop_cent
# for the purpose of this analysis, because the geographical distribution of the total population in Russia
# is heavily inflenced by its distant far east, and does not represent well the distribution of migrants
# within Europe, it is excluded for the data to be more analyzable
countries_to_consider.remove('RUS')
migrant_nr_data = []
log_gdp_per_capita_data = []
null_model = []
distance_data = []
max_migration_factor=0
for emigrating_country in countries_to_consider:
    for immigrating_country in countries_to_consider:
        if emigrating_country == immigrating_country:
            continue
        migrant_nr = migration[year][emigrating_country][immigrating_country]
        weight = population[year][emigrating_country] * population[year][immigrating_country] / europe_population[year]
        migration_factor = migrant_nr*1.0 / weight
        if migration_factor > max_migration_factor:
            max_migration_factor = migration_factor
            max_country_pair = (country_name[emigrating_country], country_name[immigrating_country])
            max_population_pair = (population[year][emigrating_country], population[year][immigrating_country])
            max_migration = migrant_nr
            max_index = len(migrant_nr_data)
        # data for other years not available or need cleaning
        distance = haversine(pop_cent[year][emigrating_country], pop_cent[year][immigrating_country])
        distance_data.append(distance)
        migrant_nr_data.append([migration_factor])
        log_gdp_per_capita_data.append(log_gdp_per_capita[year][immigrating_country] -
                                       log_gdp_per_capita[year][emigrating_country])
        null_model.append(weight)

dist_regr = linear_model.LinearRegression()
# distance correlates negatively with migration
dist_regr.fit([[d,g] for d,g in zip(distance_data,log_gdp_per_capita_data)], migrant_nr_data, null_model)
# removing the counfounding effect of GDP by setting its difference between pairs of countries to 0
migrant_rem_gdp = dist_regr.predict(zip(distance_data, [0] * len(distance_data)))
#fitting_data = []
#for i in range(len(migrant_rem_gdp)):
#    for j in range(len(migrant_rem_gdp[i])):
#        fitting_data.append(distance_data[i])
#fit = powerlaw.Fit(fitting_data)
#print fit.xmin
max_rem_gdp = max(migrant_rem_gdp)
min_rem_gdp = min(migrant_rem_gdp)
total_rem_gdp = np.sum(migrant_rem_gdp)
min_null = min(null_model)
max_null = min(null_model)
total_null = np.sum(null_model)
min_dist = min(distance_data)
#den_rem_gdp = np.sum([migrant_nr_data[i][0] * math.log(distance_data[i] / min_dist) for i in range(len(distance_data))])
#den_null = np.sum([null_model[i] * math.log(distance_data[i] / min_dist) for i in range(len(distance_data))])
den_ratio = np.sum([migrant_nr_data[i][0] / null_model[i] * math.log(distance_data[i] / min_dist)
                      for i in range(len(distance_data))])
num_ratio = np.sum([migrant_nr_data[i][0] / null_model[i] for i in range(len(distance_data))])
# alpha is the exponent of power-law
alpha = 1 + num_ratio / den_ratio
print "The power-law exponent, alpha = ", alpha
slope = -alpha + 1
x_log= np.linspace(math.log(min(distance_data)),  math.log(max(distance_data)), 20)
y_log = [slope * (x - math.log(min_dist)) for x in x_log]
x = [math.exp(a) for a in x_log]
y = [math.exp(a) for a in y_log]
line_pl, = plt.plot(x,y,color='darkred', lw=2, label='Power-law fit for ratio')
x = np.linspace(min(distance_data), max(distance_data), 1e4)
# CCDF is complementary cumulative distribution function
ccdf_rem_gdp = []
ccdf_null = []
ratio = []
for i in range(len(x)):
    j = 0
    for k in range(len(distance_data)):
        if distance_data[k] > x[i]:
            j += migrant_rem_gdp[k]
    ccdf_rem_gdp.append(j / total_rem_gdp)
    for k in range(len(distance_data)):
        if distance_data[k] > x[i]:
            j += null_model[k]
    ccdf_null.append(j / total_null)
    if ccdf_null[-1] > 0:
        ratio.append(ccdf_rem_gdp[-1] / ccdf_null[-1])
    else:
        ratio.append(0)
coef_ratio = np.zeros((10))
for idx,cur in enumerate(ratio):
    coef_ratio[idx/(len(x)/len(coef_ratio))] += cur/(len(x)/len(coef_ratio))
p, q = misc.pade(coef_ratio, 5)
curve_rem_gdp, = plt.plot(x, ccdf_rem_gdp, color='green', label='Migrant number (GDP adjusted)')
curve_null, = plt.plot(x, ccdf_null, color='blue', label='Total migrant population')
curve_ratio, = plt.plot(x, ratio, color='red', label='Ratio of migrant number over population')
plt.yscale('log')
plt.xscale('log')
plt.title('CCDF Fitting Power-law to Populations over Distances')
plt.xlabel('Haversine distance between centers of population in European countries (km)')
plt.ylabel('Proportion of population beyond the distance')
plt.xlim((100, max(distance_data)))
plt.ylim((1e-3, 1.1))
plt.legend(handles=[curve_rem_gdp, curve_null, curve_ratio, line_pl], loc=0, prop={'size':12})
plt.savefig('./../report/ccdf_distance.png')
plt.clf()

print "Program exited successfully"