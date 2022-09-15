Filebeat
=========

[![CI](https://github.com/widhalmt/ansible-role-beats/workflows/Molecule%20Test/badge.svg?event=push)](https://github.com/widhalmt/ansible-role-beats/workflows/Molecule%20Test/badge.svg)

This role installs and configures Filebeat.

*WARNING*: This is a very, very early prototype only usable for a very specific environment. **DO NOT USE IN PRODUCTION**

Requirements
------------

You need to have Filebeat available in your software repositories. We provide a role for just that but if you have other ways of managing software, just make sure it's available. Alternatively you can install Filebeat yourself.

Role Variables
--------------

* *beats_filebeat*: Install and manage filebeat (Default: `true`)
* *beats_filebeat_version*: Install specific version (Default: none. Possible values: e.g. ``-7.10.1` for RedHat compatible systems or `=1:7.10.1-1` for Debian compatible systems or `latest`)
* *filebeat_enable*: Automatically start Filebeat (Default: `true`)
* *filebeat_output*: Set to `logstash` or `elasticsearch`. (default: `logstash`)
* *filebeat_syslog_udp*: Use UDP Syslog input (Default: `false`)
* *filebeat_syslog_udp_port*: Port of UDP Syslog input (Default: `514`)
* *filebeat_syslog_tcp*: Use TCP Syslog input (Default: `false`)
* *filebeat_syslog_tcp_port*: Port of TCP Syslog input (Default: `514`)
* *filebeat_log_input*: Enable Logfile reading (Default: `true`)
* *filebeat_mysql_slowlog_input*: Enable MySQL/MariaDB slow query log collection incl. multiline (Default: `false`)
* *filebeat_log_inputs*: Logfiles to read (Default: see below)

Default of `filebeat_log_inputs`
```
  messages:
    name: messages
    paths:
      - /var/log/messages
```
You can optionally add `fields` to every input as well. You can also add a `multiline` section with options (`type`, `pattern`, `negate` and `match` so far)

Here's a longer example for an input:
```
filebeat_log_inputs:
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
* *filebeat_journald*: Enable collection of JournalD logs (default: `false`) - available since Filebeat 7.16
* *filebeat_journald_inputs*: List of journald inputs. Use for different filters on events. You can add a list of `include_matches` entries for filtering.
Default of `filebeat_journald_inputs:
```
filebeat_journald_inputs:
  everything:
    id: everything
```
* *filebeat_docker*: Enable collection of Docker logs (default: `false`)
* *filebeat_docker_ids*: IDs of containers to collect. (default: `*`)

* *filebeat_loadbalance*: Enable loadbalancing for Filebeats Logstash output (default: `true`)

* *beats_auditbeat*: Install and manage filebeat (Default: `false`)
* *beats_auditbeat_version*: Install specific version (Default: none. Possible values: e.g. ``-7.10.1` for RedHat compatible systems or `=1:7.10.1-1` for Debian compatible systems or `latest`)
* *auditbeat_output*: Output for Auditbeat Set to `logstash` or `elasticsearch`. (default: `elasticsearch`)
* *auditbeat_enable*: Automatically start Auditbeat (Default: `true`)
* *auditbeat_setup*: Run Auditbeat Setup (Default: `true`) (Only works with Elasticsearch output)
* *auditbeat_loadbalance*: Enable loadbalancing for Auditbeats Logstash output (default: `true`)

* *beats_metricbeat*: Enable installation and management of Metricbeat (Default: `false`)
* *beats_metricbeat_version*: Install specific version (Default: none. Possible values: e.g. ``-7.10.1` for RedHat compatible systems or `=1:7.10.1-1` for Debian compatible systems or `latest`)
* *metricbeat_enable*: Start Metricbeat automatically (Default: `true`)
* *metricbeat_output*: Set to `logstash` or `elasticsearch`. (default: `elasticsearch`)
* *metricbeat_modules*: List of modules to enable. (Default: `- system`)
* *metricbeat_loadbalance*: Enable loadbalancing for Metricbeats Logstash output (default: `true`)

* *beats_security*: Activate TLS for connections to targets. Can either be use with our other roles and `elastic_stack_full_stack` to automatically create certificates or `beats_tls*` variables for custom certificates. (default: `false`)
* *beats_target_hosts*: Only use when this role is used standalone. When used in combination with our other roles, the target hosts will be determined automatically. Use a YAML list. (default: `- localhost`)
* *beats_elasticsearch_output_port*: Port of Elasticsearch to send events to (Default: `9200`)
* *beats_logstash_output_port*: Port of Logstash to send events to (Default: `5400`)
* *beats_logging*: Where to log (Default: `file`)
* *beats_loglevel*: Level of logging (for all beats) (Default: `info`)
* *beats_logpath*: If logging to file, where to put logfiles (Default: `/var/log/beats`)
* *beats_fields*: Fields that are added to every input in the configuration
* *beats_manage_unzip*: Install `unzip` via package manager (Default: `true`)

The following variables only apply if you use this role together with our other Elastic Stack roles.

* *elastic_stack_full_stack*: Use `ansible-role-elasticsearch` as well (default: `false`)
* *elastic_variant*: Define which variant of elastic stack to use. (default: `elastic`)
* *elastic_ca_dir*: Directory where on the Elasticsearch CA host certificates are stored. This is only useful in connection with out other Elastic Stack related roles. (default: `/opt/es-ca`)
* *elastic_ca_pass*: Password for Elasticsearch CA (default: `PleaseChangeMe`)
* *elastic_initial_passwords*: Path to file with initical elasticsearch passwords (default: `/usr/share/elasticsearch/initial_passwords`)

If you want to use this role with your own TLS certificates, use these variables.

* *beats_ca_dir*: Path to custom CA certificates and keys (default: none - if not set will be filled with different values depending on which Stack variant is used)
* *beats_tls_key*: Path to the keyfiles (default: `{{ beats_ca_dir }}/{{ ansible_hostname }}.key`)
* *beats_tls_cert*: Path to the certificate (default: `{{ beats_ca_dir }}/{{ ansible_hostname }}.crt`)
* *beats_tls_key_passphrase*: Passphrase of the keyfile (default: `ChangeMe`)
* *beats_tls_cacert*: Path to the CA.crt (default: `{{ beats_ca_dir }}/ca.crt`)


Dependencies
------------

None yet

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

GPL-3.0-or-later

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
