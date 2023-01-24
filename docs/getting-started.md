Collection Elastic Stack
-------------------------

Installation
-----------

You can easily install the collection with the ansible-galaxy command.

```
ansible-galaxy collection install netways.elasticstack
```

Or if you are using Tower or AWX add the collection to your requirements file.

```
collections:
  - name: NETWAYS.elasticstack
```

Usage
---------

To use the collection in your Ansible playbook add the following key to your playbook.

```
- name: Playbook
  hosts: some_host_pattern
  collections:
    - NETWAYS.elasticstack
  tasks:
    - name: import role logstash
      import_role:
        name: logstash
```

Or refer to the role with the FQCN of the role.

```
- name: Playbook
  hosts: some_host_pattern
  tasks:
    - name: import role by FQCN  from a collection
      import_role:
        name: NETWAYS.elasticstack.logstash
```

Roles
-------

* [Beats](docs/role-beats.md)
* [Elasticsearch](docs/role-elasticsearch.md)
* [Kibana](docs/role-kibana.md)
* [Logstash](docs/role-logstash.md)
* [Repos](docs/role-repos.md)


Variables
-----------

Every role got its own set of variables, in addition a few variables are useable on any role. Below are all general collection vars.

* *elastic_release*: Major release version of Elastic stack to configure. (default: `7`)
* *elastic_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)
