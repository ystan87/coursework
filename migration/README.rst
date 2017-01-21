:Title:
    Dynamics of International Migration
:Author:
    F16-DG-4074, Yee Sern Tan, yeestan@indiana.edu
:Project Type:
    Analytics

**Problem Description**

Analyze major trends in international migration

**Requirements**

- The programs installed on the VM for this course will suffice.
- Python version 2.7.12 is used, to be invoked with command 'python'
- Disk space of 100 MB is required.

**Running**

The completion of each previous step is necessary for running the next step. These steps are necessary:

1. Open Terminal, and cd to the folder to work on.
2. git clone https://gitlab.com/cloudmesh_fall2016/project-060.git

    This will require the username and password to download

3. cd ./project-060

    The following will install the required packages for python
    
4. bash install.sh

    The following will prompt download of data for analysis

5. bash download.sh

    The following will perform the commands to process the data

6. bash analyze.sh

    The next step, for visualization is optional, and may introduce errors, 
    especially when it is performed twice. If possible, open all visualizations
    in one run of the script.

7. bash visualization.sh

There is an interactive element to be loaded with a browser: key in 1, 2 or 3 for various visualizations; 0 to exit.

If step 7 has exited, and you wish to view the visualization, enter the following:

cd ./code

    followed by any of the following:

python open_immigration.py

python open_emigration.py

python open_community.py

**Report**

The report can be obtained at

- project-060/report/report.pdf

The following files are used to generate the report

- project-060/report/report.tex 
- project-060/report/report.bib 
- project-060/report/acm_proc_article-sp.cls

**Artifacts**

Some files with arranged data are generated as artifacts of this analysis. They include:

partition of countries into 12 largest communities (some have been omitted)

- project-060/report/supplementary_material.txt

country pairs with bidirectional migration ordered in descending order

- project-060/data/LargestBidirectional.csv

immigrating-emigrating country pairs with positive net migration, ordered in descending order

- project-060/data/LargestNetMigration.csv

immigrating-emigrating country pairs with migration rate in descending order

- project-060/data/LargestMigrationRate.csv

**Acknowledgments**

The availability of migration data by OECD, World Bank and United Nations, and that of python programming language and many open source packages enabled this project. The author is very much helped by online sources, on areas including getting contents from spreadsheets [1]  , loading html file from python [2] , selecting colors for communities within the world map [3]. The visualization using D3.js is modified from the template by VIDA [4].

**References**

1. Website: https://blogs.harvard.edu/rprasad/2014/06/16/reading-excel-with-python-xlrd/

2. Website: http://stackoverflow.com/questions/10752055/cross-origin-requests-are-only-supported-for-http-error-when-loading-a-local

3. Website: http://stackoverflow.com/questions/470690/how-to-automatically-generate-n-distinct-colors

4. Website: https://vida.io/gists/TWNbJrHvRcR3DeAZq

@TechReport{project-060,
  author =     {Tan, Yee Sern},
  title =      {{Dynamics of International Migration}},
  institution =  {Indiana University},
  year =       2016,
  type =       {Project},
  number =     {project-060},
  address =    {Bloomington, IN 47408, U.S.A.},
  month =      dec,
  url={https://gitlab.com/cloudmesh_fall2016/project-060/blob/master/report/report.pdf}
}