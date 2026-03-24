#!/usr/bin/python

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: elasticsearch_user
short_description: Manage Elasticsearch users
description:
  - Creates, updates, or deletes Elasticsearch native users using the Security API.
  - Requires the C(elasticsearch) Python library on the target host.
version_added: "1.0.0"
author:
  - Tobias Bauriedel (@tbauriedel)
requirements:
  - elasticsearch < 9
options:
  name:
    description: Username of the Elasticsearch user.
    type: str
    required: true
  fullname:
    description: Full display name of the user.
    type: str
    required: false
  password:
    description: Password for the user. Required when (state=present).
    type: str
    required: false
    default: null
  email:
    description: Email address of the user.
    type: str
    required: false
  roles:
    description: List of roles assigned to the user. Required when (state=present).
    type: list
    elements: str
    required: false
    default: null
  enabled:
    description: Whether the user account is enabled.
    type: bool
    required: false
    default: true
  state:
    description: Whether the user should exist or not.
    type: str
    required: false
    default: present
    choices: [present, absent]
  host:
    description: URL of the Elasticsearch host, including protocol and port.
    type: str
    required: true
  auth_user:
    description: Username for authentication.
    type: str
    required: true
  auth_pass:
    description: Password for authentication.
    type: str
    required: true
  ca_certs:
    description: Path to the CA certificate file for TLS verification.
    type: str
    required: false
  verify_certs:
    description: Whether to verify TLS certificates.
    type: bool
    required: false
    default: true
'''

EXAMPLES = r'''
- name: Create an Elasticsearch user
  netways.elasticstack.elasticsearch_user:
    name: john
    fullname: John Doe
    password: "{{ user_password }}"
    email: john@example.com
    roles:
      - my-role
    enabled: true
    state: present
    host: https://localhost:9200
    auth_user: elastic
    auth_pass: "{{ elastic_password }}"
    ca_certs: /etc/elasticsearch/certs/http_ca.crt

- name: Delete an Elasticsearch user
  netways.elasticstack.elasticsearch_user:
    name: john
    state: absent
    host: https://localhost:9200
    auth_user: elastic
    auth_pass: "{{ elastic_password }}"
    verify_certs: false
'''

RETURN = r'''
changed:
  description: Whether the user was created, updated, or deleted.
  type: bool
  returned: always
msg:
  description: Human-readable status message.
  type: str
  returned: on change
'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.netways.elasticstack.plugins.module_utils.api import (
    HAS_ELASTICSEARCH, ELASTICSEARCH_IMPORT_ERROR
)
from ansible_collections.netways.elasticstack.plugins.module_utils.elasticsearch_user import (
    User
)


def run_module():

    module = AnsibleModule(
        argument_spec=dict(
            # User args
            name=dict(type='str', required=True),
            fullname=dict(type='str', required=False),
            password=dict(type='str', required=False, no_log=True),
            email=dict(type='str', required=False),
            roles=dict(type='list', elements='str', required=False),
            enabled=dict(type='bool', required=False, default=True),
            state=dict(type='str', required=False, default='present', choices=['present', 'absent']),

            # Auth args
            host=dict(type='str', required=True),
            auth_user=dict(type='str', required=True),
            auth_pass=dict(type='str', required=True, no_log=True),
            ca_certs=dict(type='str', required=False),
            verify_certs=dict(type='bool', required=False, default=True)
        ),
        required_if=[
            ('state', 'present', ['password', 'roles']),
        ]
    )

    result = dict(
        failed=False,
        changed=False
    )

    if not HAS_ELASTICSEARCH:
        module.fail_json(
            msg=missing_required_lib('elasticsearch'),
            exception=ELASTICSEARCH_IMPORT_ERROR
        )

    user = User(
        result=result,
        user_name=module.params['name'],
        full_name=module.params['fullname'],
        password=module.params['password'],
        email=module.params['email'],
        roles=module.params['roles'],
        enabled=module.params['enabled'],
        state=module.params['state'],
        host=module.params['host'],
        auth_user=module.params['auth_user'],
        auth_pass=module.params['auth_pass'],
        ca_certs=module.params['ca_certs'],
        verify_certs=module.params['verify_certs'],
    )

    result = user.return_result()

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
