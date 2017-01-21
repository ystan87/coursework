import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from GDPIn import countries_with_gdp, log_gdp_per_capita
from MigrIn import migration, countries_with_migration
import sys

# only consider countries that have both GDP, population_cell and migration data
if len(sys.argv) < 2:
    print "Invalid input."
    print "Format: python Density.py [year]"
    exit()
year = int(sys.argv[1])
countries_to_consider = countries_with_gdp[year] & countries_with_migration[year]
migrant_nr_kernel = []
for emigrating_country in countries_to_consider:
    for immigrating_country in countries_to_consider:
        if emigrating_country == immigrating_country:
            continue
        migrant_nr = migration[year][emigrating_country][immigrating_country]
        if migrant_nr >= 100:
            migrant_nr_kernel.append((migrant_nr/100, log_gdp_per_capita[year][immigrating_country]-
                                      log_gdp_per_capita[year][emigrating_country]))

sigma = 0.35
precision = 0.01
migrant_nr = [x[0] for x in migrant_nr_kernel]
total = np.sum(migrant_nr)
gdp = [x[1] for x in migrant_nr_kernel]
start = min(gdp)-5*sigma
end = max(gdp)+5*sigma
x = np.linspace(start, end, (end-start)/precision)
kernel_density_estimator = [0] * len(x)
for country_kernel in migrant_nr_kernel:
    # rounding off
    mean = int(country_kernel[1]/precision)*precision
    kernel_density_estimator += country_kernel[0]*1.0/total*norm(mean,sigma).pdf(x)
plt.fill(x, kernel_density_estimator, fc='gray')
plt.xlabel("Relative economic productivity of resident country over country of origin")
plt.ylabel("Probability density function of migrants")
plt.title("Levels of International Migration")
if year == 2000:
    plt.savefig('./../report/Smoothed_Density_Estimator2000.png')
if year == 2010:
    plt.savefig('./../report/Smoothed_Density_Estimator2010.png')
print "Program exited successfully"