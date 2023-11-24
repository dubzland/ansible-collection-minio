# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    # Allow wildcard import because we really do want to import all of mock's
    # symbols into this compat shim
    # pylint: disable=wildcard-import,unused-wildcard-import
    from unittest.mock import *  # noqa: F401, pylint: disable=unused-import
except ImportError:
    # Python 2
    # pylint: disable=wildcard-import,unused-wildcard-import
    try:
        from mock import *  # noqa: F401, pylint: disable=unused-import
    except ImportError:
        print("You need the mock library installed on python2.x to run tests")
