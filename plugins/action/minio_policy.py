#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ansible.plugins.action import ActionBase
from ansible.errors import (
    AnsibleAction,
    AnsibleActionFail,
)


class ActionModule(ActionBase):
    TRANSFERS_FILES = True

    POLICY_TEMPLATE = """
{
    "Version": "2012-10-17",
    "Statement": [
{% for statement in statements %}
        {
            "Effect": "{{ statement['effect'] }}",
            "Action": ["{{ statement['action'].join('", "') }}"],
            "Resource": ["{{ statement['resource'].join('", "') }}"]
        },
{% endfor %}
    ]
}
    """

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        name = self._task.args.get("name", None)
        state = self._task.args.get("state", None)
        data = self._task.args.get("data", None)

        try:
            if "statements" in self._task.args:
                if data is not None:
                    raise AnsibleActionFail(
                        "parameters are mutually exclusive: ('data', 'statements')"
                    )
                else:
                    statements = self._task.args.get("statements")
                    template_vars = {"statements": statements}
                    templar = self._templar.copy_with_new_env(
                        available_variables=template_vars
                    )
                    data = templar.do_template(self.POLICY_TEMPLATE)

            module_args = dict(name=name, state=state, data=data)

            result.update(
                self._execute_module(
                    module_name="dubzland.minio.minio_policy",
                    module_args=module_args,
                    task_vars=task_vars,
                )
            )

        except AnsibleAction as e:
            result.update(e.result)

        return result
