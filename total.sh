#!/bin/bash

filename="$1"
NUMOFLINES=$(wc -l < "$filename")
COUNTER=1

while read -r line; do
	echo "${COUNTER}/${NUMOFLINES}"
	COUNTER=$[$COUNTER +1]
	name="$line"
	output=$(python collect.py $line)
	if [ -n "$output" ]
	then
		nodejs singleAST.js
		python 2eCount.py $output
	fi
done < $filename

