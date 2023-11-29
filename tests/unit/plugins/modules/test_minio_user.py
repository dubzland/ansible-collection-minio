# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from datetime import datetime, timezone

from ansible_collections.dubzland.minio.tests.unit.plugins.modules.utils import (
    MinioAdminClientTestCase,
)

from ansible_collections.dubzland.minio.plugins.modules.minio_user import MinioUser


class TestMinioUser(MinioAdminClientTestCase):
    def setUp(self):
        super(TestMinioUser, self).setUp()
        self.mock_module.check_mode = False

        self.user_module = MinioUser(self.mock_module, self.mock_client)

    def test_find_user(self):
        user_obj = {
            "policyName": "test-policy",
            "status": "enabled",
            "updatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        self.mock_client.user_list.return_value = json.dumps({"tester": user_obj})

        res = self.user_module.find_user("notester")
        self.assertEqual(res, None)

        res = self.user_module.find_user("tester")
        self.assertEqual(res, user_obj)

    def test_user_exists(self):
        user_obj = {
            "policyName": "test-policy",
            "status": "enabled",
            "updatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        self.mock_client.user_list.return_value = json.dumps({"tester": user_obj})

        res = self.user_module.user_exists("notester")
        self.assertEqual(res, False)

        res = self.user_module.user_exists("tester")
        self.assertEqual(res, True)
        self.assertEqual(self.user_module.user_object, user_obj)

    def test_create_or_update_user(self):
        self.mock_client.user_add.return_value = ""
        existing_user = {
            "policyName": "test-policy",
            "status": "enabled",
            "updatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        # Creating a new user
        self.mock_client.user_info.return_value = '{"status": "enabled"}'
        res = self.user_module.create_or_update_user(
            "tester2", {"secret_key": "testing321", "state": "present"}
        )
        self.mock_client.user_add.assert_called_once_with("tester2", "testing321")
        self.assertEqual(res, True)

        # Creating a new user (with a policy)
        self.mock_client.reset_mock()
        self.user_module.user_object = None
        self.mock_client.policy_set.return_value = ""
        self.mock_client.user_info.return_value = '{"status": "enabled"}'
        res = self.user_module.create_or_update_user(
            "tester2",
            {"secret_key": "testing321", "policy": "test-policy", "state": "present"},
        )
        self.mock_client.user_add.assert_called_once_with("tester2", "testing321")
        self.mock_client.policy_set.assert_called_once_with(
            "test-policy", user="tester2"
        )
        self.assertEqual(res, True)

        # Updating an existing user (no change)
        self.mock_client.reset_mock()
        self.mock_client.policy_set.return_value = ""
        self.user_module.user_object = existing_user
        res = self.user_module.create_or_update_user(
            "tester",
            {"secret_key": "testing123", "policy": "test-policy", "state": "present"},
        )
        self.mock_client.user_add.assert_not_called()
        self.assertEqual(res, False)

        # Updating an existing user (policy)
        self.mock_client.reset_mock()
        self.user_module.user_object = existing_user
        res = self.user_module.create_or_update_user(
            "tester",
            {
                "secret_key": "testing123",
                "policy": "new-test-policy",
                "state": "present",
            },
        )
        self.mock_client.user_add.assert_not_called()
        self.mock_client.policy_set.assert_called_once_with(
            "new-test-policy", user="tester"
        )
        self.assertEqual(res, True)

        # Updating an existing user (state)
        self.mock_client.reset_mock()
        self.user_module.user_object = existing_user
        res = self.user_module.create_or_update_user(
            "tester",
            {"secret_key": "testing123", "policy": "test-policy", "state": "disabled"},
        )
        self.mock_client.user_disable.assert_called_once_with("tester")
        self.assertEqual(res, True)

        # Updating an existing user (forced)
        self.mock_client.reset_mock()
        self.user_module.user_object = existing_user
        self.user_module.create_or_update_user(
            "tester",
            {
                "secret_key": "testing123",
                "policy": "test-policy",
                "state": "present",
                "force": True,
            },
        )
        self.mock_client.user_add.assert_called_once_with("tester", "testing123")

    def test_delete_user(self):
        existing_user = {
            "policyName": "test-policy",
            "status": "enabled",
            "updatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        self.user_module.user_object = existing_user
        self.mock_client.user_remove.return_value = ""
        self.user_module.delete_user("tester")
        self.mock_client.user_remove.assert_called_once_with("tester")
