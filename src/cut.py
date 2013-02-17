#!/usr/bin/env python
from optparse import OptionParser
import sys
import csv
import pdb

import homework_02.src.common as common


def main():
    r"""
    Reads a csv file, keeping only certain columns.  Prints to stdout.

    Examples
    ---------
    Read a comma delimited csv file, data.csv, keep the 'name' column
    $ python cut.py -l name,age test/commafile.csv

    Use a tab delimited dataset 
    $ python cut.py -d'\t' -l name  test/tabfile.csv
    Note that -dt  -dtab -d\t -d'\t' -d\\t  also work
    """
    usage = "usage: %prog [options] dataset"
    usage += '\n'+main.__doc__
    parser = OptionParser(usage=usage) # Creating OptionParser 'parser'
    parser.add_option(
        "-l", "--keep_list",
        help="Only keep variables in this (comma delimited) list."
        " [default: %default] ",
        action="store", dest='keep_list', default=None)
    parser.add_option(
        "-d", "--delimiter",
        help="Use DELIMITER as the column delimiter.  [default: %default]",
        action="store", dest='delimiter', default=',')
    parser.add_option(
        "-o", "--outfilename",
        help="Write to this file rather than stdout.  [default: %default]",
        action="store", dest='outfilename', default=None)

    pdb.set_trace()
    (options, args) = parser.parse_args()

    ### Parse args
    # Raise an exception if the length of args is greater than 1
    assert len(args) <= 1
    # If an argument is given, then it is the 'infilename'
    # If no arguments are given, set infilename equal to None
    infilename = args[0] if args else None

    ## Handle the options
    # Change keep_list to a Python list
    keep_list = options.keep_list.split(',') if options.keep_list else None

    # Deal with tabs
    if options.delimiter in ['t', '\\t', '\t', 'tab']:
        options.delimiter = '\t'

    ## Get the infile/outfile
    infile, outfile = common.get_inout_files(infilename, options.outfilename)

    ## Call the function that does the real work
    cut_file(infile, outfile, delimiter=options.delimiter, keep_list=keep_list)

    ## Close the files iff not stdin, stdout
    common.close_files(infile, outfile)


def cut_file(infile, outfile, delimiter=',', keep_list=None):

    # pdb.set_trace()

    """
    Write later, if module interface is needed.
    """

    """
    Current status: no tests pass. Will rewrite using different method,
    creating index using for loop on old header comparing to keep_list,
    creating a list of indexes of items to keep per line, and iterating
    through lines keeping only items at those indices in the list spat out by
    reader.
    """

    ## Get the csv reader and writer.  Use these to read/write the files.
    reader = csv.reader(infile, delimiter=delimiter)
    writer = csv.writer(outfile, delimiter=delimiter)

    ## Extract the first row of the file
    old_header = reader.next()

    ## Get and write the new header
    if keep_list is None: # If keep_list is None, treat as though empty
        keep_list = []

    writer.writerow(keep_list)

    ## Get the indices in the file that we will keep
    keep_index = []
    for item in keep_list:
        item_pos = old_header.index(item)
        keep_index.append(item_pos)


    ## Iterate through the file, printing out the reformatted lines
    for old_row in reader:
        new_row = []
        for i in keep_index:
            new_row.append(old_row[i])
        writer.writerow(new_row)


    ## pass just means "do nothing".  Remove it from your final version.



if __name__=='__main__':
    main()

