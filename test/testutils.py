import unittest
from StringIO import StringIO
import sys
from numpy.testing import assert_allclose
from datetime import datetime

import homework_02.src.common as common
from homework_02.src.common import BadDataError
import homework_02.src.cut as cut
import homework_02.src.reformat as reformat
import homework_02.src.averager as averager
import homework_02.src.timeopen as timeopen
import homework_02.src.subsample as subsample


"""
Tests for the homework 2 utils.  To run, from the test/ directory, type:
$ python -m unittest testutils

OR for verbose output
$ python -m unittest -v testutils

OR to run only the methods in TestCut
$ python -m unittest testutils.TestCut

OR to run only the TestCut.test_cut_file_keepname method
$ python -m unittest testutils.TestCut.test_cut_file_keepname
"""


class TestSubsample(unittest.TestCase):
    """
    Tests the subsampler
    """
    def setUp(self):
        self.outfile = StringIO()
        commastr = 'name,age,weight\nian,1,11\ndaniel,2,22\nchang,3,33'
        pipestr = 'name|age|weight\nian|1|11\ndaniel|2|22\nchang|3|33'
        self.commafile = StringIO(commastr)
        self.pipefile = StringIO(pipestr)
        self.seed = 1234

    def test_r0p0_comma(self):
        subsample.subsample(
            self.commafile, self.outfile, subsample_rate=0.0, seed=self.seed)
        result = self.outfile.getvalue()
        benchmark = 'name,age,weight\r\n'
        self.assertEqual(result, benchmark)

    def test_r0p5_comma(self):
        subsample.subsample(
            self.commafile, self.outfile, subsample_rate=0.5, seed=self.seed)
        result = self.outfile.getvalue()
        benchmark = 'name,age,weight\r\nian,1,11\r\nchang,3,33\r\n'
        self.assertEqual(result, benchmark)

    def test_r0p5_pipe(self):
        subsample.subsample(
            self.pipefile, self.outfile, subsample_rate=0.5, seed=self.seed)
        result = self.outfile.getvalue()
        benchmark = 'name|age|weight\r\nian|1|11\r\nchang|3|33\r\n'
        self.assertEqual(result, benchmark)

    def tearDown(self):
        self.outfile.close()


class TestCut(unittest.TestCase):
    """
    Tests the implementation (but not the interface) of cut.py
    """
    def setUp(self):
        self.outfile = StringIO()

        commastring = \
        "name,age,weight\r\nian,1,11\r\ndaniel,2,22\r\nchang,3,33"
        self.commafile = StringIO(commastring)

        pipestring = \
        "name|age|weight\r\nian|1|11\r\ndaniel|2|22\r\nchang|3|33"
        self.pipefile = StringIO(pipestring)

    def test_cut_file_keepname(self):
        cut.cut_file(self.commafile, self.outfile, keep_list=['name'])
        result = self.outfile.getvalue()
        self.assertEqual('name\r\nian\r\ndaniel\r\nchang\r\n', result)

    def test_cut_file_keepnameage(self):
        cut.cut_file(self.commafile, self.outfile, keep_list=['name', 'age'])
        result = self.outfile.getvalue()
        self.assertEqual('name,age\r\nian,1\r\ndaniel,2\r\nchang,3\r\n', result)

    def test_cut_file_keepagename(self):
        cut.cut_file(self.commafile, self.outfile, keep_list=['age', 'name'])
        result = self.outfile.getvalue()
        self.assertEqual('age,name\r\n1,ian\r\n2,daniel\r\n3,chang\r\n', result)

    def test_cut_file_keepagename_pipe(self):
        cut.cut_file(
            self.pipefile, self.outfile, keep_list=['age', 'name'],
            delimiter='|')
        result = self.outfile.getvalue()
        self.assertEqual('age|name\r\n1|ian\r\n2|daniel\r\n3|chang\r\n', result)

    def test_cut_file_keepempty(self):
        """
        Test keeping no columns
        """
        cut.cut_file(self.commafile, self.outfile, keep_list=[])
        result = self.outfile.getvalue()
        self.assertEqual('\r\n\r\n\r\n\r\n', result)

    def test_cut_file_keepNone(self):
        """
        Test keeping no columns
        """
        cut.cut_file(self.commafile, self.outfile, keep_list=None)
        result = self.outfile.getvalue()
        self.assertEqual('\r\n\r\n\r\n\r\n', result)

    def tearDown(self):
        self.outfile.close()


class TestReformat(unittest.TestCase):
    """
    Tests reformat utility
    """
    def setUp(self):
        self.outfile = StringIO()
        self.errfile = StringIO()

        self.headerstr = \
            'Case ID,Opened,Closed,Status,Work Status,Responsible Agency'
        self.headerfile = StringIO(self.headerstr)

        self.datafile = (
            'Address,Category\n'
            'Intersection of | 25TH ST and FOLSOM ST,Street Cleaning\n'
            '"1620 MONTGOMERY ST, SAN FRANCISCO, CA, 94111",Streetlights\n'
            '"19 CORTLAND AVE, SAN FRANCISCO, CA, 94110",Street Cleaning\n'
            '"1482 MASONIC AVE, SAN FRANCISCO, CA, 94117",Abandoned Vehicle\n'
            'Intersection of COLUMBUS | AVE and FRANCISCO ST,Street Defects\n')

    def test_reformat_header(self):
        headerlist = self.headerstr.split(',')
        result = reformat._reformat_header(headerlist)
        benchmark = [
            'case_id', 'opened', 'closed', 'status', 'work_status',
            'responsible_agency']
        self.assertEqual(result, benchmark)

    def test_reformat_emptyheader(self):
        headerlist = []
        result = reformat._reformat_header(headerlist)
        self.assertEqual(result, [])

    def test_reformat_item(self):
        item = 'hello  | , | goodbye '
        result = reformat._reformat_item(item)
        self.assertEqual(result, 'hello   ,  goodbye ')

    def test_reformat_emptyitem(self):
        item = ''
        result = reformat._reformat_item(item)
        self.assertEqual(result, '')

    def test_checkrowlength_good(self):
        row = ['a', 'b']
        reformat._checkrowlength(row, 1, 2)

    def test_checkrowlength_bad(self):
        row = ['a', 'b', 'c']
        args = (row, 1, 2)
        self.assertRaises(BadDataError, reformat._checkrowlength, *args)

    def test_reformat_headerpart(self):
        infile = StringIO(self.datafile)
        reformat.reformat(infile, self.outfile)
        rows = self.outfile.getvalue().split('\r\n')
        header = rows[0]
        self.assertEqual(header, 'address|category')

    def test_reformat_piperow(self):
        infile = StringIO(self.datafile)
        reformat.reformat(infile, self.outfile)
        rows = self.outfile.getvalue().split('\r\n')
        piperow = rows[1]
        benchmarkpiperow = \
            'Intersection of  25TH ST and FOLSOM ST|Street Cleaning'
        self.assertEqual(piperow, benchmarkpiperow)

    def test_reformat_countrows(self):
        infile = StringIO(self.datafile)
        reformat.reformat(infile, self.outfile)
        rows = self.outfile.getvalue().split('\r\n')
        # This includes the last empty row
        benchmarknumrows = 7
        self.assertEqual(len(rows), benchmarknumrows)

    def test_reformat_badrowlength(self):
        # The second row will have the wrong length
        datafile = (
            'Address,Category\n'
            'fakeaddress,fakecategory,extraentry')
        infile = StringIO(datafile)
        reformat.reformat(infile, self.outfile, errfile=self.errfile)
        errstr = self.errfile.getvalue()
        benchmarkerror = \
            "BadDataError. 3 items in row 0.  Should have been 2. "\
            "Row = ['fakeaddress', 'fakecategory', 'extraentry']\n"
        self.assertEqual(errstr, benchmarkerror)

    def test_reformat_allrows(self):
        infile = StringIO(self.datafile)
        reformat.reformat(infile, self.outfile)
        outstr = self.outfile.getvalue()
        benchoutstr = \
            'address|category\r\nIntersection of  25TH ST and FOLSOM ST|'\
            'Street Cleaning\r\n1620 MONTGOMERY ST, SAN FRANCISCO, CA, 94111'\
            '|Streetlights\r\n19 CORTLAND AVE, SAN FRANCISCO, CA, 94110|'\
            'Street Cleaning\r\n1482 MASONIC AVE, SAN FRANCISCO, CA, 94117|'\
            'Abandoned Vehicle\r\nIntersection of COLUMBUS  AVE and '\
            'FRANCISCO ST|Street Defects\r\n'
        self.assertEqual(outstr, benchoutstr)

    def tearDown(self):
        self.outfile.close()
        self.errfile.close()


class TestAverager(unittest.TestCase):
    """
    Tests average utility
    """
    def setUp(self):
        self.outfile = StringIO()
        self.group = [[1, 2, 3], [4.3, 5.2, 6.9], [7.1, 8.8, 9.11]]

        commastr = "a,b,c\n1,2,3\n1,3,4\n11,22,33"
        self.commafile = StringIO(commastr)

        pipestr = "a|b|c\n1|2|3\n1|3|4\n11|22|33"
        self.pipefile = StringIO(pipestr)

    def test_average_bcomma(self):
        averager.average(
            self.commafile, self.outfile, key=['a'], fieldnames=['b'])
        result = self.outfile.getvalue()
        benchmark = 'key,b_ave\r\n1,2.5\r\n11,22.0\r\n'
        self.assertEqual(result, benchmark)

    def test_average_bcpipe(self):
        averager.average(
            self.pipefile, self.outfile, key=['a'], fieldnames=['b', 'c'],
            delimiter='|')
        result = self.outfile.getvalue()
        benchmark = 'key|b_ave|c_ave\r\n1|2.5|3.5\r\n11|22.0|33.0\r\n'
        self.assertEqual(result, benchmark)

    def test_average_accomma(self):
        averager.average(
            self.commafile, self.outfile, key=['a'], fieldnames=['a', 'b', 'c'])
        result = self.outfile.getvalue()
        benchmark = \
            'key,a_ave,b_ave,c_ave\r\n1,1.0,2.5,3.5\r\n11,11.0,22.0,33.0\r\n'
        self.assertEqual(result, benchmark)

    def test_get_group_ave_all(self):
        field_idx = [0, 1, 2]
        result = averager._get_group_ave(self.group, field_idx)
        benchmark = [4.133333333333333, 5.333333333333333, 6.336666666666666]
        assert_allclose(result, benchmark, atol=1e-5)

    def test_get_group_ave_1(self):
        field_idx = [1]
        result = averager._get_group_ave(self.group, field_idx)
        benchmark = [5.333333333333333]
        assert_allclose(result, benchmark, atol=1e-5)

    def test_get_group_ave_12(self):
        field_idx = [0, 1]
        result = averager._get_group_ave(self.group, field_idx)
        benchmark = [4.133333333333333, 5.333333333333333]
        assert_allclose(result, benchmark, atol=1e-5)

    def test_get_group_ave_20(self):
        field_idx = [2, 0]
        result = averager._get_group_ave(self.group, field_idx)
        benchmark = [6.336666666666666, 4.133333333333333]
        assert_allclose(result, benchmark, atol=1e-5)

    def test_get_group_ave_empty(self):
        field_idx = []
        result = averager._get_group_ave(self.group, field_idx)
        benchmark = []
        assert_allclose(result, benchmark, atol=1e-5)


    def tearDown(self):
        self.outfile.close()


class TestTimeOpen(unittest.TestCase):
    """
    Tests timeopen utility
    """
    def setUp(self):
        self.outfile = StringIO()
        self.errfile = StringIO()
        self.opendate = '12/31/2012 11:35 PM'
        self.closedate = '01/01/2013 12:00 AM'

    def test_add_timeopen(self):
        nowstring = '02/01/2013'
        infilestr = 'status|opened|closed|updated\n'\
            'Open|12/06/2012 12:28 AM||12/06/2012\n'\
            'Closed|12/06/2012 12:50 AM|12/10/2012 02:24 PM|12/10/2012\n'\
            'Closed|12/06/2012 12:04 AM|12/11/2012 04:47 PM|12/11/2012'
        infile = StringIO(infilestr)

        timeopen.add_timeopen(
            infile, self.outfile, delimiter='|', nowstring=nowstring)
        result = self.outfile.getvalue()

        benchmarkresult = 'status|opened|closed|updated|timeopen\r\n'\
        'Open|12/06/2012 12:28 AM||12/06/2012|4923120\r\n'\
        'Closed|12/06/2012 12:50 AM|12/10/2012 02:24 PM|12/10/2012|394440\r\n'\
        'Closed|12/06/2012 12:04 AM|12/11/2012 04:47 PM|12/11/2012|492180\r\n'
        self.assertEqual(result, benchmarkresult)

        infile.close()

    def test_add_timeopen_badticket1(self):
        # Closed with no close date
        infilestr = 'status,opened,closed\n'\
            'Closed,12/06/2012,,'
        infile = StringIO(infilestr)
        timeopen.add_timeopen(infile, self.outfile, errfile=self.errfile)
        benchmarkerror = \
            "BadDataError.  Bad status. "\
            "row = ['Closed', '12/06/2012', '', '']\n"
        self.assertEqual(self.errfile.getvalue(), benchmarkerror)

    def test_add_timeopen_badticket2(self):
        # Open with a close date
        infilestr = 'status,opened,closed\n'\
            'Open,12/06/2012,12/07/2012,'
        infile = StringIO(infilestr)
        timeopen.add_timeopen(infile, self.outfile, errfile=self.errfile)
        benchmarkerror = \
            "BadDataError.  Bad status. row = "\
            "['Open', '12/06/2012', '12/07/2012', '']\n"
        self.assertEqual(self.errfile.getvalue(), benchmarkerror)

    def test_get_timeopen_openticket(self):
        now = datetime(2013, 01, 01)
        result = timeopen._get_timeopen_openticket(self.opendate, now)
        self.assertEqual(result, 1500)
    
    def test_get_timeopen_closedticket(self):
        result = timeopen._get_timeopen_closedticket(
            self.opendate, self.closedate)
        self.assertEqual(result, 1500)

    def test_checkstatus_allokOpen(self):
        timeopen._checkstatus('Open', self.opendate, '', ['samplerow'])

    def test_checkstatus_allokClosed(self):
        timeopen._checkstatus(
            'Closed', self.opendate, self.closedate, ['samplerow'])

    def test_checkstatus_notokClosed1(self):
        # Closed with no opendate
        args = ('Closed', '', self.closedate, ['samplerow'])
        self.assertRaises(BadDataError, timeopen._checkstatus, *args)

    def test_checkstatus_notokClosed2(self):
        # Closed with no closedate
        args = ('Closed', self.opendate, '', ['samplerow'])
        self.assertRaises(BadDataError, timeopen._checkstatus, *args)

    def test_checkstatus_notokClosed3(self):
        # Closed with no open or closedate
        args = ('Closed', '', '', ['samplerow'])
        self.assertRaises(BadDataError, timeopen._checkstatus, *args)

    def test_checkstatus_notokOpen1(self):
        # Open with no opendate
        args = ('Open', '', self.closedate, ['samplerow'])
        self.assertRaises(BadDataError, timeopen._checkstatus, *args)

    def test_checkstatus_notokOpen2(self):
        # Open with a closedate
        args = ('Open', self.opendate, self.closedate, ['samplerow'])
        self.assertRaises(BadDataError, timeopen._checkstatus, *args)

    def test_checkstatus_notokOpen3(self):
        # Open with no open or closedate
        args = ('Open', '', '', ['samplerow'])
        self.assertRaises(BadDataError, timeopen._checkstatus, *args)

    def tearDown(self):
        self.errfile.close()
        self.outfile.close()


