#!/bin/bash
FILES=submissions/*.py
for a in $FILES
do
	for b in $FILES
	do
		aFilePath=${a[0]%%.*}
		aFile=${aFilePath##*/}
		
		bFilePath=${b[0]%%.*}
		bFile=${bFilePath##*/}
		
		if [ "$aFile" != "__init__" ] && [ "$bFile" != "__init__" ];
		then
			#echo $aFile $bFile
			python negotiator_framework.py submissions.$aFile $aFile submissions.$bFile $bFile sample_scenario2.csv
		fi
	done
done
