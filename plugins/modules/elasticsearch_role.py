#!/usr/bin/python

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.netways.elasticstack.plugins.module_utils.elasticsearch_role import (
    Role
)

def run_module():
    '''
    Elasticsearch user management.

    ```
    netways.elasticstack.elasticsearch_role:
        name: new-role
        cluster:
          - manage_own_api_key
          - delegate_pki
        indicies:
          - names:
              - foobar
            privileges:
              - read
              - write
        state: present
        host: https://localhost:9200
        auth_user: elastic
        auth_pass: changeMe123!
        verify_certs: false
        ca_certs: /etc/elasticsearch/certs/http_ca.crt
    ```
    '''

    # get role
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-role.html

    # create or update role
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role.html

    module = AnsibleModule(
        argument_spec=dict(
            # User args
            name=dict(type=str, required=True),
            cluster=dict(type=list, required=False),
            indicies=dict(type=list, required=False),
            state=dict(type=str, required=False, default='present'),

            # Auth args
            host=dict(type=str, required=True),
            auth_user=dict(type=str, required=True),
            auth_pass=dict(type=str, required=True),
            ca_certs=dict(type=str, required=False),
            verify_certs=dict(type=bool, required=False, default=True)
        )
    )

    result = dict(
        failed=False,
        changed=False
    )

    if module.params['state'] != 'absent' and module.params['state'] != 'present':
        result['stderr'] = "Invalid state given. Please use 'absent' or 'present'"
        result['failed'] = True
        
        module.exit_json(**result)


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