#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: minio_user
short_description: Manages Minio users
description:
  - When the user does not exist, it will be created.
  - When the user does exist and O(state=absent), the user will be deleted.
  - When changes are made to the user, the user will be updated.
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
  access_key:
    type: str
    required: true
    description: Access key (username) for the user.
  secret_key:
    type: str
    required: true
    description: Secret key (password) for the user.
  policy:
    type: str
    required: false
    description: An existing policy to apply to this user.
  force:
    type: bool
    default: False
    description: When set to V(true), the O(secret_key) will always be updated (and the module will always return changed to V(true)).
  state:
    description:
      - Indicates the desired user state.
      - V(present) ensures the user is present.
      - V(absent) ensures the user is absent.
      - V(enabled) ensures the user is enabled.
      - V(disabled) ensures the user is disabled.
    default: present
    choices: [ "present", "absent", "enabled", "disabled" ]
    type: str
seealso:
  - name: mc mb
    description: Documentation for the B(mc mb) command.
    link: https://min.io/docs/minio/linux/reference/minio-mc/mc-mb.html
extends_documentation_fragment: dubzland.minio.minio_auth
"""

EXAMPLES = """
- name: Add a Minio user
  dubzland.minio.minio_user:
    access_key: testuser
    secret_key: supersekret
    auth:
      access_key: minioadmin
      secret_key: minioadmin
      url: http://minio.example.com:9000
    state: present
  delegate_to: localhost
"""

import json

from ansible_collections.dubzland.minio.plugins.module_utils.minio import (
    minio_admin_client,
    minio_argument_spec,
)

from ansible.module_utils.basic import AnsibleModule


class MinioUser:
    def __init__(self, module, minio_client):
        self._module = module
        self._client = minio_client
        self.user_object = None

    def find_user(self, access_key):
        user_list_str = self._client.user_list()
        user_list = json.loads(user_list_str)

        if access_key in user_list:
            return user_list[access_key]

    def user_exists(self, access_key):
        user = self.find_user(access_key)
        if user:
            self.user_object = user
            return True

        return False

    def create_or_update_user(self, access_key, options):
        changed = False

        if self.user_object is None:
            if self._module.check_mode:
                return True

            self._client.user_add(access_key, options["secret_key"])
            self.user_object = self._client.user_info(access_key)
            changed = True
        else:
            changed = False
            # We have to update the password first, as this will automatically
            # enable them
            if (
                "force" in options
                and options["force"] is True
                and options["secret_key"]
            ):
                if self._module.check_mode:
                    return True

                self._client.user_add(access_key, options["secret_key"])
                self.user_object = self._client.user_info(access_key)
                changed = True

        new_policy = None
        if "policy" in options:
            new_policy = options["policy"]

        if "policyName" in self.user_object:
            # User has a policy set
            if new_policy is None:
                if self._module.check_mode:
                    return True

                self._client.policy_unset(
                    self.user_object["policyName"], user=access_key
                )
                self.user_object = self._client.user_info(access_key)
                changed = True
            elif new_policy != self.user_object["policyName"]:
                if self._module.check_mode:
                    return True

                self._client.policy_set(new_policy, user=access_key)
                self.user_object = self._client.user_info(access_key)
                changed = True
        else:
            # No policy set
            if new_policy is not None:
                if self._module.check_mode:
                    return True

                self._client.policy_set(new_policy, user=access_key)
                self.user_object = self._client.user_info(access_key)
                changed = True

        if options["state"] == "disabled" and self.user_object["status"] != "disabled":
            if self._module.check_mode:
                return True

            self._client.user_disable(access_key)
            self.user_object = self._client.user_info(access_key)
            changed = True
        elif options["state"] == "enabled" and self.user_object["status"] != "enabled":
            if self._module.check_mode:
                return True

            self._client.user_enable(access_key)
            self.user_object = self._client.user_info(access_key)
            changed = True

        return changed

    def delete_user(self, access_key):
        self._client.user_remove(access_key)


def main():
    argument_spec = minio_argument_spec(
        access_key=dict(type="str", required=True, no_log=True),
        secret_key=dict(type="str", required=True, no_log=True),
        policy=dict(type="str", required=False, default=None),
        force=dict(type="bool", required=False, default=False),
        state=dict(
            default="present", choices=["present", "absent", "enabled", "disabled"]
        ),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    access_key = module.params["access_key"]
    secret_key = module.params["secret_key"]
    policy = module.params["policy"]
    force = module.params["force"]
    state = module.params["state"]

    changed = False

    client = minio_admin_client(module)

    minio_user = MinioUser(module, client)

    exists = minio_user.user_exists(access_key)

    if state != "absent":
        changed = minio_user.create_or_update_user(
            access_key,
            {
                "secret_key": secret_key,
                "policy": policy,
                "state": state,
                "force": force,
            },
        )
    else:
        if exists:
            changed = minio_user.delete_user(access_key)

    module.exit_json(changed=changed)


if __name__ == "__main__":
    main()
