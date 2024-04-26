# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from ansible.playbook.task import Task

from ansible_collections.dubzland.minio.plugins.action.minio_policy import (
    ActionModule as MinioPolicyAction,
)


class TestNetworkFacts(unittest.TestCase):
    task = MagicMock(Task)
    play_context = MagicMock()
    play_context.check_mode = False
    connection = MagicMock()
    templar = MagicMock()

    def test_minio_policy_with_policy_data(self):
        self.fqcn_task_vars = {}
        self.task.action = "minio_policy"
        self.task.async_val = False
        self.task.args = dict(name="testing", data="testing_data")

        plugin = MinioPolicyAction(
            self.task,
            self.connection,
            self.play_context,
            loader=None,
            shared_loader_obj=None,
            templar=self.templar,
        )
        execute_module = MagicMock()
        plugin._execute_module = execute_module

        plugin.run(task_vars=self.fqcn_task_vars)
        self.assertEqual(execute_module.call_count, 1)
        self.assertEqual(
            execute_module.call_args.kwargs["module_name"],
            "dubzland.minio.minio_policy",
        )
        self.assertEqual(
            execute_module.call_args.kwargs["module_args"],
            dict(name="testing", state=None, data="testing_data"),
        )

    def test_minio_policy_with_statements(self):
        self.fqcn_task_vars = {}
        self.task.action = "minio_policy"
        self.task.async_val = False
        self.task.args = dict(
            name="testing",
            statements=[dict(effect="Allow", action="s3:*", resource="arn:aws:s3:::*")],
        )

        plugin = MinioPolicyAction(
            self.task,
            self.connection,
            self.play_context,
            loader=None,
            shared_loader_obj=None,
            templar=self.templar,
        )

        execute_module = MagicMock()
        plugin._execute_module = execute_module

        expected_policy_data = "policy_data"

        self.templar.copy_with_new_env = MagicMock()
        self.templar.copy_with_new_env.return_value = self.templar

        do_template = MagicMock()
        do_template.return_value = expected_policy_data
        self.templar.do_template = do_template

        plugin.run(task_vars=self.fqcn_task_vars)
        self.assertEqual(execute_module.call_count, 1)
        self.assertEqual(
            execute_module.call_args.kwargs["module_name"],
            "dubzland.minio.minio_policy",
        )

        self.assertEqual(
            execute_module.call_args.kwargs["module_args"],
            dict(name="testing", state=None, data=expected_policy_data),
        )
