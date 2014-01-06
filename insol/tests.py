#!/usr/bin/env python
# encoding: utf-8

"""
tests.py

Created by mdomans on 2009-03-26.
"""


def test_searchables():
    from datastructures import Searchable
    from query import Query
    #
    #  this is how you may define your very own searchables
    #
    class CategorySearchable(Searchable):
        multivalued = True
        solr_query_field = 'categories'
        solr_query_param = 'fq'
    class RegionSearchable(Searchable):
        multivalued = True
        solr_query_field = 'regions'
        solr_query_param = 'fq'
    #
    # use them
    # 
    reg1 = RegionSearchable(1)
    cat1 = CategorySearchable(1)
    #
    # mix them
    #
    anded = Searchable(reg1, cat1, operator='AND')
    ored = Searchable(reg1, cat1, operator='OR')
    #
    # and make a query...simple, huh ? :)
    #
    q = Query(anded)
    return locals()# this is usefull for testing in ipython, and nosetests still pass :)
    #connection.search(Query(CategorySearchable(category_value)))
        
def test_connection():
    from datastructures import Searchable, Facet
    from query import Query
    import connection
    import config
    #
    #  define all , will be rewritten to set_up/tear_down when i find some time for cleanup
    #
    class CategorySearchable(Searchable):
        multivalued = True
        solr_query_field = 'categories'
        solr_query_param = 'fq'
    class RegionSearchable(Searchable):
        multivalued = True
        solr_query_field = 'regions'
        solr_query_param = 'fq'
    reg1 = RegionSearchable(1)
    cat1 = CategorySearchable(1)
    OR_searchable = Searchable(reg1, cat1, operator='OR')
    
    config.set_config('dev', '0.0.0.0', 8983)
    config.load_config('dev') # set up addresses and stuff 
    
    connection.search(Query(OR_searchable, Facet('regions', mincount=1)))

def test_query_syntax():
    from datastructures import Facet, Filter
    from query import Query
    from connection import InsolConnection
    conn = InsolConnection('0.0.0.0', 8983, 'collection')

    resp = conn.search(Query('test', Facet('cat', mincount=1)))
    assert resp.docs
    assert resp.facets

    resp = conn.search(Query(Facet('cat', mincount=1)))
    assert resp.facets, "Query: *:* with faceting failed"

    resp = conn.search(Query())
    assert resp.docs, "Query: *:* failed"

    resp = conn.search(Query(facets=['cat']))
    assert resp.facets, 'Faceting query failed'

    resp = conn.search(Query(facets=[Facet('cat')]))
    assert resp.facets, 'Faceting query failed'

    resp = conn.search(Query('test', fq=[('name','test')]))
    assert resp.docs, "Failed fq query"

    resp = conn.search(Query('test', fq=[('name','test')], facets=[Facet('cat', mincount=1)]))
    assert resp.docs, "Failed fq query"

    resp = conn.search(Query('*:*', fq=[Filter('cat', 'electronics')], facets=[Facet('cat')]))
    assert resp.docs, "Failed fq and facets object query"

def test_shortcuts():
    import shortcuts
    assert shortcuts.find()
    resp = shortcuts.find()
    assert resp.docs
    assert resp.hits
    assert resp.params
    assert resp.params == {u'q': u'*:*', u'wt': u'json'}
    assert shortcuts.find({'q': '*:*'})

def test():
    test_query_syntax()
    
if __name__ == '__main__':
    test()
