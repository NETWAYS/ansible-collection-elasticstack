ELASTICSEARCH
=========

This role installs Elasticsearch on your hosts. Optionally it can configure Elastics Security components, too.

If you use the role to set up security you can use its CA to create certificates for Logstash and Kibana, too.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

* *elasticsearch_ca*: Set to the inventory hostname of the host that should house the CA for certificates for inter-node communication. (default: First node in the `elasticsearch` host group)

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
