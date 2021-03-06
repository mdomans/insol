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
        
def test_faceting():
    from datastructures import Facet
    from query import Query
    import connection
    import config
    config.set_config('dev', '0.0.0.0', 8983)
    config.load_config('dev') # set up addresses and stuff 
    
    response = connection.search(Query(Facet('regions', mincount=1)))

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
    test_shortcuts()
    
if __name__ == '__main__':
    test()
