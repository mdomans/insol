#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""

.. module:: query
   :platform: Unix, Windows, Linux
   :synopsis: Code for construction and handling of data send to solr
.. :moduleauthor: Michal Domanski <mdomans@gmail.com>

"""


from datastructures import Searchable
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
        self.facets = {}
        self.stats = {}
        self.fl = []
        self.start = 0
        self.rows = 0


    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def _clean(self, *args, **kwargs):
        """        
        """
        if args and isinstance(args[0], Searchable):# we have query to be built from Searchables
            self._build_from_searchables(args)
        else:
            self._build_from_args(*args, **kwargs)

    def _build_from_args(self, *args, **kwargs):
        if args or 'q' in kwargs:
            q = kwargs.get('q') or args and args[0]
            # assert isinstance(q, basestring),
            if isinstance(q, basestring):
                raise Warning("q parameter should be a string")
                self.q['from_args'] = q
        if 'fq' in kwargs:
            self.fq['from_args'] = kwargs.get('fq')
        if 'facets' in kwargs:
            self.facets['from_args'] = kwargs.get('facets')
        if 'stats' in kwargs:
            self.stats['from_args'] = kwargs.get('stats')



    def _build_from_searchables(self, searchables):
        for searchable in searchables:
            if searchable.solr_query_param == 'q':
                self.q[searchable._id] = searchable.parsed_search_term
            elif searchable.solr_query_param == 'fq':
                self.fq[searchable._id] = searchable.parsed_search_term
            elif searchable.solr_query_param == 'facet':
                self.facets[searchable._id] = searchable.parsed_search_term
            elif searchable.solr_query_param == 'stats':
                self.stats[searchable._id] = searchable.parsed_search_term
        
    @property
    def _url(self):
        params = []
        q = False
        for key, value in self.items():
            if not value or key.startswith('_'):
                continue
            if key in ['q','fq']:
                params.append( (key, ''.join(value.values())) )
            elif key in ['stats','facets']:
                for facet_params in value.values():
                    params.extend(facet_params)
            elif key == 'sort':
                params.append( ('sort', ','.join(value)), )
            else:
                params.append( (key, value) )

        if not 'q' in self or not self['q']:
            params.append(('q','*:*'))
        query = urllib.urlencode(params)

        if 'facets' in self and self.facets:
            query = '%s&%s' % (query, 'facet=true')

        if 'stats' in self and self.stats:
            query = '%s&%s' % (query, 'stats=on')
            
        return query




