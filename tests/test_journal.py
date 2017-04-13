# to use this, cd .. from this directory and type
# "python -m unittest tests.test_journal"

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import unittest as _unittest
import journal as lg
datetime = lg._dt
numpy = lg._numpy
ROOT = './tests/'

class TestDataColumnInit(_unittest.TestCase):

    def test_init_empty(self):
        col = lg.DataColumn()
        self.assertIsInstance(col, lg.DataColumn)
        self.assertEqual(col.type, numpy.float64)
        self.assertEqual(len(col), 0)
        self.assertFalse(col)

    def test_init_int(self):
        col = lg.DataColumn(3)
        self.assertIsInstance(col, lg.DataColumn)
        self.assertIn(col.type, [numpy.int32, numpy.int64])
        self.assertEqual(len(col), 1)
        self.assertTrue(col)

    def test_init_str(self):
        col = lg.DataColumn('1 A')
        self.assertIsInstance(col, lg.DataColumn)
        self.assertEqual(col.type, numpy.string_)
        self.assertEqual(len(col), 1)
        self.assertTrue(col)

    def test_init_list(self):
        col = lg.DataColumn([1, 5])
        self.assertIsInstance(col, lg.DataColumn)
        self.assertIn(col.type, [numpy.int32, numpy.int64])
        self.assertEqual(len(col), 2)
        self.assertTrue(col)

    def test_init_array(self):
        col = lg.DataColumn(numpy.array([1, 5]))
        self.assertIsInstance(col, lg.DataColumn)
        self.assertIn(col.type, [numpy.int32, numpy.int64])
        self.assertEqual(len(col), 2)
        self.assertTrue(col)

    def test_init_col(self):
        col = lg.DataColumn(numpy.array([1, 5]))
        col2 = lg.DataColumn(col)
        self.assertIsInstance(col2, lg.DataColumn)
        self.assertIn(col2.type, [numpy.int32, numpy.int64])
        self.assertEqual(len(col2), 2)
        self.assertTrue(col)

class TestTimeColumnInit(_unittest.TestCase):

    def test_init_int(self):
        with self.assertRaises(ValueError):
            col = lg.TimeColumn(3)

    def test_init_nondatestr(self):
        with self.assertRaises(ValueError):
            col = lg.TimeColumn('1 Awreg')

    def test_init_datestr(self):
        col = lg.TimeColumn('22/3/2014')
        self.assertIsInstance(col, lg.TimeColumn)
        self.assertEqual(col.type, numpy.string_)
        self.assertEqual(len(col), 1)
        self.assertEqual(col.date[0], datetime.datetime(2014,3,22))

    def test_init_list(self):
        col = lg.TimeColumn(['22/3/2014', '22/3/2015'])
        self.assertIsInstance(col, lg.TimeColumn)
        self.assertEqual(col.type, numpy.string_)
        self.assertEqual(len(col), 2)
        self.assertEqual(col.date[0], datetime.datetime(2014,3,22))

    def test_init_array(self):
        col = lg.TimeColumn(numpy.array(['22/3/2014', '22/3/2015']))
        self.assertIsInstance(col, lg.TimeColumn)
        self.assertEqual(col.type, numpy.string_)
        self.assertEqual(len(col), 2)
        self.assertEqual(col.date[0], datetime.datetime(2014,3,22))

    def test_init_col(self):
        col = lg.TimeColumn(['22/3/2014', '22/3/2015'])
        col2 = lg.TimeColumn(col)
        self.assertIsInstance(col2, lg.TimeColumn)
        self.assertEqual(col2.type, numpy.string_)
        self.assertEqual(len(col2), 2)

class TestDataMatrixInit(_unittest.TestCase):

    def test_init_empty(self):
        dm = lg.DataMatrix()
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.columns, {})
        self.assertEqual(dm.names, [])
        self.assertEqual(len(dm), 0)
        self.assertEqual(dm.shape, (0, 0))
        self.assertFalse(dm)

    def test_init_int(self):
        dm = lg.DataMatrix(3)
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm['A'][0], 3)
        self.assertEqual(dm.names, ['A'])
        self.assertEqual(dm.shape, (1, 1))
        self.assertTrue(dm)

    def test_init_int_with_strnames(self):
        dm = lg.DataMatrix(3, names='Blah')
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['Blah'])
        self.assertEqual(dm['Blah'][0], 3)
        self.assertEqual(dm.shape, (1, 1))
        self.assertTrue(dm)

    def test_init_int_with_listnames(self):
        dm = lg.DataMatrix(3, names=['Blah'])
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['Blah'])
        self.assertEqual(dm['Blah'][0], 3)
        self.assertEqual(dm.shape, (1, 1))
        self.assertTrue(dm)

    def test_init_col(self):
        col = lg.DataColumn([3, 7])
        dm = lg.DataMatrix(col)
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm['A'][1], 7)
        self.assertEqual(dm.names, ['A'])
        self.assertEqual(dm.shape, (2, 1))
        self.assertTrue(dm)

    def test_init_col_with_strnames(self):
        col = lg.DataColumn([3, 7])
        dm = lg.DataMatrix(col, names='Blah')
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['Blah'])
        self.assertEqual(dm['Blah'][1], 7)
        self.assertEqual(dm.shape, (2, 1))
        self.assertTrue(dm)

    def test_init_col_with_listnames(self):
        col = lg.DataColumn([3, 7])
        dm = lg.DataMatrix(col, names=['Blah'])
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['Blah'])
        self.assertEqual(dm['Blah'][1], 7)
        self.assertEqual(dm.shape, (2, 1))
        self.assertTrue(dm)

    def test_init_col_with_listnames_and_title(self):
        col = lg.DataColumn([3, 7], title='Test')
        dm = lg.DataMatrix(col, names=['Blah'])
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['Blah'])
        self.assertEqual(dm['Blah'][1], 7)
        self.assertEqual(dm.shape, (2, 1))
        self.assertTrue(dm)

    def test_init_col_with_title(self):
        col = lg.DataColumn([3, 7], title='Test')
        dm = lg.DataMatrix(col)
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['Test'])
        self.assertEqual(dm['Test'][1], 7)
        self.assertEqual(dm.shape, (2, 1))
        self.assertTrue(dm)

    def test_init_dict(self):
        col = lg.DataColumn([3, 7])
        dic = {'test': col}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['test'])
        self.assertEqual(dm['test'][1], 7)
        self.assertEqual(dm.shape, (2, 1))
        self.assertTrue(dm)

    def test_init_dict_with_title(self):
        col = lg.DataColumn([3, 7], title='fre')
        dic = {'test': col}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['test'])
        self.assertEqual(dm['test'][1], 7)
        self.assertEqual(dm.shape, (2, 1))
        self.assertTrue(dm)

    def test_init_dict2(self):
        col = lg.DataColumn([3, 7])
        col2 = col.copy()
        dic = {'test': col, '2': 3.*col}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['test', '2'])
        self.assertEqual(dm['2'][1], 21.)
        self.assertEqual(dm.shape, (2, 2))
        self.assertTrue(dm)

    def test_init_list_of_col(self):
        col = lg.DataColumn([3, 7])
        col2 = col.copy()
        dm = lg.DataMatrix([col, 3*col2])
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.names, ['A', 'B'])
        self.assertEqual(dm['B'][1], 21.)
        self.assertEqual(dm.shape, (2, 2))
        self.assertTrue(dm)

    def test_init_list_of_col_with_names(self):
        col = lg.DataColumn([3, 7])
        col2 = col.copy()
        dm = lg.DataMatrix([col, 3*col2], names=['Bob','Aoa'])
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(sorted(dm.names), sorted(['Bob', 'Aoa']))
        self.assertEqual(dm['Bob'][1], 7)
        self.assertEqual(dm.shape, (2, 2))
        self.assertTrue(dm)

    def test_init_list_of_col_with_toofewnames(self):
        col = lg.DataColumn([3, 7])
        col2 = col.copy()
        with self.assertRaises(ValueError):
            dm = lg.DataMatrix([col, col2], names=['Bob'])

    def test_init_list_of_col_with_titles(self):
        col = lg.DataColumn([3, 7], title='d')
        col2 = col.copy()
        col2.title = 's'
        dm = lg.DataMatrix([col, col2])
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(sorted(dm.names), sorted(['d', 's']))
        self.assertEqual(dm['d'][1], 7)
        self.assertEqual(dm.shape, (2, 2))
        self.assertTrue(dm)

    def test_init_list_of_misc(self):
        col = lg.DataColumn([3, 7])
        dm = lg.DataMatrix([col, numpy.arange(2), 5])
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(sorted(dm.names), sorted(['A', 'B', 'C']))
        self.assertEqual(dm['B'][0], 0)
        self.assertEqual(dm.shape, (2, 3))
        self.assertTrue(dm)

    def test_init_list_of_misc_with_title(self):
        col = lg.DataColumn([3, 7], title='d')
        dm = lg.DataMatrix([col, numpy.arange(2), 5])
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(sorted(dm.names), sorted(['A', 'B', 'd']))
        self.assertEqual(dm['B'][0], 5)
        self.assertEqual(dm.shape, (2, 3))
        self.assertTrue(dm)

    def test_init_list_of_misc_with_names(self):
        col = lg.DataColumn([3, 7], title='d')
        dm = lg.DataMatrix([col, numpy.arange(2), 5], names=['f', 'g', 'h'])
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(sorted(dm.names), sorted(['f', 'g', 'h']))
        self.assertEqual(dm['g'][1], 1)
        self.assertEqual(dm.shape, (2, 3))
        self.assertTrue(dm)

class TestDataColumnItems(_unittest.TestCase):

    def test_getint(self):
        col = lg.DataColumn([3, 7])
        self.assertIsInstance(col[0], (numpy.int32, numpy.int64))
        self.assertTrue(col[0] == 3)

    def test_getslice(self):
        col = lg.DataColumn([3, 7])
        self.assertIsInstance(col[0:], lg.DataColumn)
        self.assertTrue(((col[0:]).values == [3, 7]).all())

    def test_getmask(self):
        col = lg.DataColumn([3, 7])
        mask = lg.DataColumn([True, False])
        self.assertIsInstance(col[mask], lg.DataColumn)
        self.assertTrue(((col[mask]).values == [3]).all())

    def test_getcol(self):
        col = lg.DataColumn([3, 7])
        col2 = lg.DataColumn([1,0,1,1,0])
        self.assertTrue(len(col[col2]) == 5)
        self.assertIsInstance(col[col2], lg.DataColumn)

    def test_setint(self):
        col = lg.DataColumn([3, 7])
        col[0] = 2
        self.assertTrue(col[0] == 2)

    def test_setslice(self):
        col = lg.DataColumn([3, 7])
        col[0:] = numpy.array([2, 5])
        self.assertTrue(col[0] == 2)
        self.assertTrue(col[1] == 5)

class TestTimeColumnItems(_unittest.TestCase):

    def test_getint(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col[0], str)
        self.assertEqual(col[0], '2015-02-01T00:00:00.000000')

    def test_getslice(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col[0:], lg.TimeColumn)
        self.assertTrue(((col[0:]).date.values == [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)]).all())

    def test_getmask(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        mask = lg.DataColumn([True, False])
        self.assertIsInstance(col[mask], lg.TimeColumn)
        self.assertTrue(((col[mask]).date.values == [datetime.datetime(2015,2,1)]).all())

    def test_getcol(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([1,0,1,1,0])
        self.assertTrue(len(col[col2]) == 5)
        self.assertIsInstance(col[col2], lg.TimeColumn)

    def test_setint(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        now = datetime.datetime.now()
        col[0] = now
        self.assertEqual(col.date[0], now)

    def test_setslice(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        now = datetime.datetime.now()
        col[0:] = now
        self.assertEqual(col.date[0], now)
        self.assertEqual(col.date[1], now)

    def test_setarr(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        now = datetime.datetime.now()
        nowcol = numpy.array([now, now])
        col[0:] = nowcol
        self.assertEqual(col.date[0], now)
        self.assertEqual(col.date[1], now)

    def test_setcol(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        now = datetime.datetime.now()
        nowcol = lg.TimeColumn([now, now])
        col[0:] = nowcol
        self.assertEqual(col.date[0], now)
        self.assertEqual(col.date[1], now)

    def test_format(self):
        col = lg.TimeColumn(['2015-02-01T00:00:00.000000', '2015-01-05T00:00:00.000000', '20150403'])
        self.assertTrue((col.format('%Y%m%d').values == ['20150201', '20150105', '20150403']).all())

    def test_reformat(self):
        col = lg.TimeColumn(['2015-02-01T00:00:00.000000', '2015-01-05T00:00:00.000000', '20150403'])
        col.reformat('%Y%m%d')
        self.assertTrue((col.values == ['20150201', '20150105', '20150403']).all())

class TestDataMatrixItems(_unittest.TestCase):

    def test_getint(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm[0], dict)
        self.assertEqual(len(dm[0]), 2)
        self.assertEqual(dm[0], {'time': col[0], 'blah': col2[0]})

    def test_getwrongstr(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        with self.assertRaises(IndexError):
            a=dm['blih']

    def test_getstr(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm['blah'], lg.DataColumn)
        self.assertIsInstance(dm['time'], lg.TimeColumn)
        self.assertEqual(len(dm['blah']), 2)
        self.assertEqual(dm['blah'], col2)

    def test_getmask(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        mask = lg.DataColumn([False, True])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm[mask], lg.DataMatrix)
        self.assertEqual(dm[mask].shape, (1, 2))
        self.assertEqual(dm[mask][0], {'time': col[1], 'blah': col2[1]})

    def test_getemptymask(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        mask = lg.DataColumn([False, False])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm[mask], lg.DataMatrix)
        self.assertEqual(dm[mask].shape, (0, 2))
        with self.assertRaises(IndexError):
            a = dm[mask][0]

    def test_getintmask(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        mask = lg.DataColumn([1, 0])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm[mask], lg.DataMatrix)
        self.assertEqual(dm[mask].shape, (2, 2))
        self.assertEqual(dm[mask][0], {'time': col[1], 'blah': col2[1]})

    def test_getlist(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        mask = [1, 0]
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm[mask], lg.DataMatrix)
        self.assertEqual(dm[mask].shape, (2, 2))
        self.assertEqual(dm[mask][0], {'time': col[1], 'blah': col2[1]})

    def test_getnparray(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        mask = numpy.array([1, 0])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm[mask], lg.DataMatrix)
        self.assertEqual(dm[mask].shape, (2, 2))
        self.assertEqual(dm[mask][0], {'time': col[1], 'blah': col2[1]})

    def test_getslice(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7, 5])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertIsInstance(dm[1:], lg.DataMatrix)
        self.assertEqual(dm[1:].shape, (2, 2))
        self.assertEqual(dm[1:].columns, {'time': col[1:], 'blah': col2[1:]})

    def test_setind(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        with self.assertRaises(IndexError):
            dm[0] = {'time': 3, 'blah': 5}

    def test_setslice(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        with self.assertRaises(IndexError):
            dm[0:] = dm

    def test_setstr_existing(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        dm['blah'] = 2*dm['blah']
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.shape, (2, 2))
        self.assertEqual(dm['blah'][0], 6)
        self.assertEqual(dm['blah'][1], 14)

    def test_setstr_time(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        dm['time'] = col
        with self.assertRaises(ValueError):
            dm['time'] = col2

    def test_setstr_time2(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertEqual(dm.shape, (2, 1))

        dm['time'] = col
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.shape, (2, 2))

    def test_setstr_time3(self):
        col2 = lg.DataColumn([3, 7])
        dic = {'blah': col2}
        dm = lg.DataMatrix(dic)
        self.assertEqual(dm.shape, (2, 1))

        dm['time'] = [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)]
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.shape, (2, 2))
        self.assertIsInstance(dm['time'], lg.TimeColumn)
        self.assertEqual(sorted(dm.names), sorted(['blah', 'time']))

    def test_setstr_nondatacolumn(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = [3, 7, 5]
        dic = {'time': col}
        dm = lg.DataMatrix(dic)
        self.assertEqual(dm.shape, (2, 1))

        dm['blah'] = col2
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.shape, (3, 2))
        self.assertIsInstance(dm['blah'], lg.DataColumn)
        self.assertEqual(sorted(dm.names), sorted(['blah', 'time']))

    def test_setstr_nonexisting(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        dm = lg.DataMatrix(dic)
        dm['blih'] = 2*dm['blah']
        self.assertIsInstance(dm, lg.DataMatrix)
        self.assertEqual(dm.shape, (2, 3))
        self.assertEqual(dm['blih'][0], 6)
        self.assertEqual(dm['blih'][1], 14)

class TestDataColumnOperations(_unittest.TestCase):

    def test_add(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col+2), lg.DataColumn)
        self.assertTrue(((col+2).values == [5, 9]).all())

    def test_radd(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(2+col), lg.DataColumn)
        self.assertTrue(((2+col).values == [5, 9]).all())

    def test_sub(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col-2), lg.DataColumn)
        self.assertTrue(((col-2).values == [1, 5]).all())

    def test_rsub(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(2-col), lg.DataColumn)
        self.assertTrue(((2-col).values == [-1, -5]).all())

    def test_mul(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col*2), lg.DataColumn)
        self.assertTrue(((col*2).values == [6, 14]).all())

    def test_rmul(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(2*col), lg.DataColumn)
        self.assertTrue(((2*col).values == [6, 14]).all())

    def test_intdiv(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col/7), lg.DataColumn)
        self.assertTrue(((col/7).values == [0, 1]).all())

    def test_rintdiv(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(7/col), lg.DataColumn)
        self.assertTrue(((7/col).values == [2, 1]).all())

    def test_div(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col/7.), lg.DataColumn)
        self.assertTrue(((col/7.).values == [3/7., 1.]).all())

    def test_rdiv(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(7./col), lg.DataColumn)
        self.assertTrue(((7./col).values == [7/3., 1.]).all())

    def test_pow(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col**2), lg.DataColumn)
        self.assertTrue(((col**2).values == [9, 49]).all())

    def test_rpow(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(2**col), lg.DataColumn)
        self.assertTrue(((2**col).values == [8, 128]).all())

    def test_mod(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col%7), lg.DataColumn)
        self.assertTrue(((col%7).values == [3, 0]).all())

    def test_rmod(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(7%col), lg.DataColumn)
        self.assertTrue(((7%col).values == [1, 0]).all())

    def test_addcol(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col+col), lg.DataColumn)
        self.assertTrue(((col+col).values == [6, 14]).all())

    def test_subcol(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col-col), lg.DataColumn)
        self.assertTrue(((col-col).values == [0, 0]).all())

    def test_mulcol(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col*col), lg.DataColumn)
        self.assertTrue(((col*col).values == [9, 49]).all())

    def test_divcol(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col/col), lg.DataColumn)
        self.assertTrue(((col/col).values == [1, 1]).all())

    def test_powcol(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col**col), lg.DataColumn)
        self.assertTrue(((col**col).values == [3**3, 7**7]).all())

    def test_modcol(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(type(col%col), lg.DataColumn)
        self.assertTrue(((col%col).values == [0, 0]).all())

class TestDataColumnComparisons(_unittest.TestCase):

    def setUp(self):
        self.col = lg.DataColumn([1, 3, 7])
        self.arr = numpy.array([8, 3, 1])
        self.col2 = lg.DataColumn(self.arr)
        self.scalar = 3

    def test_intlt(self):
        self.assertEqual(type(self.col<self.scalar), lg.DataColumn)
        self.assertTrue(((self.col<self.scalar).values == [True, False, False]).all())
        
        # Test with a numpy array        
        self.assertEqual(type(self.col<self.arr), lg.DataColumn)
        self.assertTrue(((self.col<self.arr).values == [True, False, False]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col<self.col2), lg.DataColumn)
        self.assertTrue(((self.col<self.col2).values == [True, False, False]).all())

    def test_intgt(self):
        self.assertEqual(type(self.col>self.scalar), lg.DataColumn)
        self.assertTrue(((self.col>self.scalar).values == [False, False, True]).all())

        # Test with a numpy array        
        self.assertEqual(type(self.col>self.arr), lg.DataColumn)
        self.assertTrue(((self.col>self.arr).values == [False, False, True]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col>self.col2), lg.DataColumn)
        self.assertTrue(((self.col>self.col2).values == [False, False, True]).all())

    def test_intle(self):
        self.assertEqual(type(self.col<=self.scalar), lg.DataColumn)
        self.assertTrue(((self.col<=self.scalar).values == [True, True, False]).all())

        # Test with a numpy array        
        self.assertEqual(type(self.col<=self.arr), lg.DataColumn)
        self.assertTrue(((self.col<=self.arr).values == [True, True, False]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col<=self.col2), lg.DataColumn)
        self.assertTrue(((self.col<=self.col2).values == [True, True, False]).all())

    def test_intge(self):
        self.assertEqual(type(self.col>=self.scalar), lg.DataColumn)
        self.assertTrue(((self.col>=self.scalar).values == [False, True, True]).all())
        
        # Test with a numpy array        
        self.assertEqual(type(self.col>=self.arr), lg.DataColumn)
        self.assertTrue(((self.col>=self.arr).values == [False, True, True]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col>=self.col2), lg.DataColumn)
        self.assertTrue(((self.col>=self.col2).values == [False, True, True]).all())

    def test_inteq(self):
        self.assertEqual(type(self.col==self.scalar), lg.DataColumn)
        self.assertTrue(((self.col==self.scalar).values == [False, True, False]).all())

        # Test with a numpy array        
        self.assertEqual(type(self.col==self.arr), lg.DataColumn)
        self.assertTrue(((self.col==self.arr).values == [False, True, False]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col==self.col2), lg.DataColumn)
        self.assertTrue(((self.col==self.col2).values == [False, True, False]).all())

    def test_intne(self):
        self.assertEqual(type(self.col!=self.scalar), lg.DataColumn)
        self.assertTrue(((self.col!=self.scalar).values == [True, False, True]).all())
        
        # Test inequality with a numpy array        
        self.assertEqual(type(self.col!=self.arr), lg.DataColumn)
        self.assertTrue(((self.col!=self.arr).values == [True, False, True]).all())
        
        # Test inequality with another TimeColumn
        self.assertEqual(type(self.col!=self.col2), lg.DataColumn)
        self.assertTrue(((self.col!=self.col2).values == [True, False, True]).all())

class TestDataColumnProperties(_unittest.TestCase):

    def test_min(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(col.min, 3)

    def test_max(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(col.max, 7)

    def test_mean(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(col.mean, 5.0)

    def test_median(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(col.median, 5.0)

    def test_sum(self):
        col = lg.DataColumn([3, 7])
        self.assertEqual(col.sum, 10)
        
    def test_all(self):
        col = lg.DataColumn([True, True])
        self.assertTrue(col.all)
        col = lg.DataColumn([True, False])
        self.assertFalse(col.all)
        col = lg.DataColumn([1, 1])
        self.assertTrue(col.all)
        col = lg.DataColumn([1, 0])
        self.assertFalse(col.all)
        col = lg.DataColumn([1.0, 3.5])
        self.assertTrue(col.all)
        col = lg.DataColumn([1.0, 0.])
        self.assertFalse(col.all)
        
    def test_any(self):
        col = lg.DataColumn([True, False])
        self.assertTrue(col.any)
        col = lg.DataColumn([False, False])
        self.assertFalse(col.any)
        col = lg.DataColumn([1, 0])
        self.assertTrue(col.any)
        col = lg.DataColumn([0, 0])
        self.assertFalse(col.any)
        col = lg.DataColumn([1.0, 3.5])
        self.assertTrue(col.any)
        col = lg.DataColumn([0., 0.])
        self.assertFalse(col.any)

class TestDataAppend(_unittest.TestCase):

    def test_append_int(self):
        col = lg.DataColumn([3, 7])
        col.append(5)
        self.assertIn(col.type, [numpy.int32, numpy.int64])
        self.assertEqual(len(col), 3)
        self.assertTrue((col.values == [3, 7, 5]).all())

    def test_append_float(self):
        col = lg.DataColumn([3, 7])
        col.append(5.)
        self.assertEqual(col.type, numpy.float64)
        self.assertEqual(len(col), 3)
        self.assertTrue((col.values == [3., 7., 5.]).all())

    def test_append_str(self):
        col = lg.DataColumn([3, 7])
        col.append('5')
        self.assertEqual(col.type, numpy.string_)
        self.assertEqual(len(col), 3)
        self.assertTrue((col.values == ['3', '7', '5']).all())

    def test_append_array(self):
        col = lg.DataColumn([3, 7])
        col.append(numpy.array([5, 4]))
        self.assertIn(col.type, [numpy.int32, numpy.int64])
        self.assertEqual(len(col), 4)
        self.assertTrue((col.values == [3, 7, 5, 4]).all())

    def test_append_col(self):
        col = lg.DataColumn([3, 7])
        col.append(col)
        self.assertIn(col.type, [numpy.int32, numpy.int64])
        self.assertEqual(len(col), 4)
        self.assertTrue((col.values == [3, 7, 3, 7]).all())

class TestDataCopy(_unittest.TestCase):

    def test_append(self):
        col = lg.DataColumn([3, 7])
        col2 = col.copy()
        self.assertEqual(col, col2)
        col.append(5)
        self.assertEqual(len(col), 3)
        self.assertTrue((col.values == [3, 7, 5]).all())
        self.assertEqual(len(col2), 2)
        self.assertTrue((col2.values == [3, 7]).all())
        self.assertNotEqual(col, col2)

class TestTimeColumnOperations(_unittest.TestCase):

    def test_add(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        jd = col.jd+1
        td = datetime.timedelta(days=1)
        self.assertEqual(type(col+td), lg.TimeColumn)
        self.assertTrue(((col+td).jd.values == jd.values).all())

    def test_coladd(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            col+col

    def test_intadd(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            col+2

    def test_radd(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        jd = col.jd+1
        td = datetime.timedelta(days=1)
        self.assertEqual(type(td+col), lg.TimeColumn)
        self.assertTrue(((td+col).jd.values == jd.values).all())

    def test_rintadd(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            2+col

    def test_sub(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        jd = col.jd-1
        td = datetime.timedelta(days=1)
        self.assertEqual(type(col-td), lg.TimeColumn)
        self.assertTrue(((col-td).jd.values == jd.values).all())

    def test_intsub(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            col-2

    def test_colsub(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            col-col

    def test_rsub(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        td = datetime.timedelta(days=1)
        with self.assertRaises(TypeError):
            td-col

    def test_rintsub(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            2-col

    def test_mul(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            col*2

    def test_rmul(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            2*col

    def test_intdiv(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            col/2

    def test_rintdiv(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            2/col

    def test_pow(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            col**2

    def test_rpow(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            2**col

    def test_mod(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            col%2

    def test_rmod(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            2%col

class TestTimeColumnComparisons(_unittest.TestCase):

    def setUp(self):
        self.col = lg.TimeColumn([datetime.datetime(2015,2,1),
                                  datetime.datetime(2015,2,3),
                                  datetime.datetime(2015,2,7)])

        self.arr = numpy.array([datetime.datetime(2015,2,8),
                                datetime.datetime(2015,2,3),
                                datetime.datetime(2015,2,1)])

        self.col2 = lg.TimeColumn(self.arr)
        
        self.scalar = datetime.datetime(2015,2,3)

    def test_intlt(self):
        self.assertEqual(type(self.col<self.scalar), lg.DataColumn)
        self.assertTrue(((self.col<self.scalar).values == [True, False, False]).all())
        
        # Test with a numpy array        
        self.assertEqual(type(self.col<self.arr), lg.DataColumn)
        self.assertTrue(((self.col<self.arr).values == [True, False, False]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col<self.col2), lg.DataColumn)
        self.assertTrue(((self.col<self.col2).values == [True, False, False]).all())

    def test_intgt(self):
        self.assertEqual(type(self.col>self.scalar), lg.DataColumn)
        self.assertTrue(((self.col>self.scalar).values == [False, False, True]).all())

        # Test with a numpy array        
        self.assertEqual(type(self.col>self.arr), lg.DataColumn)
        self.assertTrue(((self.col>self.arr).values == [False, False, True]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col>self.col2), lg.DataColumn)
        self.assertTrue(((self.col>self.col2).values == [False, False, True]).all())

    def test_intle(self):
        self.assertEqual(type(self.col<=self.scalar), lg.DataColumn)
        self.assertTrue(((self.col<=self.scalar).values == [True, True, False]).all())

        # Test with a numpy array        
        self.assertEqual(type(self.col<=self.arr), lg.DataColumn)
        self.assertTrue(((self.col<=self.arr).values == [True, True, False]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col<=self.col2), lg.DataColumn)
        self.assertTrue(((self.col<=self.col2).values == [True, True, False]).all())

    def test_intge(self):
        self.assertEqual(type(self.col>=self.scalar), lg.DataColumn)
        self.assertTrue(((self.col>=self.scalar).values == [False, True, True]).all())
        
        # Test with a numpy array        
        self.assertEqual(type(self.col>=self.arr), lg.DataColumn)
        self.assertTrue(((self.col>=self.arr).values == [False, True, True]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col>=self.col2), lg.DataColumn)
        self.assertTrue(((self.col>=self.col2).values == [False, True, True]).all())

    def test_inteq(self):
        self.assertEqual(type(self.col==self.scalar), lg.DataColumn)
        self.assertTrue(((self.col==self.scalar).values == [False, True, False]).all())

        # Test with a numpy array        
        self.assertEqual(type(self.col==self.arr), lg.DataColumn)
        self.assertTrue(((self.col==self.arr).values == [False, True, False]).all())
        
        # Test with another TimeColumn
        self.assertEqual(type(self.col==self.col2), lg.DataColumn)
        self.assertTrue(((self.col==self.col2).values == [False, True, False]).all())

    def test_intne(self):
        self.assertEqual(type(self.col!=self.scalar), lg.DataColumn)
        self.assertTrue(((self.col!=self.scalar).values == [True, False, True]).all())
        
        # Test inequality with a numpy array        
        self.assertEqual(type(self.col!=self.arr), lg.DataColumn)
        self.assertTrue(((self.col!=self.arr).values == [True, False, True]).all())
        
        # Test inequality with another TimeColumn
        self.assertEqual(type(self.col!=self.col2), lg.DataColumn)
        self.assertTrue(((self.col!=self.col2).values == [True, False, True]).all())

class TestTimeColumnProperties(_unittest.TestCase):

    def test_year(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.year, lg.UnchangeableDataColumn)
        self.assertTrue((col.year.values == [2015, 2015]).all())

    def test_month(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.month, lg.UnchangeableDataColumn)
        self.assertTrue((col.month.values == [2, 1]).all())

    def test_day(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.day, lg.UnchangeableDataColumn)
        self.assertTrue((col.day.values == [1, 5]).all())

    def test_hour(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1,13), datetime.datetime(2015,1,5,7)])
        self.assertIsInstance(col.hour, lg.UnchangeableDataColumn)
        self.assertTrue((col.hour.values == [13, 7]).all())

    def test_minute(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1,13, 52), datetime.datetime(2015,1,5,7,13)])
        self.assertIsInstance(col.minute, lg.UnchangeableDataColumn)
        self.assertTrue((col.minute.values == [52, 13]).all())

    def test_second(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1,13,52,14), datetime.datetime(2015,1,5,7,13,25)])
        self.assertIsInstance(col.second, lg.UnchangeableDataColumn)
        self.assertTrue((col.second.values == [14, 25]).all())

    def test_microsecond(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1,13,52,14,253), datetime.datetime(2015,1,5,7,13,25,121)])
        self.assertIsInstance(col.microsecond, lg.UnchangeableDataColumn)
        self.assertTrue((col.microsecond.values == [253, 121]).all())

    def test_date(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.date, lg.UnchangeableDataColumn)
        self.assertTrue((col.date.values == [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)]).all())

    def test_jd(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.jd, lg.UnchangeableDataColumn)
        self.assertTrue((col.jd.values == [2457055.,  2457028.]).all())

    def test_timeepoch(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.time_since_epoch, lg.UnchangeableDataColumn)
        self.assertTrue((col.time_since_epoch.values == [1.42274880e+09,   1.42041600e+09]).all())

    def test_time(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.time, lg.UnchangeableDataColumn)
        self.assertTrue((col.time.values == [2332800., 0.]).all())

    def test_min(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.min, datetime.datetime)
        self.assertEqual(col.min, datetime.datetime(2015,1,5))

    def test_max(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.max, datetime.datetime)
        self.assertEqual(col.max, datetime.datetime(2015,2,1))

    def test_mean(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.mean, datetime.datetime)
        self.assertEqual(col.mean, datetime.datetime(2015, 1, 18, 12, 0))

    def test_median(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.assertIsInstance(col.median, datetime.datetime)
        self.assertEqual(col.median, datetime.datetime(2015, 1, 18, 12, 0))

    def test_sum(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(TypeError):
            col.sum

class TestTimeAppend(_unittest.TestCase):

    def test_append_int(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        with self.assertRaises(ValueError):
            col.append(5)

    def test_append_datetime(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        now = datetime.datetime.now()
        col.append(now)
        self.assertEqual(len(col), 3)
        self.assertTrue((col.date.values == [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5), now]).all())

    def test_append_str(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        now = '20150403'
        col.append(now)
        self.assertEqual(len(col), 3)
        self.assertTrue((col.date.values == [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5), lg.TimeColumn.parser.parse(now)]).all())


    def test_append_array(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        now = '20150403'
        now2 = datetime.datetime(2013,10,7)
        col.append(numpy.array([now, now2]))
        self.assertEqual(len(col), 4)
        self.assertTrue((col.date.values == [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5), lg.TimeColumn.parser.parse(now), now2]).all())

    def test_append_col(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col.append(col)
        self.assertEqual(len(col), 4)
        self.assertTrue((col.date.values == [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5), datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)]).all())

class TestTimeCopy(_unittest.TestCase):

    def test_append_datetime(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = col.copy()
        self.assertEqual(col, col2)
        now = datetime.datetime.now()
        col.append(now)
        self.assertEqual(len(col), 3)
        self.assertTrue((col.date.values == [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5), now]).all())
        self.assertEqual(len(col2), 2)
        self.assertTrue((col2.date.values == [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)]).all())
        self.assertNotEqual(col, col2)

class TestDataMatrixCopy(_unittest.TestCase):

    def setUp(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        self.dm = lg.DataMatrix(dic)
        self.dm2 = self.dm.copy()

    def test_copy_are_equal(self):
        self.assertTrue(self.dm == self.dm2)
        self.assertFalse(self.dm != self.dm2)
        
    def test_copy_is_modified(self):
        self.assertTrue(self.dm == self.dm2)
        self.assertFalse(self.dm != self.dm2)
        self.assertEqual(self.dm.shape, (2, 2))
        self.assertEqual(self.dm2.shape, (2, 2))
        
        self.dm2['time'].append(datetime.datetime(2015,2,9))
        self.dm2['blah'].append(9)
        self.assertTrue(self.dm != self.dm2)
        self.assertFalse(self.dm == self.dm2)
        self.assertEqual(self.dm.shape, (2, 2))
        self.assertEqual(self.dm2.shape, (3, 2))
        
class TestDataMatrixAppend(_unittest.TestCase):

    def setUp(self):
        self.col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        self.col2 = lg.DataColumn([3, 7])
        dic = {'time': self.col, 'blah': self.col2}
        self.dm = lg.DataMatrix(dic)

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            self.dm.append(5)

        with self.assertRaises(TypeError):
            self.dm.append("5")
            
        with self.assertRaises(TypeError):
            self.dm.append(self.col)

        self.dm.append(self.dm)
        
    def test_wrong_column_names(self):
        dic2 = {'time': self.col, 'blaaah': self.col2}
        dm2 = lg.DataMatrix(dic2)
        
        with self.assertRaises(ValueError):
            self.dm.append(dm2)

        dic = {'time': self.col, 'blah': self.col2}
        dm2 = lg.DataMatrix(dic)
        self.dm.append(dm2)
        
    def test_append(self):

        self.assertEqual(self.dm.shape, (2, 2)) 

        dic = {'time': self.col, 'blah': self.col2+1}
        dm2 = lg.DataMatrix(dic)
        
        self.dm.append(dm2)

        self.assertEqual(self.dm.shape, (4, 2)) 
        self.assertTrue((self.dm['time'].date.values == [datetime.datetime(2015,2,1), datetime.datetime(2015,1,5), datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)]).all())
        self.assertTrue((self.dm['blah'].values == [3, 7, 4, 8]).all())

class TestDataMatrixComparisons(_unittest.TestCase):
    
    def setUp(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        self.dm = lg.DataMatrix(dic)

    def test_eq(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2}
        dm2 = lg.DataMatrix(dic)        
        self.assertTrue(self.dm == dm2)
        self.assertFalse(self.dm != dm2)
        
    def test_eq_different_type(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dm2 = {'time': col, 'blah': col2}
        self.assertFalse(self.dm == dm2)
        self.assertTrue(self.dm != dm2)

    def test_eq_different_number_of_columns(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blah': col2, 'blah2': col2.copy()}
        dm2 = lg.DataMatrix(dic)
        self.assertFalse(self.dm == dm2)
        self.assertTrue(self.dm != dm2)
        
    def test_eq_different_number_of_rows(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1)])
        col2 = lg.DataColumn([3])
        dic = {'time': col, 'blah': col2}
        dm2 = lg.DataMatrix(dic)
        self.assertFalse(self.dm == dm2)
        self.assertTrue(self.dm != dm2)
        
    def test_eq_different_column_names(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,1), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 7])
        dic = {'time': col, 'blaaaaah': col2}
        dm2 = lg.DataMatrix(dic)
        self.assertFalse(self.dm == dm2)
        self.assertTrue(self.dm != dm2)
        
    def test_eq_different_column_data(self):
        col = lg.TimeColumn([datetime.datetime(2015,2,3), datetime.datetime(2015,1,5)])
        col2 = lg.DataColumn([3, 8])
        dic = {'time': col, 'blah': col2}
        dm2 = lg.DataMatrix(dic)        
        self.assertFalse(self.dm == dm2)
        self.assertTrue(self.dm != dm2)

class TestReadCSV(_unittest.TestCase):

    def test_header(self):
        dm = lg.read_csv(ROOT+'logs_test_hdr.csv')
        self.assertEqual(dm.shape, (5, 4))
        self.assertEqual(dm['time'].type, numpy.string_)
        self.assertIn(dm['hum'].type, [numpy.int32, numpy.int64])
        self.assertEqual(dm['temp'].type, numpy.float64)
        self.assertEqual(dm['status'].type, numpy.string_)

    def test_skiplines(self):
        dm = lg.read_csv(ROOT+'logs_test_hdr.csv', skiplines=2)
        self.assertEqual(dm.shape, (3, 4))
        self.assertEqual(dm['time'].type, numpy.string_)
        self.assertEqual(dm['temp'].type, numpy.float64)
        self.assertIn(dm['hum'].type, [numpy.int32, numpy.int64])
        self.assertEqual(dm['status'].type, numpy.string_)

    def test_wrongline(self):
        dm = lg.read_csv(ROOT+'logs_test_wrong.csv')
        self.assertEqual(dm.shape, (4, 4))
        self.assertEqual(dm['time'].type, numpy.string_)
        self.assertEqual(dm['temp'].type, numpy.float64)
        self.assertIn(dm['hum'].type, [numpy.int32, numpy.int64])
        self.assertEqual(dm['status'].type, numpy.string_)

    def test_no_header(self):
        dm = lg.read_csv(ROOT+'logs_test_no_hdr.csv', field_header=False)
        self.assertEqual(dm.shape, (5, 4))
        self.assertEqual(dm['A'].type, numpy.string_)
        self.assertEqual(dm['B'].type, numpy.float64)
        self.assertIn(dm['C'].type, [numpy.int32, numpy.int64])
        self.assertEqual(dm['D'].type, numpy.string_)

    def test_no_header_names(self):
        dm = lg.read_csv(ROOT+'logs_test_no_hdr.csv', field_header=False, names=['time', 'aaa', 'bbb', 'ccc'])
        self.assertEqual(dm.shape, (5, 4))
        self.assertEqual(dm['time'].type, numpy.string_)
        self.assertEqual(dm['aaa'].type, numpy.float64)
        self.assertIn(dm['bbb'].type, [numpy.int32, numpy.int64])
        self.assertEqual(dm['ccc'].type, numpy.string_)

    def test_no_header_fewnames(self):
        dm = lg.read_csv(ROOT+'logs_test_no_hdr.csv', field_header=False, names=['time', 'aaa'])
        self.assertEqual(dm.shape, (5, 4))
        self.assertIsInstance(dm['time'], lg.TimeColumn)
        self.assertIsInstance(dm['aaa'], lg.DataColumn)
        self.assertEqual(dm['time'].type, numpy.string_)
        self.assertEqual(dm['aaa'].type, numpy.float64)
        self.assertIn(dm['A'].type, [numpy.int32, numpy.int64])
        self.assertEqual(dm['B'].type, numpy.string_)

class TestCreateLog(_unittest.TestCase):

    def test_log(self):
        log = lg.Logger(fileroot='TestLog_', logdir=ROOT+'logs')
        log.log('test')
        fname = log.filename
        with open(fname, 'r') as fil:
            for lastline in fil:
                pass
        line = lastline.strip().split(log.delimiter)
        self.assertEqual(line[1], 'test')

    def test_log_error(self):
        log = lg.Logger(fileroot='TestLog_', logdir=ROOT+'logs')
        log.log('test', error=True)
        fname = log.filename
        with open(fname, 'r') as fil:
            for lastline in fil:
                pass
        line = lastline.strip().split(log.delimiter)
        self.assertEqual(line[1], 'ERROR: test')

    def test_log_warning(self):
        log = lg.Logger(fileroot='TestLog_', logdir=ROOT+'logs')
        log.log('test', warning=True)
        fname = log.filename
        with open(fname, 'r') as fil:
            for lastline in fil:
                pass
        line = lastline.strip().split(log.delimiter)
        self.assertEqual(line[1], 'WARNING: test')

    def test_log_header(self):
        log = lg.Logger(fileroot='TestLogHeader_', headers=['status','blah','price'],
                        logdir=ROOT+'logs')
        log.log('ok',numpy.random.randint(10),numpy.random.rand()*50)
        fname = log.filename
        with open(fname, 'r') as fil:
            for j, line in enumerate(fil):
                if j == 0:
                    line = line.strip()
                    self.assertEqual(line, 'time,status,blah,price')
        line = line.strip().split(log.delimiter)
        self.assertEqual(len(line), 4)

    def test_log_header_notime(self):
        log = lg.Logger(fileroot='TestLogHeaderNoTime_', headers=['status','blah','price'],
                        timestamp=False, logdir=ROOT+'logs')
        log.log('ok',numpy.random.randint(10),numpy.random.rand()*50)
        fname = log.filename
        with open(fname, 'r') as fil:
            for j, line in enumerate(fil):
                if j == 0:
                    line = line.strip()
                    self.assertEqual(line, 'status,blah,price')
        line = line.strip().split(log.delimiter)
        self.assertEqual(len(line), 3)

    def test_log_int_float_str_date(self):
        log = lg.Logger(fileroot='TestLog_', logdir=ROOT+'logs')
        log.log(3,4.5,'test',datetime.datetime(2015,4,3))
        fname = log.filename
        with open(fname, 'r') as fil:
            for lastline in fil:
                pass
        line = log.delimiter.join(lastline.strip().split(log.delimiter)[1:])
        self.assertEqual(line, '3,4.5,test,2015-04-03 00:00:00')
## Plots
##
## dm = lg.read_csv('HumTemp_20150417.txt')

## ax, l = dm.timeplot(dm['temp enclosure'], format='%H:%M', ylabel='Temperature (in C)', color='r')
## dm.timeplot(dm['temp dome'], format='%H:%M', color='g', ax=ax)

## ax, l = dm.timeplot(dm['temp enclosure'], rightax=1/dm['hum enclosure'], time_format='%H:%M', ylabel='Temperature (in C)')

##



if __name__ == '__main__':
    _unittest.main()