'''
.. module: logger
.. moduleauthor: Julien Spronck
.. created: April 21, 2015

Simple module to handle time-dependent data from csv files.
'''
__version__ = '1.1'


import numpy as _numpy
import matplotlib.pyplot as _plt
import pickle as _pickle
import datetime as _dt

try:
    import colorama as _colorama
except ImportError:
    _colorama = None

def _date2jd(date):
    '''
    Returns the Julian date from a datetime object

    Args:
        date (datetime.datetime object): the date to transform
    '''
    year = date.year
    mth = date.month
    day = date.day
    float64 = _numpy.float64
    hour = float64(date.hour)
    minu = float64(date.minute)
    sec = float64(date.second + date.microsecond * 1e-6)

    # Condition for the leap years:
    if mth < 3:
        leap = -1
    else:
        leap = 0
    thour = hour + minu/60 + sec/3600
    return float64(day - 32075 + 1461*(year + 4800 +leap)/4 +
                   367*(mth -2 -leap*12)/12 -
                   3 *(year + 4900 + leap)/400) + thour/24

def _isiterable(obj):
    '''
    Checks if an object is iterable

    Args:
        obj: the object to check
    '''
    return hasattr(obj, '__iter__')

def _iter_letters():
    '''
    Generator that returns upper case letter combinations:
        A, B, C, ..., AA, AB, AC, ... ZX, ZY, ZZ, AAA, AAB, ...

    Args:
    '''
    from string import ascii_uppercase
    import itertools
    size = 1
    while True:
        for syms in itertools.product(ascii_uppercase, repeat=size):
            yield "".join(syms)
        size += 1

class AbstractDataColumn(object):
    '''
    Base class for all data column objects
    '''
    def __init__(self, the_input=None, title=''):
        '''
        Initialization of the AbstractDataColumn class

        Args:
            the_input (object, optional): data input. Can be an iterable, a
                string, an integer, a float, ...
            title (str, optional): column title. By default, ''

        Raises:
        '''
        array = _numpy.array
        if the_input is None:
            self.values = array([])
        elif isinstance(the_input, str):
            self.values = array([the_input])
        else:
            try:
                self.values = array(list(the_input))
            except TypeError:
                self.values = array([the_input])
        self.title = title
        self.type = self.values.dtype.type


    def __str__(self):
        '''
        String representation of data column
        '''
        prefix = self.title+': ' if self.title else ''
        return prefix+'['+', '.join([str(val) for val in self.values])+']'

    def __repr__(self):
        '''
        __repr__ for data column
        '''
        return 'DataColumn('+self.values.__repr__()+', \''+self.title+'\')'

    def __len__(self):
        '''
        Length of column
        '''
        return len(self.values)

    def __nonzero__(self):
        '''
        truth value
        '''
        return len(self) != 0

    def __getitem__(self, item):
        '''
        Gets item from column

        Args:
            item (DataColumn, list, numpy.ndarray, slice or int): the item to get
        '''
        if isinstance(item, DataColumn):
            return DataColumn(self.values[item.values], title=item.title)
        if type(item) in [list, _numpy.ndarray]:
            return DataColumn(self.values[item], title=self.title)
        if isinstance(item, slice):
            return DataColumn(self.values[item], title=self.title)
        return self.values[item]

    def __setitem__(self, item, value):
        '''
        Sets item of column
        '''
        self.values[item] = value

    def itervalues(self):
        '''
        Generator of values
        '''
        for val in self.values:
            yield val

    def map(self, callback, title=''):
        '''
        Maps the column to a new column
        '''
        return DataColumn([callback(val) for val in self.values], title=title)

    def itermap(self, callback):
        '''
        Generator that maps the values in the column
        '''
        for val in self.values:
            yield callback(val)

    def copy(self):
        '''
        Returns a copy of the object
        '''
        return AbstractDataColumn(self.values, self.title)

    @property
    def max(self):
        '''
        Maximum value in the column
        '''
        return max(_numpy.asarray(self.values))

    @property
    def maxlength(self):
        '''
        Returns the maximal length of the items in the column
        '''
        dtype = self.values.dtype
        if dtype.name.startswith('string'):
            byts = dtype.itemsize
            return byts
        if dtype.name.startswith('int') or dtype.name.startswith('float'):
            return len(str(self.max))
        return 12

class DataColumn(AbstractDataColumn):
    '''
    DataColumn class
    '''
    def __init__(self, the_input=None, title=''):
        '''
        Initialization of the DataColumn class

        Args:
            the_input (object, optional): data input. Can be an iterable, a
                string, an integer, a float, ...
            title (str, optional): column title. By default, ''

        Raises:
        '''
        AbstractDataColumn.__init__(self, the_input=the_input, title=title)

    ##################
    ### Comparison ###
    ##################

    def __lt__(self, other):
        '''
        Comparison method: __lt__
        '''
        return DataColumn(self.values.__lt__(other))

    def __le__(self, other):
        '''
        Comparison method: __le__
        '''
        return DataColumn(self.values.__le__(other))

    def __gt__(self, other):
        '''
        Comparison method: __gt__
        '''
        return DataColumn(self.values.__gt__(other))

    def __ge__(self, other):
        '''
        Comparison method: __ge__
        '''
        return DataColumn(self.values.__ge__(other))

    def __eq__(self, other):
        '''
        Comparison method: __eq__
        '''
        return DataColumn(self.values.__eq__(other))

    def __ne__(self, other):
        '''
        Comparison method: __ne__
        '''
        return DataColumn(self.values.__ne__(other))

    ##################
    ### Operations ###
    ##################

    def __add__(self, other):
        '''
        __add__ operator
        '''
        return DataColumn(self.values.__add__(other))

    def __sub__(self, other):
        '''
        __sub__ operator
        '''
        return DataColumn(self.values.__sub__(other))

    def __mul__(self, other):
        '''
        __mul__ operator
        '''
        return DataColumn(self.values.__mul__(other))

    def __floordiv__(self, other):
        '''
        __floordiv__ operator
        '''
        return DataColumn(self.values.__floordiv__(other))

    def __mod__(self, other):
        '''
        __mod__ operator
        '''
        return DataColumn(self.values.__mod__(other))

    def __divmod__(self, other):
        '''
        __divmod__ operator
        '''
        return DataColumn(self.values.__divmod__(other))

    def __pow__(self, other):
        '''
        __pow__ operator
        '''
        return DataColumn(self.values.__pow__(other))

    def __div__(self, other):
        '''
        __div__ operator
        '''
        return DataColumn(self.values.__div__(other))

    def __truediv__(self, other):
        '''
        __truediv__ operator
        '''
        return DataColumn(self.values.__truediv__(other))

    def __radd__(self, other):
        '''
        __radd__ operator
        '''
        return DataColumn(self.values.__radd__(other))

    def __rsub__(self, other):
        '''
        __rsub__ operator
        '''
        return DataColumn(self.values.__rsub__(other))

    def __rmul__(self, other):
        '''
        __rmul__ operator
        '''
        return DataColumn(self.values.__rmul__(other))

    def __rdiv__(self, other):
        '''
        __rdiv__ operator
        '''
        return DataColumn(self.values.__rdiv__(other))

    def __rtruediv__(self, other):
        '''
        __rtruediv__ operator
        '''
        return DataColumn(self.values.__rtruediv__(other))

    def __rfloordiv__(self, other):
        '''
        __rfloordiv__ operator
        '''
        return DataColumn(self.values.__rfloordiv__(other))

    def __rmod__(self, other):
        '''
        __rmod__ operator
        '''
        return DataColumn(self.values.__rmod__(other))

    def __rdivmod__(self, other):
        '''
        __rdivmod__ operator
        '''
        return DataColumn(self.values.__rdivmod__(other))

    def __rpow__(self, other):
        '''
        __rpow__ operator
        '''
        return DataColumn(self.values.__rpow__(other))

    def copy(self):
        '''
        Returns a copy of the object
        '''
        return DataColumn(self.values, self.title)

    def append(self, other):
        '''
        Appends object to the end of column

        Args:
            other (object): can be a DataColumn, a numpy array or a scalar value
        '''
        if isinstance(other, DataColumn):
            self.values = _numpy.append(self.values, other.values)
        else:
            self.values = _numpy.append(self.values, other)
        self.type = self.values.dtype.type

    ##############################
    ### Statistical properties ###
    ##############################

    @property
    def nonnan(self):
        '''
        non-NAN values in the column
        '''
        return self.values[~_numpy.isnan(self.values)]

    @property
    def min(self):
        '''
        Minimum value in the column
        '''
        return min(_numpy.asarray(self.values))

    @property
    def max(self):
        '''
        Maximum value in the column
        '''
        return max(_numpy.asarray(self.values))

    @property
    def mean(self):
        '''
        Mean value in the column
        '''
        return self.sum/len(self.nonnan)

    @property
    def sum(self):
        '''
        sum of all values in the column
        '''
        if len(self) == 0:
            return 0.
        return float(_numpy.nansum(_numpy.asarray(self.values)))

    @property
    def median(self):
        '''
        Median value in the column
        '''
        return float(_numpy.median(_numpy.asarray(self.nonnan)))
    
    @property
    def all(self):
        '''
        True if all values are True
        '''
        return self.values.all()
        
    @property
    def any(self):
        '''
        True if all values are True
        '''
        return self.values.any()

class UnchangeableDataColumn(DataColumn):
    '''
    Class for unchangeable data. This is similar to other DataColumns but
        it cannot be set using UDC[...] = .... Appending is also disabled
        for this class.
    '''
    def __init__(self, the_input=None):
        '''
        UnchangeableDataColumn initiliazation

        Args:
            the_input (list, optional): the_input

        Raises:
            TypeError (Cannot assign an UnchangeableDataColumn object)
        '''
        DataColumn.__init__(self, the_input=the_input)

    def __repr__(self):
        '''
        __repr__ for unchangeable data column
        '''
        return 'UnchangeableDataColumn('+self.values.__repr__()+')'

    def __setitem__(self, item, value):
        '''
        __setitem__ is disabled for UnchangeableDataColumn data
        '''
        raise TypeError('Cannot assign an UnchangeableDataColumn object')

    def append(self, other):
        '''
        append is disabled for UnchangeableDataColumn data
        '''
        raise TypeError('Cannot append to an UnchangeableDataColumn object')

class TimeColumn(AbstractDataColumn):
    '''
    Class for time data
    '''
    import dateutil.parser as parser
    __default_epoch = _dt.datetime(1970, 1, 1)

    def __init__(self, the_input=None, epoch=None):
        '''
        Time data initiliazation

        Args:
            the_input (list, optional): sequence of strings representing the
                time
            epoch (datetime object, optional): epoch. By default,
                dt.datetime(1970,1,1)

        Raises:
            ValueError (cannot be converted to a date)
        '''
        AbstractDataColumn.__init__(self, the_input=the_input, title='time')
        for j, val in enumerate(self.values):
            if isinstance(val, _dt.datetime):
                self.values[j] = val.strftime('%Y-%m-%dT%H:%M:%S.%f')
                continue
            try:
                _ = TimeColumn.parser.parse(val)
            except:
                raise ValueError('{0} cannot be converted to a date'.format(val))

        if epoch is None:
            self.epoch = TimeColumn.__default_epoch
        else:
            self.epoch = epoch

    def __repr__(self):
        '''
        __repr__ for time column
        '''
        return 'TimeColumn('+self.values.__repr__()+')'


    def __getitem__(self, item):
        '''
        Gets item from column
        '''
        if isinstance(item, DataColumn):
            return TimeColumn(self.values[item.values])
        elif isinstance(item, slice):
            return TimeColumn(self.values[item])
        else:
            return self.values[item]

    def __setitem__(self, item, value):
        '''
        Sets item of column
        '''
        if isinstance(value, TimeColumn):
            self.values[item] = value.values
            return
        if _isiterable(value):
            for j, val in enumerate(value):
                ### do sth about datetime objects here
                if isinstance(val, _dt.datetime):
                    value[j] = val.strftime('%Y-%m-%dT%H:%M:%S.%f')
                    continue
                try:
                    _ = TimeColumn.parser.parse(val)
                except:
                    raise ValueError('{0} cannot be converted to a date'.format(val))
        else:
            if isinstance(value, _dt.datetime):
                value = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
            try:
                _ = TimeColumn.parser.parse(value)
            except:
                raise ValueError('{0} cannot be converted to a date'.format(value))

        self.values[item] = value


    def __lt__(self, other):
        '''
        Comparison method: __lt__
        '''
        if isinstance(other, TimeColumn):
            return self.date.__lt__(other.date)
        return self.date.__lt__(other)

    def __le__(self, other):
        '''
        Comparison method: __le__
        '''
        if isinstance(other, TimeColumn):
            return self.date.__le__(other.date)
        return self.date.__le__(other)

    def __gt__(self, other):
        '''
        Comparison method: __gt__
        '''
        if isinstance(other, TimeColumn):
            return self.date.__gt__(other.date)
        return self.date.__gt__(other)

    def __ge__(self, other):
        '''
        Comparison method: __ge__
        '''
        if isinstance(other, TimeColumn):
            return self.date.__ge__(other.date)
        return self.date.__ge__(other)

    def __eq__(self, other):
        '''
        Comparison method: __eq__
        '''
        if isinstance(other, TimeColumn):
            return self.date.__eq__(other.date)
        return self.date.__eq__(other)

    def __ne__(self, other):
        '''
        Comparison method: __ne__
        '''
        if isinstance(other, TimeColumn):
            return self.date.__ne__(other.date)
        return self.date.__ne__(other)

    def __add__(self, other):
        '''
        __add__ operator
        '''
        return TimeColumn(self.date.__add__(other))

    def __sub__(self, other):
        '''
        __sub__ operator
        '''
        if isinstance(other, _dt.datetime):
            return self.date.__sub__(other).map(lambda x: x.total_seconds())
        else:
            return TimeColumn(self.date.__sub__(other))

    def __radd__(self, other):
        '''
        __radd__ operator
        '''
        return TimeColumn(self.date.__radd__(other))

    def copy(self):
        '''
        Returns a copy of the object
        '''
        return TimeColumn(self.values, self.title)

    @property
    def date(self):
        '''
        date property: _numpy array of datetime objects

        Returns:
            a new UnchangeableDataColumn with datetime objects
        '''
        return UnchangeableDataColumn([TimeColumn.parser.parse(val)
                                       for val in self.values])

    def iterdates(self):
        '''
        Generator of dates
        '''
        for val in self.values:
            yield TimeColumn.parser.parse(val)

    @property
    def time_since_epoch(self):
        '''
        time_since_epoch property: _numpy array with time since epoch in seconds

        Returns:
            a new UnchangeableDataColumn with times since epoch in seconds
        '''
        return UnchangeableDataColumn([(TimeColumn.parser.parse(val)-self.epoch).total_seconds()
                                       for val in self.values])

    def itertimes_since_epoch(self):
        '''
        Generator of time_since_epoch
        '''
        for val in self.values:
            yield (TimeColumn.parser.parse(val)-self.epoch).total_seconds()

    def time_from_epoch(self, timestamp):
        '''
        datetime obtained from timestamp since epoch

        Returns:
            datetime.datetime object
        '''
        return self.epoch + _dt.timedelta(seconds=timestamp)

    @property
    def jd(self):
        '''
        jd property: _numpy array with Julian dates

        Returns:
            a new UnchangeableDataColumn with the jds
        '''
        return UnchangeableDataColumn([_date2jd(TimeColumn.parser.parse(val))
                                       for val in self.values])

    @property
    def time(self):
        '''
        time property: _numpy array with times in seconds
            compared to the earliest time in the column

        Returns:
            a new UnchangeableDataColumn with the times in seconds
                starting from 0
        '''
        return UnchangeableDataColumn([val for val in self-self.date.min])

    def iterjds(self):
        '''
        Generator of jds
        '''
        for val in self.values:
            yield _date2jd(TimeColumn.parser.parse(val))

    @property
    def year(self):
        '''
        year property: _numpy array with years

        Returns:
            a new UnchangeableDataColumn with the years
        '''
        return UnchangeableDataColumn([TimeColumn.parser.parse(val).year
                                       for val in self.values])

    @property
    def month(self):
        '''
        month property: _numpy array with months

        Returns:
            a new UnchangeableDataColumn with the months
        '''
        return UnchangeableDataColumn([TimeColumn.parser.parse(val).month
                                       for val in self.values])

    @property
    def day(self):
        '''
        day property: _numpy array with days

        Returns:
            a new UnchangeableDataColumn with the day
        '''
        return UnchangeableDataColumn([TimeColumn.parser.parse(val).day
                                       for val in self.values])

    @property
    def hour(self):
        '''
        hour property: _numpy array with hours

        Returns:
            a new UnchangeableDataColumn with the hours
        '''
        return UnchangeableDataColumn([TimeColumn.parser.parse(val).hour
                                       for val in self.values])

    @property
    def minute(self):
        '''
        minute property: _numpy array with minutes

        Returns:
            a new UnchangeableDataColumn with the minutes
        '''
        return UnchangeableDataColumn([TimeColumn.parser.parse(val).minute
                                       for val in self.values])

    @property
    def second(self):
        '''
        second property: _numpy array with seconds

        Returns:
            a new UnchangeableDataColumn with the seconds
        '''
        return UnchangeableDataColumn([TimeColumn.parser.parse(val).second
                                       for val in self.values])

    @property
    def microsecond(self):
        '''
        microsecond property: _numpy array with micro-seconds

        Returns:
            a new UnchangeableDataColumn with the micro-seconds
        '''
        return UnchangeableDataColumn([TimeColumn.parser.parse(val).microsecond
                                       for val in self.values])

    def reformat(self, the_format):
        '''
        reformats the time stamps to the_format and change all values in the column

        Args:
            the_format: date format (same as for time.strftime)
        '''
        self.values = _numpy.array([TimeColumn.parser.parse(val).strftime(the_format)
                                    for val in self.values])

    def format(self, the_format):
        '''
        formats the time stamps to the_format

        Args:
            the_format: date format (same as for time.strftime)

        Returns:
            a new UnchangeableDataColumn with the formatted times
        '''
        return UnchangeableDataColumn([TimeColumn.parser.parse(val).strftime(the_format)
                                       for val in self.values])

    def iterformat(self, the_format):
        '''
        Generator of formatted time stamps

        Args:
            the_format: date format (same as for time.strftime)
        '''
        for val in self.values:
            yield TimeColumn.parser.parse(val).strftime(the_format)

    @property
    def min(self):
        '''
        Minimum time value in the column as datetime object
        '''
        return self.date.min

    @property
    def max(self):
        '''
        Maximum value in the column
        '''
        return self.date.max

    @property
    def mean(self):
        '''
        Mean value in the column
        '''
        return self.time_from_epoch(self.time_since_epoch.mean)

    @property
    def sum(self):
        '''
        sum of all values in the column.

        Raises:
            TypeError: Cannot perform a sum on a TimeColumn object
        '''
        raise TypeError('Cannot perform a sum on a TimeColumn object')

    @property
    def median(self):
        '''
        Median value in the column
        '''
        return self.time_from_epoch(self.time_since_epoch.median)


    def append(self, other):
        '''
        appends other to the end of column
        '''
        append = _numpy.append
        if isinstance(other, TimeColumn):
            self.values = append(self.values, other.values)
        elif _isiterable(other):
            for j, val in enumerate(other):
                if isinstance(val, _dt.datetime):
                    other[j] = val.strftime('%Y-%m-%dT%H:%M:%S.%f')
                    continue
                try:
                    _ = TimeColumn.parser.parse(val)
                except:
                    raise ValueError('{0} cannot be converted to a date'.format(val))
            self.values = append(self.values, other)
        else:
            if isinstance(other, _dt.datetime):
                other = other.strftime('%Y-%m-%dT%H:%M:%S.%f')
            try:
                _ = TimeColumn.parser.parse(other)
            except:
                raise ValueError('{0} cannot be converted to a date'.format(other))
            self.values = append(self.values, other)
        self.type = self.values.dtype.type

class DataMatrix(object):
    '''
    DataMatrix class
    '''
    def __init__(self, inp=None, names=None):
        '''
        DataMatrix initialization
        '''

        self._letters = _iter_letters()
        columns = {}
        if isinstance(inp, dict):
            for title, column in inp.iteritems():
                if isinstance(column, AbstractDataColumn):
                    column.title = title
                    columns[title] = column.copy()
                elif title == 'time':
                    columns[title] = TimeColumn(column)
                else:
                    columns[title] = DataColumn(column, title=title)
        elif _isiterable(inp):
            if names is not None and len(names) != len(inp):
                raise ValueError('The number of names must match the number of columns')
            for j, column in enumerate(inp):
                if isinstance(column, AbstractDataColumn):
                    if names is not None:
                        title = names[j]
                        column.title = title
                    elif column.title:
                        title = column.title
                    else:
                        title = self._letters.next()
                        column.title = title
                    columns[title] = column
                else:
                    if names is not None:
                        title = names[j]
                    else:
                        title = self._letters.next()
                    columns[title] = DataColumn(column, title=title)
        else:
            if inp is None:
                columns = {}
            elif isinstance(inp, AbstractDataColumn):
                if names is not None and isinstance(names, str):
                    title = names
                    inp.title = title
                elif names is not None and isinstance(names, list):
                    title = names[0]
                    inp.title = title
                elif inp.title:
                    title = inp.title
                else:
                    title = self._letters.next()
                    inp.title = title
                columns[title] = inp
            else:
                if names is not None and isinstance(names, str):
                    title = names
                elif names is not None and isinstance(names, list):
                    title = names[0]
                else:
                    title = self._letters.next()
                columns[title] = DataColumn(inp, title=title)
        self.columns = columns

    @property
    def names(self):
        '''
        names property: returns the column titles/headers
        '''
        return [col.title for col in self.columns.itervalues()]

    def __len__(self):
        '''
        Length of matrix
        '''
        return len(self.columns)

    def __nonzero__(self):
        '''
        truth value
        '''
        return len(self) != 0
        
    def __eq__(self, other):
        '''
        Comparison method: __eq__: Two DataMatrix objects are equal if they
        have the same shape, the same column names and their columns are
        identical.
        '''
        if not isinstance(other, DataMatrix):
            return False
        if self.shape != other.shape:
            return False
        if self.names != other.names:
            return False
        for col in self.names:
            if (self[col] != other[col]).any:
                return False
        return True

    def __ne__(self, other):
        '''
        Comparison method: __ne__
        '''
        if not isinstance(other, DataMatrix):
            return True
        if self.shape != other.shape:
            return True
        if self.names != other.names:
            return True
        for col in self.names:
            if (self[col] != other[col]).any:
                return True
        return False

    def __str__(self):
        '''
        String representation of data column
        '''
        maxind = len(str(self.nrows))+1
        red = '' if not _colorama else _colorama.Fore.RED
        reset_all = '' if not _colorama else _colorama.Style.RESET_ALL
        the_str = '\n'+' '*maxind+red
        names = self.names
        if 'time' in names:
            names.remove('time')
            names = ['time']+ sorted(names)
        else:
            names = sorted(names)
        lengths = [max(len(name), self[name].maxlength)+1 for name in names]
        for j, name in enumerate(names):
            the_str += '  | {name:>{length}}'.format(name=name, length=lengths[j])
        the_str += '\n'+'-'*maxind
        for j, name in enumerate(names):
            the_str += '--|-{name:->{length}}'.format(name='', length=lengths[j])
        the_str += reset_all
        for j, row in enumerate(self):
            the_str += '\n{0:<{maxind}}'.format(j, maxind=maxind)
            for k, name in enumerate(names):
                the_str += ('  '+red+'|'+reset_all+
                            ' {val:>{length}}').format(val=row[name], length=lengths[k])
        return the_str

    def __getitem__(self, index):
        '''
        Gets item from matrix
        '''
        if type(index) in [slice, DataColumn, list, _numpy.ndarray]:
            return DataMatrix({hdr: col[index] for hdr, col in self.columns.iteritems()})

        if index in self.columns:
            return self.column(index)

        if isinstance(index, int):
            return self.row(index)

        raise IndexError('Wrong index type')

    def __setitem__(self, index, value):
        '''
        Sets item of matrix
        '''
        if isinstance(index, slice):
            raise IndexError('Wrong index type')

        if isinstance(index, int):
            raise IndexError('Wrong index type')

        if isinstance(index, str):
            if isinstance(value, AbstractDataColumn):
                if index == 'time' and not isinstance(value, TimeColumn):
                    raise ValueError('The time column must be a TimeColumn object')
                value.title = index
                self.columns[index] = value
            elif index == 'time':
                self.columns[index] = TimeColumn(value)
            else:
                self.columns[index] = DataColumn(value, title=index)

    @property
    def ncols(self):
        '''
        Number of columns
        '''
        return len(self)

    @property
    def nrows(self):
        '''
        Number of rows
        '''
        lengths = [len(col) for col in self.columns.itervalues()]
        if len(lengths) == 0:
            return 0
        if len(lengths) == 1:
            return lengths[0]
        return max(lengths)

    @property
    def shape(self):
        '''
        Matrix shape
        '''
        return self.nrows, self.ncols

    def column(self, index):
        '''
        Gets the column at index
        '''
        return self.columns[index]

    def row(self, index):
        '''
        Gets the row at index
        '''
        if index >= self.nrows:
            raise IndexError('index out of bounds')

        return {hdr: _numpy.nan if index >= len(col) else col[index]
                for hdr, col in self.columns.iteritems()}

    def copy(self):
        '''
        Returns a copy of the object
        '''
        import copy
        input = copy.deepcopy(self.columns)
        return DataMatrix(inp=input)

    def append(self, other):
        '''
        appends other DataMatrix at the bottom
        ''' 
        append = _numpy.append
        
        if not isinstance(other, DataMatrix):
            raise TypeError("Cannot append an object of type {0} to a "
                            "DataMatrix object".format(type(other)))

        if self.names != other.names:
            raise ValueError("Cannot append: the two DataMatrix objects have "
                             "different column names")
        
        for col in self.names:
            self[col].append(other[col])

    def timeplot(self,
                 data=None,
                 ax=None,
                 xlabel='',
                 ylabel='', 
                 time_format='seconds',
                 title='',
                 grid=True,
                 legend=True,
                 prevlines=None,
                 right_data=None,
                 right_color='r',
                 right_label='',
                 **kwargs):
        '''
        Plots a data column as a function of time
        '''
        if 'time' not in self.columns:
            raise TypeError('This data does not contain a `time` column')

        if ax is None:
            fig = _plt.figure()
            ax = fig.add_subplot(111)

        if data is None:
            data = self.columns
            
        otherFormat = False

        if time_format.lower() in ['sec', 'secs', 'second', 'seconds']:
            timevalues = self['time'].time.values
            if not xlabel:
                xlabel = 'Time (in seconds)'
        elif time_format.lower() in ['min', 'mins', 'minute', 'minutes']:
            timevalues = self['time'].time.values/60.
            if not xlabel:
                xlabel = 'Time (in minutes)'
        elif time_format.lower() in ['hr', 'hrs', 'hour', 'hours']:
            timevalues = self['time'].time.values/3600.
            if not xlabel:
                xlabel = 'Time (in hours)'
        elif time_format.lower() in ['day', 'days']:
            timevalues = self['time'].time.values/3600./24.
            if not xlabel:
                xlabel = 'Time (in days)'
        elif time_format.lower() in ['jd', 'jds']:
            timevalues = self['time'].jd.values
            if not xlabel:
                xlabel = 'Time (in Julian Days)'
        elif time_format == '':
            timevalues = self['time'].date.values
            fig.autofmt_xdate()
        else:
            import matplotlib.dates as mdates
            dates = self['time'].date
            timevalues = dates.values
            otherFormat = True
        
        if isinstance(data, AbstractDataColumn):
            line, = ax.plot(timevalues, data.values, label=data.title,
                            **kwargs)
        elif isinstance(data, tuple):
        
            colors = kwargs.pop('color', None)
            if isinstance(colors, str) or colors is None:
                colors = tuple(colors for _ in xrange(len(data)))
            if len(colors) != len(data):
                raise ValueError("Wrong color argument")
                
            linewidths = kwargs.pop('linewidth', 0) or kwargs.pop('lw', 1)
            if isinstance(linewidths, int) or linewidths is None:
                linewidths = tuple(linewidths for _ in xrange(len(data)))
            if len(linewidths) != len(data):
                raise ValueError("Wrong linewidth argument")

            markers = kwargs.pop('marker', None)
            if isinstance(markers, str) or markers is None:
                markers = tuple(markers for _ in xrange(len(data)))
            if len(markers) != len(data):
                raise ValueError("Wrong marker argument")

            for j, subdata in enumerate(data):
                if not isinstance(subdata, AbstractDataColumn):
                    raise TypeError("You can only plots DataColumn objects")
                
                line, = ax.plot(timevalues, subdata.values,
                                label=subdata.title,
                                color=colors[j],
                                linewidth=linewidths[j],
                                marker=markers[j],
                                **kwargs)
        
        elif isinstance(data, dict):

            for j, subdata in enumerate(data.itervalues()):
                if not isinstance(subdata, AbstractDataColumn):
                    raise TypeError("You can only plots DataColumn objects")
                
                try:
                    line, = ax.plot(timevalues, subdata.values,
                                    label=subdata.title, **kwargs)
                except ValueError:
                    print ("Warning: data column not plotted "
                           "({0})".format(subdata.title))
        
        if otherFormat:
            ax.set_xlim([dates.min, dates.max])
            datediff = (dates.max-dates.min).total_seconds()
            daterange = mdates.drange(dates.min, dates.max,
                                      _dt.timedelta(seconds=datediff/6.))
            ax.set_xticks(daterange)
            ax.get_xaxis().set_major_formatter(mdates.DateFormatter(time_format))
            if not xlabel:
                xlabel = 'Time'            
        
        if right_data:
            grid = False

            ax2 = ax.twinx()
            if 'color' in kwargs:
                kwargs.pop('color')
            line2, = ax2.plot(timevalues, right_data.values,
                              color=right_color, label=right_data.title,
                              **kwargs)
            ax2.set_zorder(0)
            if right_label:
                ax2.set_ylabel(right_label, rotation=270, labelpad=15)

        if grid:
            ax.grid(b=True, which='major')
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if title:
            ax.set_title(title)

        if legend:
            if right_data:
                lines = [line, line2]
                ax.set_frame_on(False)
                ax2.set_frame_on(True)
            elif prevlines:
                import matplotlib.lines
                if isinstance(prevlines, matplotlib.lines.Line2D):
                    lines = [prevlines, line]
                elif isinstance(prevlines, list):
                    lines = prevlines + [line]
            else:
                lines = ax.lines
            ax.set_zorder(1)
            labs = [ln.get_label() for ln in lines]
            leg = ax.legend(lines, labs, loc=3)
#            leg.set_zorder(20)
            leg.get_frame().set_alpha(0.8)
        if right_data:
            return (ax, ax2), (line, line2)
        
        return ax, line

    def save_pickle(self, filename):
        '''
        Saves DataMatrix to a pickle file

        Args:
            filename (str): file name.

        Returns:

        Raises:
        '''
        with open(filename, 'w') as fil:
            _pickle.dump(self.columns, fil)

def getheader(filename, delimiter=','):
    '''
    Reads the first line of the csv file, split into an array of column
    headers.

    Args:
        filename (str): file name.
        delimiter (str, optional): Delimiter. Defaults to ','.

    Returns:
        list of column headers of the csv file

    Raises:
    '''
    with open(filename, mode='r') as fil:
        header = fil.readline()
    header = header.strip('\n\r# ')
    fields = header.split(delimiter)
    fields = [field.strip('\'" ') for field in fields]
    return fields

def read_pickle(filename):
    '''
    Reads a pickle file and transfer the content into a DataMatrix.

    Args:
        filename (str): file name.

    Returns:
        DataMatrix with content of the csv file

    Raises:
    '''
    with open(filename, 'r') as fil:
        dic = _pickle.load(fil)
    return DataMatrix(dic)

def read_csv(filename, names=None, delimiter=',', skiplines=0,
             field_header=True):
    '''
    Reads the csv file and transfer the content into a DataMatrix.

    Args:
        filename (str): file name.
        fields (list of str, optional): list of fields or key for the output
            dictionary. This must have the same number of elements than the
            number of columns in your csv file. Defaults to None. If None, the
            keys to the output dictionary will simply be numbers from 0 to the
            number of columns - 1.
        types (function or list of function, optional): function or list of
            functions to convert the data from a string to what you want. You
            can use the functions csvfiles.str2date and csvfiles.str2float.
            Defaults to None. If None, the data type will be str.
        delimiter (str, optional): Delimiter. Defaults to ','.
        skiplines (int, optional): Skip the first n lines. Defaults to 0.
        field_header (bool, optional): If True, it uses the first line of the
            file to determine what the fields are. Defaults to False.

    Returns:
        DataMatrix with content of the csv file

    Raises:
        ValueError, TypeError
    '''

    cols = []
    start = True

    if field_header:
        fields = getheader(filename, delimiter=delimiter)
        skiplines += 1
    elif names:
        fields = names
    else:
        fields = []
    linecounter = 0

    with open(filename, mode='r') as fil:
        for line in fil:
            line = line.strip()
            if not line:
                continue
            row = line.strip('\r\n').split(delimiter)
            linecounter += 1
            if linecounter <= skiplines:
                continue
            if not start:
                if len(row) != len(fields):
                    print ('Line ignored (wrong number of fields: '
                           '{0} instead of {1})').format(len(row), len(fields))
                    print line
                    continue
            for j, item in enumerate(row):
                try:
                    theel = int(item)
                except ValueError:
                    try:
                        theel = float(item)
                    except ValueError:
                        theel = item
                if start:
                    if j >= len(fields):
                        fields.append(j)
                    if (isinstance(fields[j], str)
                            and fields[j].lower() == 'time'):
                        fields[j] = fields[j].lower()
                        cols.append(TimeColumn(theel))
                    else:
                        title = fields[j]
                        if fields[j] == j:
                            title = ''
                        cols.append(DataColumn(theel, title=title))
                else:
                    cols[j].append(theel)
            start = False

    return DataMatrix(cols)

class LoggingError(Exception):
    '''
    LoggingError exception
    '''
    pass

class Logger(object):
    '''
    Logger class: allows easy logging of timed events or variables
    '''
    import os

    def __init__(self, fileroot, delimiter=',', logdir='logs', headers=None,
                 utc=True, timestamp=True, time_format='%Y-%m-%d %H:%M:%S.%f'):
        '''
        Logger initialization:

        Args:
            fileroot (str): the root of the file name. For example,
                if fileroot = 'Blah_', the log files will be similar to
                Blah_20150403.txt

            delimiter (str, optional): the delimiter between columns in the file.
                Default is ',' (csv file)

            logdir (str, optional): name of the directory where to save the logs.
                Default is './logs/'. The logs will then be saved in
                './logs/20150403/Blah_20150403.txt'

            headers (list of str, optional): list of column headers. Default is None.

            utc (bool, optional): time stamps in utc times? Default is True.

            timestamp (bool, optional): Add timestamps to each row? Default is True.

            time_format (str, optional): format for time stamps.
                Default is '%Y-%m-%d %H:%M:%S.%f'.

        '''
        self.fileroot = fileroot
        self.utc = utc
        self.logdir = logdir
        self.headers = [] if headers is None else headers
        self.ncols = len(self.headers)
        self.delimiter = delimiter
        self.time_format = time_format
        self.timestamp = timestamp

    @property
    def datestr(self):
        '''
        datestr property: returns the current date in the format '%Y%m%d'
        '''
        if self.utc:
            return (_dt.datetime.utcnow()-
                    _dt.timedelta(hours=12)).strftime('%Y%m%d')
        else:
            return (_dt.datetime.now()-
                    _dt.timedelta(hours=12)).strftime('%Y%m%d')

    @property
    def filename(self):
        '''
        filename property: returns the name of the file given the current date
        '''
        return Logger.os.path.join(self.logdir, self.datestr,
                                   self.fileroot+'_'+self.datestr+'.txt')

    def exists(self):
        '''
        Does the file exist?
        '''
        return Logger.os.path.exists(self.filename)

    def create_directory(self):
        '''
        Create all directories
        '''
        path, _ = Logger.os.path.split(self.filename)
        if not Logger.os.path.exists(path):
            Logger.os.makedirs(path)

    def write_headers(self):
        '''
        Writes headers to file if file does not already exists
        '''
        if not self.exists() and len(self.headers):
            self.create_directory()
            if self.timestamp:
                hdr = 'time'+self.delimiter
            else:
                hdr = ''
            with open(self.filename, 'a') as fil:
                fil.write(hdr + self.delimiter.join(self.headers)+'\n')
#
    def log(self, *args, **kwargs):
        '''
        Logs data to file

        Args:
            *args: data to log

            warning (bool, optional): adds 'WARNING: ' at the beginning of entry (after timestamp)

            error (bool, optional): adds 'ERROR: ' at the beginning of entry (after timestamp)
        '''
        warning = kwargs.get('warning', False)
        error = kwargs.get('error', False)
        if not self.exists():
            self.create_directory()
            self.write_headers()

        if self.ncols and len(args) != self.ncols:
            raise LoggingError(('The number of arguments must match the number '
                                'of columns in the file ({0} columns, {1} '
                                'arguments)').format(self.ncols, len(args)))
        if self.timestamp:
            timestamp = _dt.datetime.utcnow() if self.utc else _dt.datetime.now()
            timestamp = timestamp.strftime(self.time_format)
            line = timestamp+self.delimiter
        else:
            line = ''
        if error:
            line += 'ERROR: '
        elif warning:
            line += 'WARNING: '
        line += self.delimiter.join('{0}'.format(arg) for arg in args)
        with open(self.filename, 'a') as fil:
            fil.write(line+'\n')
