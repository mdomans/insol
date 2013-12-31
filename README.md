[![Build Status](https://travis-ci.org/mdomans/insol.png?branch=master)](https://travis-ci.org/mdomans/insol)
#insol
***
##Python - Solr API

Insol is an evolution of a battle tested API for [Solr](http://lucene.apache.org/solr/) search engine, the development of which started while I was working at [SensiSoft](http://www.sensisoft.com/).

As far as my experience goes good Solr API should be:

- __developer friendly__ - you can connect and get result from a working Solr instance in less than 5 minutes and you can test all featuers of Solr
- __teamwork friendly__ - you can write code others can use without being Solr experts and debug without spending a week analyzing some weird code constructs or mysterious strings
- __scale friendly__ - API needs to support sharding, multiple core deployments, querying Solr instances at various paths and should be performant

So, to solve that problems, __insol__ delivers:

- REPL friendly __shortcuts__ module to start working right away
- Solr queries as Python objects, so that others can use your code abstracted away from inner workings of Solr - this is a design similar to Django ORM with it's Q and F objects
- fast and cache friendly - results as simple dicts, no builtin dict to object inflation code - either use the results as-is or provide your own inflation mechanism
- configuration module with live config reload to support connecting to multiple Solr instances or cores at run time
- flexible structure allowing you to customize the whole process of connecting to Solr instance and fetching documents without rewriting whole API

The core concept of __insol__ is that building software is a group effort with a business objective, so API authors should strive to make it easy to write understandable and flexible code.

## Compatibility

__insol__ is compatible works with:

- Python 2.6 and later versions
- Solr 1.4

## Instalation

To install latest version from PyPI typing:

`pip install insol`

is enough.
Or you can install this package (cutting edge version):
`python setup.py install`

## Usage

To simply try to see what happens or for testing particular queries against your Solr instance:

```python
from insol.shortcuts import find
resp = find()
print resp.docs
```

##Roadmap:

* adding JSON to supported communication formats
* moving to **requests** library for handling HTTP and HTTPS communication




