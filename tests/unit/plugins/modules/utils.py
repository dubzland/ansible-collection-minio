# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.net>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible_collections.dubzland.minio.tests.unit.compat import unittest
from ansible_collections.dubzland.minio.tests.unit.compat.mock import patch
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
from contextlib import contextmanager


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""

    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""

    pass


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


def get_bin_path(self, arg, required=False):
    """Mock AnsibleModule.get_bin_path"""
    if arg.endswith("mc"):
        return "/usr/local/bin/mc"
    else:
        if required:
            fail_json(msg="%r not found !" % arg)


@contextmanager
def mock_run_command(module, stdout, stderr, rc):
    with patch.object(module, "run_command") as run_command:
        run_command.return_value = rc, stdout, stderr
        yield run_command


class ModuleTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_module = patch.multiple(
            basic.AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json,
            get_bin_path=get_bin_path,
        )
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)
