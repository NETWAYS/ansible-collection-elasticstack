# Ansible Collection - netways.elasticstack

This collection installs and manages the Elastic Stack. It provides roles every component which is part of the Stack. Furthermore it is possible to differentiate between Enterprise or OSS releases. Every role is documented with all variables, please refer to the documentation found in **[Getting-Started](./docs/getting-started.md)**



## Roles Documentation

* [Beats](docs/role-beats.md)
* [Elasticsearch](docs/role-elasticsearch.md)
* [Kibana](docs/role-kibana.md)
* [Logstash](docs/role-logstash.md)
* [Repos](docs/role-repos.md)

## Installation

You can easily install the collection with the ansible-galaxy command.

```
ansible-galaxy collection install netways.elasticstack
```

Or if you are using Tower or AWX add the collection to your requirements file.

```
collections:
  - name: netways.elasticstack
```

## Usage

```
- name: Install Elasticsearch
  hosts: all
  collections:
    - NETWAYS.elasticstack
  vars:
    elastic_variant: oss
    elasticsearch_jna_workaround: true
  roles:
    - repos
    - beats
    - elasticsearch
    - logstash
    - kibana
```
