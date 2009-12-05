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

.. module:: query
   :platform: Unix, Windows, Linux
   :synopsis: Code for construction and handling of data send to solr
.. :moduleauthor: Michal Domanski <mdomans@gmail.com>

"""


from datastructures import Searchable, py_to_solr
import config
import urllib



class Query(dict):


    def __init__(self, *args, **kwargs):
        self.clear()
        self._clean(*args, **kwargs)

    def clear(self):
        """
           Clear any changes to query
        """
        self.q = {}
        self.sort = []
        self.fq = {}
        self.fl = []
        self.start = 0
        self.rows = 20


    #So we can do url.url
    def __getattr__(self, name):
        return self[name]
    #So we can do url.url = '/'
    def __setattr__(self, name, value):
        self[name] = value

    def _clean(self, *args, **kwargs):
        """        
        """
        if args and isinstance(args[0], Searchable):# we have query to be built from Searchables
            self._build_from_searchables(args)

        else:
            self._build_from_args(*args, **kwargs)
    
    def _build_from_searchables(self, searchables):
        for searchable in searchables:
            if searchable.solr_query_param == 'q':
                self.q[searchable._id] = searchable.parsed_search_term
            elif searchable.solr_query_param == 'fq':
                self.fq[searchable._id] = searchable.parsed_search_term
            elif searchable.solr_query_param == 'facet':
                self.facets[searchable._id] == searchable.parsed_search_term
            elif searchable.solr_query_param == 'stats':
                self.stats[searchable._id] == searchable.parsed_search_term
        
    @property
    def _url(self):
        params = []
        q = False
        for key, value in self.items():
            if not value or key.startswith('_'):
                continue
            if key in ['q','fq','stats','facets']:
                params.append( (key, ''.join(value.values())) )
            elif key == 'sort':
                params.append( ('sort', ','.join(value)), )
            else:
                params.append( (key, value) )

        if not q in self:
            params.append(('q','*:*'))
            
        query = urllib.urlencode(params)

        if hasattr(self, 'facet') and self.facets:
            query = '%s&%s' % (query, 'facet=true')

        if hasattr(self, 'stats') and self.stats:
            query = '%s&%s&%s' % (query, 'stats=on')
            
        return query




