import urllib2
import os
import zipfile
from threading import Thread
# consulted https://blogs.harvard.edu/rprasad/2014/06/16/reading-excel-with-python-xlrd/
# 50 MB required for download and storage of files

dir_path = os.path.dirname(os.path.realpath(__file__))

target_url = "http://cs.baylor.edu/~hamerly/software/" \
             "europe_population_weighted_centers.txt"
print "downloading from" + target_url
data = urllib2.urlopen(target_url)
output_folder = dir_path + "/../data/Hamerly"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
output_path = output_folder + "/europe_population_weighted_centers.txt"
with open(output_path, 'wb') as output:
    output.write(data.read())

target_url = "http://www.migrationdrc.org/research/typesofmigration/" \
             "Global_Migrant_Origin_Database_Version_4.xls"
print "downloading from" + target_url
data = urllib2.urlopen(target_url)
output_folder = dir_path + "/../data/MigrationDRC"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
output_path = output_folder + "/Global_Migrant_Origin_Database_Version_4.xls"
with open(output_path, 'wb') as output:
    output.write(data.read())

def download_OECD():
    target_url = "http://www.oecd.org/els/mig/DIOC%202010-11Rev4.zip"
    print "downloading from" + target_url
    data = urllib2.urlopen(target_url)
    batch_size = 16 * 1024
    output_folder = dir_path + "/../data/OECD"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = output_folder + "/DIOC__2010-11Rev4.zip"
    with open(output_path, 'wb') as output:
        while True:
            batch = data.read(batch_size)
            if not batch:
                break
            output.write(batch)

t_OECD = Thread(target=download_OECD)
t_OECD.start()
t_OECD.join()
unzip_source = dir_path + "/../data/OECD/DIOC__2010-11Rev4.zip"
unzip_target = dir_path + "/../data/OECD"
extract_folder = "DIOC 2010-11Rev4"
extract_target = "/DIOC_2010_11_File_A_quater_REV.csv"
zip_ref = zipfile.ZipFile(unzip_source, 'r')
zip_ref.extract(extract_folder + extract_target, unzip_target)
zip_ref.close()
old_folder = '/'.join(['OECD', extract_folder])
new_folder = old_folder.replace(" ", "__")
to_path = dir_path + "/../data"
if os.path.exists("/".join([to_path, old_folder])) and not os.path.exists('/'.join([to_path, new_folder])):
    os.rename("/".join([to_path, old_folder]), "/".join([to_path, new_folder]))
    print "download complete"
else:
    print "unable to rename folder. Please make sure folder project-060/data/OECD/DIOC__2010-11Rev4 is there for analysis"
