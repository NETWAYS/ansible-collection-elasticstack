Ansible module: elasticsearch_role
===

This module creates, updates and deletes roles from your Elasticsearch.

Requirements
---

As this module uses the Elasticsearch API you will need to install the `elasticsearch` Python3 library.
```
pip3 install elasticsearch
```

Module arguments
---

* *name*: Name of your role (**Required**)
* *cluster*: List of clusters
* *indicies*: List of indicies
  * *names*: List of names (**Required**)
  * *privileges*: List of privileges (**Required**)
* *state*: State of the role (Default: `present`)
* *host*: API endpoint (**Required**)
* *auth_user*: User to authenticate on the Elasticsearch API (**Required**)
* *auth_pass*: Password for the given user (**Required**)
* *verify_certs*: Verify certificates (Default: True)
* *ca_certs*: Verify HTTPS connection by using ca certificate. Path to ca needs to be given

Example usage
---
```
    - name: Create elasticsearch role 'new-role1'
      netways.elasticstack.elasticsearch_role:
        name: new-role1
        cluster:
          - manage_own_api_key
          - delegate_pki
        indicies:
          - names:
              - default01
            privileges:
              - read
              - write
        state: present
        host: https://localhost:9200
        auth_user: elastic
        auth_pass: changeMe123!
        verify_certs: true
        ca_certs: /etc/elasticsearch/certs/http_ca.crt

    - name: Create elasticsearch role 'new-role2'
      netways.elasticstack.elasticsearch_role:
        name: new-role2
        cluster:
          - manage_own_api_key
          - delegate_pki
        indicies:
          - names:
              - default01
            privileges:
              - read
              - write
        state: present
        host: https://localhost:9200
        auth_user: elastic
        auth_pass: changeMe123!
        verify_certs: false
```