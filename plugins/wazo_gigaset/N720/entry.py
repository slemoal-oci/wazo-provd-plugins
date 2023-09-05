# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

common = {}
execfile_('common.py', common)  # type: ignore[name-defined]


MODEL_VERSIONS = {
    'N720 DM PRO': '70.117.00.000.000',
    'N720 IP PRO': '70.117.00.000.000',
}


class GigasetPlugin(common['BaseGigasetPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BaseGigasetPgAssociator'](MODEL_VERSIONS)
