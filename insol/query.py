#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""

.. module:: query
   :platform: Unix, Windows, Linux
   :synopsis: Code for construction and handling of data send to solr
.. :moduleauthor: Michal Domanski <mdomans@gmail.com>

"""


import urllib
import datastructures


class Query(dict):


    def __init__(self, *args, **kwargs):
        self.clear()
        self._build(*args, **kwargs)

    def clear(self):
        """
           Clear any changes to query
        """
        self.q = []
        self.sort = []
        self.fq = []
        self.facets = []
        self.stats = {}
        self.fl = []
        self.start = 0
        self.rows = 0


    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def _build(self, *args, **kwargs):
        if args:
            self._parse_args(args)
        if kwargs:
            self._parse_kwargs(kwargs)

    def _parse_args(self, args):
        if args and isinstance(args[0], dict):
            self._parse_kwargs(args[0])
        if args and isinstance(args[0], basestring):
            self.q.append(('q',args[0]))
        for arg in args:
            if isinstance(arg, datastructures.Facet):
                self.facets.extend(arg.parsed_search_term)
            elif isinstance(arg, datastructures.Filter):
                self.fq.extend(arg.parsed_search_term)


    def _parse_kwargs(self, kwargs):
        if 'q' in kwargs:
            self.q.append(('q',kwargs.get('q')))
        if 'fq' in kwargs:
            fq = kwargs['fq']
            assert isinstance(fq, list), "fq argument needs to be a list"
            self.fq = [x for y in [self._parse_fq(f) for f in fq] for x in y]

        if 'facets' in kwargs:
            facets = kwargs['facets']
            assert isinstance(facets, list), "facets argument needs to be a list"
            self.facets = [x for y in [self._parse_facet(f) for f in facets] for x in y]

        if 'stats' in kwargs:
            self.stats['from_kwargs'] = kwargs.get('stats')

    def _parse_fq(self, f):
        if isinstance(f, basestring):
            return [('fq', f)]
        if isinstance(f, tuple):
            return [('fq', ':'.join(f))]
        if isinstance(f, datastructures.Filter):
            return f.parsed_search_term

    def _parse_facet(self, f):
        if isinstance(f, basestring):
            return [('facet.field', f)]
        if isinstance(f, datastructures.Facet):
            return f.parsed_search_term

    @property
    def _url(self):
        params = []
        q = False
        for key, value in self.items():
            if key in ['q', 'fq', 'fl', 'facets']:
                params.extend(value)
            elif key == 'sort':
                params.append( ('sort', ','.join(value)), )


        if not 'q' in self or not self['q']:
            params.append(('q','*:*'))
        query = urllib.urlencode(params)

        if 'facets' in self and self.facets:
            query = '%s&%s' % (query, 'facet=true')

        if 'stats' in self and self.stats:
            query = '%s&%s' % (query, 'stats=on')

        if 'wt' in self and self.wt:
            query = '%s&wt=%s' % (query, self.wt)
            
        return query




