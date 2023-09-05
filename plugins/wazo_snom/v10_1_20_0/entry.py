# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

common_globals = {}
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODELS = [
    'D785',
]
VERSION = '10.1.20.0'


class SnomPlugin(common_globals['BaseSnomPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common_globals['BaseSnomPgAssociator'](MODELS, VERSION)
