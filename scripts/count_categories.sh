# Produces output showing the number of tickets in each category.
# Largest category on top

SRC=../src
DATA=../data


## Print list of categories and their size
# Use cat, reformat.py, cut.py, tail, sort, uniq, sort
#


cat $DATA/Case_Data_from_San_Francisco_311.csv \
    | python $SRC/reformat.py \
    | python $SRC/cut.py -d \| -l category \
    | tail -n +2 \
    | sort -k1 \
    | uniq -c \
    | sort -r -n -k1

