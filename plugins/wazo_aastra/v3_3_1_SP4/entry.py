# Copyright 2014-2023 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

common = {}
execfile_('common.py', common)  # type: ignore[name-defined]


MODEL_VERSIONS = {
    '6730i': '3.3.1.4365',
    '6731i': '3.3.1.4365',
    '6735i': '3.3.1.8215',
    '6737i': '3.3.1.8215',
    '6739i': '3.3.1.4365',
    '6753i': '3.3.1.4365',
    '6755i': '3.3.1.4365',
    '6757i': '3.3.1.4365',
    '9143i': '3.3.1.4365',
    '9480i': '3.3.1.4365',
}


class AastraPlugin(common['BaseAastraPlugin']):
    IS_PLUGIN = True
    _LANGUAGE_PATH = 'i18n/'

    pg_associator = common['BaseAastraPgAssociator'](MODEL_VERSIONS)
