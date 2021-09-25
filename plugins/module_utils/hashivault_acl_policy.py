# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Xabier Napal (@xabinapal) <xabier.napal@dvzr.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import typing

from ansible_collections.dvzrio.hashivault.plugins.module_utils.hashivault import (
    HashivaultBaseAnsibleSpec,
    hashivault_base_ansible_spec,
)


class HashivaultACLPolicy(typing.TypedDict):
    name: str
    policy: str


class HashivaultACLPolicyAnsibleSpec(HashivaultBaseAnsibleSpec):
    name: str
    policy: str
    state: typing.Union[typing.Literal["present"], typing.Literal["absent"]]


def hashivault_acl_policy_ansible_spec():
    return dict(
        **hashivault_base_ansible_spec(),
        **dict(
            name=dict(
                type="str",
                required=True,
            ),
            policy=dict(
                type="str",
            ),
            state=dict(
                type="str",
                choices=["present", "absent"],
                default="present",
            ),
        )
    )
