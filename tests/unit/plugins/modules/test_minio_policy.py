# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.dubzland.minio.tests.unit.compat.mock import (
    ANY,
    patch,
)
from ansible_collections.dubzland.minio.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    MinioAdminClientTestCase,
    set_module_args,
)

from ansible_collections.dubzland.minio.plugins.modules import minio_policy


class TestMinioPolicy(MinioAdminClientTestCase):
    def setUp(self):
        super(TestMinioPolicy, self).setUp()
        patcher = patch(
            "ansible_collections.dubzland.minio.plugins.modules.minio_policy.minio_admin_client"
        )
        self.MockClient = patcher.start()
        self.addCleanup(patcher.stop)

    @pytest.fixture(autouse=True)
    def _mocker(self, mocker):
        self.mocker = mocker

    def test_module_fail_when_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            minio_policy.main()

    def test_module_unchanged_when_exists(self):
        mock_client = self.MockClient.return_value
        mock_client.policy_list.return_value = '{"%s": {}}' % "testing"
        set_module_args(
            {
                "name": "testing",
                "statements": [],
                "minio_access_key": "testing",
                "minio_secret_key": "supersekret",
                "minio_url": "http://localhost:9000",
            }
        )

        with self.assertRaises(AnsibleExitJson):
            minio_policy.main()

    def test_module_update_when_different(self):
        mock_client = self.MockClient.return_value
        mock_client.policy_list.return_value = '{"%s": {"existing": "value"}}'
        set_module_args(
            {
                "name": "testing",
                "statements": [],
                "minio_access_key": "testing",
                "minio_secret_key": "supersekret",
                "minio_url": "http://localhost:9000",
            }
        )

        with self.assertRaises(AnsibleExitJson):
            minio_policy.main()

    def test_module_create_when_not_exist(self):
        mock_client = self.MockClient.return_value
        mock_client.policy_list.return_value = "{}"
        mock_client.policy_add.return_value = ""
        set_module_args(
            {
                "name": "testing",
                "statements": [],
                "minio_access_key": "testing",
                "minio_secret_key": "supersekret",
                "minio_url": "http://localhost:9000",
            }
        )

        with self.assertRaises(AnsibleExitJson) as r:
            minio_policy.main()

        mock_client.policy_list.assert_called_once()
        mock_client.policy_add.assert_called_with("testing", ANY)
        result = r.exception.args[0]
        assert result["changed"] is True

    def test_module_unchanged_when_not_exist_and_state_absent(self):
        mock_client = self.MockClient.return_value
        mock_client.policy_list.return_value = "{}"
        mock_client.policy_add.return_value = ""
        set_module_args(
            {
                "name": "testing",
                "statements": [],
                "minio_access_key": "testing",
                "minio_secret_key": "supersekret",
                "minio_url": "http://localhost:9000",
                "state": "absent",
            }
        )

        with self.assertRaises(AnsibleExitJson) as r:
            minio_policy.main()

        mock_client.policy_list.assert_called_once()
        mock_client.policy_add.assert_not_called()
        result = r.exception.args[0]
        assert result["changed"] is False

    def test_module_changed_when_exists_and_state_absent(self):
        mock_client = self.MockClient.return_value
        mock_client.policy_list.return_value = '{"testing": {}}'
        mock_client.policy_remove.return_value = ""
        set_module_args(
            {
                "name": "testing",
                "statements": [],
                "minio_access_key": "testing",
                "minio_secret_key": "supersekret",
                "minio_url": "http://localhost:9000",
                "state": "absent",
            }
        )

        with self.assertRaises(AnsibleExitJson) as r:
            minio_policy.main()

        mock_client.policy_list.assert_called_once()
        mock_client.policy_remove.assert_called_once_with("testing")
        result = r.exception.args[0]
        assert result["changed"] is True
