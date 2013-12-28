[![Build Status](https://travis-ci.org/mdomans/insol.png?branch=master)](https://travis-ci.org/mdomans/insol)
insol
=====
***
##Python - Solr API

Insol is a API for [Solr](http://lucene.apache.org/solr/) search engine. It's main features are:

- ability to start hacking away fast
- object oriented approach to Queries, instead of returning objects and taking string queries, __insol__ uses object oriented query building and returns simple python dicts

The core concept of insol is that building properly structured queries is hard while parsing returned values is rather simple. For that problem we need a way to express complex queries as objects.

What's more, __insol__ does not perform any _result-to-object_ evaluation, avoiding unnecessary DB hits. In case you need such mode of operation, it's easy to implement.



