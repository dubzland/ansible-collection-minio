#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, Josh Williams <jdubz@dubzland.net>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: minio_alias
short_description: Manages Minio aliases
description:
  - Manages Minio Client (mc) aliases
author: "Josh Williams (@t3hpr1m3)"
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
    description: Name of the alias to be managed
  url:
    type: str
    required: true
    description: Url of the Minio server to associate with this alias
  access_key:
    type: str
    required: true
    description: Minio access key use to connect to the instance
  secret_key:
    type: str
    required: true
    description: Minio secret key use to connect to the instance
  state:
    description:
      - Indicates the desired alias state.
      - V(present) ensures the alias is present.
      - V(absent) ensures the alias is absent.
    default: present
    choices: [ "present", "absent" ]
    type: str
'''

EXAMPLES = '''
- name: Add alias for Minio server
  dubzland.minio.minio_alias:
    name: local
    url: http://localhost:9000
    access_key: myuser
    secret_key: supersekret
    state: present
'''

import json

from ansible.module_utils.basic import AnsibleModule


class MinioAlias(object):
    def __init__(self, module):
        self.module = module
        self.name = self.module.params['name']
        self.url = self.module.params['url']
        self.access_key = self.module.params['access_key']
        self.secret_key = self.module.params['secret_key']
        self.state = self.module.params['state']

        self.mc_path = self.module.get_bin_path(
            'mc',
            required=True
        )

        self.loaded = False
        self.record = None

    def _record(self):
        if not self.loaded:
            self.record = self.find()
            self.loaded = True

        return self.record

    def find(self):
        cmd = [
            "{mc_path}".format(mc_path=self.mc_path),
            "--json",
            "alias",
            "list",
        ]

        rc, out, err = self.module.run_command(cmd)
        records = out.splitlines()
        aliases = []
        for record in records:
            alias = json.loads(record)
            if 'accessKey' in alias.keys():
                aliases.append(alias)

        for alias in aliases:
            if alias['alias'] == self.name:
                return alias

        return None

    def exists(self):
        return self._record() is not None

    def needs_update(self):
        record = self._record()

        if record is None:
            return False

        if record['URL'] != self.url or \
                record['accessKey'] != self.access_key or \
                record['secretKey'] != self.secret_key:
            return True

        return False

    def update(self):
        cmd = [
            "{mc_path}".format(mc_path=self.mc_path),
            "--json",
            "alias",
            "set",
            self.name,
            self.url,
            self.access_key,
            self.secret_key
        ]

        rc, out, err = self.module.run_command(cmd)

        if rc != 0:
            self.module.fail_json(msg="Failed to update alias", stdout=out,
                                  stderr=err, cmd=cmd.join(' '))

    def create(self):
        cmd = [
            "{mc_path}".format(mc_path=self.mc_path),
            "--json",
            "alias",
            "set",
            self.name,
            self.url,
            self.access_key,
            self.secret_key
        ]

        rc, out, err = self.module.run_command(cmd)

        if rc != 0:
            self.module.fail_json(msg="Failed to add alias", stdout=out,
                                  stderr=err, cmd=' '.join(cmd))

    def delete(self):
        cmd = [
            "{mc_path}".format(mc_path=self.mc_path),
            "--json",
            "alias",
            "remove",
            self.name,
        ]

        rc, out, err = self.module.run_command(cmd)

        if rc != 0:
            self.module.fail_json(msg="Failed to delete alias", stdout=out,
                                  stderr=err, cmd=cmd.join(' '))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            url=dict(type='str', required=True),
            access_key=dict(type='str', required=True, no_log=True),
            secret_key=dict(type='str', required=True, no_log=True),
            state=dict(default='present', choices=['present', 'absent']),
        ),
        supports_check_mode=True
    )

    # Set LANG env since we parse stdout
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')

    name = module.params['name']
    url = module.params['url']
    access_key = module.params['access_key']
    secret_key = module.params['secret_key']
    state = module.params['state']
    changed = False

    minio_alias = MinioAlias(module)

    if minio_alias.exists():
        if state == 'present':
            if minio_alias.needs_update():
                minio_alias.update()
                changed = True
        else:
            minio_alias.delete()
            changed = True
    else:
        if state == 'present':
            minio_alias.create()
            changed = True

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
