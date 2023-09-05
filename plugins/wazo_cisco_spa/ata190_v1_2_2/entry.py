# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

common = {}
execfile_('common.py', common)  # type: ignore[name-defined]

MODEL_VERSION = {'ATA190': '1.2.2'}


class CiscoPlugin(common['BaseCiscoPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = ['dialplan.xml']
    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
