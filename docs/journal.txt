NAME
    journal

DESCRIPTION
    .. module: logger
    .. moduleauthor: Julien Spronck
    .. created: April 21, 2015
    
    Simple module to handle time-dependent data from csv files.


VERSION
    1.0


MODULES
    datetime
    matplotlib
    numpy
    pickle


FUNCTIONS

    _date2jd(date)
     |  Returns the Julian date from a datetime object
     |  
     |  Args:
     |      date (datetime.datetime object): the date to transform

    _isiterable(obj)
     |  Checks if an object is iterable
     |  
     |  Args:
     |      obj: the object to check

    _iter_letters()
     |  Generator that returns upper case letter combinations:
     |      A, B, C, ..., AA, AB, AC, ... ZX, ZY, ZZ, AAA, AAB, ...
     |  
     |  Args:

    read_csv(filename, names=None, delimiter=', skiplines=0, field_header=True)
     |  Reads the csv file and transfer the content into a DataMatrix.
     |  
     |  Args:
     |      filename (str): file name.
     |      fields (list of str, optional): list of fields or key for the output
     |          dictionary. This must have the same number of elements than the
     |          number of columns in your csv file. Defaults to None. If None, the
     |          keys to the output dictionary will simply be numbers from 0 to the
     |          number of columns - 1.
     |      types (function or list of function, optional): function or list of
     |          functions to convert the data from a string to what you want. You
     |          can use the functions csvfiles.str2date and csvfiles.str2float.
     |          Defaults to None. If None, the data type will be str.
     |      delimiter (str, optional): Delimiter. Defaults to ','.
     |      skiplines (int, optional): Skip the first n lines. Defaults to 0.
     |      field_header (bool, optional): If True, it uses the first line of the
     |          file to determine what the fields are. Defaults to False.
     |  
     |  Returns:
     |      DataMatrix with content of the csv file
     |  
     |  Raises:
     |      ValueError, TypeError

    read_pickle(filename)
     |  Reads a pickle file and transfer the content into a DataMatrix.
     |  
     |  Args:
     |      filename (str): file name.
     |  
     |  Returns:
     |      DataMatrix with content of the csv file
     |  
     |  Raises:



CLASSES

    AbstractDataColumn(object)
     |  Base class for all data column objects
     |  
     |  MODULES
     |      
     |  
     |  VARIABLES
     |      
     |  
     |  FUNCTIONS
     |  
     |      __init__(self, the_input=None, title='')
     |       |  Initialization of the AbstractDataColumn class
     |       |  
     |       |  Args:
     |       |      the_input (object, optional): data input. Can be an iterable, a
     |       |          string, an integer, a float, ...
     |       |      title (str, optional): column title. By default, ''
     |       |  
     |       |  Raises:
     |  
     |      __nonzero__(self)
     |       |  truth value
     |  
     |      __repr__(self)
     |       |  __repr__ for data column
     |  
    DataColumn(AbstractDataColumn)
     |  DataColumn class
     |  
     |  MODULES
     |      
     |  
     |  VARIABLES
     |      
     |  
     |  FUNCTIONS
     |  
     |      __div__(self, other)
     |       |  __div__ operator
     |  
     |      __divmod__(self, other)
     |       |  __divmod__ operator
     |  
     |      __floordiv__(self, other)
     |       |  __floordiv__ operator
     |  
     |      __ge__(self, other)
     |       |  Comparison method: __ge__
     |  
     |      __init__(self, the_input=None, title='')
     |       |  Initialization of the DataColumn class
     |       |  
     |       |  Args:
     |       |      the_input (object, optional): data input. Can be an iterable, a
     |       |          string, an integer, a float, ...
     |       |      title (str, optional): column title. By default, ''
     |       |  
     |       |  Raises:
     |  
     |      __init__(self, the_input=None)
     |       |  UnchangeableDataColumn initiliazation
     |       |  
     |       |  Args:
     |       |      the_input (list, optional): the_input
     |       |  
     |       |  Raises:
     |       |      TypeError (Cannot assign an UnchangeableDataColumn object)
     |  
     |      __le__(self, other)
     |       |  Comparison method: __le__
     |  
     |      __ne__(self, other)
     |       |  Comparison method: __ne__
     |  
     |      __radd__(self, other)
     |       |  __radd__ operator
     |  
     |      __rmod__(self, other)
     |       |  __rmod__ operator
     |  
     |      __rmul__(self, other)
     |       |  __rmul__ operator
     |  
     |      __rpow__(self, other)
     |       |  __rpow__ operator
     |  
     |      __rtruediv__(self, other)
     |       |  __rtruediv__ operator
     |  
     |      __setitem__(self, item, value)
     |       |  __setitem__ is disabled for UnchangeableDataColumn data
     |  
     |      __sub__(self, other)
     |       |  __sub__ operator
     |  
     |      append(self, other)
     |       |  Appends object to the end of column
     |       |  
     |       |  Args:
     |       |      other (object): can be a DataColumn, a numpy array or a scalar value
     |  
     |      max(self)
     |       |  Maximum value in the column
     |  
     |      mean(self)
     |       |  Mean value in the column
     |  
     |      median(self)
     |       |  Median value in the column
     |  
     |      min(self)
     |       |  Minimum value in the column
     |  
     |      nonnan(self)
     |       |  non-NAN values in the column
     |  
     |      sum(self)
     |       |  sum of all values in the column
     |  
    DataMatrix(object)
     |  DataMatrix class
     |  
     |  MODULES
     |      
     |  
     |  VARIABLES
     |      
     |  
     |  FUNCTIONS
     |  
     |      __getitem__(self, index)
     |       |  Gets item from matrix
     |  
     |      __init__(self, inp=None, names=None)
     |       |  DataMatrix initialization
     |  
     |      __nonzero__(self)
     |       |  truth value
     |  
     |      names(self)
     |       |  names property: returns the column titles/headers
     |  
     |      ncols(self)
     |       |  Number of columns
     |  
     |      nrows(self)
     |       |  Number of rows
     |  
     |      row(self, index)
     |       |  Gets the row at index
     |  
     |      save_pickle(self, filename)
     |       |  Saves DataMatrix to a pickle file
     |       |  
     |       |  Args:
     |       |      filename (str): file name.
     |       |  
     |       |  Returns:
     |       |  
     |       |  Raises:
     |  
     |      shape(self)
     |       |  Matrix shape
     |  
    Logger(object)
     |  Logger class: allows easy logging of timed events or variables
     |  
     |  MODULES
     |      os
     |  
     |  VARIABLES
     |      
     |  
     |  FUNCTIONS
     |  
     |      __init__(self, fileroot, delimiter=', logdir='logs', headers=None, utc=True, timestamp=True, time_format='%Y-%m-%d %H:%M:%S.%f')
     |       |  Logger initialization:
     |       |  
     |       |  Args:
     |       |      fileroot (str): the root of the file name. For example,
     |       |          if fileroot = 'Blah_', the log files will be similar to
     |       |          Blah_20150403.txt
     |       |  
     |       |      delimiter (str, optional): the delimiter between columns in the file.
     |       |          Default is ',' (csv file)
     |       |  
     |       |      logdir (str, optional): name of the directory where to save the logs.
     |       |          Default is './logs/'. The logs will then be saved in
     |       |          './logs/20150403/Blah_20150403.txt'
     |       |  
     |       |      headers (list of str, optional): list of column headers. Default is None.
     |       |  
     |       |      utc (bool, optional): time stamps in utc times? Default is True.
     |       |  
     |       |      timestamp (bool, optional): Add timestamps to each row? Default is True.
     |       |  
     |       |      time_format (str, optional): format for time stamps.
     |       |          Default is '%Y-%m-%d %H:%M:%S.%f'.
     |  
     |      datestr(self)
     |       |  datestr property: returns the current date in the format '%Y%m%d'
     |  
     |      filename(self)
     |       |  filename property: returns the name of the file given the current date
     |  
     |      create_directory(self)
     |       |  Create all directories
     |  
     |      log(self)
     |       |  Logs data to file
     |       |  
     |       |  Args:
     |       |      *args: data to log
     |       |  
     |       |      warning (bool, optional): adds 'WARNING: ' at the beginning of entry (after timestamp)
     |       |  
     |       |      error (bool, optional): adds 'ERROR: ' at the beginning of entry (after timestamp)
     |  
    LoggingError(Exception)
     |  LoggingError exception
     |  
     |  MODULES
     |      
     |  
     |  VARIABLES
     |      
     |  
     |  FUNCTIONS
     |  
    TimeColumn(AbstractDataColumn)
     |  Class for time data
     |  
     |  MODULES
     |      dateutil
     |  
     |  VARIABLES
     |      __default_epoch
     |  
     |  FUNCTIONS
     |  
     |      __add__(self, other)
     |       |  __add__ operator
     |  
     |      __eq__(self, other)
     |       |  Comparison method: __eq__
     |  
     |      __getitem__(self, item)
     |       |  Gets item from column
     |  
     |      __gt__(self, other)
     |       |  Comparison method: __gt__
     |  
     |      __init__(self, the_input=None, epoch=None)
     |       |  Time data initiliazation
     |       |  
     |       |  Args:
     |       |      the_input (list, optional): sequence of strings representing the
     |       |          time
     |       |      epoch (datetime object, optional): epoch. By default,
     |       |          dt.datetime(1970,1,1)
     |       |  
     |       |  Raises:
     |       |      ValueError (cannot be converted to a date)
     |  
     |      __lt__(self, other)
     |       |  Comparison method: __lt__
     |  
     |      __radd__(self, other)
     |       |  __radd__ operator
     |  
     |      date(self)
     |       |  date property: _numpy array of datetime objects
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with datetime objects
     |  
     |      day(self)
     |       |  day property: _numpy array with days
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with the day
     |  
     |      hour(self)
     |       |  hour property: _numpy array with hours
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with the hours
     |  
     |      jd(self)
     |       |  jd property: _numpy array with Julian dates
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with the jds
     |  
     |      microsecond(self)
     |       |  microsecond property: _numpy array with micro-seconds
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with the micro-seconds
     |  
     |      minute(self)
     |       |  minute property: _numpy array with minutes
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with the minutes
     |  
     |      month(self)
     |       |  month property: _numpy array with months
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with the months
     |  
     |      second(self)
     |       |  second property: _numpy array with seconds
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with the seconds
     |  
     |      time(self)
     |       |  time property: _numpy array with times in seconds
     |       |      compared to the earliest time in the column
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with the times in seconds
     |       |          starting from 0
     |  
     |      time_from_epoch(self, timestamp)
     |       |  datetime obtained from timestamp since epoch
     |       |  
     |       |  Returns:
     |       |      datetime.datetime object
     |  
     |      time_since_epoch(self)
     |       |  time_since_epoch property: _numpy array with time since epoch in seconds
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with times since epoch in seconds
     |  
     |      year(self)
     |       |  year property: _numpy array with years
     |       |  
     |       |  Returns:
     |       |      a new UnchangeableDataColumn with the years
     |  