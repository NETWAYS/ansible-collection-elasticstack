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

### Requirements

You will need the following Ansible collections installed

* community.general (probably already present)

You may want the following Ansible roles installed. There other ways to achieve what they are doing but using them is easy and convenient.

* geerlingguy.redis

### Supported systems

We test the collection on the following Linux distributions. Each one with Elastic Stack 7 and 8.

* Rocky Linux 8
* Ubuntu 20.04 LTS
* Ubuntu 22.04 LTS
* Debian 11

We know from personal experience, that the collections work in following combinations. Missing tests mostly come from incompatibilties between the distribution and our testing environment, not from problems with the collection itself.

* CentOS 7 - Elastic Stack 7

We have known issues with the following Distributions.

* Rocky Linux 9: The GnuPG key used by Elastic seems to be incompatible with this version of Rocky.

## Usage

* *elastic_version*: Version number of tools to install Only set if you don't want the latest. (default: none). For OSS version see `elastic_variant` below. **IMPORTANT** Do not change the version once you have set up the stack. There are unpredictable effects to be expected when using this for upgrades. And upgrade mechanism is already on it's way. (default: none. Example: `7.17.2`
*elastic_release*: Major release version of Elastic stack to configure. (default: `7`)
*elastic_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)

Make sure all hosts that should be configured are part of your playbook. (See below for details on groups etc.). The collection is built to first collect all facts from all hosts (including those only running beats) and then use facts like hostnames or ip addresses to connect the tools to each other.

You will want to have reliable DNS resolution or enter all hosts of the stack into your systems hosts files.

### Default Passwords 

Default Passwords can be seen during generation, or found later in `/usr/share/elasticsearch/initial_passwords`

To turn off security currently:
`elastic_override_beats_tls: true`
### Redis

0) You need to install the redis role which is maintained by geerlingguy.

```
ansible-galaxy install geerlingguy.redis 
```

1) Default: For general Elastic Stack installations using all features use the following. You will need Redis installed and running for the default setup to run. A viable way is using the `geerlingguy.redis` role. (You can install it with `ansible-galaxy install geerlingguy.redis)

2) Specific: For OSS Installation without X-Pack features you can use the following. _Note_ this is only available for version `7.x`.

Our default configuration will collect filesystem logs placed by `rsyslog`. Therefor our example playbook makes sure, `rsyslog` is installed. If you don't want that, please change the configuration of the `beats` module. Without syslog you won't receive any messages with the default configuration.

There are some comments in the Playbook. Either fill them with the correct values (`remote_user`) or consider them as a hint to commonly used options.

_Note_: The roles rely on hardcoded group names for placing services on hosts. Please make sure you have groups named `elasticsearch`, `logstash` and `kibana` in your Ansible inventory. Hosts in these groups will get the respective services. Restricting your plays to the appropriate hosts will not work because the roles interact with hosts from other groups e.g. for certificate generation.

The execution order of the roles is important! (see below)

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
