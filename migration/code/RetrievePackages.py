import os
import urllib2
import tarfile

dir_path = os.path.dirname(os.path.realpath(__file__))

target_url = "https://pypi.python.org/packages/f1/5f/1cd2040382f56b21ef731f09fd7a818ad2bbcd5a8201fd2ebd4ec15297bb/" \
             "python-louvain-0.3.tar.gz"
package = urllib2.urlopen(target_url)
output_folder = dir_path + "/../downloads"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
output_path = output_folder + "/python-louvain-0.3.tar.gz"
with open(output_path, 'wb') as output:
    output.write(package.read())

tar_source = output_path
untar_target = output_folder
tar_ref = tarfile.open(tar_source)
tar_ref.extractall(untar_target)
tar_ref.close()

# to install the package in terminal cd to the folder dir_path + '/python-louvain-0.3'
# and enter command
# $ python setup.py install