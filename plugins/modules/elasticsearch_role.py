#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.netways.elasticstack.plugins.module_utils.api import (
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
            name=dict(type=str, required=True),
            cluster=dict(type=list, required=False),
            indicies=dict(type=list, required=False), # indicies.{n}.name, indicies.{n}.privileges
            state=dict(type=str, required=False, default='present'),
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