Ansible module: elasticsearch_user
===

This module creates, updates and deletes users from your Elasticsearch.

Requirements
---

As this module uses the Elasticsearch API you will need to install the `elasticsearch` Python3 library.
```
pip3 install elasticsearch
```

Module arguments
---

* *name*: Name of your user (**Required**)
* *fullname*: Fullname of your user
* *password*: Password for your user (**Required**)
* *email*: Email for your user
* *roles*: List of roles (**Required**)
* *enabled*: Define wheter this user should be enabled (Default: `true`)
* *state*: State of the role. `absent` to delete the user (Default: `present`)
* *host*: API endpoint (**Required**)
* *auth_user*: User to authenticate on the Elasticsearch API (**Required**)
* *auth_pass*: Password for the given user (**Required**)
* *verify_certs*: Verify certificates (Default: True)
* *ca_certs*: Verify HTTPS connection by using ca certificate. Path to ca needs to be given

Example usage
---
```
    - name: Create elasticsearch user 'new-user'
      netways.elasticstack.elasticsearch_user:
        name: new-user
        fullname: New User
        password: changeMe321!
        email: new@user.de
        roles:
          - new-role
          - logstash-writer
        enabled: true
        state: present
        host: https://localhost:9200
        auth_user: elastic
        auth_pass: changeMe123!
        verify_certs: false
```