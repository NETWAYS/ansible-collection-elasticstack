#!/usr/bin/python

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.netways.elasticstack.plugins.module_utils.elasticsearch_api import (
    UserObject,
)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def run_module():
    '''
    Elasticsearch user management.
    '''

    # https://github.com/NETWAYS/ansible-collection-elasticstack/blob/main/roles/logstash/tasks/logstash-security.yml#L405-L472

    # get user
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-user.html

    # create or update user
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-user.html

    # delete user
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-delete-user.html

    # enable user
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-enable-user.html

    # disable user
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-disable-user.html

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type=str, required=True),
            fullname=dict(type=str, required=False),
            password=dict(type=str, required=True),
            email=dict(type=str, required=False),
            roles=dict(type=list, required=True),
            metadata=dict(type=dict, required=False),
            state=dict(type=str, required=False, default="present"), # 'present' or 'absent'
            enabled=dict(type=bool, required=False, default=True), # True=enabled & False=disabled
            endpoint=dict(type=str, required=False, default="https://localhost:9200"),
            ca=dict(type=str, required=True), # Path to ca to authenticate API requests
            es_version=dict(type=int, required=False, default=8), # Elasticsearch version
        )
    )

    # Check if provided state is valid
    valid_states = list("present", "absent")
    if module.params['state'] not in valid_states:
        module.exit_json(
            failed=True,
            changed=False,
            stderr="Invalid state provided. Use 'present' or 'absent."
        )

    user = UserObject(module)

    module.exit_json(
        debug=user
    )

    # Block 1
        # if (current state == configured state) && (current properties == configured properties) -> exit

        # if (current enabled != configured enable) -> change

        # if current state != configured state -> create or delete (based on configured state)

        # if (current state == configured state) && (current properties != configured properties) -> update user properties

    # Block 2

if __name__ == "__main__":
    run_module()