# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

if sys.version_info < (3, 5):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from ansible.module_utils.basic import missing_required_lib


try:
    import minio

    python_minio_installed = True
except ImportError:
    python_minio_installed = False


def minio_argument_spec(**kwargs):
    argument_spec = dict(
        auth=dict(
            type="dict",
            required=True,
            options=dict(
                access_key=dict(type="str", required=True, no_log=True),
                secret_key=dict(type="str", required=True, no_log=True),
                url=dict(type="str", required=True),
            ),
        )
    )
    argument_spec.update(**kwargs)
    return argument_spec


def ensure_minio_package(module):
    if not python_minio_installed:
        module.fail_json(
            msg=missing_required_lib(
                "minio",
                url="https://min.io/docs/minio/linux/developers/python/minio-py.html",
            ),
        )


def minio_client(module):
    ensure_minio_package(module)

    auth = module.params["auth"]
    o = urlparse(auth["url"])

    client = minio.Minio(
        o.netloc,
        access_key=auth["access_key"],
        secret_key=auth["secret_key"],
        secure=o.scheme == "https",
    )

    return client


def minio_admin_client(module):
    ensure_minio_package(module)

    auth = module.params["auth"]
    o = urlparse(auth["url"])

    client = minio.MinioAdmin(
        o.netloc,
        minio.credentials.providers.StaticProvider(
            auth["access_key"], auth["secret_key"]
        ),
        "",
        o.scheme == "https",
    )

    return client
