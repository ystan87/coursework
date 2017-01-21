#!/bin/bash
cd ./code
echo "Running WealthEquality.py 2000"
python WealthEquality.py 2000
echo "Running WealthEquality.py 2010"
python WealthEquality.py 2010
echo "Running Density.py 2000"
python Density.py 2000
echo "Running Density.py 2010"
python Density.py 2010
echo "Running PopCenter.py"
python PopCenter.py
echo "Running GDPPredictorStrength.py"
python GDPPredictorStrength.py
echo "Running CommunityPartition.py"
python CommunityPartition.py
echo "Running ArrangeMigration.py"
echo "This may take a few minutes to write to file"
python ArrangeMigration.py
