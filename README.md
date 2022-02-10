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

* *metricbeat_enable*: Start Metricbeat automatically (Default: `true`)
* *metricbeat_output*: Set to `logstash` or `elasticsearch`. (default: `elasticsearch`)
* *metricbeat_modules*: List of modules to enable. (Default: `- system`)

* *beats_metricbeat*: Enable installation and management of Metricbeat (Default: `false`)
* *beats_target_hosts*: Only use when this role is used standalone. When used in combination with our other roles, the target hosts will be determined automatically. Use a YAML list. (default: `- localhost`)
* *beats_elasticsearch_output_port*: Port of Elasticsearch to send events to (Default: `9200`)
* *beats_logstash_output_port*: Port of Logstash to send events to (Default: `5400`)
* *beats_logging*: Where to log (Default: `file`)
* *beats_loglevel*: Level of logging (for all beats) (Default: `info`)
* *beats_logpath*: If logging to file, where to put logfiles (Default: `/var/log/beats`)
* *beats_fields*: Fields that are added to every input in the configuration

The following variables only apply if you use this role together with our other Elastic Stack roles.

* *elastic_stack_full_stack*: Use `ansible-role-elasticsearch` as well (default: `false`)
* *elastic_variant*: Define which variant of elastic stack to use. (default: `elastic`)
* *elastic_ca_dir*: Directory where on the Elasticsearch CA host certificates are stored. This is only useful in connection with out other Elastic Stack related roles. (default: `/opt/es-ca`)
* *elastic_ca_pass*: Password for Elasticsearch CA (default: `PleaseChangeMe`)
* *elastic_initial_passwords*: Path to file with initical elasticsearch passwords (default: `/usr/share/elasticsearch/initial_passwords`)

If you want to use this role with your own TLS certificates, use these variables.

* *beats_tls*: Enable TLS without X-Pack (default: `false`)
* *beats_ca_dir*: Path to custom CA certificates and keys (default: `/opt/ca`)
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
