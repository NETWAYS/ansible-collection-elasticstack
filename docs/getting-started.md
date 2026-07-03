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
* *elasticstack_version*: Full version to pin all components to (e.g. `8.13.0`). Leave unset to install the latest available version. (default: unset)


Version handling
-----------

All roles share a single version selection scheme, so Elasticsearch, Kibana, Logstash and the Beats always behave the same way:

* If `elasticstack_version` is **not set** (or set to the special value `latest`), the roles install the newest package available in the configured repository and keep it up to date on every run (`state: latest`). This is the default.
* If `elasticstack_version` is **set to a concrete version** (e.g. `8.13.0`), that exact version is installed and pinned (`state: present`); the package is not upgraded on later runs as long as the value stays the same.

Internally each role derives the package name and the package state from `elasticstack_version` and stores the result in the internal fact `_elasticstack_package_state`. This variable is computed automatically and is not meant to be set by users.

To keep the whole stack on one version, set `elasticstack_version` once at the play or group level. When running the full stack, the meta role also determines the version from the already installed Elasticsearch package (see `roles/elasticstack/tasks/elasticstack-versions.yml`), so the remaining components stay aligned.

> **Note:** With the default (`latest`), every run may upgrade a component to the newest available release. For Elasticsearch clusters where controlled, orchestrated upgrades matter, pin `elasticstack_version` to a concrete value instead.
