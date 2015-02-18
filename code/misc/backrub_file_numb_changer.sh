#!/bin/bash
## This script adds a number to the end 
## of the file name
##
## Author: Mehdi Nellen, Tuebingen 2015

## NOTE! This assumes the number in the script is after the first underscore.


# How much to add?
ADD=125
# whats the base name?
STEM="1ogx_scaffold"

for FILE in $( ls | grep "${STEM}*" ); do
    count=1
    for j in $(echo $FILE | tr "_" "\n" ); do
        j=${j%\.pdb}
        if [ $count = 1 ]; then
            
            NFILE="$j"
        elif [ $count = 3 ]; then
            NUM=$( echo "$j + $ADD" | bc )
            NFILE="${NFILE}_0$NUM"
        else
            NFILE="${NFILE}_$j"
        fi
         
        count=$( echo "$count + 1" | bc )
    done
NFILE="${NFILE}.pdb"
# show what happened
echo "changed $FILE to $NFILE"
# move old to new file
mv $FILE $NFILE 
done
