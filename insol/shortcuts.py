#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""

.. module:: shortcuts
   :platform: Unix, Windows, Linux
   :synopsis: Shortcuts for adhoc development, testing and hacking around with your server
.. :moduleauthor: Michal Domanski <mdomans@gmail.com>

"""

import query, config, connection

def find(*args, **kwargs):
    """
    Wrapper around the API:
    - loads default config (check config module)
    - builds query from *args and **kwargs
    - passes that query into connection for searching

    """
    config.load_config(config.DEFAULT_CONFIG)
    connection_kwargs = {}
    if 'wt' in kwargs:
        connection_kwargs['wt'] = kwargs.pop('wt')
    return connection.search(query.Query(*args, **kwargs), **connection_kwargs)

def index():
    pass