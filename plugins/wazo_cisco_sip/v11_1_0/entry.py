# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)  # type: ignore[name-defined]

MODEL_VERSION = {
    'ATA191': 'MPP-11-1-0MPP0401-002',
    'ATA192': 'MPP-11-1-0MPP0401-002',
}


class CiscoSipPlugin(common['BaseCiscoSipPlugin']):
    IS_PLUGIN = True
    _COMMON_FILENAMES = [
        'ata191.cfg',
        'ata192.cfg',
    ]

    pg_associator = common['BaseCiscoPgAssociator'](MODEL_VERSION)
