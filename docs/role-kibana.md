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
* *kibana_tls*: Whether to offer `https` for clients or not (default: `false`)
* *kibana_tls_cert*: Path to the certificate Kibana should show to its clients (default: `/etc/kibana/certs/cert.pem`)
* *kibana_tls_key*: Path to the key Kibana should use when communicating with clients (default: `/etc/kibana/certs/key.pem`)

* *kibana_security*: Activate TLS and authentication when connecting to Elasticsearch. **Note**: Only works when `elastic_stack_full_stack` is enabled. (default: `true`)

These variables are identical over all our elastic related roles, hence the different naming scheme.

* *elastic_stack_full_stack*: Use `ansible-role-elasticsearch` as well (default: `false`)
* *elasticsearch_ca*: Set to the inventory hostname of the host that should house the CA for certificates for inter-node communication. (default: First node in the `elasticsearch` host group)
* *elastic_ca_dir*: Directory where on the Elasticsearch CA host certificates are stored. This is only useful in connection with out other Elastic Stack related roles. (default: `/opt/es-ca`)
* *elastic_ca_pass*: Password for Elasticsearch CA (default: `PleaseChangeMe`)
* *elastic_initial_passwords*: Path to file with initical elasticsearch passwords (default: `/usr/share/elasticsearch/initial_passwords`)
* *elastic_release*: Major release version of Elastic stack to configure. (default: `7`)
* *elastic_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)

If you use `localhost` in `kibana_elasticsearch_hosts` , certificate verification will skip hostname checks

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



This role was created in 2019 by [Netways](https://www.netways.de/).
