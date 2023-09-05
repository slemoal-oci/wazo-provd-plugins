# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common_globals = {}
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODELS = [
    'D315',
    'D335',
    'D345',
    'D385',
    'D712',
    'D713',
    '715',
    'D717',
    '725',
    'D735',
    'D785',
    'D862',
    'D865',
]
VERSION = '10.1.141.13'


class SnomPlugin(common_globals['BaseSnomPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common_globals['BaseSnomPgAssociator'](MODELS, VERSION)
