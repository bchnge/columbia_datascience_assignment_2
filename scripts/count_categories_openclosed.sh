# Produces output showing the number of tickets in each category.
# Largest category on top

SRC=../src
DATA=../data


## Print list of categories and their size and if Open/Closed
# Use reformat.py, cut.py, tail, sort, uniq, sed
# The sed command should be 
# sed -e 's/|Open/&\n/g'

cat $DATA/Case_Data_from_San_Francisco_311.csv \
    | python $SRC/reformat.py \
    | python $SRC/cut.py --delimiter=\| --keep_list=category,status \
    | tail -n +2 \
    | sort --field-separator=\| --key=1 \
    | uniq --count \
    | sed -e 's/|Open/&\n/g'
