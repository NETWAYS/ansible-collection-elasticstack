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
ansible-galaxy collection install https://github.com/netways/ansible-collection-elasticstack.git
```

Or if you are using Tower or AWX add the collection to your requirements file.

```
collections:
  - name: netways.elasticstack
```

## Usage

Our default configuration will collect filesystem logs placed by `rsyslog`. Therefor our example playbook makes sure, `rsyslog` is installed. If you don't want that, please change the configuration of the `beats` module. Without syslog you won't receive any messages with the default configuration.

There are some comments in the Playbook. Either fill them with the correct values (`remote_user`) or consider them as a hint to commonly used options.

_Note_: The roles rely on hardcoded group names for placing services on hosts. Please make sure you have groups named `elasticsearch`, `logstash` and `kibana` in your Ansible inventory. Hosts in these groups will get the respective services. Restricting your plays to the appropriate hosts will not work because the roles interact with hosts from other groups e.g. for certificate generation.

```
---
- hosts: all
    # remote_user: my_username
  become: true
  collections:
    - netways.elasticstack
  vars:
    elastic_variant: elastic #oss
    elasticsearch_jna_workaround: true
    elastic_override_beats_tls: true
    #  elastic_release: 8 #7
  pre_tasks:
    - name: Install Rsyslog
      package:
        name: rsyslog
    - name: Start rsyslog
      service:
        name: rsyslog
        state: started
        enabled: true
  roles:
    - repos
    - elasticsearch
    - geerlingguy.redis
    - logstash
    - kibana
    - beats

```
