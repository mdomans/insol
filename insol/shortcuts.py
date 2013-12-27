#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

.. module:: shortcuts
   :platform: Unix, Windows, Linux
   :synopsis: Shortcuts for adhoc development, testing and hacking around with your server
.. :moduleauthor: Michal Domanski <mdomans@gmail.com>

"""

import query,config, connection

def find(*args, **kwargs):
    """
    Wrapper around the API:
    - loads default config (check config module)
    - builds query from *args and **kwargs
    - passes that query into connection for searching

    """
    config.set_config(
        config.DEFAULT_CONFIG,
        config.CONFIGS[config.DEFAULT_CONFIG]['host'],
        config.CONFIGS[config.DEFAULT_CONFIG]['port'],
        core=config.CONFIGS[config.DEFAULT_CONFIG]['core']
    )
    config.load_config(config.DEFAULT_CONFIG)
    connection_kwargs = {}
    if 'wt' in kwargs:
        connection_kwargs['wt'] = kwargs.pop('wt')
    return connection.search(query.Query(*args, **kwargs), **connection_kwargs)