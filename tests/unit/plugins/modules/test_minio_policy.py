# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.net>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.dubzland.minio.tests.unit.compat.mock import (
    patch,
    ANY,
    MagicMock,
)

from ansible_collections.dubzland.minio.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    set_module_args,
)

from ansible_collections.dubzland.minio.plugins.modules import minio_policy


class TestMinioPolicy(ModuleTestCase):
    def setUp(self):
        super(TestMinioPolicy, self).setUp()

    @pytest.fixture(autouse=True)
    def _mocker(self, mocker):
        self.mocker = mocker

    def test_module_fail_when_args_missing(self):
        with self.assertRaises(AnsibleFailJson) as r:
            set_module_args({})
            minio_policy.main()

    @patch("ansible_collections.dubzland.minio.plugins.modules.minio_policy.MinioAdmin")
    def test_module_unchanged_when_exists(self, mock_admin_client):
        client = MagicMock()
        client.policy_list.return_value = '{"%s": {}}' % "testing"
        mock_admin_client.return_value = client

        with self.assertRaises(AnsibleExitJson) as r:
            set_module_args(
                {
                    "name": "testing",
                    "data": "{}",
                    "access_key": "testing",
                    "secret_key": "supersekret",
                    "minio_url": "http://localhost:9000",
                }
            )
            minio_policy.main()

    @patch("ansible_collections.dubzland.minio.plugins.modules.minio_policy.MinioAdmin")
    def test_module_update_when_different(self, mock_admin_client):
        client = MagicMock()
        client.policy_list.return_value = '{"%s": {"existing": "value"}}'
        mock_admin_client.return_value = client

        with self.assertRaises(AnsibleExitJson) as r:
            set_module_args(
                {
                    "name": "testing",
                    "data": "{}",
                    "access_key": "testing",
                    "secret_key": "supersekret",
                    "minio_url": "http://localhost:9000",
                }
            )
            minio_policy.main()

    @patch("ansible_collections.dubzland.minio.plugins.modules.minio_policy.MinioAdmin")
    def test_module_create_when_not_exist(self, mock_admin_client):
        client = MagicMock()
        client.policy_list.return_value = "{}"
        client.policy_add.return_value = ""
        mock_admin_client.return_value = client

        with self.assertRaises(AnsibleExitJson) as r:
            set_module_args(
                {
                    "name": "testing",
                    "data": "{}",
                    "access_key": "testing",
                    "secret_key": "supersekret",
                    "minio_url": "http://localhost:9000",
                }
            )
            minio_policy.main()

        client.policy_list.assert_called_once()
        client.policy_add.assert_called_with("testing", ANY)
        result = r.exception.args[0]
        assert result["changed"] is True

    @patch("ansible_collections.dubzland.minio.plugins.modules.minio_policy.MinioAdmin")
    def test_module_unchanged_when_not_exist_and_state_absent(self, mock_admin_client):
        client = MagicMock()
        client.policy_list.return_value = "{}"
        client.policy_add.return_value = ""
        mock_admin_client.return_value = client

        with self.assertRaises(AnsibleExitJson) as r:
            set_module_args(
                {
                    "name": "testing",
                    "data": "{}",
                    "access_key": "testing",
                    "secret_key": "supersekret",
                    "minio_url": "http://localhost:9000",
                    "state": "absent",
                }
            )
            minio_policy.main()

        client.policy_list.assert_called_once()
        client.policy_add.assert_not_called()
        result = r.exception.args[0]
        assert result["changed"] is False

    @patch("ansible_collections.dubzland.minio.plugins.modules.minio_policy.MinioAdmin")
    def test_module_changed_when_exists_and_state_absent(self, mock_admin_client):
        client = MagicMock()
        client.policy_list.return_value = '{"testing": {}}'
        client.policy_remove.return_value = ""
        mock_admin_client.return_value = client

        with self.assertRaises(AnsibleExitJson) as r:
            set_module_args(
                {
                    "name": "testing",
                    "data": "{}",
                    "access_key": "testing",
                    "secret_key": "supersekret",
                    "minio_url": "http://localhost:9000",
                    "state": "absent",
                }
            )
            minio_policy.main()

        client.policy_list.assert_called_once()
        client.policy_remove.assert_called_once_with("testing")
        result = r.exception.args[0]
        assert result["changed"] is True
