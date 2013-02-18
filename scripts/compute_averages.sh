#!/bin/bash
# Script for computing averages of the dataset

SRC=../src
DATA=../data

# Compute average timeopen for different categories (field 8), status (field 4)
# Use cat, reformat.py, timeopen.py, sort, sort, averager.py
# You will have to use the body utility in conjunction with something
#

head -n 1000 $DATA/Case_Data_from_San_Francisco_311.csv \
    | python $SRC/reformat.py \
    | python $SRC/timeopen.py -d \| \
    | body sort --field-separator=\| -k4 -k8 \
    | python $SRC/averager.py -d \| --key=status,category --fieldnames=timeopen
