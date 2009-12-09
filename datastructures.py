#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""

.. module:: datastructures
   :platform: Unix, Windows, Linux
   :synopsis: Code for easy data managment
.. :moduleauthor: Michal Domanski <michal.domanski@sensisoft.com>


"""




from converters import py_to_solr
from config import DEFAULT_OPERATOR


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
    solr_query_param = 'q'  #default target for solr query, either q or fq.
                        #using fq allows better query result caching in solr, so params with commonly used values shoud go there
                        #good candidates are: advert_type, region, category, is_active

    orderable = False   # is it possible to order search results by it?
    _parsed_search_term = None


    def __init__(self, *searchables, **kwargs):
        self.operator = kwargs.get('operator', DEFAULT_OPERATOR )
        if isinstance(searchables[0], Searchable):# we are inside more complicated query
            self._parsed_search_term = self.operator.join([searchable.parsed_search_term for searchable in searchables])
        else:# we are simple creating one object
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
        temp = []
        temp.append('(')
        temp.append(str(key))
        temp.append(':')
        temp.append(py_to_solr(value))
        if cls.boost:
            temp.append('^%s'%str(cls.boost))
        temp.append(')')
        return ''.join(temp)



class Facet(Searchable):
    """

    Class for handling faceting in pythonic way, yet with a somehow shameful biterness of java.
    Used only as an attribute of Query class instance.

    .. warning:: 
        Beware, this should only be used in conjuntion with Query class instance.


    """
    solr_query_param = 'facet'  #default target for solr query, either q or fq.
    
    
    def __init__(self, *args, **kwargs):
        self._parsed_search_term = self.__class__.search_term(*args, **kwargs)
        
    
    @property
    def _id(self):
        return '%s_%s'%(self.__class__.__name__, hash(tuple(self.parsed_search_term)) )

    
    @classmethod
    def search_term(cls, field, prefix=None, sort=None, limit=None, offset=None, mincount=None, missing=False, method=None):
        temp = []
        temp.append( ('facet.field', field ))
        if prefix:
            temp.append( ('f.%s.facet.prefix' % field, prefix) )
        if sort:
            temp.append( ('f.%s.facet.sort'% field , 'true') )
        if limit:
            temp.append( ('f.%s.limit' % field, limit) )
        if offset:
            temp.append( ('f.%s.offset'% field, offset) )
        if mincount:
            temp.append( ('f.%s.mincount'% field, mincount) )
        if missing:
            temp.append( ('f.%s.missing'% field , 'true'))
        if method:
            temp.append( ('f.%s.method' % field, method) )
        return temp
            

