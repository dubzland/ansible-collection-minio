# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.dubzland.minio.tests.unit.compat.mock import MagicMock

from ansible_collections.dubzland.minio.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    set_module_args,
    with_mock_client,
)

from ansible_collections.dubzland.minio.plugins.modules import minio_bucket


class TestMinioBucket(ModuleTestCase):
    def setUp(self):
        super(TestMinioBucket, self).setUp()

    @pytest.fixture(autouse=True)
    def _mocker(self, mocker):
        self.mocker = mocker

    def test_module_fail_when_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            minio_bucket.main()

    @with_mock_client("minio_bucket")
    def test_module_unchanged_when_exists(self, mock_client):
        mock_client.bucket_exists.return_value = True

        with self.assertRaises(AnsibleExitJson) as r:
            set_module_args(
                {
                    "name": "testing",
                    "minio_access_key": "testing",
                    "minio_secret_key": "supersekret",
                    "minio_url": "http://localhost:9000",
                }
            )
            minio_bucket.main()

        mock_client.bucket_exists.assert_called_once()
        mock_client.make_bucket.assert_not_called()
        result = r.exception.args[0]
        assert result["changed"] is False

    @with_mock_client("minio_bucket")
    def test_module_create_when_not_exist(self, mock_client):
        bucket = MagicMock()
        bucket.name.return_value = "testing"
        mock_client.bucket_exists.return_value = False

        with self.assertRaises(AnsibleExitJson) as r:
            set_module_args(
                {
                    "name": "testing",
                    "minio_access_key": "testing",
                    "minio_secret_key": "supersekret",
                    "minio_url": "http://localhost:9000",
                }
            )
            minio_bucket.main()

        mock_client.bucket_exists.assert_called_once()
        mock_client.make_bucket.assert_called_once_with("testing")
        result = r.exception.args[0]
        assert result["changed"] is True

    @with_mock_client("minio_bucket")
    def test_module_unchanged_when_not_exist_and_state_absent(self, mock_client):
        mock_client.bucket_exists.return_value = False

        with self.assertRaises(AnsibleExitJson) as r:
            set_module_args(
                {
                    "name": "testing",
                    "minio_access_key": "testing",
                    "minio_secret_key": "supersekret",
                    "minio_url": "http://localhost:9000",
                    "state": "absent",
                }
            )
            minio_bucket.main()

        mock_client.bucket_exists.assert_called_once()
        mock_client.make_bucket.assert_not_called()
        result = r.exception.args[0]
        assert result["changed"] is False

    @with_mock_client("minio_bucket")
    def test_module_changed_when_exists_and_state_absent(self, mock_client):
        mock_client.bucket_exists.return_value = True

        with self.assertRaises(AnsibleExitJson) as r:
            set_module_args(
                {
                    "name": "testing",
                    "minio_access_key": "testing",
                    "minio_secret_key": "supersekret",
                    "minio_url": "http://localhost:9000",
                    "state": "absent",
                }
            )
            minio_bucket.main()

        mock_client.bucket_exists.assert_called_once()
        mock_client.make_bucket.assert_not_called()
        result = r.exception.args[0]
        assert result["changed"] is False
