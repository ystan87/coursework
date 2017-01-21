#!/bin/bash
cwd=$(pwd)
loaded=0
val=1
while [ $val -ne 0 ]; do
	echo "Welcome to visualization."
	echo "Upon request, an interactive browser window will open."
	echo "To display GDP correlation of immigration, key in 1"
	echo "To display GDP correlation of emigration, key in 2"
	echo "To display communities of migration, key in 3"
	echo "To quit, key in 0"
	read val
	if [ "$val" -eq 1 ]; then
		if [ "$loaded" -eq 0 ]; then
			cd ./display
			python -m SimpleHTTPServer &
			loaded=1
			cd $cwd
		fi
		cd ./code
		python open_immigration.py
		cd $cwd
	elif [ "$val" -eq 2 ]; then
		if [ "$loaded" -eq 0 ]; then
			python -m SimpleHTTPServer &
			loaded=1
			cd $cwd
		fi
		cd ./code
		python open_emigration.py
		cd $cwd
	elif [ "$val" -eq 3 ]; then
		if [ "$loaded" -eq 0 ]; then
			python -m SimpleHTTPServer &
			loaded=1
			cd $cwd
		fi
		cd ./code
		python open_community.py
		cd $cwd
	elif [ "$val" -ne 0 ]; then
		echo "Invalid input. Please try again."
		echo ""
	fi
done
