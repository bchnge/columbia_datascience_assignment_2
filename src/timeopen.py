#!/usr/bin/env python
from optparse import OptionParser
import sys
import csv
from datetime import datetime
from dateutil.parser import parse

import homework_02.src.common as common

### Constants
SECONDSINADAY = 24 * 60 * 60


def main():
    r"""
    Reads a SF 311 case file, appends a 'timeopen' column giving the time
    (in minutes) a case was open.  Prints to stdout.  
    
    If the case is still
    open, prints the time it has been open.


    Examples
    ---------
    Add a timeopen column to a comma delimited file (that we create with echo)
    $  echo -e 'status,opened,closed\nOpen,12/06/2012,' \
        | python timeopen.py

    Add a timeopen column to a pipe delimited file (that we create with echo)
    $  echo -e 'status|opened|closed\nClosed|12/06/2012|01/01/2013' \
        | python timeopen.py -d \|

    Add a timeopen column to a file and redirect standard output to a new file
    and standard error to a log file
    $ ptyhon timeopen.py  infile.csv  >  outfile.csv 2> logfile
    """
    usage = "usage: %prog [options] dataset"
    usage += '\n'+main.__doc__
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-d", "--delimiter",
        help="Use DELIMITER as the column delimiter.  [default: %default]",
        action="store", dest='delimiter', default=',')
    parser.add_option(
        "-n", "--nowstringing",
        help="String defining current time.  In the format "
        "'MM/DD/YYYY HH:MM XM' where XM is AM or PM and is optional.  "
        "If not given, use the current time [default: %default]",
        action="store", dest='nowstring', default=None)
    parser.add_option(
        "-o", "--outfilename",
        help="Write to this file rather than stdout.  [default: %default]",
        action="store", dest='outfilename', default=None)

    (options, args) = parser.parse_args()

    ### Parse args
    # Only deal with the case of one or no infiles
    assert len(args) <= 1
    infilename = args[0] if args else None

    # Deal with tabs
    if options.delimiter in ['t', '\\t', '\t', 'tab']:
        options.delimiter = '\t'

    ## Get the infile/outfile
    infile, outfile = common.get_inout_files(infilename, options.outfilename)

    ### Call the function that does the real work
    add_timeopen(
        infile, outfile, delimiter=options.delimiter,
        nowstring=options.nowstring)

    ## Close the files iff not stdin, stdout
    common.close_files(infile, outfile)


def add_timeopen(
    infile, outfile, delimiter=',', nowstring=None, errfile=sys.stderr):
    """
    Write later, if module interface is needed.
    """
    # Get the csv reader and writer.  Use these to read/write the files.
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    ## Extract, modify, and write the header
    header = reader.next()
    header.append('timeopen')
    writer.writerow(header)

    # Set a variable called 'now', depending on whether we passed nowstring
    # or not.  Try using 'parse'

    ## Get the indicies corresponding to columns that are needed to make
    ## timeopen

    ## Iterate through the file, add timeopen to each row, print
    for row in reader:
        try:
            pass
            # Get timeopen by calling _get_timeopen, write the new row
        except common.BadDataError as e:
            # write an error message
            pass


def _get_timeopen(row, status_idx, opened_idx, closed_idx, now):
    """
    Returns the time a ticket has been open.

    Parameters
    ----------
    row : List
        A row from the file
    status_idx, opened_idx, closed_idx : Integers
        The indices of status, opened, closed
    now : datetime.datetime object
        Gives the current time
    """
    # Call _checkstatus.  Exception will be raised if status is wrong.
    # It will be caught up one level.


def _checkstatus(status, opendate, closedate, row):
    """
    We should see closedate if and only if status == 'Closed'.  

    Also check to make sure status is either Open or Closed.

    If things are ok, do nothing, if not ok, raise an exception with an
    error message attached

    Notes to students:
    Cycle through the possible conditions.  The error message is:
    message = 'BadDataError.  Bad status. row = %s\n' % row
    """
    # Start out by setting 'allok = True' then cycle through conditions
    # under which you may have to set 'allok = False'
    allok = True

    # if not allok raise an exception and give an error message
    if not allok:
        pass


def _get_timeopen_closedticket(opendate, closedate):
    """
    For a ticket that is closed, returns the time a ticket was open in seconds
    by subtracting opendate from closedate.

    Parameters
    ---------=
    opendate : String
        MM/DD/YYYY HH:MM XM
    closedate : String
        MM/DD/YYYY HH:MM XM
    """
    # Convert opendate and closedate to datetime objects. Use 'parse'


def _get_timeopen_openticket(opendate, now):
    """
    For a ticket that is still open, returns the time a ticket was open in
    seconds by subtracting opendate from the current date.

    Parameters
    ---------=
    opendate : String
        MM/DD/YYYY HH:MM XM, where XM is AM or PM and is optional
    now : datetime.datetime object
        Gives the current time
    """
    # Convert opendate to a datetime object


    


if __name__=='__main__':
    main()


