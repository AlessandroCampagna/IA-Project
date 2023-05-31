#!/bin/bash

pip install numpy

for infile in ins/*.txt; do
    basename=${infile%.*}
    time python3 bimaru.py < $infile > $basename.output
    diff $basename.output $basename.out > $basename.diff

    if [[ $? == "0" ]]
    then 
        echo -e "> $basename \e[1;32mpassed\e[0m 🟢"
    else 
        cat $basename.diff
        echo -e "> $basename \e[1;31mfailed\e[0m ❌"
    fi

    echo ""

    rm $basename.output
    rm $basename.diff
done

echo ""
echo "Total: "