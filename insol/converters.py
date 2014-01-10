#!/usr/bin/env python
# encoding: utf-8


"""
converters.py

same set of python_to_solr data format converting function as in pysolr or solango,
this is as common as it can be

"""

from datetime import datetime, date

try:
    import cElementTree as ElementTree
except ImportError:
    try:
        # for python 2.5
        from xml.etree import ElementTree
    except ImportError:
        from elementtree import ElementTree

def py_to_solr(value):
    """
    Converts python values to a form suitable for insertion into the xml
    we send to solr.
    """
    if isinstance(value, datetime):
        value = value.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    elif isinstance(value, date):
        value = value.strftime('%Y-%m-%dT00:00:00.000Z')
    elif isinstance(value, bool):
        if value:
            value = 'true'
        else:
            value = 'false'
    elif isinstance(value, unicode):
        pass
    elif isinstance(value, str):
        value = value.decode('utf-8')
    else:
        value = unicode(value)
    return value

def bool_to_python(self, value):
    """
    Convert a 'bool' field from solr's xml format to python and return it.
    """
    if value == 'true':
        return True
    elif value == 'false':
        return False

def str_to_python(self, value):
    """
    Convert an 'str' field from solr's xml format to python and return it.
    """
    return unicode(value)

def int_to_python(self, value):
    """
    Convert an 'int' field from solr's xml format to python and return it.
    """
    return int(value)

def date_to_python(self, value):
    """
    Convert a 'date' field from solr's xml format to python and return it.
    """
    # this throws away fractions of a second
    return datetime(*strptime(value[:-5], "%Y-%m-%dT%H:%M:%S")[0:6])

def double_to_python(self, value):
    """
    Convert a 'double' field from solr's xml format to python and
    return it.
    As Python does not have separate type for double, this is the same
    as float.
    """
    return self.float_to_python(value)

def float_to_python(self, value):
    """
    Convert a 'float' field from solr's xml format to python and return it.
    """
    return float(value)

# API Methods ############################################################



def _field_to_xml(args):
    """
    takes two arguments in a form of tuple \n
    a field name and a field value         \n
    """
    key = args[0]
    value = args[1]
    field = ElementTree.Element('field', name = key)
    field.text = py_to_solr(value)
    return field

def _iterable_to_xml(iterable):
    """
    converts iterable object to xml   \n
    
    """
    converted = list()
    for key, value in iterable.iteritems():
        if hasattr(value, '__iter__'):
            converted.extend(map(_field_to_xml, ((key, val) for val in value)))
        else:
            converted.append(_field_to_xml((key, value)))
    return converted

def _to_document(data):
    """
    convert data dict to xml 'doc' element
    """
    
    document = ElementTree.Element('doc')
    map(document.append, _iterable_to_xml(data))
    return document


def msg_from_iterable(elems):
    """
    create full valid xml message for solr (adding data)
    """
    message = ElementTree.Element('add')
    map(message.append,  map(_to_document, elems))
    return ElementTree.tostring(message)


def solr_inf(x):
    """
    treat -1 in range queries as infinity
    """
    if x == -1:
        return '*'
    return x


def datemath(start, end, gap):
    """
    Function to parse pythonic objects into Solr DateMath
     compatible string
     
    :rtype dict: dict with start, end and gap converted to Solr DateMath compatible params
    :param datetime start: begining of the date facet
    :param datetime end: end of the date facet
    :param timedelta gap: gap for faceting - increment between consecutive facets
    """
    now = datetime.now()
    assert start <= end, "Date range start value cannot be greater then end"
    start_td = start - now
    end_td = end - now
    _n = 'NOW-0SECONDS'
    resp = dict()
    for field, value in [
        ('start', start_td),
        ('end', end_td),
    ]:
        if int(value.total_seconds()):
            resp[field] = 'NOW%sSECONDS' % int(value.total_seconds())
        else:
            resp[field] = 'NOW-0SECONDS'
    resp['gap'] = '+%sSECONDS' % int(gap.total_seconds())
    return resp



