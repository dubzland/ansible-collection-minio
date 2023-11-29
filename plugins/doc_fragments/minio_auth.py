# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = """
options:
    minio_access_key:
        type: str
        required: true
        description: Minio access key to use to authenticate with the Minio instance.
    minio_secret_key:
        type: str
        required: true
        description: Minio secret key used to connect to the Minio instance.
    minio_url:
        type: str
        required: true
        description: Minio Server URL.
"""
