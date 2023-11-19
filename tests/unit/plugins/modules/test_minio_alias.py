# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.net>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest

from unittest.mock import patch, ANY

from ansible_collections.dubzland.minio.plugins.modules import minio_alias
from ansible_collections.dubzland.minio.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    mock_run_command,
    set_module_args,
)


@pytest.fixture()
def mock_alias_record(
    name="testing",
    url="http://localhost:9001",
    access_key="test",
    secret_key="supersekret",
):
    data = {}
    if name is not None:
        data["alias"] = name
    if url is not None:
        data["URL"] = url
    if access_key is not None:
        data["accessKey"] = access_key
    if secret_key is not None:
        data["secretKey"] = secret_key

    return data


def test_alias_find_runs_command(mock_module):
    with mock_run_command(mock_module, "", "", 0) as run_command:
        minio_alias.alias_find(mock_module, "testing")

    run_command.assert_called_with(["/mock/bin/testing", "--json", "alias", "list"])


def test_alias_find_returns_none(mock_module):
    with mock_run_command(mock_module, "", "", 0):
        assert minio_alias.alias_find(mock_module, "testing") is None


def test_alias_find_returns_alias(mock_module, mock_alias_record):
    with mock_run_command(mock_module, json.dumps(mock_alias_record), "", 0):
        res = minio_alias.alias_find(mock_module, "testing")

        assert res["name"] == mock_alias_record["alias"]
        assert res["url"] == mock_alias_record["URL"]
        assert res["access_key"] == mock_alias_record["accessKey"]
        assert res["secret_key"] == mock_alias_record["secretKey"]


def test_alias_create_or_update_when_not_exist(mock_module, mock_alias_record):
    with mock_run_command(mock_module, "", "", 0) as run_command:
        minio_alias.alias_create_or_update(
            mock_module,
            "testing",
            mock_alias_record["URL"],
            mock_alias_record["accessKey"],
            mock_alias_record["secretKey"],
        )

    run_command.assert_called_with(
        [
            "/mock/bin/testing",
            "--json",
            "alias",
            "set",
            "testing",
            mock_alias_record["URL"],
            mock_alias_record["accessKey"],
            mock_alias_record["secretKey"],
        ]
    )


def test_alias_create_or_update_when_exists(mock_module, mock_alias_record):
    with mock_run_command(mock_module, mock_alias_record, "", 0) as run_command:
        minio_alias.alias_create_or_update(
            mock_module,
            "testing",
            mock_alias_record["URL"],
            mock_alias_record["accessKey"],
            "newsekretkey",
        )

    run_command.assert_called_with(
        [
            "/mock/bin/testing",
            "--json",
            "alias",
            "set",
            "testing",
            mock_alias_record["URL"],
            mock_alias_record["accessKey"],
            "newsekretkey",
        ]
    )


def test_alias_delete(mock_module):
    with mock_run_command(mock_module, "", "", 0) as run_command:
        minio_alias.alias_delete(mock_module, "testing")

    run_command.assert_called_with(
        ["/mock/bin/testing", "--json", "alias", "remove", "testing"]
    )


class TestMinioAlias(ModuleTestCase):
    def setUp(self):
        super().setUp()
        self.alias_find_mock = patch(
            "ansible_collections.dubzland.minio.plugins.modules.minio_alias.alias_find"
        ).start()
        self.alias_create_or_update_mock = patch(
            "ansible_collections.dubzland.minio.plugins.modules.minio_alias.alias_create_or_update"
        ).start()
        self.alias_delete_mock = patch(
            "ansible_collections.dubzland.minio.plugins.modules.minio_alias.alias_delete"
        ).start()

    def tearDown(self):
        self.alias_find_mock.stop()
        self.alias_create_or_update_mock.stop()

    def test_module_fail_when_args_missing(self):
        with self.assertRaises(AnsibleFailJson) as r:
            set_module_args({})
            minio_alias.main()

    def test_module_unchanged_when_exists(self):
        record = {
            "name": "testing",
            "url": "http://localhost:9000",
            "access_key": "test",
            "secret_key": "supersekret",
        }
        set_module_args(record)

        self.alias_find_mock.return_value = record

        with self.assertRaises(AnsibleExitJson) as r:
            minio_alias.main()

        assert self.alias_find_mock.call_count == 1
        result = r.exception.args[0]
        assert result["changed"] is False

    def test_module_update_when_exists(self):
        record = {
            "name": "testing",
            "url": "http://localhost:9000",
            "access_key": "test",
            "secret_key": "supersekret",
        }
        args = record.copy()
        args["secret_key"] = "newsekretkey"
        set_module_args(args)

        self.alias_find_mock.return_value = record

        with self.assertRaises(AnsibleExitJson) as r:
            minio_alias.main()

        assert self.alias_find_mock.call_count == 1
        result = r.exception.args[0]
        assert result["changed"] is True

        self.alias_create_or_update_mock.assert_called_with(
            ANY,
            "testing",
            args["url"],
            args["access_key"],
            args["secret_key"],
        )

    def test_module_create_when_not_exist(self):
        record = {
            "name": "testing",
            "url": "http://localhost:9000",
            "access_key": "test",
            "secret_key": "supersekret",
        }
        set_module_args(record)

        self.alias_find_mock.return_value = None

        with self.assertRaises(AnsibleExitJson) as r:
            minio_alias.main()

        assert self.alias_find_mock.call_count == 1
        result = r.exception.args[0]
        assert result["changed"] is True

        self.alias_create_or_update_mock.assert_called_with(
            ANY, "testing", record["url"], record["access_key"], record["secret_key"]
        )

    def test_module_unchanged_when_not_exist_and_state_absent(self):
        set_module_args(
            {
                "name": "testing",
                "url": "http://localhost:9000",
                "access_key": "test",
                "secret_key": "supersekret",
                "state": "absent",
            }
        )

        self.alias_find_mock.return_value = None

        with self.assertRaises(AnsibleExitJson) as r:
            minio_alias.main()

        assert self.alias_find_mock.call_count == 1
        assert self.alias_create_or_update_mock.call_count == 0
        result = r.exception.args[0]
        assert result["changed"] is False

    def test_module_changed_when_exists_and_state_absent(self):
        record = {
            "name": "testing",
            "url": "http://localhost:9000",
            "access_key": "test",
            "secret_key": "supersekret",
        }
        args = record.copy()
        args["state"] = "absent"
        set_module_args(args)

        self.alias_find_mock.return_value = record

        with self.assertRaises(AnsibleExitJson) as r:
            minio_alias.main()

        assert self.alias_find_mock.call_count == 1
        result = r.exception.args[0]
        assert result["changed"] is True

        self.alias_delete_mock.assert_called_with(ANY, record["name"])
