# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
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

MODELS = [
    '7906G',
    '7911G',
    '7931G',
    '7941G',
    '7942G',
    '7945G',
    '7961G',
    '7962G',
    '7965G',
    '7970G',
    '7971G',
    '7975G',
]


class CiscoSccpPlugin(common['BaseCiscoSccpPlugin']):
    IS_PLUGIN = True

    pg_associator = common['BaseCiscoPgAssociator'](MODELS)
