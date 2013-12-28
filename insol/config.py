#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Created by michal.domanski on 2009-02-24.
"""


SEARCH_FACET_PARAMS = ''
SEARCH_HL_PARAMS = ''
SOLR_ADDRESS = ''
SOLR_PORT = 0
SOLR_CORE = 'collection'
SOLR_SELECT_PATH = 'select'
SOLR_UPDATE_PATH = 'update'
SOLR_PING_PATH = 'admin/ping'
DEFAULT_OPERATOR = 'OR'

CONFIGS = {
    'dev': {
        'host': '0.0.0.0',
        'port': '8983',
        'core': 'collection',
    },
}
DEFAULT_CONFIG = 'dev'

CONFIGS = {}
SEARCH_PLUGINS = []


def get_configs():
    "return list of configs"
    return CONFIGS
    
def load_config(config_name):
    """
    loads config specified by name given and reload connnection
    """
    import connection
    global SOLR_PORT, SOLR_ADDRESS, SOLR_CORE
    config = CONFIGS[config_name]
    SOLR_CORE = config['core']
    SOLR_PORT = config['port']
    SOLR_ADDRESS = config['host']
    connection.reload_config()

def add_to_plugins(plugin):
    global SEARCH_PLUGINS
    SEARCH_PLUGINS.append(plugin)
        
def set_plugins(plugins):
    global SEARCH_PLUGINS
    SEARCH_PLUGINS = plugins

def set_config(config_name, host, port, core=''):
    """
    adds your config to global set of configs
    """
    global CONFIGS
    CONFIGS[config_name] = {'host': host, 'port': port, 'core': core}
        
def get_current_config():
    """
    return current config loaded data
    """
    global SOLR_ADDRES, SOLR_PORT, SOLR_CORE
    return {'host': SOLR_ADDRESS, 'port': SOLR_PORT, 'core': SOLR_CORE}


