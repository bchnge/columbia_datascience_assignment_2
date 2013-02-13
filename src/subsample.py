#!/usr/bin/env python
from optparse import OptionParser
import sys
import csv
from numpy.random import rand
from numpy.random import seed as randomseed

import homework_02.src.common as common


def main():
    r"""
    DESCRIPTION
    -----------
    Subsample files or stdin and write to stdout.


    NOTES
    -----
    Assumes the first row is a header.


    EXAMPLES
    ---------
    Subsample a comma delimited dataset and redirect output to a new file
    $ python subsample.py data.csv > subsampled_data.csv

    Subsample, keeping only 10% of rows
    $ python subsample.py -r 0.1 data.csv

    """
    usage = "usage: %prog [options] dataset"
    usage += '\n'+main.__doc__
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-r", "--subsample_rate",
        help="Subsample subsample_rate, 0 <= r <= 1.  E.g. r = 0.1 keeps 10% "
        "of rows. [default: %default] ",
        action="store", dest='subsample_rate', type=float, default=0.01)
    parser.add_option(
        "-d", "--delimiter",
        help="Use DELIMITER as the column delimiter.  [default: %default]",
        action="store", dest='delimiter', default=',')
    parser.add_option(
        "-s", "--seed",
        help="Integer to seed the random number generator with. "
        "[default: %default] ",
        action="store", dest='seed', type=int, default=None)
    parser.add_option(
        "-o", "--outfilename",
        help="Write to this file rather than stdout.  [default: %default]",
        action="store", dest='outfilename', default=None)

    (options, args) = parser.parse_args()

    ### Parse args
    # Raise an exception if the length of args is greater than 1
    assert len(args) <= 1
    # If an argument is given, then it is the 'infilename'
    # If no arguments are given, set infilename equal to None
    infilename = args[0] if args else None

    ## Handle the options
    # Deal with tabs
    if options.delimiter in ['t', '\\t', '\t', 'tab']:
        options.delimiter = '\t'

    ## Get the infile/outfile
    infile, outfile = common.get_inout_files(infilename, options.outfilename)

    ## Call the function that does the real work
    subsample(
        infile, outfile, options.subsample_rate, options.delimiter,
        options.seed)

    ## Close the files iff not stdin, stdout
    common.close_files(infile, outfile)


def subsample(infile, outfile, subsample_rate=0.01, delimiter=',', seed=None):
    """
    Write later, if module interface is needed.
    """
    ## Seed the random number generator for deterministic results
    if seed:
        randomseed(seed)

    ## Get the csv reader and writer.  Use these to read/write the files.
	outfile=csv.writer(csvfile, delimiter=' ')
	infile=csv.reader(csvfile, delimiter=' ')

    ## Extract and write the header
	first_line = infile.readline()  	
	#first_line = infile.split('\n', 1)[0]
	outfile.writerow(first_line)
		

    ## Iterate through the file and print a selection of rows
	#cat inline | body sort -k1,1
	no_rows = 0
	for row in infile:
		no_rows += 1

	end_iter = no_rows*subsample_rate+1

	from itertools import *
	for i in inslice(infile, 2, end_iter):
		outfile.writerow(i)
	

if __name__=='__main__':
    main()
