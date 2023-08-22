# Ansible Collection - netways.elasticstack

![Test ElasticStack](https://github.com/NETWAYS/ansible-collection-elasticstack/actions/workflows/test_full_stack.yml/badge.svg)

This collection installs and manages the Elastic Stack. It provides roles for every component of the Stack. Furthermore, it is possible to differentiate between Enterprise or OSS releases.

Every role is documented with all variables, please refer to the documentation found in **[Getting-Started](./docs/getting-started.md)**

**Please note**: If you are already using this collection before version `1.0.0`, please note that we had to rename a significant amount of variables due to naming schema changes made by Ansible. Please review the variables you have set in your playbooks and variable files.

## Roles Documentation

* [Beats](docs/role-beats.md)
* [Elasticsearch](docs/role-elasticsearch.md)
* [Kibana](docs/role-kibana.md)
* [Logstash](docs/role-logstash.md)
* [Repos](docs/role-repos.md)

## Installation

You can easily install the collection with the `ansible-galaxy` command.

```
ansible-galaxy collection install git+https://github.com/netways/ansible-collection-elasticstack.git
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
* openssl if you want to use Elastic Security

### Supported systems

We test the collection on the following Linux distributions. Each one with Elastic Stack 7 and 8.

* Rocky Linux 8
* Ubuntu 20.04 LTS
* Ubuntu 22.04 LTS
* Debian 11

We know from personal experience, that the collections work in following combinations. Missing tests mostly come from incompatibilties between the distribution and our testing environment, not from problems with the collection itself.

* CentOS 7 - Elastic Stack 7

### Known Issues

There are known issues with the following Linux distributions.

* Rocky Linux 9: The GnuPG key used by Elastic seems to be incompatible with this version of Rocky.

## Usage

Every role is documented with all variables, please refer to the documentation found in **[Getting-Started](./docs/getting-started.md)**

Make sure all hosts that should be configured are part of your playbook. (See below for details on groups etc.). The collection is built to first collect all facts from all hosts (including those only running beats) and then use facts like hostnames or ip addresses to connect the tools to each other.

You will want to have reliable DNS resolution or enter all hosts of the stack into your systems hosts files.

### Versioning

*elasticstack_version*: Version number of tools to install. Only set if you don't want the latest. (default: none).

*elasticstack_release*: Major release version of Elastic stack to configure. (default: `7`)

For OSS version see `elasticstack_variant` below. **IMPORTANT** Do not change the version once you have set up the stack. There are unpredictable effects to be expected when using this for upgrades. And upgrade mechanism is already on it's way. (default: none. Example: `7.17.2`)

*elasticstack_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)

```yaml
roles:
   - role: netways.elasticstack.kibana
     vars:
        elasticstack_version: 8.7.1
   - role: netways.elasticstack.elasticsearch
     vars:
        elasticstack_version: 8.8.1
```

### Default Passwords

Default passwords can be seen during generation, or found later in `/usr/share/elasticsearch/initial_passwords`

To turn off security:

`elasticstack_override_beats_tls: true`

### Requirements

0) You need to install the redis role which is maintained by geerlingguy.

```
ansible-galaxy install geerlingguy.redis
```

1) Default: For general Elastic Stack installations using all features use the following. You will need Redis installed and running for the default setup to run. A viable way is using the `geerlingguy.redis` role.

2) Specific: For OSS Installation without X-Pack features you can use the following. _Note_: this is only available for version `7.x`.

Our default configuration will collect filesystem logs placed by `rsyslog`. Therefor our example playbook makes sure, `rsyslog` is installed. If you don't want that, please change the configuration of the `beats` module. Without syslog you won't receive any messages with the default configuration.

There are some comments in the Playbook. Either fill them with the correct values (`remote_user`) or consider them as a hint to commonly used options.

### Inventory

_Note_: The roles rely on hardcoded group names for placing services on hosts. Please make sure you have groups named `elasticsearch`, `logstash` and `kibana` in your Ansible inventory. Hosts in these groups will get the respective services. Just restricting your plays to the appropriate hosts will not work because the roles interact with hosts from other groups e.g. for certificate generation.

The execution order of the roles is important! (see below)

```yaml
---
- hosts: all
  # remote_user: my_username
  become: true
  collections:
    - netways.elasticstack
  vars:
    elasticstack_variant: elastic #oss
    #  elasticstack_release: 8 #7
  roles:
    - repos

- hosts: elasticsearch
  # remote_user: my_username
  become: true
  collections:
    - netways.elasticstack
  vars:
    elasticstack_variant: elastic #oss
    elasticsearch_jna_workaround: true
    #  elasticstack_release: 8 #7
  roles:
    - elasticsearch

- hosts: logstash
  # remote_user: my_username
  become: true
  collections:
    - netways.elasticstack
  vars:
    elasticstack_variant: elastic #oss
    elasticstack_override_beats_tls: true
    #  elasticstack_release: 8 #7
  roles:
    - geerlingguy.redis
    - logstash

- hosts: kibana
  # remote_user: my_username
  become: true
  collections:
    - netways.elasticstack
  vars:
    elasticstack_variant: elastic #oss
    #  elasticstack_release: 8 #7
  roles:
    - kibana

- hosts: all
  # remote_user: my_username
  become: true
  collections:
    - netways.elasticstack
  vars:
    elasticstack_variant: elastic #oss
    elasticstack_override_beats_tls: true
    #  elasticstack_release: 8 #7
  pre_tasks:
    - name: Install Rsyslog
      ansible.builtin.package:
        name: rsyslog
    - name: Start rsyslog
       ansible.builtin.service:
        name: rsyslog
        state: started
        enabled: true
  roles:
    - beats

```

## Contributing

Every kind of contribution is very welcome. Open [issues](https://github.com/NETWAYS/ansible-collection-elasticstack/issues) or provide [pull requests](https://github.com/NETWAYS/ansible-collection-elasticstack/pulls).

Please note that we have some actions bound to specific names of branches. So please stick to the following naming scheme:

* `fix/` as a prefix for every branch that fixes a problem
* `feature/` for every branch that enhances the code with new features
* `doc/` as a prefix for every branch that only changes documentation

For now we open pull requests against `main`. We are planning to introduce dedicated branches to support older versions without breaking changes. Since we don't need them for now, please check back with this section because when we decided on how to proceed, you will find the information here. For now `main` always has the newest changes and if you want a stable version, please use the newest release.
