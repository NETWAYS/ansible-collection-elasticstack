Ansible Role: Kibana
=========

[![Molecule Tests](https://github.com/widhalmt/ansible-role-kibana/workflows/Molecule%20Test/badge.svg?event=push)](https://github.com/widhalmt/ansible-role-kibana/workflows/Molecule%20Test/badge.svg)

This roles installs and configures Kibana.

Requirements
------------

You need to have the Elastic Repos configured on you system. You can use our [role](https://github.com/widhalmt/ansible-role-elastic-repos) for that but you don't have to.

Role Variables
--------------

* *kibana_elasticsearch_hosts*: A list of DNS resolvable hostnames of Elasticsearch hosts to connect your Kibana instance to. (default: `- localhost`)
* *kibana_manage_yaml*: Change Kibanas main configuration file (default: `true`)
* *kibana_config_backup*: Keep backups if we change any configuration file (default: `true`)
* *elastic_ca_dir*: Directory where on the Elasticsearch CA host certificates are stored. This is only useful in connection with out other Elastic Stack related roles. (default: `/opt/es-ca`)

If you don't change `kibana_elasticsearch_hosts`, certificate verification will skip hostname checks

Dependencies
------------

There's no real dependency but you might want to use this role together with our other Elastic Stack related roles:

* [Elasticsearch](https://github.com/widhalmt/ansible-role-elasticsearch)
* [Logstash](https://github.com/NETWAYS/ansible-role-logstash)
* [Elastic Repositories](https://github.com/widhalmt/ansible-role-elastic-repos)

Example Playbook
----------------

    - hosts: kibana
      roles:
         - kibana

License
-------

GPLv3+

Author Information
------------------

This role was created in 2019 by [Netways](https://www.netways.de/).
