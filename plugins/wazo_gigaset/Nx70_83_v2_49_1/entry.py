# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

common = {}
execfile_('common.py', common)  # type: ignore[name-defined]


MODEL_VERSIONS = {
    'N670 IP PRO': '83.V2.49.1',
    'N870 IP PRO': '83.V2.49.1',
    'N870E IP PRO': '83.V2.49.1',
}


class GigasetPlugin(common['BaseGigasetPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BaseGigasetPgAssociator'](MODEL_VERSIONS)
