#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: minio_policy
short_description: Manages Minio policies
description:
  - When the policy does not exist, it will be created.
  - When the policy does exist and O(state=absent), the policy will be deleted.
  - When changes are made to the policy, the policy will be updated.
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
    description: Name of the policy to be managed.
  src:
    type: path
    description: Local file containing the JSON policy information.
  statements:
    type: list
    elements: dict
    options:
      effect:
        type: str
        choices:
          - Allow
          - Deny
        required: true
        description: Determines whether this policy allows or denies access.
      action:
        type: list
        elements: str
        required: true
        description: >-
          Actions allowed or denied by this policy.  See
          L(https://min.io/docs/minio/linux/administration/identity-access-management/policy-based-access-control.html#minio-policy-actions)
          for a list of valid policy actions.
      resource:
        type: list
        elements: str
        required: true
        description: >-
          List of resources to which this policy will apply.
    description: List of policy statements to include
  state:
    description:
      - Indicates the desired policy state.
      - V(present) ensures the policy is present.
      - V(absent) ensures the policy is absent.
    default: present
    choices: [ "present", "absent" ]
    type: str
  mutually_exclusive:
    - ['data', 'statements']
seealso:
  - name: mc admin policy
    description: Documentation for the B(mc admin policy) command.
    link: https://min.io/docs/minio/linux/reference/minio-mc-admin/mc-admin-policy-create.html
notes:
  - The O(minio_access_key) provided must have the B(admin:CreatePolicy) permission.
extends_documentation_fragment: dubzland.minio.minio_auth
"""

EXAMPLES = """
- name: Add a policy to the Minio server via policy file
  dubzland.minio.minio_policy:
    name: fullaccess
    data: |
      {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListAllMyBuckets"
                ],
                "Resource": [
                    "arn:aws:s3:::*"
                ]
            }
        ]
      }
    minio_url: http://localhost:9000
    minio_access_key: myuser
    minio_secret_key: supersekret
    state: present


- name: Add a policy to the Minio server via statements
  dubzland.minio.minio_policy:
    name: fullaccess
    statements:
      - effect: Allow
        action: "s3:*"
        resource: "arn:aws:s3:::*"
    minio_url: http://localhost:9000
    minio_access_key: myuser
    minio_secret_key: supersekret
    state: present
"""

import json
import os
import tempfile

from contextlib import contextmanager

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.dubzland.minio.plugins.module_utils.minio import (
    minio_admin_client,
    minio_auth_argument_spec,
)


@contextmanager
def policy_tempfile(data):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = os.path.join(tmp_dir, "policy.json")
        f = open(tmp_path, "w")
        f.write(data)
        f.close()
        yield tmp_path


def main():
    argument_spec = minio_auth_argument_spec()
    argument_spec.update(
        dict(
            name=dict(type="str", required=True),
            data=dict(type="str", required=True),
            state=dict(default="present", choices=["present", "absent"]),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    name = module.params["name"]
    data = module.params["data"]
    state = module.params["state"]

    needs_policy_add = False
    changed = False

    client = minio_admin_client(module)

    res = client.policy_list()
    policies = json.loads(res)

    if name in policies:
        if state == "present":
            # policy already exists
            new_policy = json.loads(data)
            current_policy = policies[name]
            if json.dumps(current_policy, sort_keys=True) != json.dumps(
                new_policy, sort_keys=True
            ):
                needs_policy_add = True
        else:
            client.policy_remove(name)
            changed = True
    else:
        if state == "present":
            needs_policy_add = True

    if needs_policy_add:
        with policy_tempfile(data) as policy_file:
            client.policy_add(name, policy_file)
            changed = True

    module.exit_json(changed=changed)


if __name__ == "__main__":
    main()
