# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.dubzland.minio.tests.unit.compat.mock import patch

from ansible_collections.dubzland.minio.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    set_module_args,
)

from ansible_collections.dubzland.minio.plugins.modules import minio_user


class TestMinioUserModule(ModuleTestCase):
    def setUp(self):
        super(TestMinioUserModule, self).setUp()
        patcher = patch(
            "ansible_collections.dubzland.minio.plugins.modules.minio_user.MinioUser"
        )
        self.MockMinioUser = patcher.start()
        self.addCleanup(patcher.stop)

    @pytest.fixture(autouse=True)
    def _mocker(self, mocker):
        self.mocker = mocker

    def test_module_fail_when_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            minio_user.main()

    def test_module_creates_when_user_does_not_exist(self):
        set_module_args(
            {
                "access_key": "testuser",
                "secret_key": "testuser123",
                "auth": {
                    "access_key": "minioadmin",
                    "secret_key": "minioadmin",
                    "url": "http://localhost:9000",
                },
            }
        )

        mock_user = self.MockMinioUser.return_value
        mock_user.user_exists.return_value = False
        mock_user.create_or_update_user.return_value = True
        with self.assertRaises(AnsibleExitJson) as r:
            minio_user.main()

        mock_user.create_or_update_user.assert_called_once_with(
            "testuser",
            {
                "secret_key": "testuser123",
                "policy": None,
                "state": "present",
                "force": False,
            },
        )
        result = r.exception.args[0]
        assert result["changed"] is True

    def test_module_updates_when_user_exists(self):
        set_module_args(
            {
                "access_key": "testuser",
                "secret_key": "testuser123",
                "auth": {
                    "access_key": "minioadmin",
                    "secret_key": "minioadmin",
                    "url": "http://localhost:9000",
                },
            }
        )

        mock_user = self.MockMinioUser.return_value
        mock_user.user_exists.return_value = True
        mock_user.create_or_update_user.return_value = False
        with self.assertRaises(AnsibleExitJson) as r:
            minio_user.main()

        mock_user.create_or_update_user.assert_called_once_with(
            "testuser",
            {
                "secret_key": "testuser123",
                "policy": None,
                "state": "present",
                "force": False,
            },
        )
        result = r.exception.args[0]
        assert result["changed"] is False

    def test_module_deletes_when_state_is_absent_and_user_exists(self):
        set_module_args(
            {
                "access_key": "testuser",
                "secret_key": "testuser123",
                "auth": {
                    "access_key": "minioadmin",
                    "secret_key": "minioadmin",
                    "url": "http://localhost:9000",
                },
                "state": "absent",
            }
        )

        mock_user = self.MockMinioUser.return_value
        mock_user.user_exists.return_value = True
        mock_user.delete_user.return_value = True
        with self.assertRaises(AnsibleExitJson) as r:
            minio_user.main()

        mock_user.delete_user.assert_called_once_with("testuser")
        result = r.exception.args[0]
        assert result["changed"] is True
