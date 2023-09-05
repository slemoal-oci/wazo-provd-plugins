# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

common_globals = {}
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODEL_VERSIONS = {
    'CP960': '73.85.0.5',
    'CP920': '78.85.0.5',
    'T27G': '69.85.0.5',
    'T30': '124.85.0.40',
    'T30P': '124.85.0.40',
    'T31': '124.85.0.40',
    'T31P': '124.85.0.40',
    'T31G': '124.85.0.40',
    'T33P': '124.85.0.40',
    'T33G': '124.85.0.40',
    'T41S': '66.85.0.5',
    'T42S': '66.85.0.5',
    'T46S': '66.85.0.5',
    'T48S': '66.85.0.5',
    'T53': '96.85.0.5',
    'T53W': '96.85.0.5',
    'T54W': '96.85.0.5',
    'T57W': '96.85.0.5',
    'T58': '58.85.0.5',
    'W60B': '77.85.0.25',
    'W70B': '146.85.0.37',
    'W90DM': '130.85.0.44',
    'W90B': '130.85.0.44',
}

COMMON_FILES = [
    ('y000000000069.cfg', 'T27G-69.85.0.5.rom', 'model.tpl'),
    ('y000000000065.cfg', 'T46S(T48S,T42S,T41S)-66.85.0.5.rom', 'model.tpl'),
    ('y000000000066.cfg', 'T46S(T48S,T42S,T41S)-66.85.0.5.rom', 'model.tpl'),
    ('y000000000067.cfg', 'T46S(T48S,T42S,T41S)-66.85.0.5.rom', 'model.tpl'),
    ('y000000000068.cfg', 'T46S(T48S,T42S,T41S)-66.85.0.5.rom', 'model.tpl'),
    ('y000000000073.cfg', 'CP960-73.85.0.5.rom', 'model.tpl'),
    ('y000000000078.cfg', 'CP920-78.85.0.5.rom', 'model.tpl'),
    (
        'y000000000123.cfg',
        'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
        'model.tpl',
    ),
    (
        'y000000000124.cfg',
        'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
        'model.tpl',
    ),
    (
        'y000000000127.cfg',
        'T31(T30,T30P,T31G,T31P,T33P,T33G)-124.85.0.40.rom',
        'model.tpl',
    ),
]

HANDSETS_FW = {
    'w53h': 'W53H-88.85.0.20.rom',
    'w56h': 'W56H-61.85.0.20.rom',
    'w59r': 'W59R-115.85.0.20.rom',
    'w73h': 'W73H-116.85.0.15.rom',
    'cp930w': 'CP930W-87.85.0.20.rom',
    't41s_dd10k': 'T4S-ddphone-66.85.0.56.rom',
    't54w_dd10k': 'T54W-ddphone-96.85.0.65.rom ',
}

COMMON_FILES_DECT = [
    {
        'filename': 'y000000000130.cfg',
        'fw_filename': '$PN-130.85.0.44.rom',  # $PN = Product Name, i.e W90B/W90DM
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': 'dect_model.tpl',
    },
    {
        'filename': 'y000000000058.cfg',
        'fw_filename': 'T58-58.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': 'dect_model.tpl',
    },
    {
        'filename': 'y000000000077.cfg',
        'fw_filename': 'W60B-77.85.0.25.rom',
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': 'dect_model.tpl',
    },
    {
        'filename': 'y000000000146.cfg',
        'fw_filename': 'W70B-146.85.0.37.rom',
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': 'dect_model.tpl',
    },
    {
        'filename': 'y000000000095.cfg',
        'fw_filename': 'T54W(T57W,T53W,T53)-96.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': 'dect_model.tpl',
    },
    {
        'filename': 'y000000000096.cfg',
        'fw_filename': 'T54W(T57W,T53W,T53)-96.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': 'dect_model.tpl',
    },
    {
        'filename': 'y000000000097.cfg',
        'fw_filename': 'T54W(T57W,T53W,T53)-96.85.0.5.rom',
        'handsets_fw': HANDSETS_FW,
        'tpl_filename': 'dect_model.tpl',
    },
]


class YealinkPlugin(common_globals['BaseYealinkPlugin']):
    IS_PLUGIN = True

    pg_associator = common_globals['BaseYealinkPgAssociator'](MODEL_VERSIONS)

    # Yealink plugin specific stuff

    _COMMON_FILES = COMMON_FILES

    def configure_common(self, raw_config):
        super().configure_common(raw_config)
        for dect_info in COMMON_FILES_DECT:
            tpl = self._tpl_helper.get_template(f'common/{dect_info["tpl_filename"]}')
            dst = os.path.join(self._tftpboot_dir, dect_info['filename'])
            raw_config['XX_handsets_fw'] = dect_info['handsets_fw']
            raw_config['XX_fw_filename'] = dect_info['fw_filename']

            self._tpl_helper.dump(tpl, raw_config, dst, self._ENCODING)
