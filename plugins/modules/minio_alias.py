#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.net>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: minio_alias
short_description: Manages Minio Client (mc) aliases
description:
  - When the alias does not exist, it will be created.
  - When the alias does exist and O(state=absent), the alias will be deleted.
  - When changes are made to the alias, the alias will be updated.
author:
    - Josh Williams (@t3hpr1m3)
requirements:
  - python >= 3.8
  - Minio client binary (mc)
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
    description: Name of the alias to be managed.
  url:
    type: str
    required: true
    description: Url of the Minio server to associate with this alias.
  access_key:
    type: str
    required: true
    description: Minio access key use to connect to the instance.
  secret_key:
    type: str
    required: true
    description: Minio secret key use to connect to the instance.
  state:
    description:
      - Indicates the desired alias state.
      - V(present) ensures the alias is present.
      - V(absent) ensures the alias is absent.
    default: present
    choices: [ "present", "absent" ]
    type: str
seealso:
  - name: mc alias
    description: Documentation for the B(mc alias) command.
    link: https://min.io/docs/minio/linux/reference/minio-mc/mc-alias.html
"""

EXAMPLES = """
- name: Add alias for Minio server
  dubzland.minio.minio_alias:
    name: localhost
    url: http://localhost:9000
    access_key: myuser
    secret_key: supersekret
    state: present
"""


import json

from ansible.module_utils.basic import AnsibleModule


def alias_command(module, *args):
    mc_path = module.get_bin_path("mc", required=True)

    cmd = ["{mc_path}".format(mc_path=mc_path), "--json", "alias"]
    cmd.extend(args)
    return cmd


def alias_find(module, name):
    cmd = alias_command(module, "list")

    rc, out, err = module.run_command(cmd)
    records = out.splitlines()
    for record in records:
        alias = json.loads(record)
        if alias["alias"] == name:
            return {
                "name": alias["alias"],
                "url": alias["URL"],
                "access_key": alias["accessKey"],
                "secret_key": alias["secretKey"],
            }

    return None


def alias_create_or_update(module, name, url, access_key, secret_key):
    cmd = alias_command(module, "set", name, url, access_key, secret_key)

    rc, out, err = module.run_command(cmd)

    if rc != 0:
        module.fail_json(
            msg="Failed to add alias", stdout=out, stderr=err, cmd=" ".join(cmd)
        )


def alias_delete(module, name):
    cmd = alias_command(module, "remove", name)

    rc, out, err = module.run_command(cmd)

    if rc != 0:
        module.fail_json(
            msg="Failed to delete alias", stdout=out, stderr=err, cmd=cmd.join(" ")
        )


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            url=dict(type="str", required=True),
            access_key=dict(type="str", required=True, no_log=True),
            secret_key=dict(type="str", required=True, no_log=True),
            state=dict(default="present", choices=["present", "absent"]),
        ),
        supports_check_mode=True,
    )

    # Set LANG env since we parse stdout
    module.run_command_environ_update = dict(
        LANG="C", LC_ALL="C", LC_MESSAGES="C", LC_CTYPE="C"
    )

    name = module.params["name"]
    url = module.params["url"]
    access_key = module.params["access_key"]
    secret_key = module.params["secret_key"]
    state = module.params["state"]
    changed = False

    record = alias_find(module, name)

    if record is not None:
        if state == "present":
            # Convert both to a JSON string
            current_str = json.dumps(record, sort_keys=True)
            new_str = json.dumps(
                {
                    "name": name,
                    "url": url,
                    "access_key": access_key,
                    "secret_key": secret_key,
                },
                sort_keys=True,
            )
            if current_str != new_str:
                alias_create_or_update(module, name, url, access_key, secret_key)
                changed = True
        else:
            alias_delete(module, name)
            changed = True
    else:
        if state == "present":
            alias_create_or_update(module, name, url, access_key, secret_key)
            changed = True

    module.exit_json(changed=changed)


if __name__ == "__main__":
    main()
