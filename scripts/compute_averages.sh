#!/bin/bash
# Script for computing averages of the dataset

SRC=../src
DATA=../data

# Compute average timeopen for different categories (field 8), status (field 4)
# Use cat, reformat.py, timeopen.py, sort, sort, averager.py
# You will have to use the body utility in conjunction with something
#

cat $DATA/Case_Data_from_San_Francisco_311.csv \
    | python $SRC/reformat.py \
    | python $SRC/timeopen.py -d \| \
    | python $SRC/cut.py -d \| -l category,status,timeopen \
    | body sort --ignore-case --field-separator=\|  --key=1,2 \
    | python $SRC/averager.py -d \| --key=category,status --fieldnames=timeopen
