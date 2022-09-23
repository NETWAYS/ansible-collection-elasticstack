ELASTICSEARCH
=========

This role installs Elasticsearch on your hosts. Optionally it can configure Elastics Security components, too.

If you use the role to set up security you can use its CA to create certificates for Logstash and Kibana, too.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

* *elasticsearch_enable*: Start and enable Elasticsearch (default: `true`)
* *elasticsearch_ca*: Set to the inventory hostname of the host that should house the CA for certificates for inter-node communication. (default: First node in the `elasticsearch` host group)
* *elasticsearch_datapath*: Path where Elasticsearch will store it's data. (default: `/var/lib/elasticsearch` - the packages default)
* *elasticsearch_create_datapath*: Create the path for data to store if it doesn't exist. (default: `false` - only useful if you change `elasticsearch_datapath`)
*elasticsearch_fs_repo*: List of paths that should be registered as repository for snapshots (only filesystem supported so far). (default: none) Remember, that every node needs access to the same share under the same path.
* *elasticsearch_disable_systemcallfilterchecks*: Disable system call filter checks. This has a security impact but is necessary on some systems. Please refer to the [docs](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/_system_call_filter_check.html) for details. (default: `false`)

These variables are identical over all our elastic related roles, hence the different naming schemes.

*elastic_release*: Major release version of Elastic stack to configure. (default: `7`)
*elastic_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)


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
