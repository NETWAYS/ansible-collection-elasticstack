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
  - name: netways.elasticstack
```

Usage
---------

To use the collection in your Ansible playbook add the following key to your playbook.

```
- name: Playbook
  hosts: some_host_pattern
  collections:
    - netways.elasticstack
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
        name: netways.elasticstack.logstash
```

Roles
-------

* [Beats](role-beats.md)
* [Elasticsearch](role-elasticsearch.md)
* [Kibana](role-kibana.md)
* [Logstash](role-logstash.md)
* [Repos](role-repos.md)


Variables
-----------

Every role got its own set of variables, in addition a few variables are useable on any role. Below are all general collection vars.

* *elasticstack_release*: Major release version of Elastic stack to configure. (default: `7`)
* *elasticstack_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)

Tags
-----------

As of the beginning of now, we introduce the usage of tags in the role as well for quicker and more precise control of the installs.
More Info on the usable tags can be found in the respective documentation of the role part.

As of now *Beats*,*Elasticsearch*,*Kibana* and *Logstash* have tags available for usage.

Most tags can be used in the role the following way:

```
- name: Playbook
  hosts: some_host_pattern
  collections:
    - netways.elasticstack
  vars:
    component_install_tags: "tag1, tag2, tag3"
  tasks:
    - name: install elastic component
      import_role:
        name: netways.elasticstack.logstash
  tags: "{{ component_install_tags }}"
```
