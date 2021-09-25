# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Xabier Napal (@xabinapal) <xabier.napal@dvzr.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import typing

import json
import json.decoder
import urllib.request

from ansible.module_utils.basic import AnsibleModule, to_native, to_text
from ansible.module_utils.urls import open_url


class HashivaultBaseAnsibleSpec(typing.TypedDict):
    endpoint: str
    token: str


def hashivault_base_ansible_spec():
    return dict(
        endpoint=dict(
            type="str",
            default="https://localhost:8200",
        ),
        token=dict(
            type="str",
            required=True,
            no_log=True,
        ),
    )


def hashivault_open_url(
    module: AnsibleModule,
    method: typing.Union[typing.Literal["GET"], typing.Literal["PUT"], typing.Literal["DELETE"]],
    path: str,
    data: typing.Optional[typing.Mapping[str, typing.Any]] = None,
):
    params: HashivaultBaseAnsibleSpec = module.params

    url = params["endpoint"] + path

    body, code = None, None
    try:
        response = open_url(
            url,
            method=method,
            data=json.dumps(data) if data is not None else None,
            headers=dict(
                Content-Type="application/json",
                X-Vault-Token=params["token"],
            ),
        )

        body = to_text(response.read())
        code = response.code
    except urllib.request.HTTPError as e:
        body = to_text(e.read())
        code = e.code
    except Exception as e:
        module.fail_json(msg=to_native(e))

    response = None
    try:
        response = json.loads(body)
    except json.decoder.JSONDecodeError as e:
        response = body
    except Exception as e:
        module.fail_json(msg=to_native(e))

    return response, code
