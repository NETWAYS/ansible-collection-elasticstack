# Getting started

This page shows how to run the collection. For installation see the
[README](../README.md#using-this-collection), for what the roles expect from your inventory see
[Requirements](requirements.md).

## Inventory groups

The roles place services on hosts by inventory group name. The group names and their defaults
are listed in [Requirements](requirements.md#inventory-group-names).

Hosts in these groups get the respective services. Restricting your plays to only the
appropriate hosts does **not** work, because the roles read facts from hosts in other groups,
for example to generate certificates.

Make sure every host that should be configured is part of your playbook, including hosts that
only run Beats. The collection first gathers facts from all hosts and then uses facts such as
host names and IP addresses to connect the tools to each other.

You will want reliable DNS resolution, or all hosts of the stack in your systems' hosts files.

## Before the first run

Redis has to be running for the default setup, because the default Logstash pipeline uses it.
The example playbook below gets it there with the `geerlingguy.redis` role, listed under
external requirements in the [README](../README.md#external-requirements).

The default Beats configuration collects file system logs written by `rsyslog`, which is why the
example playbook installs it. Without syslog you will not receive any messages with the default
configuration. If you do not want that, change the configuration of the beats role.

`elasticstack_variant: oss` is not available for the whole stack on every release. OSS
Elasticsearch and Kibana exist only up to Elastic Stack `7`, while OSS Logstash and Beats are
available on later releases too.

## Variables

Every role has its own set of variables, documented in the role's README. In addition the
collection-wide `elasticstack_*` variables apply to any role and are documented centrally with
the [elasticstack role](../roles/elasticstack/README.md). Two common ones:

* `elasticstack_release`: major release version of the Elastic Stack to configure
  (default: `8`)
* `elasticstack_variant`: variant of the stack to install, `elastic` or `oss`
  (default: `elastic`)

For pinning a specific version and for upgrading, see [Versions and upgrades](upgrades.md).

## Example playbook

The execution order of the plays matters. There are comments in the playbook below: either fill
them with the correct values, such as `remote_user`, or take them as a hint about commonly used
options.

```yaml
---
- hosts: all
  # remote_user: my_username
  become: true
  vars:
    elasticstack_variant: elastic # oss
    #  elasticstack_release: 8
  roles:
    - netways.elasticstack.repos

- hosts: elasticsearch
  # remote_user: my_username
  become: true
  vars:
    elasticstack_variant: elastic # oss
    elasticsearch_jna_workaround: true
    #  elasticstack_release: 8
  roles:
    - netways.elasticstack.elasticsearch

- hosts: logstash
  # remote_user: my_username
  become: true
  vars:
    elasticstack_variant: elastic # oss
    elasticstack_override_beats_tls: true
    #  elasticstack_release: 8
  roles:
    - geerlingguy.redis
    - netways.elasticstack.logstash

- hosts: kibana
  # remote_user: my_username
  become: true
  vars:
    elasticstack_variant: elastic # oss
    #  elasticstack_release: 8
  roles:
    - netways.elasticstack.kibana

- hosts: all
  # remote_user: my_username
  become: true
  vars:
    elasticstack_variant: elastic # oss
    elasticstack_override_beats_tls: true
    #  elasticstack_release: 8
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
    - netways.elasticstack.beats
```

## Generated passwords

Passwords for the built-in users are generated on the CA host during the first run. They are
printed while they are generated and stored in the file that `elasticstack_initial_passwords`
points to, by default `/usr/share/elasticsearch/initial_passwords`.

Security is on by default and controlled by `elasticstack_security`. A related but much
narrower switch is `elasticstack_override_beats_tls`: it only stops TLS between Beats and
Logstash from being enabled automatically, and skips the Beats certificate generation. It does
not turn off security anywhere else.

## Seeing what the tasks do

`elasticstack_no_log` defaults to `true`, because some tasks could reveal passwords in
production. Set it to `false` if you want to see the output of all tasks.
