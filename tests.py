#!/usr/bin/env python
# encoding: utf-8

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
tests.py

Created by mdomans on 2009-03-26.
"""

import nose


def test_import_config():
    import config
def test_import_connection():
    import connection
def test_import_datastructures():
    import datastructures
def test_import_query():
    import query
def test_import_results():
    import results
def test_import_converters():
    import converters
def test_import_manager():
    import manager
def test_import_tools():
    import tools

def test_searchables():
    from datastructures import Searchable
    from query import Query
    
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
    
    anded = Searchable(reg1, cat1, operator='AND')
    ored = Searchable(reg1, cat1, operator='OR')
    q = Query(anded)
    return locals()
    #connection.search(Query(CategorySearchable(category_value)))
        
        
        
        
    
    
    
    
    