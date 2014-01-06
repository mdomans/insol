.. insol documentation master file, created by
   sphinx-quickstart on Wed Jan  1 21:11:09 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Insol
=====
Insol is an:

- clean, flexible object oriented Solr_ API designed for large project development
- evolution of a battle tested API for Solr_ search engine from Sensisoft_ (I used to work there)
- released unders Apache_ license

It enables simple hacking around with Solr_
    >>> from insol.shortcuts import find
    >>> resp = find('test')
    >>> print resp.docs

As well as more advanced constructs
    >>> from insol import connection
    >>> from insol.query import Query
    >>> connection.search(Query(q='testing',fq=['region:1'],facets=['category']))

And very objectified structures
    >>> from insol import connection
    >>> from insol.datastructures import Facet
    >>> from inso.query import Query
    >>> connection.search(Query('tests', Facet('region', mincount=3)))


Motivation
----------

As far as my experience goes good Solr API should be:

- **developer friendly** - you can connect and get result from a working Solr instance in less than 5 minutes and you can test all featuers of Solr
- **teamwork friendly** - you can write code others can use without being Solr experts and debug without spending a week analyzing some weird code constructs or mysterious strings
- **scale friendly** - API needs to support sharding, multiple core deployments, querying Solr instances at various paths and should be performant
So, to solve that problems, insol delivers:

- REPL friendly shortcuts module to start working right away
- Solr queries as Python objects, so that others can use your code abstracted away from inner workings of Solr - this is a design similar to Django ORM with it's Q and F objects
- fast and cache friendly - results as simple dicts, no builtin dict to object inflation code - either use the results as-is or provide your own inflation mechanism
- configuration module with live config reload to support connecting to multiple Solr instances or cores at run time
- flexible structure allowing you to customize the whole process of connecting to Solr instance and fetching documents without rewriting whole API

The core concept of **insol** is that building software is a group effort with a business objective, so API authors should strive to make it easy to write understandable and flexible code.


.. _Solr: http://lucene.apache.org/solr/
.. _SensiSoft: http://www.sensisoft.com/
.. _Apache: http://opensource.org/licenses/Apache-2.0

.. toctree::
   :maxdepth: 2


   installation
   compatibility
   philosophy
   basic
   searchables
   faceting
   spatial
   contributing
   roadmap


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

