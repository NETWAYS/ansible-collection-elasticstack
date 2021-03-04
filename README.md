Role Name
=========

[![CI](https://github.com/widhalmt/ansible-role-beats/workflows/Molecule%20Test/badge.svg?event=push)](https://github.com/widhalmt/ansible-role-beats/workflows/Molecule%20Test/badge.svg)

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

* *beats_output*: Set to `logstash` or `elasticsearch`. (default: `logstash`)
* *beats_target_hosts*: Only use when this role is used standalone. When used in combination with our other roles, the target hosts will be determined automatically. (default: `localhost`)

The following variables only apply if you use this role together with our other Elastic Stack roles.

* *elastic_stack_full_stack*: Use `ansible-role-elasticsearch` as well (default: `false`)
* *elastic_ca_dir*: Directory where on the Elasticsearch CA host certificates are stored. This is only useful in connection with out other Elastic Stack related roles. (default: `/opt/es-ca`)
* *elastic_ca_pass*: Password for Elasticsearch CA (default: `PleaseChangeMe`)
* *elastic_initial_passwords*: Path to file with initical elasticsearch passwords (default: `/usr/share/elasticsearch/initial_passwords`)

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
