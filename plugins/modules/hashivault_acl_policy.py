#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Xabier Napal (@xabinapal) <xabier.napal@dvzr.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import typing

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.dvzrio.hashivault.plugins.module_utils.hashivault import hashivault_open_url
from ansible_collections.dvzrio.hashivault.plugins.module_utils.hashivault_acl_policy import (
    HashivaultACLPolicy,
    HashivaultACLPolicyAnsibleSpec,
    hashivault_acl_policy_ansible_spec,
)


DOCUMENTATION = r"""
---
module: hashivault_acl_policy

short_description: Manages Vault ACL policies.

description:
  - Creates, updates and deletes Vault ACL policies.

options:
  name:
    description:
      - Name of the ACL policy.
    type: str
    required: true

  policy:
    description:
      - Raw ACL policy contents, either on HCL or JSON format.
      - U(https://www.vaultproject.io/docs/concepts/policies#policy-syntax).
      - Required if I(state=present).
    type: str

  state:
    description:
      - Whether to ensure the ACL policy should exist or not.
    type: str
    choices:
      - present
      - absent
    default: present

author:
  - Xabier Napal (@xabinapal)

extends_documentation_fragment:
  - dvzrio.hashivault.hashivault
"""

EXAMPLES = r"""
- name: Create or update test policy
  dvzrio.hashivault.hashivault_acl_policy:
    endpoint: https://localhost:8200
    token: dvzrio
    name: test
    policy: |-
      path "secret/test" {
        capabilities = ["read", "write"]
      }
    state: present

- name: Delete test policy
  dvzrio.hashivault.hashivault_acl_policy:
    endpoint: https://localhost:8200
    token: dvzrio
    name: test
    state: absent
"""

RETURN = r"""
name:
  description: Name of the ACL policy.
  returned: always
  type: str
  sample: test
policy:
  description: Raw ACL policy contents.
  returned: always
  type: str
  sample: |-
    path "secret/test" {
    capabilities = ["read", "write"]
    }
"""


def acl_policy_get(module: AnsibleModule, params: HashivaultACLPolicyAnsibleSpec) -> typing.Optional[HashivaultACLPolicy]:
    response, code = hashivault_open_url(module, "GET", f"/v1/sys/policies/acl/{params['name']}")
    if code == 200:
        return HashivaultACLPolicy(
            name=response["data"]["name"],
            policy=response["data"]["policy"],
        )
    elif code == 404:
        return None

    module.fail_json("unexpected error getting acl policy", code=code)


def acl_policy_put(module: AnsibleModule, params: HashivaultACLPolicyAnsibleSpec) -> HashivaultACLPolicy:
    if not module.check_mode:
        response, code = hashivault_open_url(module, "PUT", f"/v1/sys/policies/acl/{params['name']}", dict(
            name=params["name"],
            policy=params["policy"]
        ))
        if code != 204:
            module.fail_json("unexpected error putting acl policy", response=response, code=code)

    return HashivaultACLPolicy(name=module.params['name'], policy=module.params['policy'])


def acl_policy_delete(module: AnsibleModule, params: HashivaultACLPolicyAnsibleSpec):
    if not module.check_mode:
        response, code = hashivault_open_url(module, "DELETE", f"/v1/sys/policies/acl/{params['name']}")
        if code != 204:
            module.fail_json("unexpected error deleting acl policy", response=response, code=code)

    return HashivaultACLPolicy(name=module.params['name'], policy=None)


def main():
    spec = hashivault_acl_policy_ansible_spec()
    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("policy",),),
        ],
    )

    params: HashivaultACLPolicyAnsibleSpec = module.params

    changed = False
    result = acl_policy_get(module, params)

    if params["state"] == "present":
        if result is None or result["policy"] != params["policy"]:
            changed = True
            result = acl_policy_put(module, params)
    elif params["state"] == "absent":
        if result is not None:
            changed = True
            result = acl_policy_delete(module, params)

    module.exit_json(changed=changed, **(result or dict()))


if __name__ == "__main__":
    main()
