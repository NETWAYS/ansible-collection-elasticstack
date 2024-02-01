#!/usr/bin/python

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.netways.elasticstack.plugins.module_utils.api import (
    User
)


def run_module():
    '''
    Elasticsearch user management.

    ```
    netways.elasticstack.elasticsearch_user:
        name: new-user1
        fullname: New User
        password: changeMe123!
        email: "new@user.de"
        roles:
          - new-role1
        enabled: true
        state: absent
        host: https://localhost:9200
        auth_user: elastic
        auth_pass: "{{ elasticstack_password.stdout }}"
        verify_certs: false
        ca_certs: /etc/elasticsearch/certs/http_ca.crt
    ```
    '''

    module = AnsibleModule(
        argument_spec=dict(
            # User args
            name=dict(type=str, required=True),
            fullname=dict(type=str, required=False),
            password=dict(type=str, required=True),
            email=dict(type=str, required=False),
            roles=dict(type=list, required=True),
            enabled=dict(type=bool, required=False, default=True),
            state=dict(type=str, required=False, default="present"),
            
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