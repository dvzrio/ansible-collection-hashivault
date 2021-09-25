# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Xabier Napal (@xabinapal) <xabier.napal@dvzr.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  endpoint:
    description:
      - Endpoint where the Vault cluster is accessible.
    type: str
    default: https://localhost:8200

  token:
    description:
      - The token used to authenticate with.
    type: str
    required: true
"""
