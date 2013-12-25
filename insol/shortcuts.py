__author__ = 'alakota'

import query, config, connection

def find(*args, **kwargs):
    config.set_config('dev', '0.0.0.0', 8983)
    config.load_config('dev')
    connection_kwargs = {}
    if 'wt' in kwargs:
        connection_kwargs['wt'] = kwargs.pop('wt')
    return connection.search(query.Query(*args, **kwargs), **connection_kwargs)