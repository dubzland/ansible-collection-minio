# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys
import traceback

if sys.version_info < (3, 5):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from ansible.module_utils.basic import missing_required_lib

MINIO_IMP_ERR = None
try:
    from minio import Minio, MinioAdmin
    from minio.credentials.providers import StaticProvider

    HAS_MINIO_PACKAGE = True
except Exception:
    MINIO_IMP_ERR = traceback.format_exc()
    HAS_MINIO_PACKAGE = False


def ensure_minio_package(module):
    if not HAS_MINIO_PACKAGE:
        module.fail_json(
            msg=missing_required_lib(
                "minio",
                url="https://min.io/docs/minio/linux/developers/python/minio-py.html",
            ),
            exception=MINIO_IMP_ERR,
        )


def minio_client(module):
    ensure_minio_package(module)

    o = urlparse(module.params["minio_url"])

    client = Minio(
        o.netloc,
        access_key=module.params["access_key"],
        secret_key=module.params["secret_key"],
        secure=o.scheme == "https",
    )

    return client


def minio_admin_client(module):
    ensure_minio_package(module)

    o = urlparse(module.params["minio_url"])

    client = MinioAdmin(
        o.netloc,
        StaticProvider(module.params["access_key"], module.params["secret_key"]),
        "",
        o.scheme == "https",
    )

    return client
