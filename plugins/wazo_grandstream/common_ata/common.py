# Copyright 2010-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
import re
import os.path

from provd import synchronize
from provd.devices.config import RawConfigError
from provd.plugins import FetchfwPluginHelper, StandardPlugin, TemplatePluginHelper
from provd.devices.pgasso import BasePgAssociator, DeviceSupport
from provd.servers.http import HTTPNoListingFileService
from provd.servers.http_site import Request
from provd.devices.ident import RequestType
from provd.util import format_mac, norm_mac
from twisted.internet import defer

logger = logging.getLogger('plugin.wazo-grandstream')

TZ_NAME = {'Europe/Paris': 'CET-1CEST-2,M3.5.0/02:00:00,M10.5.0/03:00:00'}
LOCALE = {
    'de_DE': 'de',
    'es_ES': 'es',
    'fr_FR': 'fr',
    'fr_CA': 'fr',
    'it_IT': 'it',
    'nl_NL': 'nl',
    'en_US': 'en',
}


class BaseGrandstreamHTTPDeviceInfoExtractor:
    # Grandstream Model HW HT801 V1.1A SW 1.0.17.5 DevId c074ad273a10

    _UA_REGEX_LIST = [
        re.compile(
            r'^Grandstream Model HW (\w+)(?:\s+V[^ ]+)? SW ([^ ]+) DevId ([^ ]+)'
        ),
    ]

    def extract(self, request: Request, request_type: RequestType):
        return defer.succeed(self._do_extract(request))

    def _do_extract(self, request: Request):
        ua = request.getHeader(b'User-Agent')
        if ua:
            return self._extract_from_ua(ua.decode('ascii'))

    def _extract_from_ua(self, ua: str):
        for UA_REGEX in self._UA_REGEX_LIST:
            m = UA_REGEX.match(ua)
            if m:
                raw_model, raw_version, raw_mac = m.groups()
                try:
                    mac = norm_mac(raw_mac)
                except ValueError as e:
                    logger.warning(
                        'Could not normalize MAC address "%s": %s', raw_mac, e
                    )
                    return None
                return {
                    'vendor': 'Grandstream',
                    'model': raw_model,
                    'version': raw_version,
                    'mac': mac,
                }


class BaseGrandstreamPgAssociator(BasePgAssociator):
    def __init__(self, models, version):
        super().__init__()
        self._models = models
        self._version = version

    def _do_associate(
        self, vendor: str, model: str | None, version: str | None
    ) -> DeviceSupport:
        if vendor == 'Grandstream':
            if model in self._models:
                if version.startswith(self._version):
                    return DeviceSupport.EXACT
                return DeviceSupport.COMPLETE
            return DeviceSupport.UNKNOWN
        return DeviceSupport.IMPROBABLE


class BaseGrandstreamPlugin(StandardPlugin):
    _ENCODING = 'UTF-8'

    DTMF_MODES = {
        # mode: (in audio, in RTP, in SIP)
        'RTP-in-band': ('Yes', 'Yes', 'No'),
        'RTP-out-of-band': ('No', 'Yes', 'No'),
        'SIP-INFO': ('No', 'No', 'Yes'),
    }

    SIP_TRANSPORTS = {
        'udp': 'UDP',
        'tcp': 'TCP',
        'tls': 'TlsOrTcp',
    }

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)
        # update to use the non-standard tftpboot directory
        self._tpl_helper = TemplatePluginHelper(plugin_dir)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)
        # update to use the non-standard tftpboot directory
        fetchfw_helper.root_dir = self._tftpboot_dir

        self.services = fetchfw_helper.services()
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)

    http_dev_info_extractor = BaseGrandstreamHTTPDeviceInfoExtractor()

    def _dev_specific_filename(self, device: dict[str, str]) -> str:
        # Return the device specific filename (not pathname) of device
        formatted_mac = format_mac(device['mac'], separator='', uppercase=False)
        return f'cfg{formatted_mac}.xml'

    def _check_config(self, raw_config):
        if 'http_port' not in raw_config:
            raise RawConfigError('only support configuration via HTTP')

    def _check_device(self, device):
        if 'mac' not in device:
            raise Exception('MAC address needed for device configuration')

    def configure(self, device, raw_config):
        self._check_config(raw_config)
        self._check_device(device)
        self._check_lines_password(raw_config)
        self._add_sip_transport(raw_config)
        self._add_timezone(raw_config)
        self._add_locale(raw_config)
        self._add_dtmf_mode(raw_config)
        self._add_dns(raw_config)
        filename = self._dev_specific_filename(device)
        tpl = self._tpl_helper.get_dev_template(filename, device)

        path = os.path.join(self._tftpboot_dir, filename)
        self._tpl_helper.dump(tpl, raw_config, path, self._ENCODING)

    def deconfigure(self, device):
        self._remove_configuration_file(device)

    def _remove_configuration_file(self, device):
        path = os.path.join(self._tftpboot_dir, self._dev_specific_filename(device))
        try:
            os.remove(path)
        except OSError as e:
            logger.info('error while removing configuration file: %s', e)

    def synchronize(self, device, raw_config):
        return synchronize.standard_sip_synchronize(device)

    def get_remote_state_trigger_filename(self, device):
        if 'mac' in device:
            return self._dev_specific_filename(device)

    def _check_lines_password(self, raw_config):
        for line in raw_config['sip_lines'].values():
            if line['password'] == 'autoprov':
                line['password'] = ''

    def _add_timezone(self, raw_config):
        if 'timezone' in raw_config and raw_config['timezone'] in TZ_NAME:
            raw_config['XX_timezone'] = TZ_NAME[raw_config['timezone']]
        else:
            raw_config['timezone'] = TZ_NAME['Europe/Paris']

    def _add_locale(self, raw_config):
        locale = raw_config.get('locale')
        if locale in LOCALE:
            raw_config['XX_locale'] = LOCALE[locale]

    def _add_dns(self, raw_config):
        if raw_config.get('dns_enabled'):
            dns_parts = raw_config['dns_ip'].split('.')
            for part_nb, part in enumerate(dns_parts, start=1):
                raw_config[f'XX_dns_{part_nb}'] = part

    def _add_dtmf_mode(self, raw_config):
        if raw_config.get('sip_dtmf_mode'):
            dtmf_info = self.DTMF_MODES[raw_config['sip_dtmf_mode']]
            raw_config['XX_dtmf_in_audio'] = dtmf_info[0]
            raw_config['XX_dtmf_in_rtp'] = dtmf_info[1]
            raw_config['XX_dtmf_in_sip'] = dtmf_info[2]

    def _add_sip_transport(self, raw_config):
        sip_transport = raw_config.get('sip_transport')
        if sip_transport in self.SIP_TRANSPORTS:
            raw_config['XX_sip_transport'] = self.SIP_TRANSPORTS[sip_transport]
