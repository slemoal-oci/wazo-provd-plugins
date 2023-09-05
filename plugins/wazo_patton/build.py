"""
Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
SPDX-License-Identifier: GPL-3.0-or-later

Depends on the following external programs:
 -rsync
"""

from subprocess import check_call


@target('6.11', 'wazo-patton-6.11')
def build_6_11(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', '6.11/', path])


@target('6.9', 'wazo-patton-6.9')
def build_6_9(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])

    check_call(['rsync', '-rlp', '--exclude', '.*', '6.9/', path])
