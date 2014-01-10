#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""

.. module:: datastructures
   :platform: Unix, Windows, Linux
   :synopsis: Code for easy data managment
.. :moduleauthor: Michal Domanski <michal.domanski@sensisoft.com>


"""


from converters import py_to_solr, datemath
from config import DEFAULT_OPERATOR
from datetime import datetime, timedelta

class Searchable(object):
    """ 
    Field parameters are class variables, define per class
    """

    multivalued = False
    required = False    # field required by the search app (show "what should i search for")
    boost = False
    field_name = None   # the application field_name, used as query parameters, may be different from the...
    solr_query_field = None   # SOLR schema name
    solr_index_field = None
    solr_query_param = 'q'  # default target for solr query, either q or fq.
                        # using fq allows better query result caching in solr, so params with commonly used values shoud go there
                        #good candidates are: advert_type, region, category, is_active

    orderable = False   # is it possible to order search results by it?
    _parsed_search_term = None


    def __init__(self, *searchables, **kwargs):
        self.operator = kwargs.get('operator', DEFAULT_OPERATOR )
        if isinstance(searchables[0], Searchable):  # we are inside more complicated query
            self._parsed_search_term = self.operator.join([searchable.parsed_search_term for searchable in searchables])
        else:  # we are simple creating one object
            self.value = searchables[0]

    # A helper method for returning a single solr term according to the fields mandatory and boost settings
    # Can be used to join multivalue queries (right?)
    
    @property
    def _id(self):
        return '%s_%s'%(self.__class__.__name__, hash(self.parsed_search_term) )
    
    @property
    def parsed_search_term(self):
        if not self._parsed_search_term:
            self._parsed_search_term = self.__class__.search_term(self.solr_query_field, self.value)
        return self._parsed_search_term
        
    @classmethod
    def search_term(cls, key, value):
        """ 
        Default search term for signle value lookup
        """
        temp = list()
        temp.append('(')
        temp.append(str(key))
        temp.append(':')
        temp.append(py_to_solr(value))
        if cls.boost:
            temp.append('^%s' % str(cls.boost))
        temp.append(')')
        return ''.join(temp)

class Filter(Searchable):
    """
    Class for use of advanced filtering options and/or writing down queries as objects.
    """

    solr_query_param = 'fq'

    def __init__(self, *args, **kwargs):
        self._parsed_search_term = self.__class__.search_term(*args, **kwargs)

    @classmethod
    def search_term(cls, field, value, cache=None, cost=None):
        full_field = '%s:%s' % (field, value)
        if cache != None or cost:
            opts = '{!'
            if cache != None:
                opts = '%s cache=%s' % (opts, cache and 'true' or 'false')
            if cost:
                opts = '%s cost=%s' % (opts, cost)
            full_field = "%s}%s" % (opts, full_field)
        return [(cls.solr_query_param, full_field)]

class Facet(Searchable):
    """
    Class for handling faceting in pythonic way, yet with a somehow shameful biterness of java.
    Used only as an attribute of Query class instance.

    .. warning:: 
        Beware, this should only be used in conjuntion with Query class instance.

    """
    solr_query_param = 'facet'
    
    
    def __init__(self, *args, **kwargs):
        self._parsed_search_term = self.__class__.search_term(*args, **kwargs)

    @property
    def _id(self):
        return '%s_%s'%(self.__class__.__name__, hash(tuple(self.parsed_search_term)) )

    @classmethod
    def search_term(cls, field,
                    prefix=None, sort=None, limit=None,
                    offset=None, mincount=None, missing=False,
                    method=None, query=None):
        temp = [('facet.field', field)]
        if prefix:
            temp.append(('f.%s.facet.prefix' % field, prefix))
        if sort:
            temp.append(('f.%s.facet.sort' % field, 'true'))
        if limit:
            temp.append(('f.%s.facet.limit' % field, limit))
        if offset:
            temp.append(('f.%s.facet.offset' % field, offset))
        if mincount:
            temp.append(('f.%s.facet.mincount' % field, mincount))
        if missing:
            temp.append(('f.%s.facet.missing' % field, 'true'))
        if method:
            temp.append(('f.%s.facet.method' % field, method))
        if query:
            temp.append(('f.%s.facet.query' % field, query))
        return temp


class DateFacet(Searchable):
    solr_query_param = 'facet'

    def __init__(self, *args, **kwargs):
        self._parsed_search_term = self.__class__.search_term(*args, **kwargs)

    @classmethod
    def search_term(cls, field, start, end, gap,
                    hardend=None, other=None, include=False):
        temp = [('facet.date', field)]
        converted = datemath(start, end, gap)
        temp.append(('f.%s.facet.date.start' % field, converted['start']))
        temp.append(('f.%s.facet.date.end' % field, converted['end']))
        temp.append(('f.%s.facet.date.gap' % field, converted['gap']))
        if hardend:
            temp.append(('f.%s.facet.date.hardend' % field, 'true'))
        return temp

class RangeFacet(Searchable):
    solr_query_param = 'facet'

    def __init__(self, *args, **kwargs):
        self._parsed_search_term = self.__class__.search_term(*args, **kwargs)

    @classmethod
    def search_term(cls, field, start, end, gap,
                    hardend=None, other=None, include=False):
        temp = [('facet.date', field)]
        if start:
            temp.append(('f.%s.facet.start' % field, start))
        if end:
            temp.append(('f.%s.facet.end' % field, end))
        if gap:
            temp.append(('f.%s.facet.gap' % field, gap))
        if hardend:
            temp.append(('f.%s.facet.hardend' % field, 'true'))
        return temp