#!/usr/bin/python

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: elasticsearch_role
short_description: Manage Elasticsearch roles
description:
  - Creates, updates, or deletes Elasticsearch roles using the Security API.
  - Requires the C(elasticsearch) Python library on the target host.
version_added: "1.0.0"
author:
  - Tobias Bauriedel (@tbauriedel)
requirements:
  - elasticsearch < 9
options:
  name:
    description: Name of the Elasticsearch role.
    type: str
    required: true
  cluster:
    description: List of cluster-level privileges assigned to the role.
    type: list
    elements: str
    required: false
  indicies:
    description: List of index permission objects defining index patterns and privileges.
    type: list
    elements: dict
    required: false
  state:
    description: Whether the role should exist or not.
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
- name: Create an Elasticsearch role
  netways.elasticstack.elasticsearch_role:
    name: my-role
    cluster:
      - manage_own_api_key
    indicies:
      - names:
          - my-index-*
        privileges:
          - read
          - write
    state: present
    host: https://localhost:9200
    auth_user: elastic
    auth_pass: "{{ elastic_password }}"
    ca_certs: /etc/elasticsearch/certs/http_ca.crt

- name: Delete an Elasticsearch role
  netways.elasticstack.elasticsearch_role:
    name: my-role
    state: absent
    host: https://localhost:9200
    auth_user: elastic
    auth_pass: "{{ elastic_password }}"
    verify_certs: false
'''

RETURN = r'''
changed:
  description: Whether the role was created, updated, or deleted.
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
from ansible_collections.netways.elasticstack.plugins.module_utils.elasticsearch_role import (
    Role
)


def run_module():
    # get role
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-role.html

    # create or update role
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role.html

    module = AnsibleModule(
        argument_spec=dict(
            # User args
            name=dict(type='str', required=True),
            cluster=dict(type='list', elements='str', required=False),
            indicies=dict(type='list', elements='dict', required=False),
            state=dict(type='str', required=False, default='present', choices=['present', 'absent']),

            # Auth args
            host=dict(type='str', required=True),
            auth_user=dict(type='str', required=True),
            auth_pass=dict(type='str', required=True, no_log=True),
            ca_certs=dict(type='str', required=False),
            verify_certs=dict(type='bool', required=False, default=True)
        )
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

    role = Role(
        result=result,
        role_name=module.params['name'],
        cluster=module.params['cluster'],
        indicies=module.params['indicies'],
        state=module.params['state'],
        host=module.params['host'],
        auth_user=module.params['auth_user'],
        auth_pass=module.params['auth_pass'],
        ca_certs=module.params['ca_certs'],
        verify_certs=module.params['verify_certs'],
    )

    result = role.return_result()

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
