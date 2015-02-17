#!/bin/bash
## script which generates profit script

IND=$( cat $3 | sed -n -e 's/^index = //p' )


echo "reference $1"
FILES=${2}/*
for f in $FILES ; do
    echo "mobile $f"
    echo "QUIET ON"
    echo "align" 
    echo "ATOMS CA"
    echo "fit"
    for i in $IND; do
        echo "RZONE ${i}-${i}" 
    done
    echo "RATOMS CA"
    echo "QUIET OFF"
    echo "##$f"
    echo "RMS"
    done

