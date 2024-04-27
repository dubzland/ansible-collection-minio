#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: minio_bucket
short_description: Manages Minio buckets
description:
  - When the bucket does not exist, it will be created.
  - When the bucket does exist and O(state=absent), the bucket will be deleted.
  - When changes are made to the bucket, the bucket will be updated.
author:
  - Josh Williams (@t3hpr1m3)
requirements:
  - python >= 3.8
  - minio >= 7.1.4
attributes:
  check_mode:
    support: full
    description: Can run in check_mode and return changed status prediction without modifying target.
  diff_mode:
    support: none
    description: Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode.
options:
  name:
    type: str
    required: true
    description: Name of the bucket to be managed.
  state:
    description:
      - Indicates the desired bucket state.
      - V(present) ensures the bucket is present.
      - V(absent) ensures the bucket is absent.
    default: present
    choices: [ "present", "absent" ]
    type: str
seealso:
  - name: mc mb
    description: Documentation for the B(mc mb) command.
    link: https://min.io/docs/minio/linux/reference/minio-mc/mc-mb.html
extends_documentation_fragment: dubzland.minio.minio_auth
"""

EXAMPLES = """
- name: Add a Minio bucket
  dubzland.minio.minio_bucket:
    name: testbucket
    minio_url: http://minio-server:9000
    minio_access_key: myuser
    minio_secret_key: supersekret
    state: present
  delegate_to: localhost
"""

from ansible_collections.dubzland.minio.plugins.module_utils.minio import (
    minio_client,
    minio_argument_spec,
)

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = minio_argument_spec(
        name=dict(type="str", required=True),
        state=dict(default="present", choices=["present", "absent"]),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    name = module.params["name"]
    state = module.params["state"]

    changed = False

    client = minio_client(module)

    if client.bucket_exists(name):
        if state == "present":
            pass
    else:
        if state == "present":
            client.make_bucket(name)
            changed = True

    module.exit_json(changed=changed)


if __name__ == "__main__":
    main()
