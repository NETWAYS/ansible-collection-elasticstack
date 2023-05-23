Ansible Role: Beats
=========

![Test Role Beats](https://github.com/netways/ansible-collection-elasticstack/actions/workflows/test_role_beats.yml/badge.svg)

This role installs and configures Beats. You can use it as a standalone role or combine it with our other roles managing the Elastic Stack.

Requirements
------------

You need to have the beats you want to install available in your software repositories. We provide a [role](./role-repos.md) for just that but if you have other ways of managing software, just make sure it's available. Alternatively you can install the Beats yourself.

* `cryptography` >= 2.5 
* `community.crypto` collection: ansible-galaxy collection install community.crypto

Role Variables
--------------

* *beats_filebeat*: Install and manage filebeat (Default: `true`)
* *beats_filebeat_enable*: Automatically start Filebeat (Default: `true`)
* *beats_filebeat_output*: Set to `logstash` or `elasticsearch`. (default: `logstash`)
* *beats_filebeat_syslog_udp*: Use UDP Syslog input (Default: `false`)
* *beats_filebeat_syslog_udp_port*: Port of UDP Syslog input (Default: `514`)
* *beats_filebeat_syslog_tcp*: Use TCP Syslog input (Default: `false`)
* *beats_filebeat_syslog_tcp_port*: Port of TCP Syslog input (Default: `514`)
* *beats_filebeat_log_input*: Enable Logfile reading (Default: `true`)
* *beats_filebeat_mysql_slowlog_input*: Enable MySQL/MariaDB slow query log collection incl. multiline (Default: `false`)
* *beats_filebeat_log_inputs*: Logfiles to read (Default: see below)

Default of `beats_filebeat_log_inputs`

```
  messages:
    name: messages
    paths:
      - /var/log/messages
```

You can optionally add `fields` to every input as well. You can also add a `multiline` section with options (`type`, `pattern`, `negate` and `match` so far)

Here's a longer example for an input:
```
beats_filebeat_log_inputs:
  messages:
    name: messages
    paths:
      - /var/log/messages
      - /var/log/secure
      - /var/log/httpd/*access_log*
    multiline:
      type: pattern
      pattern: '^[[:space:]]+(at|\.{3})[[:space:]]+\b|^Caused by:'
      negate: false
      match: after
```
* *beats_filebeat_journald*: Enable collection of JournalD logs (default: `false`) - available since Filebeat 7.16
* *beats_filebeat_journald_inputs*: List of journald inputs. Use for different filters on events. You can add a list of `include_matches` entries for filtering.
Default of `beats_filebeat_journald_inputs`:
```
beats_filebeat_journald_inputs:
  everything:
    id: everything
```
* *beats_filebeat_docker*: Enable collection of Docker logs (default: `false`) **ONLY WORKS ON RELEASE 7 SO FAR**
* *beats_filebeat_docker_ids*: IDs of containers to collect. (default: `*`)

* *beats_filebeat_loadbalance*: Enable loadbalancing for Filebeats Logstash output (default: `true`)
* *beats_filebeat_modules*: **EXPERIMENTAL**: Give a list of modules to enable. (default: none)

* *beats_auditbeat*: Install and manage filebeat (Default: `false`)
* *beats_auditbeat_output*: Output for Auditbeat Set to `logstash` or `elasticsearch`. (default: `elasticsearch`)
* *beats_auditbeat_enable*: Automatically start Auditbeat (Default: `true`)
* *beats_auditbeat_setup*: Run Auditbeat Setup (Default: `true`) (Only works with Elasticsearch output)
* *beats_auditbeat_loadbalance*: Enable loadbalancing for Auditbeats Logstash output (default: `true`)

* *beats_metricbeat*: Enable installation and management of Metricbeat (Default: `false`)
* *beats_metricbeat_enable*: Start Metricbeat automatically (Default: `true`)
* *beats_metricbeat_output*: Set to `logstash` or `elasticsearch`. (default: `elasticsearch`)
* *beats_metricbeat_modules*: List of modules to enable. (Default: `- system`)
* *beats_metricbeat_loadbalance*: Enable loadbalancing for Metricbeats Logstash output (default: `true`)

* *beats_security*: Activate TLS for connections to targets. Can either be use with our other roles and `elasticstack_full_stack` to automatically create certificates or `beats_tls*` variables for custom certificates. (default: `false`)
* *beats_target_hosts*: Only use when this role is used standalone. When used in combination with our other roles, the target hosts will be determined automatically. Use a YAML list. (default: `- localhost`)
* *elasticstack_elasticsearch_http_port*: Port of Elasticsearch to send events to (Default: `9200`)
* *elasticstack_beats_port*: Port of Logstash to send events to (Default: `5044`)
* *beats_logging*: Where to log (Default: `file`)
* *beats_loglevel*: Level of logging (for all beats) (Default: `info`)
* *beats_logpath*: If logging to file, where to put logfiles (Default: `/var/log/beats`)
* *beats_fields*: Fields that are added to every input in the configuration
* *beats_manage_unzip*: Install `unzip` via package manager (Default: `true`)

The following variables only apply if you use this role together with our other Elastic Stack roles.

* *elasticstack_full_stack*: Use `elasticsearch` as well (default: `false`)
* *elasticstack_variant*: Define which variant of elastic stack to use. (default: `elastic`)
* *elasticstack_ca_dir*: Directory where on the Elasticsearch CA host certificates are stored. This is only useful in connection with out other Elastic Stack related roles. (default: `/opt/es-ca`)
* *elasticstack_ca_pass*: Password for Elasticsearch CA (default: `PleaseChangeMe`)
* *elasticstack_initial_passwords*: Path to file with initical elasticsearch passwords (default: `/usr/share/elasticsearch/initial_passwords`)
* *elasticstack_version*: Install specific version (Default: none. Possible values: e.g. `7.10.1` or `latest`)

If you want to use this role with your own TLS certificates, use these variables.

* *beats_ca_dir*: Path to custom CA certificates and keys (default: none - if not set will be filled with different values depending on which Stack variant is used)
* *beats_tls_key*: Path to the keyfiles (default: `{{ beats_ca_dir }}/{{ ansible_hostname }}.key`)
* *beats_tls_cert*: Path to the certificate (default: `{{ beats_ca_dir }}/{{ ansible_hostname }}.crt`)
* *beats_tls_key_passphrase*: Passphrase of the keyfile (default: `BeatsChangeMe`)
* *beats_cert_expiration_buffer*: Ansible will renew the beats certificate if its validity is shorter than this value (default: `+30d`). The valid format is `+[w | d | h | m | s]`, example `+20w5d7h`. 
* *beats_cert_will_expire_soon*: Set it to true to renew beats certificate (default: `false`), Or run the playbook with `--tags renew_beats_cert` to do that.
* *beats_tls_cacert*: Path to the CA.crt (default: `{{ beats_ca_dir }}/ca.crt`)

## Usage

```
- name: Install Elastic Beats
  hosts: beats-hosts
  collections:
    - netways.elasticstack
  vars:
    elasticsearch_jna_workaround: true
    elasticsearch_disable_systemcallfilterchecks: true
  roles:
    - repos
    - beats
```
