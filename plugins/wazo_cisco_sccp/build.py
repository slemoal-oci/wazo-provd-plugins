# Copyright (C) 2013-2022 The Wazo Authors  (see the AUTHORS file)
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

# Depends on the following external programs:
#  -rsync

from subprocess import check_call


@target('8.5.2', 'wazo-cisco-sccp-8.5.2')
def build_8_5_2(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', '8.5.2/', path])


@target('9.4', 'wazo-cisco-sccp-9.4')
def build_9_4(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', '9.4/', path])


@target('cipc-2.1.2', 'wazo-cisco-sccp-cipc-2.1.2')
def build_cipc_2_1_2(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'cipc-2.1.2/', path])


@target('legacy', 'wazo-cisco-sccp-legacy')
def build_legacy(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'legacy/', path])


@target('wireless-1.4.5', 'wazo-cisco-sccp-wireless-1.4.5')
def build_wireless(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', 'wireless-1.4.5/', path])
