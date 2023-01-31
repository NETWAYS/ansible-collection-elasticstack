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

### Default Passwords 

Default Passwords  can be seen during generation, or found later in `usr/share/elasticsearch/initial_passwords`

### Redis

0) You need to install the redis role which is maintained by geerlingguy

```
ansible-galaxy install geerlingguy.redis 
```

1) 

Default: For general Elastic Stack installations using all features use the following.

You will need Redis installed and running for the default setup to run. A viable way is using the `geerlingguy.redis` role. (You can install it with `ansible-galaxy install geerlingguy.redis)

```
- name: Install Elasticsearch
  hosts: all
  become: true
  collections:
    - netways.elasticstack
  vars:
    elastic_stack_full_stack: true
    elastic_variant: elastic
    elasticsearch_jna_workaround: true
  roles:
    - repos
    - beats
    - elasticsearch
    - geerlingguy.redis
    - logstash
    - kibana
```

2) Specific: For OSS Installation without X-Pack features you can use the following. _Note_ this is only available for version `7.x`.
```
- name: Install Elasticsearch
  hosts: all
  collections:
    - netways.elasticstack
  vars:
    elastic_stack_full_stack: true
    elastic_variant: oss
    elasticsearch_jna_workaround: true
  roles:
    - repos
    - beats
    - elasticsearch
    - geerlingguy.redis
    - logstash
    - kibana
```
