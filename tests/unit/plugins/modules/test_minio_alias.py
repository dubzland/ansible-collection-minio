from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import unittest
from unittest.mock import patch

from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes

from ansible_collections.dubzland.minio.plugins.modules import minio_alias
# from ansible_collections.dubzland.minio import minio_alias


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


def get_bin_path(self, arg, required=False):
    """Mock AnsibleModule.get_bin_path"""
    if arg.endswith('mc'):
        return '/usr/local/bin/mc'
    else:
        if required:
            fail_json(msg='%r not found !' % arg)


def minio_alias_record(status, alias=None, url=None, access_key=None, secret_key=None):
    data = {"status": status}
    if alias is not None:
        data['alias'] = alias
    if url is not None:
        data['URL'] = url
    if access_key is not None:
        data['accessKey'] = access_key
    if secret_key is not None:
        data['secretKey'] = secret_key

    return data


class TestMinioAlias(unittest.TestCase):
    def setUp(self):
        self.mock_module = patch.multiple(basic.AnsibleModule,
                                          exit_json=exit_json,
                                          fail_json=fail_json,
                                          get_bin_path=get_bin_path)
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)

    def test_alias_lists_aliases(self):
        alias = minio_alias_record('success', 'local',
                                   'http://localhost:9000', 'test',
                                   'testsekret')
        set_module_args({
            'name': alias['alias'],
            'url': alias['URL'],
            'access_key': alias['accessKey'],
            'secret_key': alias['secretKey'],
        })

        with patch.object(basic.AnsibleModule, 'run_command') as run_command:
            stdout = json.dumps(alias)
            stderr = ''
            rc = 0
            run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as r:
                minio_alias.main()

        run_command.assert_called_with([
            '/usr/local/bin/mc',
            '--json',
            'alias',
            'list'
        ])

    def test_alias_already_exists(self):
        alias = minio_alias_record('success', 'local',
                                   'http://localhost:9000', 'test',
                                   'testsekret')
        set_module_args({
            'name': alias['alias'],
            'url': alias['URL'],
            'access_key': alias['accessKey'],
            'secret_key': alias['secretKey'],
        })

        with patch.object(basic.AnsibleModule, 'run_command') as run_command:
            stdout = json.dumps(alias)
            stderr = ''
            rc = 0
            run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as r:
                minio_alias.main()

        result = r.exception.args[0]
        self.assertFalse(result['changed'])

    def test_alias_needs_update(self):
        alias = minio_alias_record('success', 'local',
                                   'http://localhost:9000', 'test',
                                   'testsekret')
        set_module_args({
            'name': alias['alias'],
            'url': 'http://localhost:9001',
            'access_key': alias['accessKey'],
            'secret_key': alias['secretKey'],
        })

        with patch.object(basic.AnsibleModule, 'run_command') as run_command:
            stdout = json.dumps(alias)
            stderr = ''
            rc = 0
            run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as r:
                minio_alias.main()

        result = r.exception.args[0]
        self.assertTrue(result['changed'])
        run_command.assert_called_with([
            '/usr/local/bin/mc',
            '--json',
            'alias',
            'set',
            alias['alias'],
            'http://localhost:9001',
            alias['accessKey'],
            alias['secretKey'],
        ])

    def test_alias_delete(self):
        alias = minio_alias_record('success', 'local',
                                   'http://localhost:9000', 'test',
                                   'testsekret')
        set_module_args({
            'name': alias['alias'],
            'url': 'http://localhost:9001',
            'access_key': alias['accessKey'],
            'secret_key': alias['secretKey'],
            'state': 'absent',
        })

        with patch.object(basic.AnsibleModule, 'run_command') as run_command:
            stdout = json.dumps(alias)
            stderr = ''
            rc = 0
            run_command.return_value = rc, stdout, stderr

            with self.assertRaises(AnsibleExitJson) as r:
                minio_alias.main()

        result = r.exception.args[0]
        self.assertTrue(result['changed'])
        run_command.assert_called_with([
            '/usr/local/bin/mc',
            '--json',
            'alias',
            'remove',
            alias['alias'],
        ])
