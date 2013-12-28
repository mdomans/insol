#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Simple set of extensible objects for easy handling of data returned from solr

Created by michal.domanski on 2009-02-24.

"""
from tools import filter_even, filter_odd


class Response:
    
    @property
    def time(self):
        return self._header['QTime']
    @property
    def status(self):
        return self._header['status']
    @property
    def params(self):
        return self._header['params']
        
class SelectResponse(Response):
    
    @property
    def docs(self):
        return self._response['docs']
    @property
    def hits(self):
        return self._response['numFound']
    @property
    def facets(self):
        return self._facets

    def get_facet_as_dict(self, field_name):
        """
        .. warning:: not properly tested yet
        
        Return facets dict for a given field name, requires faceting parameters issued in query
        """
        facet_list = self._facets['facet_fields'][field_name]
        return dict(zip( filter_odd(facet_list), filter_even(facet_list)))
        
    @property
    def facet_fields_dict(self):
        """
        .. warning:: watchout, this may cost you some RAM

        Builds a dict, where faceting field names are keys and faceting dicts are value, thus
        creating a nested dict, requires faceting parameters issued in query

        """
        loc_get_facet_as_dict = self.get_facet_as_dict
        f_keys = self._facets['facet_fields'].keys()
        return dict(zip(f_keys, map(loc_get_facet_as_dict, f_keys)))

    @property
    def stats(self):
        return self._stats
